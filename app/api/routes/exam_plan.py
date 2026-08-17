import uuid
from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.models.concept import Concept
from app.db.models.course import Course
from app.db.models.exam_plan import ExamPlan, ExamPlanDay, ExamPlanStatus
from app.db.models.mastery import Mastery
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.exam_plan import ExamPlanCreate, ExamPlanResponse, ExamPlanUpdate
from app.services.exam_planner import generate_plan_days, readiness_pct

router = APIRouter()


def _get_owned_course(db: Session, course_id: uuid.UUID, user_id: uuid.UUID) -> Course:
    course = db.get(Course, course_id)
    if course is None or course.user_id != user_id:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


def _concept_accuracy(db: Session, course_id: uuid.UUID, user_id: uuid.UUID) -> dict[uuid.UUID, float]:
    concept_ids = list(db.execute(select(Concept.id).where(Concept.course_id == course_id)).scalars().all())
    mastery_rows = {
        m.concept_id: m.accuracy_ema
        for m in db.execute(
            select(Mastery).where(Mastery.user_id == user_id, Mastery.concept_id.in_(concept_ids))
        ).scalars().all()
    }
    return {cid: mastery_rows.get(cid, 0.0) for cid in concept_ids}


def _to_response(db: Session, plan: ExamPlan, user_id: uuid.UUID) -> ExamPlanResponse:
    today = date.today()
    days_left = max((plan.exam_date - today).days, 0)

    concept_accuracy = _concept_accuracy(db, plan.course_id, user_id)
    readiness = readiness_pct(concept_accuracy)

    today_day = db.execute(
        select(ExamPlanDay).where(ExamPlanDay.exam_plan_id == plan.id, ExamPlanDay.date == today)
    ).scalar_one_or_none()
    today_targets = [uuid.UUID(cid) for cid in today_day.target_concept_ids] if today_day else []

    return ExamPlanResponse(
        id=plan.id,
        course_id=plan.course_id,
        exam_date=plan.exam_date,
        status=plan.status,
        days_left=days_left,
        readiness_pct=readiness,
        today_target_concept_ids=today_targets,
    )


def _regenerate_days(db: Session, plan: ExamPlan, user_id: uuid.UUID) -> None:
    db.query(ExamPlanDay).filter(ExamPlanDay.exam_plan_id == plan.id).delete()

    concept_accuracy = _concept_accuracy(db, plan.course_id, user_id)
    plan_days = generate_plan_days(plan.exam_date, date.today(), concept_accuracy)
    for day, target_ids in plan_days:
        db.add(
            ExamPlanDay(
                exam_plan_id=plan.id,
                date=day,
                target_concept_ids=[str(cid) for cid in target_ids],
            )
        )
    db.commit()


@router.post("/{course_id}/exam-plan", response_model=ExamPlanResponse, status_code=201)
def create_exam_plan(
    course_id: uuid.UUID,
    payload: ExamPlanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ExamPlanResponse:
    _get_owned_course(db, course_id, current_user.id)

    existing = db.execute(
        select(ExamPlan).where(
            ExamPlan.course_id == course_id,
            ExamPlan.user_id == current_user.id,
            ExamPlan.status == ExamPlanStatus.active,
        )
    ).scalar_one_or_none()
    if existing is not None:
        existing.status = ExamPlanStatus.cancelled
        db.commit()

    plan = ExamPlan(course_id=course_id, user_id=current_user.id, exam_date=payload.exam_date)
    db.add(plan)
    db.commit()
    db.refresh(plan)

    _regenerate_days(db, plan, current_user.id)
    db.refresh(plan)
    return _to_response(db, plan, current_user.id)


@router.get("/{course_id}/exam-plan", response_model=ExamPlanResponse)
def get_exam_plan(
    course_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> ExamPlanResponse:
    _get_owned_course(db, course_id, current_user.id)

    plan = db.execute(
        select(ExamPlan).where(
            ExamPlan.course_id == course_id,
            ExamPlan.user_id == current_user.id,
            ExamPlan.status == ExamPlanStatus.active,
        )
    ).scalar_one_or_none()
    if plan is None:
        raise HTTPException(status_code=404, detail="No active exam plan for this course")

    return _to_response(db, plan, current_user.id)


@router.patch("/{course_id}/exam-plan", response_model=ExamPlanResponse)
def update_exam_plan(
    course_id: uuid.UUID,
    payload: ExamPlanUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ExamPlanResponse:
    _get_owned_course(db, course_id, current_user.id)

    plan = db.execute(
        select(ExamPlan).where(
            ExamPlan.course_id == course_id,
            ExamPlan.user_id == current_user.id,
            ExamPlan.status == ExamPlanStatus.active,
        )
    ).scalar_one_or_none()
    if plan is None:
        raise HTTPException(status_code=404, detail="No active exam plan for this course")

    if payload.status is not None:
        plan.status = payload.status
        db.commit()
        db.refresh(plan)
        return _to_response(db, plan, current_user.id)

    if payload.exam_date is not None:
        plan.exam_date = payload.exam_date
        db.commit()
        db.refresh(plan)
        _regenerate_days(db, plan, current_user.id)
        db.refresh(plan)

    return _to_response(db, plan, current_user.id)

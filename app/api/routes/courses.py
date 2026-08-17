import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.models.attempt import Attempt
from app.db.models.concept import Concept
from app.db.models.course import Course
from app.db.models.mastery import Mastery
from app.db.models.material import Material
from app.db.models.module import Module
from app.db.models.question import Question
from app.db.models.schedule_item import ScheduleItem, ScheduleStatus
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.course import (
    CourseCreate,
    CourseDashboardResponse,
    CourseDetailResponse,
    CourseDueTodayOut,
    CourseListItem,
    CourseMasteryOut,
    CourseResponse,
    ModuleCreate,
    ModuleResponse,
)

router = APIRouter()


def _get_owned_course(db: Session, course_id: uuid.UUID, user_id: uuid.UUID) -> Course:
    course = db.get(Course, course_id)
    if course is None or course.user_id != user_id:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


def _course_progress(db: Session, course_id: uuid.UUID, user_id: uuid.UUID) -> tuple[float, int]:
    concept_ids = list(db.execute(select(Concept.id).where(Concept.course_id == course_id)).scalars().all())
    if not concept_ids:
        return 0.0, 0

    accuracies = list(
        db.execute(
            select(Mastery.accuracy_ema).where(Mastery.user_id == user_id, Mastery.concept_id.in_(concept_ids))
        ).scalars().all()
    )
    mastery_pct = round(100 * sum(accuracies) / len(concept_ids), 1) if concept_ids else 0.0

    now = datetime.now(timezone.utc)
    due_count = db.execute(
        select(ScheduleItem.id).where(
            ScheduleItem.user_id == user_id,
            ScheduleItem.concept_id.in_(concept_ids),
            ScheduleItem.status != ScheduleStatus.completed,
            ScheduleItem.due_at <= now,
        )
    ).scalars().all()

    return mastery_pct, len(due_count)


@router.post("", response_model=CourseResponse, status_code=201)
def create_course(
    payload: CourseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> Course:
    course = Course(user_id=current_user.id, name=payload.name, color_tag=payload.color_tag)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


@router.get("", response_model=list[CourseListItem])
def list_courses(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> list[CourseListItem]:
    courses = db.query(Course).filter(Course.user_id == current_user.id).order_by(Course.created_at.desc()).all()
    items = []
    for course in courses:
        mastery_pct, due_count = _course_progress(db, course.id, current_user.id)
        items.append(
            CourseListItem(
                id=course.id,
                name=course.name,
                color_tag=course.color_tag,
                created_at=course.created_at,
                mastery_pct=mastery_pct,
                due_count=due_count,
            )
        )
    return items


@router.get("/{course_id}", response_model=CourseDetailResponse)
def get_course(
    course_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> CourseDetailResponse:
    course = _get_owned_course(db, course_id, current_user.id)

    modules = list(
        db.execute(
            select(Module).where(Module.course_id == course_id).order_by(Module.order_index)
        ).scalars().all()
    )
    materials = list(
        db.execute(
            select(Material).where(Material.course_id == course_id).order_by(Material.created_at.desc())
        ).scalars().all()
    )
    mastery_pct, due_count = _course_progress(db, course_id, current_user.id)

    return CourseDetailResponse(
        course=course,
        modules=modules,
        materials=materials,
        mastery_pct=mastery_pct,
        due_count=due_count,
    )


@router.post("/{course_id}/modules", response_model=ModuleResponse, status_code=201)
def create_module(
    course_id: uuid.UUID,
    payload: ModuleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Module:
    _get_owned_course(db, course_id, current_user.id)
    module = Module(course_id=course_id, name=payload.name, order_index=payload.order_index)
    db.add(module)
    db.commit()
    db.refresh(module)
    return module


@router.get("/{course_id}/dashboard", response_model=CourseDashboardResponse)
def get_course_dashboard(
    course_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> CourseDashboardResponse:
    _get_owned_course(db, course_id, current_user.id)

    concept_ids = list(db.execute(select(Concept.id).where(Concept.course_id == course_id)).scalars().all())

    mastery_rows = db.execute(
        select(Mastery, Concept)
        .join(Concept, Mastery.concept_id == Concept.id)
        .where(Mastery.user_id == current_user.id, Concept.course_id == course_id)
    ).all()
    mastery = [
        CourseMasteryOut(concept_id=m.concept_id, concept_name=c.name, accuracy_ema=m.accuracy_ema, repetitions=m.repetitions)
        for m, c in mastery_rows
    ]

    now = datetime.now(timezone.utc)
    due_rows = db.execute(
        select(ScheduleItem, Concept)
        .join(Concept, ScheduleItem.concept_id == Concept.id)
        .where(
            ScheduleItem.user_id == current_user.id,
            Concept.course_id == course_id,
            ScheduleItem.status != ScheduleStatus.completed,
            ScheduleItem.due_at <= now,
        )
    ).all()
    due_today = [CourseDueTodayOut(concept_id=s.concept_id, concept_name=c.name, due_at=s.due_at) for s, c in due_rows]

    graded_stmt = (
        select(Attempt.graded_at)
        .join(Question, Attempt.question_id == Question.id)
        .where(
            Attempt.user_id == current_user.id,
            Attempt.graded_at.is_not(None),
            Question.concept_id.in_(concept_ids) if concept_ids else False,
        )
        .order_by(Attempt.graded_at.desc())
    )
    graded_dates = sorted({row[0].date() for row in db.execute(graded_stmt).all()}, reverse=True)

    current_streak = 0
    cursor = now.date()
    for d in graded_dates:
        if d == cursor:
            current_streak += 1
            cursor -= timedelta(days=1)
        elif d == cursor + timedelta(days=1):
            continue
        else:
            break

    longest_streak = 0
    running = 0
    prev_date = None
    for d in sorted(graded_dates):
        if prev_date is not None and d == prev_date + timedelta(days=1):
            running += 1
        else:
            running = 1
        longest_streak = max(longest_streak, running)
        prev_date = d

    return CourseDashboardResponse(
        mastery=mastery,
        due_today=due_today,
        current_streak_days=current_streak,
        longest_streak_days=longest_streak,
    )

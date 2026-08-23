import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.models.concept import Concept
from app.db.models.course import Course
from app.db.models.mastery import Mastery
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.quiz import QuizSessionResponse
from app.schemas.weak_spot import WeakSpotOut
from app.api.routes.quiz import build_quiz_session
from app.services import access

router = APIRouter()

WEAK_SPOT_THRESHOLD = 0.5


def _get_owned_course(db: Session, course_id: uuid.UUID, user_id: uuid.UUID) -> Course:
    course = access.get_accessible_course(db, course_id, user_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.get("/{course_id}/weak-spots", response_model=list[WeakSpotOut])
def list_weak_spots(
    course_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> list[WeakSpotOut]:
    _get_owned_course(db, course_id, current_user.id)

    rows = db.execute(
        select(Mastery, Concept)
        .join(Concept, Mastery.concept_id == Concept.id)
        .where(
            Concept.course_id == course_id,
            Mastery.user_id == current_user.id,
            Mastery.accuracy_ema < WEAK_SPOT_THRESHOLD,
        )
        .order_by(Mastery.accuracy_ema.asc())
    ).all()

    return [
        WeakSpotOut(
            concept_id=m.concept_id,
            concept_name=c.name,
            mastery_pct=round(m.accuracy_ema * 100, 1),
            error_note=m.error_note,
            last_reviewed_at=m.last_reviewed_at,
        )
        for m, c in rows
    ]


@router.post("/{course_id}/weak-spots/practice", response_model=QuizSessionResponse)
async def practice_weak_spots(
    course_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> QuizSessionResponse:
    _get_owned_course(db, course_id, current_user.id)

    weak_concept_ids = list(
        db.execute(
            select(Mastery.concept_id)
            .join(Concept, Mastery.concept_id == Concept.id)
            .where(
                Concept.course_id == course_id,
                Mastery.user_id == current_user.id,
                Mastery.accuracy_ema < WEAK_SPOT_THRESHOLD,
            )
        ).scalars().all()
    )
    if not weak_concept_ids:
        raise HTTPException(status_code=404, detail="No weak spots for this course yet")

    return await build_quiz_session(db, current_user, course_id, weak_concept_ids)

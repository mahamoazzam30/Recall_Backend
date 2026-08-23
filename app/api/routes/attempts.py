import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.models.attempt import Attempt
from app.db.models.question import Question
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.quiz import AttemptCreate, AttemptResponse
from app.services import hooks, memory
from app.services.grading import grade_attempt

router = APIRouter()


def _to_response(attempt: Attempt, question: Question) -> AttemptResponse:
    return AttemptResponse(
        id=attempt.id,
        question_id=attempt.question_id,
        student_answer=attempt.student_answer,
        score=attempt.score,
        feedback=attempt.feedback,
        source_passage=question.chunk.content,
        source_page_ref=question.chunk.page_ref,
    )


@router.post("", response_model=AttemptResponse, status_code=201)
async def submit_attempt(
    payload: AttemptCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> AttemptResponse:
    question = db.get(Question, payload.question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    attempt = Attempt(
        question_id=question.id,
        user_id=current_user.id,
        student_answer=payload.student_answer,
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    try:
        attempt = await grade_attempt(attempt, question, question.chunk)
    except ValueError:
        # Grading response was malformed — leave score/feedback unset so the
        # frontend can show a distinguishable "retry grading" state, per the
        # cross-cutting error-handling requirement.
        db.commit()
        return _to_response(attempt, question)

    db.commit()
    db.refresh(attempt)

    mastery = memory.record_attempt_result(db, current_user.id, question.concept_id, attempt.score or 0.0)
    due_at = (mastery.last_reviewed_at or datetime.now(timezone.utc)) + timedelta(days=max(mastery.interval_days, 1))
    hooks.upsert_schedule_item(db, current_user.id, question.concept_id, due_at)
    memory.maybe_update_error_note(db, current_user.id, question.concept_id)

    return _to_response(attempt, question)


@router.get("/{attempt_id}", response_model=AttemptResponse)
def get_attempt(
    attempt_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> AttemptResponse:
    attempt = db.get(Attempt, attempt_id)
    if attempt is None or attempt.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Attempt not found")
    return _to_response(attempt, attempt.question)

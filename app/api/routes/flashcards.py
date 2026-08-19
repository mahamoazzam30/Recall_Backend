import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.api.routes.quiz import select_questions_for_session
from app.db.models.attempt import Attempt
from app.db.models.question import Question
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.flashcard import (
    RECALL_SCORE,
    FlashcardReviewCreate,
    FlashcardReviewResponse,
    FlashcardSessionResponse,
)
from app.services import hooks, memory

router = APIRouter()


@router.get("/{course_id}/flashcards/next", response_model=FlashcardSessionResponse)
async def next_flashcards(
    course_id: uuid.UUID,
    concept_ids: list[uuid.UUID] | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> FlashcardSessionResponse:
    questions = await select_questions_for_session(db, current_user, course_id, concept_ids)
    return FlashcardSessionResponse(cards=questions)


@router.post("/{course_id}/flashcards/review", response_model=FlashcardReviewResponse, status_code=201)
def review_flashcard(
    course_id: uuid.UUID,
    payload: FlashcardReviewCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> FlashcardReviewResponse:
    question = db.get(Question, payload.question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    score = RECALL_SCORE[payload.recall]

    attempt = Attempt(
        question_id=question.id,
        user_id=current_user.id,
        student_answer=f"self-report:{payload.recall.value}",
        score=score,
        graded_at=datetime.now(timezone.utc),
    )
    db.add(attempt)
    db.commit()

    mastery = memory.record_attempt_result(db, current_user.id, question.concept_id, score)
    due_at = (mastery.last_reviewed_at or datetime.now(timezone.utc)) + timedelta(days=max(mastery.interval_days, 1))
    hooks.upsert_schedule_item(db, current_user.id, question.concept_id, due_at)

    return FlashcardReviewResponse(
        question_id=question.id,
        score=score,
        mastery_pct=round(mastery.accuracy_ema * 100, 1),
    )

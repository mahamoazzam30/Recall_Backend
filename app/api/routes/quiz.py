import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.models.concept import Concept
from app.db.models.question import Question
from app.db.models.subject import Subject
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.quiz import QuizSessionResponse
from app.services import memory, retrieval
from app.services.generation import generate_question

router = APIRouter()

_QUESTIONS_PER_SESSION = 5
_SEED_QUERY = "key concepts, definitions, and important facts"


@router.get("/session/next", response_model=QuizSessionResponse)
async def next_session(
    subject_id: uuid.UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> QuizSessionResponse:
    subject = db.get(Subject, subject_id)
    if subject is None or subject.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Subject not found")

    concept_ids = list(db.execute(select(Concept.id).where(Concept.subject_id == subject_id)).scalars().all())

    questions: list[Question] = []

    if concept_ids:
        weak_ids = memory.weakest_concept_ids(db, current_user.id, concept_ids, limit=_QUESTIONS_PER_SESSION)
        stmt = select(Question).where(Question.concept_id.in_(weak_ids)).limit(_QUESTIONS_PER_SESSION)
        questions = list(db.execute(stmt).scalars().all())

    if len(questions) < _QUESTIONS_PER_SESSION:
        # Not enough banked questions yet for weak concepts — generate fresh ones
        # from retrieved passages until the session is full.
        chunks = await retrieval.search(db, _SEED_QUERY, subject_id, top_k=_QUESTIONS_PER_SESSION)
        for chunk in chunks:
            if len(questions) >= _QUESTIONS_PER_SESSION:
                break
            try:
                question = await generate_question(db, chunk, subject_id)
                questions.append(question)
            except Exception:
                continue

    if not questions:
        raise HTTPException(status_code=422, detail="No material has been ingested for this subject yet")

    return QuizSessionResponse(questions=questions)

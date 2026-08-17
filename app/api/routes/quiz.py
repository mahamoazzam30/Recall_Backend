import uuid

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.models.concept import Concept
from app.db.models.course import Course
from app.db.models.question import Question
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.quiz import QuizSessionResponse
from app.services import hooks, memory, retrieval
from app.services.generation import generate_question

router = APIRouter()

_QUESTIONS_PER_SESSION = 5
_SEED_QUERY = "key concepts, definitions, and important facts"


async def build_quiz_session(
    db: Session, user: User, course_id: uuid.UUID, concept_ids: list[uuid.UUID] | None = None
) -> QuizSessionResponse:
    course = db.get(Course, course_id)
    if course is None or course.user_id != user.id:
        raise HTTPException(status_code=404, detail="Course not found")

    all_concept_ids = list(db.execute(select(Concept.id).where(Concept.course_id == course_id)).scalars().all())

    if concept_ids:
        target_ids = [cid for cid in concept_ids if cid in set(all_concept_ids)]
    else:
        target_ids = hooks.todays_exam_targets(db, user.id, course_id)
        if not target_ids and all_concept_ids:
            target_ids = memory.weakest_concept_ids(db, user.id, all_concept_ids, limit=_QUESTIONS_PER_SESSION)

    questions: list[Question] = []
    if target_ids:
        stmt = select(Question).where(Question.concept_id.in_(target_ids)).limit(_QUESTIONS_PER_SESSION)
        questions = list(db.execute(stmt).scalars().all())

    if len(questions) < _QUESTIONS_PER_SESSION:
        # Not enough banked questions yet — generate fresh ones from retrieved
        # passages until the session is full.
        chunks = await retrieval.search(db, _SEED_QUERY, course_id, top_k=_QUESTIONS_PER_SESSION)
        for chunk in chunks:
            if len(questions) >= _QUESTIONS_PER_SESSION:
                break
            try:
                question = await generate_question(db, chunk, course_id)
                questions.append(question)
            except Exception:
                continue

    if not questions:
        raise HTTPException(status_code=422, detail="No material has been ingested for this course yet")

    return QuizSessionResponse(questions=questions)


@router.get("/session/next", response_model=QuizSessionResponse)
async def next_session(
    course_id: uuid.UUID,
    concept_ids: list[uuid.UUID] | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> QuizSessionResponse:
    return await build_quiz_session(db, current_user, course_id, concept_ids)

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


async def select_questions_for_session(
    db: Session, user: User, course_id: uuid.UUID, concept_ids: list[uuid.UUID] | None = None
) -> list[Question]:
    course = db.get(Course, course_id)
    if course is None or course.user_id != user.id:
        raise HTTPException(status_code=404, detail="Course not found")

    all_concepts = list(db.execute(select(Concept).where(Concept.course_id == course_id)).scalars().all())
    all_concept_ids = [c.id for c in all_concepts]

    # A single explicit concept means the student picked one topic to be
    # quizzed on — lock both retrieval and fresh-question tagging to it so
    # the session doesn't drift onto other topics.
    topic: Concept | None = None
    if concept_ids:
        target_ids = [cid for cid in concept_ids if cid in set(all_concept_ids)]
        if len(target_ids) == 1:
            topic = next((c for c in all_concepts if c.id == target_ids[0]), None)
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
        # passages until the session is full. When a topic was picked, seed
        # retrieval with its name and pin every fresh question to it.
        seed_query = topic.name if topic else _SEED_QUERY
        chunks = await retrieval.search(db, seed_query, course_id, top_k=_QUESTIONS_PER_SESSION)
        for chunk in chunks:
            if len(questions) >= _QUESTIONS_PER_SESSION:
                break
            try:
                question = await generate_question(
                    db, chunk, course_id, concept_override=topic.name if topic else None
                )
                questions.append(question)
            except Exception:
                continue

    if not questions:
        raise HTTPException(status_code=422, detail="No material has been ingested for this course yet")

    return questions


async def build_quiz_session(
    db: Session, user: User, course_id: uuid.UUID, concept_ids: list[uuid.UUID] | None = None
) -> QuizSessionResponse:
    questions = await select_questions_for_session(db, user, course_id, concept_ids)
    return QuizSessionResponse(questions=questions)


@router.get("/session/next", response_model=QuizSessionResponse)
async def next_session(
    course_id: uuid.UUID,
    concept_ids: list[uuid.UUID] | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> QuizSessionResponse:
    return await build_quiz_session(db, current_user, course_id, concept_ids)

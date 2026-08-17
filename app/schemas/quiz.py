import uuid

from pydantic import BaseModel

from app.db.models.question import QuestionType


class QuestionOut(BaseModel):
    id: uuid.UUID
    type: QuestionType
    prompt: str
    choices: list | None = None
    concept_id: uuid.UUID
    chunk_id: uuid.UUID

    model_config = {"from_attributes": True}


class QuizSessionResponse(BaseModel):
    questions: list[QuestionOut]


class AttemptCreate(BaseModel):
    question_id: uuid.UUID
    student_answer: str


class AttemptResponse(BaseModel):
    id: uuid.UUID
    question_id: uuid.UUID
    student_answer: str
    score: float | None
    feedback: str | None
    source_passage: str | None = None
    source_page_ref: str | None = None

    model_config = {"from_attributes": True}


class ContestCreate(BaseModel):
    student_note: str


class ContestResponse(BaseModel):
    id: uuid.UUID
    attempt_id: uuid.UUID
    status: str
    student_note: str
    resolution_note: str | None

    model_config = {"from_attributes": True}

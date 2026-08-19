import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.models.course import Course
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.chat import ChatRequest, ChatResponse, ChatSourceOut
from app.services.chat import answer_question

router = APIRouter()


@router.post("/{course_id}/chat", response_model=ChatResponse)
async def chat_with_course(
    course_id: uuid.UUID,
    payload: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ChatResponse:
    course = db.get(Course, course_id)
    if course is None or course.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Course not found")

    answer, chunks = await answer_question(db, course_id, course.name, payload.question)
    return ChatResponse(
        answer=answer,
        sources=[ChatSourceOut(content=c.content, page_ref=c.page_ref) for c in chunks],
    )

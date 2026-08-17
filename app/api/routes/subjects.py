from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.models.subject import Subject
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.auth import SubjectCreate, SubjectResponse

router = APIRouter()


@router.post("", response_model=SubjectResponse, status_code=201)
def create_subject(
    payload: SubjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> Subject:
    subject = Subject(user_id=current_user.id, name=payload.name)
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject


@router.get("", response_model=list[SubjectResponse])
def list_subjects(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
) -> list[Subject]:
    return db.query(Subject).filter(Subject.user_id == current_user.id).all()

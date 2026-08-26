import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.models.attempt import Attempt
from app.db.models.contest import Contest
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.quiz import ContestCreate, ContestResponse

router = APIRouter()


@router.post("/{attempt_id}/contest", response_model=ContestResponse, status_code=201)
def contest_grade(
    attempt_id: uuid.UUID,
    payload: ContestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Contest:
    attempt = db.get(Attempt, attempt_id)
    if attempt is None or attempt.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Attempt not found")

    contest = Contest(attempt_id=attempt.id, student_note=payload.student_note)
    db.add(contest)
    db.commit()
    db.refresh(contest)
    return contest

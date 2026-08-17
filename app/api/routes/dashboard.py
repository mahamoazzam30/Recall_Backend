from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.models.attempt import Attempt
from app.db.models.concept import Concept
from app.db.models.mastery import Mastery
from app.db.models.question import Question
from app.db.models.schedule_item import ScheduleItem, ScheduleStatus
from app.db.models.user import User
from app.db.session import get_db
from app.schemas.dashboard import DueTodayOut, HistoryPoint, MasteryOut, StreakOut

router = APIRouter()


@router.get("/mastery", response_model=list[MasteryOut])
def get_mastery(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[MasteryOut]:
    stmt = select(Mastery, Concept).join(Concept, Mastery.concept_id == Concept.id).where(
        Mastery.user_id == current_user.id
    )
    rows = db.execute(stmt).all()
    return [
        MasteryOut(
            concept_id=m.concept_id,
            concept_name=c.name,
            accuracy_ema=m.accuracy_ema,
            repetitions=m.repetitions,
        )
        for m, c in rows
    ]


@router.get("/due-today", response_model=list[DueTodayOut])
def get_due_today(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[DueTodayOut]:
    now = datetime.now(timezone.utc)
    stmt = (
        select(ScheduleItem, Concept)
        .join(Concept, ScheduleItem.concept_id == Concept.id)
        .where(
            ScheduleItem.user_id == current_user.id,
            ScheduleItem.status != ScheduleStatus.completed,
            ScheduleItem.due_at <= now,
        )
    )
    rows = db.execute(stmt).all()
    return [DueTodayOut(concept_id=s.concept_id, concept_name=c.name, due_at=s.due_at) for s, c in rows]


@router.get("/streak", response_model=StreakOut)
def get_streak(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> StreakOut:
    stmt = (
        select(Attempt.graded_at)
        .where(Attempt.user_id == current_user.id, Attempt.graded_at.is_not(None))
        .order_by(Attempt.graded_at.desc())
    )
    graded_dates = sorted({row[0].date() for row in db.execute(stmt).all()}, reverse=True)

    current_streak = 0
    cursor = datetime.now(timezone.utc).date()
    for d in graded_dates:
        if d == cursor:
            current_streak += 1
            cursor -= timedelta(days=1)
        elif d == cursor + timedelta(days=1):
            continue
        else:
            break

    longest_streak = 0
    running = 0
    prev_date = None
    for d in sorted(graded_dates):
        if prev_date is not None and d == prev_date + timedelta(days=1):
            running += 1
        else:
            running = 1
        longest_streak = max(longest_streak, running)
        prev_date = d

    return StreakOut(current_streak_days=current_streak, longest_streak_days=longest_streak)


@router.get("/history", response_model=list[HistoryPoint])
def get_history(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[HistoryPoint]:
    stmt = (
        select(Attempt, Concept)
        .join(Question, Attempt.question_id == Question.id)
        .join(Concept, Concept.id == Question.concept_id)
        .where(Attempt.user_id == current_user.id, Attempt.graded_at.is_not(None))
        .order_by(Attempt.graded_at.asc())
    )
    rows = db.execute(stmt).all()
    return [
        HistoryPoint(
            date=attempt.graded_at,
            concept_id=concept.id,
            concept_name=concept.name,
            accuracy=attempt.score or 0.0,
        )
        for attempt, concept in rows
    ]

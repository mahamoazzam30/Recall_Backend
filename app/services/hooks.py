"""Scheduler interceptor.

Invoked when (a) schedule_items.due_at <= now, or (b) a concept's rolling
accuracy drops below a threshold. Surfaces a "review session available" flag
for the frontend to poll/display, rather than the student manually requesting one.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.mastery import Mastery
from app.db.models.schedule_item import ScheduleItem, ScheduleStatus

WEAK_ACCURACY_THRESHOLD = 0.6


def has_review_available(db: Session, user_id: uuid.UUID) -> bool:
    now = datetime.now(timezone.utc)

    due_stmt = select(ScheduleItem).where(
        ScheduleItem.user_id == user_id,
        ScheduleItem.status != ScheduleStatus.completed,
        ScheduleItem.due_at <= now,
    )
    if db.execute(due_stmt).first() is not None:
        return True

    weak_stmt = select(Mastery).where(
        Mastery.user_id == user_id,
        Mastery.accuracy_ema < WEAK_ACCURACY_THRESHOLD,
        Mastery.repetitions > 0,
    )
    return db.execute(weak_stmt).first() is not None


def upsert_schedule_item(db: Session, user_id: uuid.UUID, concept_id: uuid.UUID, due_at: datetime) -> ScheduleItem:
    stmt = select(ScheduleItem).where(
        ScheduleItem.user_id == user_id,
        ScheduleItem.concept_id == concept_id,
        ScheduleItem.status != ScheduleStatus.completed,
    )
    item = db.execute(stmt).scalar_one_or_none()
    if item is None:
        item = ScheduleItem(user_id=user_id, concept_id=concept_id, due_at=due_at, status=ScheduleStatus.pending)
        db.add(item)
    else:
        item.due_at = due_at
        item.status = ScheduleStatus.pending
    db.commit()
    db.refresh(item)
    return item

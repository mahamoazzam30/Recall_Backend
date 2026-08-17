"""Mastery & error-pattern store.

Updates the `mastery` row per concept after each attempt (accuracy EMA), and
tracks recurring error-pattern tags that bias future question selection
toward weak spots.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.mastery import Mastery
from app.services.scheduler import SM2State, accuracy_ema_update, sm2_update


def get_or_create_mastery(db: Session, user_id: uuid.UUID, concept_id: uuid.UUID) -> Mastery:
    stmt = select(Mastery).where(Mastery.user_id == user_id, Mastery.concept_id == concept_id)
    mastery = db.execute(stmt).scalar_one_or_none()
    if mastery is None:
        mastery = Mastery(user_id=user_id, concept_id=concept_id)
        db.add(mastery)
        db.flush()
    return mastery


def record_attempt_result(db: Session, user_id: uuid.UUID, concept_id: uuid.UUID, score_0_to_1: float) -> Mastery:
    mastery = get_or_create_mastery(db, user_id, concept_id)

    state = SM2State(
        ease_factor=mastery.ease_factor,
        interval_days=mastery.interval_days,
        repetitions=mastery.repetitions,
    )
    new_state, due_at = sm2_update(state, score_0_to_1)

    mastery.ease_factor = new_state.ease_factor
    mastery.interval_days = new_state.interval_days
    mastery.repetitions = new_state.repetitions
    mastery.accuracy_ema = accuracy_ema_update(mastery.accuracy_ema, score_0_to_1)
    mastery.last_reviewed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(mastery)
    return mastery


def weakest_concept_ids(db: Session, user_id: uuid.UUID, subject_concept_ids: list[uuid.UUID], limit: int = 1) -> list[uuid.UUID]:
    """Rank concepts by lowest accuracy_ema (weakest first); unseen concepts rank first (ema defaults to 0)."""
    stmt = select(Mastery).where(Mastery.user_id == user_id, Mastery.concept_id.in_(subject_concept_ids))
    seen = {m.concept_id: m.accuracy_ema for m in db.execute(stmt).scalars().all()}

    ranked = sorted(subject_concept_ids, key=lambda cid: seen.get(cid, 0.0))
    return ranked[:limit]

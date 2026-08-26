"""Mastery & error-pattern store.

Updates the `mastery` row per concept after each attempt (accuracy EMA), and
tracks recurring error-pattern tags that bias future question selection
toward weak spots.
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.attempt import Attempt
from app.db.models.mastery import Mastery
from app.db.models.question import Question
from app.services.scheduler import SM2State, accuracy_ema_update, sm2_update

WEAK_ACCURACY_THRESHOLD = 0.5


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


def weakest_concept_ids(db: Session, user_id: uuid.UUID, course_concept_ids: list[uuid.UUID], limit: int = 1) -> list[uuid.UUID]:
    """Rank concepts by lowest accuracy_ema (weakest first); unseen concepts rank first (ema defaults to 0)."""
    stmt = select(Mastery).where(Mastery.user_id == user_id, Mastery.concept_id.in_(course_concept_ids))
    seen = {m.concept_id: m.accuracy_ema for m in db.execute(stmt).scalars().all()}

    ranked = sorted(course_concept_ids, key=lambda cid: seen.get(cid, 0.0))
    return ranked[:limit]


def maybe_update_error_note(db: Session, user_id: uuid.UUID, concept_id: uuid.UUID) -> None:
    """If a concept has repeated weak attempts, surface the most recent grader feedback
    as a short human-readable note on its mastery row (skipped for mcq/cloze, which have
    no feedback text to draw from).
    """
    stmt = (
        select(Attempt)
        .join(Question, Attempt.question_id == Question.id)
        .where(Attempt.user_id == user_id, Question.concept_id == concept_id, Attempt.score.is_not(None))
        .order_by(Attempt.graded_at.desc())
        .limit(3)
    )
    recent = list(db.execute(stmt).scalars().all())
    weak_count = sum(1 for a in recent if a.score < WEAK_ACCURACY_THRESHOLD)
    if weak_count < 2:
        return

    latest_feedback = next((a.feedback for a in recent if a.feedback), None)
    if not latest_feedback:
        return

    mastery = get_or_create_mastery(db, user_id, concept_id)
    mastery.error_note = latest_feedback
    db.commit()

"""Pure-code midterm/exam prep planner. No DB or model calls here — takes
concept/accuracy data as input and returns day-by-day study targets, mirroring
scheduler.py's deterministic, unit-testable style.
"""
import uuid
from datetime import date, timedelta

CRAM_WINDOW_DAYS = 3


def readiness_pct(concept_accuracy: dict[uuid.UUID, float]) -> float:
    """Mean accuracy_ema across the course's concepts (unseen concepts count as 0)."""
    if not concept_accuracy:
        return 0.0
    return round(100 * sum(concept_accuracy.values()) / len(concept_accuracy), 1)


def generate_plan_days(
    exam_date: date, today: date, concept_accuracy: dict[uuid.UUID, float]
) -> list[tuple[date, list[uuid.UUID]]]:
    """Distribute concepts across the days remaining before `exam_date`, weakest-first,
    with the last CRAM_WINDOW_DAYS days narrowed to weak concepts only.
    """
    days_left = max((exam_date - today).days, 0)
    if days_left == 0 or not concept_accuracy:
        return []

    ranked = sorted(concept_accuracy.keys(), key=lambda cid: concept_accuracy[cid])
    weak_cutoff = max(1, len(ranked) // 2)
    weak_concepts = ranked[:weak_cutoff] or ranked

    plan_days: list[tuple[date, list[uuid.UUID]]] = []
    for offset in range(days_left):
        day = today + timedelta(days=offset)
        days_to_exam = (exam_date - day).days

        if days_to_exam < CRAM_WINDOW_DAYS:
            targets = weak_concepts
        else:
            # Round-robin the full ranked list so every concept resurfaces, weakest first each cycle.
            start = (offset * 3) % len(ranked)
            targets = (ranked[start:] + ranked[:start])[:3]

        plan_days.append((day, targets))

    return plan_days

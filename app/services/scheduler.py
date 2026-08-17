"""Pure-code spaced repetition (SM-2). No model calls anywhere in this file —
deliberately deterministic and unit-testable in isolation.
"""
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass
class SM2State:
    ease_factor: float
    interval_days: int
    repetitions: int


def sm2_update(state: SM2State, score_0_to_1: float) -> tuple[SM2State, datetime]:
    """Apply one SM-2 review update.

    `score_0_to_1` is the grading result (0 = fully wrong, 1 = fully correct).
    It's mapped onto SM-2's traditional 0-5 quality scale.
    """
    quality = round(score_0_to_1 * 5)

    if quality < 3:
        # Failed recall: reset repetitions, review again soon.
        new_repetitions = 0
        new_interval = 1
    else:
        new_repetitions = state.repetitions + 1
        if new_repetitions == 1:
            new_interval = 1
        elif new_repetitions == 2:
            new_interval = 6
        else:
            new_interval = round(state.interval_days * state.ease_factor)

    new_ease_factor = state.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    new_ease_factor = max(1.3, new_ease_factor)

    new_state = SM2State(
        ease_factor=new_ease_factor,
        interval_days=new_interval,
        repetitions=new_repetitions,
    )
    due_at = datetime.now(timezone.utc) + timedelta(days=new_interval)
    return new_state, due_at


def accuracy_ema_update(previous_ema: float, latest_score: float, alpha: float = 0.3) -> float:
    """Exponential moving average of accuracy, used to bias question selection."""
    return alpha * latest_score + (1 - alpha) * previous_ema

from app.services.scheduler import SM2State, accuracy_ema_update, sm2_update


def test_sm2_first_success_sets_interval_to_one_day():
    state = SM2State(ease_factor=2.5, interval_days=0, repetitions=0)
    new_state, due_at = sm2_update(state, score_0_to_1=1.0)

    assert new_state.repetitions == 1
    assert new_state.interval_days == 1
    assert new_state.ease_factor >= 2.5


def test_sm2_second_success_sets_interval_to_six_days():
    state = SM2State(ease_factor=2.5, interval_days=1, repetitions=1)
    new_state, _ = sm2_update(state, score_0_to_1=1.0)

    assert new_state.repetitions == 2
    assert new_state.interval_days == 6


def test_sm2_failure_resets_repetitions_and_interval():
    state = SM2State(ease_factor=2.6, interval_days=15, repetitions=4)
    new_state, _ = sm2_update(state, score_0_to_1=0.0)

    assert new_state.repetitions == 0
    assert new_state.interval_days == 1


def test_sm2_ease_factor_never_drops_below_minimum():
    state = SM2State(ease_factor=1.3, interval_days=1, repetitions=1)
    new_state, _ = sm2_update(state, score_0_to_1=0.0)

    assert new_state.ease_factor >= 1.3


def test_accuracy_ema_moves_toward_latest_score():
    ema = accuracy_ema_update(previous_ema=0.5, latest_score=1.0, alpha=0.3)
    assert 0.5 < ema < 1.0

    ema_after_fail = accuracy_ema_update(previous_ema=ema, latest_score=0.0, alpha=0.3)
    assert ema_after_fail < ema

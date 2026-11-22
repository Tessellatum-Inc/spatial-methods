import pytest

from clock_state_covariance import (
    clock_process_noise_covariance,
    clock_state_transition,
    propagate_clock_state_covariance,
)


def test_constant_drift_transition():
    assert clock_state_transition(2.0) == [[1.0, 2.0], [0.0, 1.0]]


def test_white_frequency_rate_process_noise_exact_integral():
    assert clock_process_noise_covariance(2.0, 3.0) == [
        [8.0, 6.0], [6.0, 6.0]
    ]


def test_zero_process_noise_matches_common_offset_and_drift_covariance():
    initial = [[0.25, 0.01], [0.01, 0.04]]
    result = propagate_clock_state_covariance([10.0, 12.0, 15.0], initial, 0.0)
    offsets = result["offset_covariance"]
    for i, ti in enumerate([10.0, 12.0, 15.0]):
        for j, tj in enumerate([10.0, 12.0, 15.0]):
            di, dj = ti - 10.0, tj - 10.0
            expected = initial[0][0] + di * initial[0][1] + dj * initial[1][0] + di * dj * initial[1][1]
            assert offsets[i][j] == pytest.approx(expected)


def test_process_noise_creates_correct_cross_epoch_offset_covariance():
    result = propagate_clock_state_covariance([0.0, 1.0, 2.0], [[0, 0], [0, 0]], 3.0)
    offsets = result["offset_covariance"]
    assert offsets[1][1] == pytest.approx(1.0)
    assert offsets[2][2] == pytest.approx(8.0)
    assert offsets[1][2] == pytest.approx(2.5)
    assert offsets[2][1] == pytest.approx(2.5)


def test_nonzero_initial_uncertainty_and_process_noise_are_both_propagated():
    result = propagate_clock_state_covariance([0.0, 2.0], [[0.25, 0], [0, 0.04]], 0.5)
    # Initial offset uncertainty plus drift uncertainty plus integrated process noise.
    assert result["offset_covariance"][1][1] == pytest.approx(0.25 + 4 * 0.04 + 0.5 * 8 / 3)


@pytest.mark.parametrize("epochs, covariance, q", [
    ([], [[0, 0], [0, 0]], 0),
    ([0, 0], [[0, 0], [0, 0]], 0),
    ([0, 1], [[1, 2], [2, 1]], 0),
    ([0, 1], [[1, 0], [0, 1]], -1),
])
def test_rejects_invalid_epochs_covariance_or_noise(epochs, covariance, q):
    with pytest.raises(ValueError):
        propagate_clock_state_covariance(epochs, covariance, q)


def test_joint_clock_state_covariance_is_symmetric_with_transposed_cross_epoch_blocks():
    result = propagate_clock_state_covariance(
        [0.0, 2.0], [[1.0, 0.2], [0.2, 0.5]], 0.0
    )
    joint = result["joint_state_covariance"]
    for i in range(4):
        for j in range(4):
            assert joint[i][j] == pytest.approx(joint[j][i])
    # Cov(x_0, x_1) = P_0 Phi(2)^T; the reverse block is its transpose.
    assert joint[0][2:4] == pytest.approx([1.4, 0.2])
    assert joint[1][2:4] == pytest.approx([1.2, 0.5])
    assert joint[2][0:2] == pytest.approx([1.4, 1.2])
    assert joint[3][0:2] == pytest.approx([0.2, 0.5])


def test_elapsed_interval_covariance_integrates_within_ping_process_noise():
    from clock_state_covariance import propagate_clock_elapsed_interval_covariance

    result = propagate_clock_elapsed_interval_covariance(
        [0.0], [2.0], [[0.0, 0.0], [0.0, 0.0]], 0.5
    )
    # Brownian frequency-rate noise integrates into offset with variance q*T^3/3.
    assert result["elapsed_interval_error_covariance"][0][0] == pytest.approx(4.0 / 3.0)
    assert result["event_epochs_s"] == [0.0, 2.0]


def test_overlapping_ping_intervals_retain_process_noise_cross_covariance():
    from clock_state_covariance import propagate_clock_elapsed_interval_covariance

    result = propagate_clock_elapsed_interval_covariance(
        [0.0, 1.0], [2.0, 3.0], [[0.0, 0.0], [0.0, 0.0]], 1.0
    )
    covariance = result["elapsed_interval_error_covariance"]
    assert covariance[0][0] == pytest.approx(8.0 / 3.0)
    assert covariance[1][1] == pytest.approx(20.0 / 3.0)
    assert covariance[0][1] == pytest.approx(23.0 / 6.0)
    assert covariance[1][0] == pytest.approx(23.0 / 6.0)


def test_elapsed_interval_constant_offset_cancels_exactly():
    from clock_state_covariance import propagate_clock_elapsed_interval_covariance

    result = propagate_clock_elapsed_interval_covariance(
        [10.0], [12.0], [[4.0, 0.0], [0.0, 0.0]], 0.0
    )
    assert result["elapsed_interval_error_covariance"][0][0] == pytest.approx(0.0)


def test_elapsed_interval_rejects_nonpositive_or_mismatched_events():
    from clock_state_covariance import propagate_clock_elapsed_interval_covariance

    with pytest.raises(ValueError, match="one receive epoch"):
        propagate_clock_elapsed_interval_covariance([0.0, 1.0], [2.0], [[0, 0], [0, 0]])
    with pytest.raises(ValueError, match="later than"):
        propagate_clock_elapsed_interval_covariance([1.0], [1.0], [[0, 0], [0, 0]])


def test_elapsed_interval_includes_initial_drift_uncertainty_and_process_noise():
    from clock_state_covariance import propagate_clock_elapsed_interval_covariance

    result = propagate_clock_elapsed_interval_covariance(
        [10.0], [12.0], [[0.0, 0.0], [0.0, 0.25]], 0.5
    )
    # T^2 Var(drift_0) + q*T^3/3; initial constant offset cancels.
    assert result["elapsed_interval_error_covariance"][0][0] == pytest.approx(
        4.0 * 0.25 + 0.5 * 8.0 / 3.0
    )



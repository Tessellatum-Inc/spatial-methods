import math
import pytest
from sampling import select_spatial_batch, ucb1_arm, gp_select_next


def test_spatial_selection_starts_with_highest_uncertainty_then_diversifies():
    points = [(0, 0), (0.1, 0), (10, 0), (10.1, 0)]
    uncertainty = [0.9, 0.8, 0.7, 0.6]
    chosen = select_spatial_batch(points, uncertainty, 2, diversity_weight=1.0)
    assert chosen[0] == 0
    assert chosen[1] == 2


def test_spatial_selection_honours_existing_samples_and_min_distance():
    points = [(0, 0), (0.5, 0), (5, 0)]
    assert select_spatial_batch(points, [1, 1, 0.1], 1,
                                selected=[0], min_distance=1.0) == [2]


def test_min_distance_can_leave_batch_partially_filled():
    points = [(0, 0), (0.1, 0)]
    assert select_spatial_batch(points, [1, 0.9], 2,
                                min_distance=1.0) == [0]


def test_ucb1_selects_untried_arm_first():
    assert ucb1_arm([5, 0, 2], [3, 0, 1]) == 1


def test_ucb1_uses_mean_plus_exploration():
    assert ucb1_arm([10, 10], [9, 1]) == 0


def test_invalid_sampling_inputs_rejected():
    with pytest.raises(ValueError):
        select_spatial_batch([(0, 0), (1, 1)], [1], 1)
    with pytest.raises(ValueError):
        ucb1_arm([1, -1], [0, 0])


def test_gp_ucb_returns_finite_posterior_and_candidate():
    idx, means, stds = gp_select_next(
        [(0.0,), (1.0,)], [0.0, 1.0],
        [(0.0,), (0.5,), (1.5,)], acquisition="ucb", beta=2.0,
    )
    assert idx in range(3)
    assert len(means) == len(stds) == 3
    assert all(math.isfinite(v) for v in means + stds)
    assert all(v >= 0 for v in stds)


def test_gp_expected_improvement_selects_from_candidate_set():
    idx, means, stds = gp_select_next(
        [(0.0,), (1.0,)], [0.0, 1.0],
        [(0.25,), (1.5,)], acquisition="ei",
    )
    assert idx in (0, 1)


def test_gp_handles_duplicate_observations_with_jitter():
    idx, means, stds = gp_select_next(
        [(0.0,), (0.0,)], [1.0, 1.0],
        [(0.5,), (1.0,)], noise=0.0,
    )
    assert idx in (0, 1)


def test_gp_rejects_invalid_acquisition():
    with pytest.raises(ValueError):
        gp_select_next([(0.0,)], [1.0], [(1.0,)], acquisition="thompson")

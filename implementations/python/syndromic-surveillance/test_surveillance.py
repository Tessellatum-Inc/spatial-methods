import pytest

from surveillance import cusum, ears


def test_cusum_accumulates_only_deviations_beyond_allowance():
    result = cusum([10, 10, 12, 13, 8, 7], 10, allowance=1, threshold=3)
    assert result["upper"] == [0, 0, 1, 3, 0, 0]
    assert result["lower"] == [0, 0, 0, 0, 1, 3]
    assert result["alarm"] == [False, False, False, True, False, True]


def test_cusum_is_two_sided_and_resets_after_return_to_target():
    result = cusum([15, 10, 5], 10, allowance=0, threshold=4)
    assert result["upper"] == [5, 0, 0]
    assert result["lower"] == [0, 0, 5]
    assert result["alarm"] == [True, False, True]


def test_ears_baselines_are_lagged_and_scores_match_hand_calculation():
    counts = [4, 4, 4, 4, 4, 4, 4, 10]
    result = ears(counts, baseline_window=7, threshold=3)
    assert result["c1"][:7] == [None] * 7
    assert result["c1"][7] == pytest.approx(3.0)
    assert result["c2"][:7] == [None] * 7
    assert result["c2"][7] is None  # C2 excludes two most recent observations.


def test_ears_c2_and_c3_use_only_prior_baseline_and_positive_scores():
    counts = [2] * 9 + [8, 8, 2]
    result = ears(counts, baseline_window=7, c2_exclusion=2, threshold=3)
    assert result["c2"][9] == pytest.approx(6 / 2)
    assert result["c2"][10] == pytest.approx(6 / 2)
    assert result["c3"][10] == pytest.approx(6.0)
    assert result["c3"][11] == pytest.approx(6.0)


def test_ears_returns_no_alarm_until_baseline_is_available():
    result = ears([0, 0, 0, 0, 0, 0, 0], baseline_window=7)
    assert result["c1"] == [None] * 7
    assert result["c1_alarm"] == [False] * 7


@pytest.mark.parametrize("observations,target,allowance,threshold", [
    ([], 0, 0, 1), ([1], float("nan"), 0, 1),
    ([1], 0, -1, 1), ([1], 0, 0, 0), ([True], 0, 0, 1),
])
def test_cusum_rejects_invalid_inputs(observations, target, allowance, threshold):
    with pytest.raises(ValueError):
        cusum(observations, target, allowance=allowance, threshold=threshold)


@pytest.mark.parametrize("counts,window,exclusion", [
    ([], 7, 2), ([1, -1], 2, 0), ([1, True], 2, 0),
    ([1, 2], 1, 0), ([1, 2], 2, -1),
])
def test_ears_rejects_invalid_inputs(counts, window, exclusion):
    with pytest.raises(ValueError):
        ears(counts, baseline_window=window, c2_exclusion=exclusion)


def test_ears_constant_baseline_does_not_divide_by_zero():
    result = ears([0] * 7 + [10], baseline_window=7)
    assert result["c1"][7] == 10.0
    assert result["c1_alarm"][7]

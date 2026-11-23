import pytest

from stratified_sampling import neyman_allocation, stratified_total_estimate


def test_neyman_allocation_matches_worked_equal_cost_example():
    assert neyman_allocation([4000, 3500, 2500], [12, 20, 8], 200) == (70, 101, 29)


def test_neyman_allocation_is_integer_bounded_and_sums_to_sample_size():
    allocation = neyman_allocation([2, 100, 3], [100, 1, 10], 50)
    assert sum(allocation) == 50
    assert all(1 <= n <= N for n, N in zip(allocation, [2, 100, 3]))


def test_zero_pilot_variance_falls_back_to_proportional_allocation():
    assert neyman_allocation([40, 35, 25], [0, 0, 0], 20) == (8, 7, 5)


def test_stratified_total_and_variance_match_hand_calculation():
    result = stratified_total_estimate(
        [4000, 3500, 2500],
        [70, 101, 29],
        [36, 57, 23],
        [12, 20, 8],
    )
    assert result.total_estimate == pytest.approx(401000)
    assert result.mean_estimate == pytest.approx(40.1)
    expected_variance = sum(
        N**2 * (1 - n / N) * sd**2 / n
        for N, n, sd in zip([4000, 3500, 2500], [70, 101, 29], [12, 20, 8])
    )
    assert result.total_variance_estimate == pytest.approx(expected_variance)
    assert result.mean_variance_estimate == pytest.approx(expected_variance / 10000**2)


def test_census_stratum_has_zero_sampling_variance():
    result = stratified_total_estimate([3, 10], [3, 4], [5, 7], [0, 2])
    assert result.stratum_variance_contributions[0] == 0
    assert result.total_variance_estimate == pytest.approx(10**2 * (1 - 4/10) * 4 / 4)


@pytest.mark.parametrize(
    "args",
    [
        ([2, 3], [1], 3),
        ([2, 3], [1, 1], 1),
        ([2, 3], [1, 1], 6),
        ([2, 3], [1, float("nan")], 3),
        ([2, 3], [1, 1], True),
    ],
)
def test_neyman_allocation_rejects_invalid_inputs(args):
    with pytest.raises(ValueError):
        neyman_allocation(*args)


def test_variance_requires_two_observations_in_non_census_strata():
    with pytest.raises(ValueError, match="at least two"):
        stratified_total_estimate([10], [1], [4], [2])


def test_estimator_rejects_misaligned_and_oversized_samples():
    with pytest.raises(ValueError):
        stratified_total_estimate([10, 20], [2], [1], [1])
    with pytest.raises(ValueError):
        stratified_total_estimate([10], [11], [1], [1])


def test_stratified_estimator_accepts_signed_means():
    result = stratified_total_estimate([10, 10], [5, 5], [-2, 1], [1, 1])
    assert result.total_estimate == pytest.approx(-10)
    assert result.mean_estimate == pytest.approx(-0.5)

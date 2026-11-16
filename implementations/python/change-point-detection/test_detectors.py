import pytest
from detectors import binary_segmentation, cusum, pelt


def test_binary_segmentation_finds_single_mean_shift():
    x = [0.0] * 20 + [5.0] * 20
    assert binary_segmentation(x, max_changes=1, min_size=4) == [20]


def test_pelt_finds_two_clear_shifts():
    x = [0.0] * 15 + [4.0] * 15 + [-3.0] * 15
    assert pelt(x, penalty=3.0, min_size=4) == [15, 30]


def test_pelt_matches_brute_force_objective_small_series():
    x = [0, 0, 3, 3, -2, -2]
    penalty = 1.0
    cuts = pelt(x, penalty=penalty, min_size=1)
    def objective(points):
        bounds = [0, *points, len(x)]
        return sum(sum((v - sum(x[a:b]) / (b-a))**2 for v in x[a:b])
                   for a, b in zip(bounds, bounds[1:])) + penalty * len(points)
    import itertools
    all_cuts = []
    for k in range(len(x)):
        all_cuts.extend(itertools.combinations(range(1, len(x)), k))
    assert objective(cuts) == pytest.approx(min(map(objective, all_cuts)))


def test_cusum_detects_persistent_upward_shift():
    x = [0.0] * 10 + [3.0] * 10
    assert cusum(x, target=0.0, threshold=5.0) == [11, 13, 15, 17, 19]


@pytest.mark.parametrize("kwargs", [
    {"max_changes": -1}, {"max_changes": 1.5}, {"max_changes": True},
])
def test_binary_segmentation_rejects_invalid_change_count(kwargs):
    with pytest.raises(ValueError):
        binary_segmentation([0, 1, 2, 3], **kwargs)


def test_invalid_penalty_and_nonfinite_data_rejected():
    with pytest.raises(ValueError):
        pelt([0, 1, 2], penalty=float("nan"))
    with pytest.raises(ValueError):
        cusum([0, float("inf")], threshold=1)


def test_pelt_rejects_impossible_minimum_segment_size():
    with pytest.raises(ValueError):
        pelt([0, 1, 2], penalty=1, min_size=4)


def test_segmentation_rejects_non_integer_min_size():
    with pytest.raises(ValueError):
        pelt([0, 1, 2, 3], penalty=1, min_size=1.5)

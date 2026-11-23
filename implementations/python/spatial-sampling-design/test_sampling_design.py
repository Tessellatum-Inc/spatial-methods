import math
import random

import pytest

from sampling_design import (
    kmeans_coverage,
    latin_hypercube,
    maximin_latin_hypercube,
    minimum_pair_distance,
)


def test_latin_hypercube_uses_each_stratum_once_per_dimension():
    n = 12
    points = latin_hypercube(n, [(-2, 4), (10, 70)], seed=11)
    assert len(points) == n
    for dimension, (lower, upper) in enumerate([(-2, 4), (10, 70)]):
        width = (upper - lower) / n
        strata = sorted(
            min(n - 1, int((point[dimension] - lower) / width))
            for point in points
        )
        assert strata == list(range(n))


def test_centered_latin_hypercube_uses_stratum_midpoints():
    points = latin_hypercube(4, [(0, 1)], seed=2, centered=True)
    assert sorted(point[0] for point in points) == [0.125, 0.375, 0.625, 0.875]


def test_seeded_design_is_reproducible_and_does_not_mutate_global_rng():
    random.seed(77)
    before = random.getstate()
    a = latin_hypercube(8, [(0, 1), (-1, 1)], seed=42)
    after = random.getstate()
    b = latin_hypercube(8, [(0, 1), (-1, 1)], seed=42)
    assert a == b
    assert before == after


def test_maximin_selects_best_candidate_design():
    bounds = [(0, 1), (0, 1)]
    selected = maximin_latin_hypercube(10, bounds, candidates=20, seed=9)
    rng = random.Random(9)
    scores = []
    for _ in range(20):
        design = latin_hypercube(10, bounds, seed=rng.getrandbits(64))
        scores.append(minimum_pair_distance(design))
    assert minimum_pair_distance(selected) == pytest.approx(max(scores))


def test_maximin_preserves_latin_stratification():
    n = 9
    points = maximin_latin_hypercube(n, [(0, 1), (0, 1)], candidates=12, seed=3)
    for d in range(2):
        assert sorted(int(point[d] * n) for point in points) == list(range(n))


def test_kmeans_coverage_recovers_two_separated_cluster_centres():
    points = [(x, y) for x in (0.0, 0.2, 0.1, 10.0, 10.2, 10.1)
              for y in (0.0, 0.2)]
    centers = kmeans_coverage(points, 2)
    centers = sorted(centers)
    expected = [(0.1, 0.1), (10.1, 0.1)]
    for actual, target in zip(centers, expected):
        assert actual == pytest.approx(target)


def test_kmeans_coverage_returns_requested_number_and_dimension():
    centers = kmeans_coverage([(0, 0), (1, 0), (4, 0), (5, 0)], 3)
    assert len(centers) == 3
    assert all(len(center) == 2 for center in centers)


@pytest.mark.parametrize("n,bounds,candidates", [
    (0, [(0, 1)], 2),
    (2, [], 2),
    (2, [(1, 1)], 2),
    (2, [(0, float("inf"))], 2),
    (2, [(0, 1)], 0),
])
def test_latin_and_maximin_reject_invalid_parameters(n, bounds, candidates):
    if candidates > 0:
        with pytest.raises(ValueError):
            latin_hypercube(n, bounds)
    with pytest.raises(ValueError):
        maximin_latin_hypercube(n, bounds, candidates=candidates)


def test_maximin_requires_at_least_two_points():
    with pytest.raises(ValueError):
        maximin_latin_hypercube(1, [(0, 1)])


def test_minimum_pair_distance_rejects_invalid_shapes():
    with pytest.raises(ValueError):
        minimum_pair_distance([(0, 0)])
    with pytest.raises(ValueError):
        minimum_pair_distance([(0, 0), (1,)])
    with pytest.raises(ValueError):
        minimum_pair_distance([(0, float("nan")), (1, 2)])


def test_kmeans_rejects_invalid_input():
    with pytest.raises(ValueError):
        kmeans_coverage([(0, 0)], 2)
    with pytest.raises(ValueError):
        kmeans_coverage([(0, 0), (1, 1)], 0)
    with pytest.raises(ValueError):
        kmeans_coverage([(0, float("inf")), (1, 1)], 1)



def test_spatial_thinning_is_seeded_and_respects_minimum_distance():
    from sampling_design import spatial_thin_indices
    points = [(0,0), (0.1,0), (1,0), (1.1,0), (3,0)]
    selected = spatial_thin_indices(points, 0.5, seed=19)
    assert selected == spatial_thin_indices(points, 0.5, seed=19)
    for pos, i in enumerate(selected):
        for j in selected[pos+1:]:
            assert math.dist(points[i], points[j]) >= 0.5


def test_spatial_thinning_zero_distance_and_empty_input():
    from sampling_design import spatial_thin_indices
    assert spatial_thin_indices([(0,0), (0,0)], 0, seed=1) == [0,1]
    assert spatial_thin_indices([], 1, seed=1) == []


def test_spatial_thinning_rejects_invalid_inputs():
    from sampling_design import spatial_thin_indices
    with pytest.raises(ValueError):
        spatial_thin_indices([(0,0)], -1)
    with pytest.raises(ValueError):
        spatial_thin_indices([(0,0), (1,)], 1)
    with pytest.raises(ValueError):
        spatial_thin_indices([(0,float("nan"))], 1)

import math
import random

import pytest

from closest_pair import closest_pair


def brute(points):
    candidates = []
    for i, a in enumerate(points):
        for j in range(i + 1, len(points)):
            b = points[j]
            d2 = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2
            candidates.append((d2, i, j))
    return min(candidates)


def test_known_triangle():
    a, b, distance = closest_pair([(0, 0), (4, 0), (1, 1), (9, 9)])
    assert {a, b} == {(0.0, 0.0), (1.0, 1.0)}
    assert distance == pytest.approx(math.sqrt(2))


def test_duplicate_coordinates_return_zero_distance():
    a, b, distance = closest_pair([(5, 7), (0, 0), (5, 7)])
    assert a == b == (5.0, 7.0)
    assert distance == 0


def test_collinear_and_negative_coordinates():
    points = [(-8, -8), (10, 10), (2, 2), (2.1, 2.1), (40, 40)]
    a, b, distance = closest_pair(points)
    assert {a, b} == {(2.0, 2.0), (2.1, 2.1)}
    assert distance == pytest.approx(math.sqrt(0.02))


def test_seeded_random_clouds_match_independent_quadratic_oracle():
    rng = random.Random(20261115)
    for n in range(2, 90):
        for _ in range(8):
            points = [(rng.uniform(-100, 100), rng.uniform(-100, 100))
                      for _ in range(n)]
            expected_d2, _, _ = brute(points)
            _, _, actual = closest_pair(points)
            assert actual ** 2 == pytest.approx(expected_d2, rel=1e-10, abs=1e-10)


def test_ties_are_deterministic_by_original_indices():
    points = [(0, 0), (1, 0), (0, 1), (1, 1)]
    assert closest_pair(points) == closest_pair(points)
    first, second, distance = closest_pair(points)
    assert (first, second, distance) == ((0.0, 0.0), (1.0, 0.0), 1.0)


@pytest.mark.parametrize("points", [[], [(1, 2)], [(float("nan"), 0), (1, 1)],
                                    [(float("inf"), 0), (1, 1)], [(1, 2, 3), (0, 0)]])
def test_invalid_inputs_rejected(points):
    with pytest.raises(ValueError):
        closest_pair(points)

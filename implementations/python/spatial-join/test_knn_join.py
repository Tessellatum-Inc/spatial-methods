import math
import random

import pytest

from knn_join import knn_join


def brute(left, right, k):
    return [
        (i, j, (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
        for i, a in enumerate(left)
        for j, b in sorted(
            enumerate(right),
            key=lambda item: ((a[0] - item[1][0]) ** 2
                              + (a[1] - item[1][1]) ** 2, item[0])
        )[:k]
    ]


def test_known_join_and_stable_ties():
    left = [(0, 0), (10, 0)]
    right = [(1, 0), (-1, 0), (9, 0), (11, 0)]
    assert knn_join(left, right, 2) == [
        (0, 0, 1.0), (0, 1, 1.0), (1, 2, 1.0), (1, 3, 1.0)
    ]


def test_seeded_differential_against_independent_brute_force():
    rng = random.Random(20261115)
    for nl, nr in ((1, 1), (4, 8), (25, 60), (100, 40)):
        left = [(rng.uniform(-20, 20), rng.uniform(-20, 20)) for _ in range(nl)]
        right = [(rng.uniform(-20, 20), rng.uniform(-20, 20)) for _ in range(nr)]
        right[0] = right[-1] if nr > 1 else right[0]
        for k in (1, 3, nr, nr + 5):
            got = knn_join(left, right, k)
            expected = brute(left, right, min(k, nr))
            assert [(i, j) for i, j, _ in got] == [(i, j) for i, j, _ in expected]
            assert [d for _, _, d in got] == pytest.approx(
                [d for _, _, d in expected]
            )


def test_empty_relations_and_oversized_k():
    assert knn_join([], [(0, 0)], 1) == []
    assert knn_join([(0, 0)], [], 1) == []
    assert knn_join([(0, 0)], [(1, 0), (2, 0)], 9) == [
        (0, 0, 1.0), (0, 1, 4.0)
    ]


def test_duplicate_coordinates_remain_distinct_records():
    assert knn_join([(0, 0)], [(0, 0), (0, 0), (1, 0)], 2) == [
        (0, 0, 0.0), (0, 1, 0.0)
    ]


def test_validation():
    with pytest.raises(ValueError):
        knn_join([(0, 0)], [(1, 1)], 0)
    with pytest.raises(ValueError):
        knn_join([(math.nan, 0)], [(1, 1)], 1)
    with pytest.raises(ValueError):
        knn_join([(0, 0)], [(1,)], 1)

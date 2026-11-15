import random
import math

import pytest

from vp_tree import VantagePointTree


def _oracle(points, query, k):
    ranked = sorted(
        ((math.dist(point, query), index, point)
         for index, point in enumerate(points)),
        key=lambda item: (item[0], item[1]),
    )
    return [(point, distance) for distance, _, point in ranked[:k]]


def test_known_nearest_and_k_nearest_results():
    points = [(0, 0), (4, 0), (0, 3), (2, 2)]
    tree = VantagePointTree(points)
    assert tree.query((1, 1), 2) == _oracle(points, (1, 1), 2)
    assert tree.query((1, 1), 20) == _oracle(points, (1, 1), 20)


def test_duplicates_are_preserved_and_ties_follow_input_order():
    points = [(1, 0), (-1, 0), (1, 0), (0, 1)]
    tree = VantagePointTree(points)
    assert tree.query((0, 0), 4) == [
        ((1.0, 0.0), 1.0),
        ((-1.0, 0.0), 1.0),
        ((1.0, 0.0), 1.0),
        ((0.0, 1.0), 1.0),
    ]


def test_seeded_random_queries_match_brute_force():
    rng = random.Random(20261115)
    for _ in range(80):
        points = [(rng.randrange(-30, 31), rng.randrange(-30, 31))
                  for _ in range(rng.randrange(0, 90))]
        tree = VantagePointTree(points)
        for _ in range(8):
            query = (rng.randrange(-35, 36), rng.randrange(-35, 36))
            k = rng.randrange(1, 15)
            assert tree.query(query, k) == _oracle(points, query, k)


def test_empty_tree_and_singleton():
    assert VantagePointTree([]).query((0, 0)) == []
    assert VantagePointTree([(2, 3)]).query((2, 3), 5) == [
        ((2.0, 3.0), 0.0)
    ]


@pytest.mark.parametrize("k", [0, -1, 1.5, True])
def test_invalid_k_is_rejected(k):
    with pytest.raises(ValueError, match="positive integer"):
        VantagePointTree([(0, 0)]).query((0, 0), k)


def test_non_finite_and_wrong_dimension_points_are_rejected():
    with pytest.raises(ValueError, match="finite"):
        VantagePointTree([(0, 0), (float("nan"), 1)])
    with pytest.raises(ValueError, match="2D"):
        VantagePointTree([(0, 0, 1)])
    with pytest.raises(ValueError, match="finite"):
        VantagePointTree([(0, 0)]).query((float("inf"), 0))

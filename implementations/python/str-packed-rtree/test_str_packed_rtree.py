import random

import pytest

from str_packed_rtree import STRPackedRTree, _intersects


def test_empty_tree_returns_no_matches():
    tree = STRPackedRTree([])
    assert len(tree) == 0
    assert tree.query((0, 0, 1, 1)) == []


def test_single_box_is_returned_when_intersecting():
    tree = STRPackedRTree([(0, 0, 2, 2)])
    assert tree.query((1, 1, 3, 3)) == [0]


def test_non_intersecting_query_returns_empty():
    tree = STRPackedRTree([(0, 0, 1, 1), (3, 3, 4, 4)])
    assert tree.query((1.1, 1.1, 2, 2)) == []


def test_boundary_touch_counts_as_intersection():
    tree = STRPackedRTree([(0, 0, 1, 1)])
    assert tree.query((1, 0.25, 2, 0.75)) == [0]


def test_query_returns_original_input_indices_in_sorted_order():
    bounds = [(5, 5, 6, 6), (0, 0, 2, 2), (1, 1, 3, 3)]
    tree = STRPackedRTree(bounds, node_capacity=2)
    assert tree.query((0.5, 0.5, 2.5, 2.5)) == [1, 2]


def test_overlapping_boxes_all_returned():
    bounds = [(0, 0, 2, 2), (1, 1, 3, 3), (2, 2, 4, 4)]
    tree = STRPackedRTree(bounds, node_capacity=2)
    assert tree.query((1.5, 1.5, 2.5, 2.5)) == [0, 1, 2]


def test_results_match_brute_force_for_random_boxes():
    rng = random.Random(20261113)
    bounds = []
    for _ in range(300):
        x, y = rng.uniform(-100, 100), rng.uniform(-100, 100)
        width, height = rng.uniform(0, 15), rng.uniform(0, 15)
        bounds.append((x, y, x + width, y + height))

    queries = []
    for _ in range(60):
        x, y = rng.uniform(-100, 100), rng.uniform(-100, 100)
        width, height = rng.uniform(0, 25), rng.uniform(0, 25)
        queries.append((x, y, x + width, y + height))

    for capacity in (2, 3, 4, 8, 10):
        tree = STRPackedRTree(bounds, node_capacity=capacity)
        for query in queries:
            expected = [i for i, item in enumerate(bounds) if _intersects(item, query)]
            assert tree.query(query) == expected


def test_invalid_node_capacity_is_rejected():
    with pytest.raises(ValueError, match="at least 2"):
        STRPackedRTree([(0, 0, 1, 1)], node_capacity=1)


@pytest.mark.parametrize(
    "bounds",
    [
        (0, 0, 1),
        (0, 2, 1, 1),
        (0, 0, float("inf"), 1),
        (0, 0, float("nan"), 1),
    ],
)
def test_invalid_stored_bounds_are_rejected(bounds):
    with pytest.raises(ValueError):
        STRPackedRTree([bounds])


def test_invalid_query_bounds_are_rejected():
    tree = STRPackedRTree([(0, 0, 1, 1)])
    with pytest.raises(ValueError):
        tree.query((2, 2, 1, 1))


def test_tree_keeps_all_input_items():
    bounds = [(i, i, i + 0.5, i + 0.5) for i in range(25)]
    tree = STRPackedRTree(bounds, node_capacity=3)
    assert len(tree) == len(bounds)
    assert tree.query((-1, -1, 30, 30)) == list(range(25))


def _point_box_distance(point, bounds):
    x, y = point
    dx = max(bounds[0] - x, 0.0, x - bounds[2])
    dy = max(bounds[1] - y, 0.0, y - bounds[3])
    return (dx * dx + dy * dy) ** 0.5


def test_nearest_box_query_orders_by_distance_then_original_index():
    bounds = [(2, 0, 3, 1), (-3, 0, -2, 1), (0, 0, 1, 1), (5, 5, 6, 6)]
    tree = STRPackedRTree(bounds, node_capacity=2)
    actual = tree.nearest((1.5, 0.5), 4)
    assert [index for index, _distance in actual] == [0, 2, 1, 3]
    assert [distance for _index, distance in actual] == pytest.approx(
        [0.5, 0.5, 3.5, (3.5**2 + 4.5**2) ** 0.5]
    )


def test_nearest_box_query_matches_brute_force_on_seeded_boxes():
    rng = random.Random(20261115)
    bounds = []
    for _ in range(240):
        x, y = rng.uniform(-50, 50), rng.uniform(-50, 50)
        width, height = rng.uniform(0, 8), rng.uniform(0, 8)
        bounds.append((x, y, x + width, y + height))
    tree = STRPackedRTree(bounds, node_capacity=4)
    for _ in range(100):
        point = (rng.uniform(-60, 60), rng.uniform(-60, 60))
        k = rng.randint(0, 20)
        expected = sorted(
            ((_point_box_distance(point, box), i) for i, box in enumerate(bounds)),
            key=lambda pair: (pair[0], pair[1])
        )[:k]
        actual = tree.nearest(point, k)
        assert [index for index, _distance in actual] == [i for _d, i in expected]
        assert [distance for _i, distance in actual] == pytest.approx(
            [distance for distance, _i in expected]
        )


@pytest.mark.parametrize("k", [-1, True, 1.5, "2"])
def test_nearest_box_query_rejects_invalid_k(k):
    with pytest.raises(ValueError, match="k must"):
        STRPackedRTree([(0, 0, 1, 1)]).nearest((0, 0), k)


@pytest.mark.parametrize("point", [(0,), (0, 1, 2), (float("nan"), 0), (0, float("inf"))])
def test_nearest_box_query_rejects_invalid_points(point):
    with pytest.raises(ValueError, match="two finite"):
        STRPackedRTree([(0, 0, 1, 1)]).nearest(point)


def test_nearest_box_query_avoids_squared_distance_overflow():
    tree = STRPackedRTree([(1e200, 0, 1e200, 0), (2e200, 0, 2e200, 0)])
    assert tree.nearest((0, 0), 2) == [(0, 1e200), (1, 2e200)]

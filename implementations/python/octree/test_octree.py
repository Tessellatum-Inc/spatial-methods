import math
import random

import pytest

from octree import PointRegionOctree


def brute_range(points, box):
    return [i for i, p in enumerate(points)
            if all(box[a] <= p[a] <= box[a + 3] for a in range(3))]


def brute_knn(points, q, k):
    return sorted(((i, p, math.dist(q, p)) for i, p in enumerate(points)),
                  key=lambda item: (item[2], item[0]))[:k]


def test_empty_and_full_extent():
    tree = PointRegionOctree((0, 0, 0, 10, 10, 10))
    assert tree.query(tree.extent) == []
    assert tree.k_nearest((0, 0, 0), 3) == []


def test_midplanes_and_closed_outer_faces():
    pts = [(5, 5, 5), (5, 2, 8), (2, 5, 2), (0, 0, 0), (10, 10, 10)]
    tree = PointRegionOctree((0, 0, 0, 10, 10, 10), pts, capacity=1)
    assert tree.query((5, 5, 5, 5, 5, 5)) == [0]
    assert tree.query((0, 0, 0, 10, 10, 10)) == list(range(5))
    assert tree.query((10, 10, 10, 10, 10, 10)) == [4]


def test_duplicates_and_depth_limit():
    pts = [(4, 4, 4)] * 30
    tree = PointRegionOctree((0, 0, 0, 8, 8, 8), pts, capacity=2, max_depth=4)
    assert tree.query((4, 4, 4, 4, 4, 4)) == list(range(30))
    assert len(tree.k_nearest((4, 4, 4), 5)) == 5


def test_nearest_ties_are_stable_by_insertion_id():
    pts = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, 0, 1)]
    tree = PointRegionOctree((-2, -2, -2, 2, 2, 2), pts, capacity=1)
    assert [x[0] for x in tree.k_nearest((0, 0, 0), 3)] == [0, 1, 2]


def test_seeded_range_and_knn_differential():
    rng = random.Random(20261115)
    for n in (1, 2, 20, 100, 500):
        pts = [tuple(rng.uniform(-10, 10) for _ in range(3)) for _ in range(n)]
        if n > 4:
            pts[2] = pts[1]
        tree = PointRegionOctree((-10, -10, -10, 10, 10, 10), pts,
                                 capacity=5, max_depth=12)
        for _ in range(30):
            lo = [rng.uniform(-12, 8) for _ in range(3)]
            hi = [rng.uniform(x, 12) for x in lo]
            box = tuple(lo + hi)
            assert tree.query(box) == brute_range(pts, box)
            q = tuple(rng.uniform(-12, 12) for _ in range(3))
            k = rng.randint(1, min(n + 2, 15))
            got = tree.k_nearest(q, k)
            expected = brute_knn(pts, q, k)
            assert [x[0] for x in got] == [x[0] for x in expected]
            assert [x[2] for x in got] == pytest.approx([x[2] for x in expected])


def test_insert_returns_stable_ids_and_rejects_outside():
    tree = PointRegionOctree((0, 0, 0, 1, 1, 1))
    with pytest.raises(ValueError):
        tree.insert((2, 0, 0))
    assert tree.insert((1, 1, 1)) == 0
    assert tree.insert((0, 0, 0)) == 1


def test_validation():
    with pytest.raises(ValueError):
        PointRegionOctree((0, 0, 0, 0, 1, 1))
    with pytest.raises(ValueError):
        PointRegionOctree((0, 0, 0, 1, 1, 1), [(math.nan, 0, 0)])
    with pytest.raises(ValueError):
        PointRegionOctree((0, 0, 0, 1, 1, 1)).query((0, 0, 0, 2, 1))
    with pytest.raises(ValueError):
        PointRegionOctree((0, 0, 0, 1, 1, 1)).k_nearest((0, 0, 0), 0)

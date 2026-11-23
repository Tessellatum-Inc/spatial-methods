import math
import random

import pytest

from kd_tree import KDTree2D


def brute_force(points, query):
    if not points:
        return None
    ranked = []
    for index, (x, y) in enumerate(points):
        distance_sq = (x - query[0]) ** 2 + (y - query[1]) ** 2
        ranked.append((distance_sq, index))
    distance_sq, index = min(ranked)
    return index, distance_sq


def test_empty_tree_returns_none():
    assert KDTree2D([]).nearest((0, 0)) is None


def test_single_point():
    tree = KDTree2D([(3, 4)])
    assert tree.nearest((0, 0)) == (0, 25.0)


def test_query_outside_data_extent():
    points = [(0, 0), (2, 0), (4, 0)]
    assert KDTree2D(points).nearest((100, 0)) == (2, 96**2)


def test_duplicate_points_use_lowest_original_index():
    tree = KDTree2D([(1, 1), (1, 1), (2, 2)])
    assert tree.nearest((1, 1)) == (0, 0.0)


def test_equidistant_points_use_lowest_original_index():
    tree = KDTree2D([(-1, 0), (1, 0), (0, 3)])
    assert tree.nearest((0, 0)) == (0, 1.0)


def test_split_plane_query_is_exact():
    points = [(0, 0), (2, 0), (1, 1), (1, -1)]
    assert KDTree2D(points).nearest((1, 0)) == (0, 1.0)


def test_rejects_wrong_dimension_and_non_finite_values():
    with pytest.raises(ValueError):
        KDTree2D([(1, 2, 3)])
    with pytest.raises(ValueError):
        KDTree2D([(math.inf, 0)])
    with pytest.raises(ValueError):
        KDTree2D([(0, 0)]).nearest((math.nan, 1))


def test_y_axis_split_uses_y_coordinate_for_pruning():
    points = [
        (-64.2034790150465, 83.46101476269169),
        (-64.2034790150465, 83.46101476269169),
        (-23.19463722930992, -69.03222635386197),
        (18.375976820856565, -9.659101004365183),
        (-97.7931466556235, -17.80389263764465),
        (34.506527685848596, 15.922510272302134),
        (2.4928967886371822, -75.88304077765495),
        (54.627354072510315, -25.259438606592852),
        (-37.53857614489722, 43.73110917885859),
        (-57.113217598128486, 64.28165806339828),
    ]
    query = (117.12119180738159, -14.495919709034766)
    assert KDTree2D(points).nearest(query) == brute_force(points, query)


def test_random_queries_match_brute_force():
    rng = random.Random(20261113)
    for size in (1, 2, 3, 10, 50, 200):
        points = [
            (rng.uniform(-100, 100), rng.uniform(-100, 100))
            for _ in range(size)
        ]
        # Include repeated coordinates to exercise deterministic tie handling.
        if size >= 3:
            points[1] = points[0]
        tree = KDTree2D(points)
        for _ in range(100):
            query = (rng.uniform(-120, 120), rng.uniform(-120, 120))
            assert tree.nearest(query) == brute_force(points, query)


def test_clustered_and_anisotropic_data_match_brute_force():
    points = [(i / 1000, i * 0.001) for i in range(-500, 501)]
    tree = KDTree2D(points)
    for query in [(-2, 0), (0, 0), (0.2, 0.2), (5, 4)]:
        assert tree.nearest(query) == brute_force(points, query)


def test_range_query_inclusive_bounds_and_original_indices():
    points = [(0, 0), (1, 1), (2, 2), (1, 2), (1, 0), (1, 1)]
    tree = KDTree2D(points)
    assert tree.range_query((1, 1), (1, 2)) == [1, 3, 5]


def test_range_query_empty_rectangle_and_empty_tree():
    assert KDTree2D([]).range_query((0, 0), (1, 1)) == []
    assert KDTree2D([(5, 5)]).range_query((0, 0), (1, 1)) == []


def test_range_query_degenerate_point_and_line_windows():
    points = [(-1, 0), (0, 0), (1, 0), (0, 1), (0, -1)]
    tree = KDTree2D(points)
    assert tree.range_query((0, 0), (0, 0)) == [1]
    assert tree.range_query((-1, 0), (1, 0)) == [0, 1, 2]


def test_range_query_matches_independent_brute_force_on_seeded_clouds():
    rng = random.Random(20261115)
    for size in (0, 1, 2, 10, 50, 200):
        points = [(rng.randint(-20, 20), rng.randint(-20, 20))
                  for _ in range(size)]
        tree = KDTree2D(points)
        for _ in range(80):
            x1, x2 = sorted((rng.randint(-25, 25), rng.randint(-25, 25)))
            y1, y2 = sorted((rng.randint(-25, 25), rng.randint(-25, 25)))
            expected = [i for i, (x, y) in enumerate(points)
                        if x1 <= x <= x2 and y1 <= y <= y2]
            assert tree.range_query((x1, y1), (x2, y2)) == expected


@pytest.mark.parametrize("minimum,maximum", [
    ((2, 0), (1, 1)), ((0, 2), (1, 1)),
    ((float("nan"), 0), (1, 1)), ((0, 0), (float("inf"), 1)),
    ((0, 0, 0), (1, 1, 1)),
])
def test_range_query_rejects_invalid_bounds(minimum, maximum):
    with pytest.raises(ValueError):
        KDTree2D([(0, 0)]).range_query(minimum, maximum)


def test_k_nearest_orders_by_distance_then_original_index():
    points = [(-1, 0), (1, 0), (0, 2), (0, 0), (0, 0)]
    tree = KDTree2D(points)
    assert tree.k_nearest((0, 0), 4) == [
        (3, 0.0), (4, 0.0), (0, 1.0), (1, 1.0)
    ]


def test_k_nearest_handles_zero_empty_and_k_larger_than_tree():
    assert KDTree2D([(0, 0)]).k_nearest((0, 0), 0) == []
    assert KDTree2D([]).k_nearest((0, 0), 3) == []
    assert KDTree2D([(0, 0), (2, 0)]).k_nearest((0, 0), 9) == [
        (0, 0.0), (1, 4.0)
    ]


def test_k_nearest_matches_brute_force_on_seeded_clouds():
    rng = random.Random(20261116)
    for size in (1, 2, 3, 10, 50, 150):
        points = [(rng.randint(-30, 30), rng.randint(-30, 30))
                  for _ in range(size)]
        tree = KDTree2D(points)
        for _ in range(35):
            query = (rng.uniform(-35, 35), rng.uniform(-35, 35))
            k = rng.randint(0, size + 4)
            expected = sorted(
                (((x - query[0]) ** 2 + (y - query[1]) ** 2, i)
                 for i, (x, y) in enumerate(points))
            )[:k]
            actual = tree.k_nearest(query, k)
            # The query and oracle evaluate equivalent squared-distance
            # expressions with different floating-point operation order.
            # Compare selected indices exactly and distances with a tight
            # tolerance rather than requiring bit-identical round-off.
            assert [index for index, _ in actual] == [i for _d2, i in expected]
            assert [distance for _index, distance in actual] == pytest.approx(
                [d2 for d2, _i in expected], rel=1e-14, abs=1e-14
            )


@pytest.mark.parametrize("k", [-1, 1.5, True, "2"])
def test_k_nearest_rejects_invalid_k(k):
    with pytest.raises(ValueError):
        KDTree2D([(0, 0)]).k_nearest((0, 0), k)


def test_radius_query_includes_boundary_and_sorts_original_indices():
    points = [(3, 4), (0, 0), (1, 0), (-1, 0), (0, 2), (0, 0)]
    tree = KDTree2D(points)
    assert tree.radius_query((0, 0), 1.0) == [1, 2, 3, 5]
    assert tree.radius_query((0, 0), 0.0) == [1, 5]
    assert tree.radius_query((0, 0), 2.0) == [1, 2, 3, 4, 5]


def test_radius_query_empty_tree_and_no_matches():
    assert KDTree2D([]).radius_query((0, 0), 10) == []
    assert KDTree2D([(5, 5)]).radius_query((0, 0), 1) == []


def test_radius_query_matches_independent_brute_force_on_seeded_clouds():
    rng = random.Random(20261118)
    for size in (0, 1, 2, 10, 50, 200):
        points = [(rng.randint(-30, 30), rng.randint(-30, 30))
                  for _ in range(size)]
        tree = KDTree2D(points)
        for _ in range(80):
            query = (rng.uniform(-35, 35), rng.uniform(-35, 35))
            radius = rng.uniform(0, 25)
            expected = [
                i for i, point in enumerate(points)
                if (point[0] - query[0]) ** 2 + (point[1] - query[1]) ** 2
                <= radius ** 2
            ]
            assert tree.radius_query(query, radius) == expected


@pytest.mark.parametrize("radius", [-1, float("nan"), float("inf"), True, "bad"])
def test_radius_query_rejects_invalid_radius(radius):
    with pytest.raises(ValueError):
        KDTree2D([(0, 0)]).radius_query((0, 0), radius)



def test_dynamic_kd_tree_insert_delete_and_queries_match_brute_force():
    from kd_tree import DynamicKDTree2D
    rng=random.Random(20261117)
    tree=DynamicKDTree2D(alpha=0.65)
    active={}
    for step in range(180):
        if not active or rng.random()<0.68:
            point=(rng.randint(-20,20),rng.randint(-20,20))
            index=tree.insert(point)
            active[index]=point
        else:
            index=rng.choice(list(active))
            assert tree.delete(index)
            del active[index]
        assert len(tree)==len(active)
        points=list(active.items())
        query=(rng.uniform(-25,25),rng.uniform(-25,25))
        expected=min(((x-query[0])**2+(y-query[1])**2,i)
                     for i,(x,y) in points) if points else None
        got=tree.nearest(query)
        assert got is None if expected is None else got[0]==expected[1] and got[1]==pytest.approx(expected[0])
        k=min(5,len(points))
        expected_k=sorted((((x-query[0])**2+(y-query[1])**2,i) for i,(x,y) in points))[:k]
        got_k=tree.k_nearest(query,k)
        assert [i for i,_ in got_k]==[i for _,i in expected_k]
        low=(-10,-10); high=(10,10)
        expected_range=sorted(i for i,(x,y) in points if -10<=x<=10 and -10<=y<=10)
        assert tree.range_query(low,high)==expected_range
        radius=7.5
        expected_radius=sorted(i for i,(x,y) in points if (x-query[0])**2+(y-query[1])**2<=radius**2)
        assert tree.radius_query(query,radius)==expected_radius


def test_dynamic_kd_tree_duplicate_points_use_stable_id_ties_and_deletion():
    from kd_tree import DynamicKDTree2D
    tree=DynamicKDTree2D([(1,1),(1,1),(2,2)])
    assert tree.nearest((1,1))==(0,0.0)
    assert tree.delete(0)
    assert tree.nearest((1,1))==(1,0.0)
    assert tree.delete(1)
    assert tree.nearest((1,1))==(2,2.0)
    assert not tree.delete(1)
    assert len(tree)==1


def test_dynamic_kd_tree_rejects_invalid_alpha_and_ids():
    from kd_tree import DynamicKDTree2D
    for alpha in (0.5,1.0,float("nan"),True):
        with pytest.raises(ValueError):
            DynamicKDTree2D(alpha=alpha)
    tree=DynamicKDTree2D([(0,0)])
    with pytest.raises(ValueError):
        tree.delete(True)
    with pytest.raises(ValueError):
        tree.insert((0,float("inf")))

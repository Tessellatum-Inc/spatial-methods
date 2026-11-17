import pytest
from ray_triangle_intersection import intersect_ray_triangle

TRIANGLE = ((0, 0, 0), (1, 0, 0), (0, 1, 0))

def test_interior_hit_returns_parameter_barycentric_weights_and_point():
    hit = intersect_ray_triangle((0.25, 0.25, 1), (0, 0, -1), TRIANGLE)
    assert hit is not None
    assert (hit.t, hit.u, hit.v, hit.w) == pytest.approx((1, .25, .25, .5))
    assert hit.point == pytest.approx((.25, .25, 0))

def test_edge_and_vertex_hits_are_included():
    assert intersect_ray_triangle((0, 0, 1), (0, 0, -1), TRIANGLE) is not None
    assert intersect_ray_triangle((.5, .5, 1), (0, 0, -1), TRIANGLE) is not None

def test_parallel_outside_and_behind_ray_miss():
    assert intersect_ray_triangle((.2, .2, 1), (1, 0, 0), TRIANGLE) is None
    assert intersect_ray_triangle((2, 2, 1), (0, 0, -1), TRIANGLE) is None
    assert intersect_ray_triangle((.2, .2, -1), (0, 0, -1), TRIANGLE) is None

def test_degenerate_triangle_misses():
    degenerate = ((0, 0, 0), (1, 1, 1), (2, 2, 2))
    assert intersect_ray_triangle((0, 0, 1), (0, 0, -1), degenerate) is None

def test_backface_culling_is_opt_in():
    assert intersect_ray_triangle((.2, .2, 1), (0, 0, -1), TRIANGLE, cull_backface=True)
    assert intersect_ray_triangle((.2, .2, -1), (0, 0, 1), TRIANGLE, cull_backface=True) is None
    assert intersect_ray_triangle((.2, .2, -1), (0, 0, 1), TRIANGLE) is not None

def test_non_unit_direction_returns_parameter_not_distance():
    hit = intersect_ray_triangle((.2, .2, 4), (0, 0, -2), TRIANGLE)
    assert hit is not None and hit.t == pytest.approx(2)

def test_ray_interval_is_respected():
    assert intersect_ray_triangle((.2, .2, 1), (0, 0, -1), TRIANGLE, t_max=.5) is None
    assert intersect_ray_triangle((.2, .2, 1), (0, 0, -1), TRIANGLE, t_min=1.1) is None

def test_invalid_shapes_and_nonfinite_values_raise():
    with pytest.raises(ValueError):
        intersect_ray_triangle((0, 0), (0, 0, 1), TRIANGLE)
    with pytest.raises(ValueError):
        intersect_ray_triangle((float("nan"), 0, 0), (0, 0, 1), TRIANGLE)

def test_invalid_tolerance_and_interval_raise():
    with pytest.raises(ValueError):
        intersect_ray_triangle((0, 0, 1), (0, 0, -1), TRIANGLE, t_min=-1)
    with pytest.raises(ValueError):
        intersect_ray_triangle((0, 0, 1), (0, 0, -1), TRIANGLE, t_min=2, t_max=1)


def test_aabb_slab_intersection_handles_parallel_axes():
    from ray_triangle_intersection import AABB
    box = AABB((0, 0, 0), (1, 1, 1))
    assert box.intersect_ray((.5, .5, 2), (0, 0, -1)) == pytest.approx((1, 2))
    assert box.intersect_ray((2, .5, 2), (0, 0, -1)) is None


def test_empty_bvh_and_invalid_leaf_size():
    from ray_triangle_intersection import build_bvh, intersect_bvh
    assert build_bvh([]) is None
    with pytest.raises(ValueError):
        build_bvh([TRIANGLE], leaf_size=0)
    assert intersect_bvh(None, [], (0, 0, 0), (1, 0, 0)) is None


def test_bvh_returns_nearest_hit_and_original_triangle_index():
    from ray_triangle_intersection import build_bvh, intersect_bvh
    triangles = [
        ((-1, -1, 0), (1, -1, 0), (0, 1, 0)),
        ((-1, -1, 2), (1, -1, 2), (0, 1, 2)),
    ]
    tree = build_bvh(triangles, leaf_size=1)
    result = intersect_bvh(tree, triangles, (0, 0, 5), (0, 0, -1))
    assert result is not None
    index, hit = result
    assert index == 1
    assert hit.t == pytest.approx(3)
    assert hit.point == pytest.approx((0, 0, 2))


def test_bvh_matches_brute_force_for_seeded_vertical_rays():
    import random
    from ray_triangle_intersection import build_bvh, intersect_bvh
    rng = random.Random(20261118)
    triangles = []
    for _ in range(80):
        x, y, z = rng.uniform(-8, 8), rng.uniform(-8, 8), rng.uniform(-4, 4)
        width, height = rng.uniform(.2, 1.5), rng.uniform(.2, 1.5)
        triangles.append(((x, y, z), (x+width, y, z), (x, y+height, z)))
    tree = build_bvh(triangles, leaf_size=3)
    for _ in range(100):
        origin = (rng.uniform(-9, 9), rng.uniform(-9, 9), 8.0)
        direction = (0.0, 0.0, -1.0)
        candidates = [
            (hit.t, index)
            for index, triangle in enumerate(triangles)
            if (hit := intersect_ray_triangle(origin, direction, triangle)) is not None
        ]
        expected = min(candidates, default=None)
        actual = intersect_bvh(tree, triangles, origin, direction)
        if expected is None:
            assert actual is None
        else:
            assert actual is not None
            index, hit = actual
            assert hit.t == pytest.approx(expected[0])
            assert index == expected[1]


def test_frustum_aabb_culling_inside_outside_and_intersecting_boxes():
    from ray_triangle_intersection import AABB, aabb_intersects_frustum
    planes = (
        (1, 0, 0, 1), (-1, 0, 0, 1),
        (0, 1, 0, 1), (0, -1, 0, 1),
        (0, 0, 1, 1), (0, 0, -1, 1),
    )
    assert aabb_intersects_frustum(AABB((-.5, -.5, -.5), (.5, .5, .5)), planes)
    assert not aabb_intersects_frustum(AABB((2, 0, 0), (3, .5, .5)), planes)
    assert aabb_intersects_frustum(AABB((.9, -.2, -.2), (1.2, .2, .2)), planes)


def test_frustum_boundary_and_tolerance_are_conservative():
    from ray_triangle_intersection import AABB, aabb_intersects_frustum
    planes = ((-1, 0, 0, 1),)
    boundary = AABB((1, 0, 0), (2, 1, 1))
    assert aabb_intersects_frustum(boundary, planes)
    assert aabb_intersects_frustum(AABB((1.0001, 0, 0), (2, 1, 1)), planes, epsilon=.001)
    assert not aabb_intersects_frustum(AABB((1.1, 0, 0), (2, 1, 1)), planes, epsilon=.001)


def test_invalid_frustum_planes_raise():
    from ray_triangle_intersection import AABB, aabb_intersects_frustum
    box = AABB((0, 0, 0), (1, 1, 1))
    with pytest.raises(ValueError):
        aabb_intersects_frustum(box, [])
    with pytest.raises(ValueError):
        aabb_intersects_frustum(box, ((1, 0, 0),))
    with pytest.raises(ValueError):
        aabb_intersects_frustum(box, ((float("nan"), 0, 0, 1),))

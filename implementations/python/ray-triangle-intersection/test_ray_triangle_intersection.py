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

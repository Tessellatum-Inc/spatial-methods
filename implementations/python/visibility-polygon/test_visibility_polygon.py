import math

import pytest

from visibility_polygon import visibility_polygon


def _area(ring):
    return abs(sum(
        ring[i][0] * ring[(i + 1) % len(ring)][1]
        - ring[(i + 1) % len(ring)][0] * ring[i][1]
        for i in range(len(ring))
    )) / 2


def _contains(point, ring):
    x, y = point
    inside = False
    for a, b in zip(ring, ring[1:] + ring[:1]):
        if (a[1] > y) != (b[1] > y):
            cross_x = a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            if x < cross_x:
                inside = not inside
    return inside


def test_viewpoint_inside_rectangle_sees_entire_convex_polygon():
    polygon = [(0, 0), (4, 0), (4, 2), (0, 2)]
    visible = visibility_polygon((2, 1), polygon)
    assert len(visible) >= 4
    assert _area(visible) == pytest.approx(8.0, abs=1e-7)
    assert all(math.isfinite(c) for point in visible for c in point)


def test_concave_notch_occludes_region_behind_reflex_corner():
    polygon = [(0, 0), (4, 0), (4, 1), (2, 1), (2, 4), (0, 4)]
    # From the right-hand arm, the reflex corner at (2, 1) occludes
    # much of the upper-left arm. The former viewpoint (1, 1) lies in
    # the shared corner of both arms, from which the entire polygon is visible.
    visible = visibility_polygon((3, 0.5), polygon)
    assert _contains((3, 0.8), visible)
    assert not _contains((1, 3), visible)
    assert _area(visible) < 10.0


def test_polygon_closure_and_vertex_order_do_not_change_visibility_area():
    polygon = [(0, 0), (5, 0), (5, 3), (0, 3)]
    a = visibility_polygon((2, 1), polygon)
    b = visibility_polygon((2, 1), polygon[2:] + polygon[:2] + [polygon[2]])
    assert _area(a) == pytest.approx(_area(b), abs=1e-8)


@pytest.mark.parametrize("viewpoint,polygon", [
    ((5, 5), [(0, 0), (2, 0), (2, 2), (0, 2)]),
    ((0, 1), [(0, 0), (2, 0), (2, 2), (0, 2)]),
])
def test_viewpoint_must_be_strictly_inside(viewpoint, polygon):
    with pytest.raises(ValueError, match="inside"):
        visibility_polygon(viewpoint, polygon)


def test_invalid_polygon_and_angular_tolerance_are_rejected():
    with pytest.raises(ValueError, match="three"):
        visibility_polygon((0, 0), [(0, 0), (1, 0)])
    with pytest.raises(ValueError, match="angular_epsilon"):
        visibility_polygon((1, 1), [(0, 0), (2, 0), (2, 2), (0, 2)],
                           angular_epsilon=0)
    with pytest.raises(ValueError, match="finite"):
        visibility_polygon((1, 1), [(0, 0), (2, 0), (2, float("inf")), (0, 2)])

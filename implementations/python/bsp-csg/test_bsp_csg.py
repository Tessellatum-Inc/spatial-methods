import math
import pytest

from bsp_csg import Polygon, box, difference, intersection, union


def signed_volume(polygons):
    volume = 0.0
    for polygon in polygons:
        vertices = [v.pos for v in polygon.vertices]
        for i in range(1, len(vertices) - 1):
            a, b, c = vertices[0], vertices[i], vertices[i + 1]
            cross = (b[1] * c[2] - b[2] * c[1],
                     b[2] * c[0] - b[0] * c[2],
                     b[0] * c[1] - b[1] * c[0])
            volume += (a[0] * cross[0] + a[1] * cross[1] +
                       a[2] * cross[2]) / 6.0
    return volume


def volume(polygons):
    return abs(signed_volume(polygons))


def test_overlapping_axis_aligned_boxes_boolean_volumes():
    a = box((0, 0, 0), (2, 2, 2))
    b = box((1, 1, 1), (3, 3, 3))
    assert volume(intersection(a, b)) == pytest.approx(1.0, abs=1e-7)
    assert volume(union(a, b)) == pytest.approx(15.0, abs=1e-7)
    assert volume(difference(a, b)) == pytest.approx(7.0, abs=1e-7)


def test_disjoint_boxes_have_empty_intersection_and_additive_union():
    a = box((0, 0, 0), (1, 1, 1))
    b = box((2, 0, 0), (3, 1, 1))
    assert intersection(a, b) == []
    assert volume(union(a, b)) == pytest.approx(2.0, abs=1e-7)
    assert volume(difference(a, b)) == pytest.approx(1.0, abs=1e-7)


def test_contained_box_boolean_volumes():
    outer = box((0, 0, 0), (3, 3, 3))
    inner = box((1, 1, 1), (2, 2, 2))
    assert volume(intersection(outer, inner)) == pytest.approx(1.0, abs=1e-7)
    assert volume(union(outer, inner)) == pytest.approx(27.0, abs=1e-7)
    assert volume(difference(outer, inner)) == pytest.approx(26.0, abs=1e-7)


def test_box_requires_strict_bounds():
    with pytest.raises(ValueError, match="maximum coordinates"):
        box((0, 0, 0), (1, 1, 0))


def test_polygon_rejects_nonconvex_input():
    with pytest.raises(ValueError, match="must be convex"):
        Polygon.from_points([(0, 0, 0), (2, 0, 0), (1, 0.5, 0),
                             (2, 2, 0), (0, 2, 0)])


def test_polygon_rejects_nonplanar_input():
    with pytest.raises(ValueError, match="not coplanar"):
        Polygon.from_points([(0, 0, 0), (1, 0, 0),
                             (1, 1, 0.1), (0, 1, 0)])

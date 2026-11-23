import math
import numpy as np
import pytest

from spherical_polygon_area import spherical_polygon_area


def test_spherical_right_triangle_has_known_spherical_excess():
    radius = 2.0
    area = spherical_polygon_area([(0, 0), (0, 90), (90, 0)], radius=radius)
    assert area == pytest.approx(math.pi * radius * radius / 2)


def test_equatorial_quarter_sphere_polygon_and_reversed_orientation_match():
    ring = [(0, 0), (0, 90), (90, 0)]
    reverse = list(reversed(ring))
    a = spherical_polygon_area(ring, radius=1)
    b = spherical_polygon_area(reverse, radius=1)
    assert a == pytest.approx(math.pi / 2)
    assert b == pytest.approx(a)


def test_antimeridian_rectangle_has_small_area():
    ring = [(-10, 170), (-10, -170), (10, -170), (10, 170)]
    area = spherical_polygon_area(ring, radius=1)
    assert 0 < area < 0.25


def test_closing_duplicate_vertex_is_accepted():
    ring = [(0, 0), (0, 1), (1, 0), (0, 0)]
    assert spherical_polygon_area(ring) > 0


def test_hole_area_is_subtracted():
    outer = [(0, 0), (0, 10), (10, 10), (10, 0)]
    hole = [(2, 2), (2, 4), (4, 4), (4, 2)]
    assert spherical_polygon_area(outer, holes=[hole]) < spherical_polygon_area(outer)


@pytest.mark.parametrize("ring", [
    [], [(0, 0), (1, 1)], [(0, 0), (0, 1), (0, 0)],
    [(91, 0), (0, 1), (1, 0)], [(0, 181), (1, 0), (2, 1)],
    [(0, 0), (0, 180), (10, 90)],
])
def test_invalid_or_ambiguous_rings_are_rejected(ring):
    with pytest.raises(ValueError):
        spherical_polygon_area(ring)


def test_invalid_radius_and_excessive_hole_are_rejected():
    ring = [(0, 0), (0, 10), (10, 0)]
    with pytest.raises(ValueError):
        spherical_polygon_area(ring, radius=0)
    with pytest.raises(ValueError):
        spherical_polygon_area(ring, holes=[[(0, 0), (0, 10), (10, 0)]])

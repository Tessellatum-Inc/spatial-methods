from collections import Counter
from fractions import Fraction
import math
import random

import pytest

from bowyer_watson import delaunay_triangulate, incircle, orient


def _edge(a, b):
    return (a, b) if a < b else (b, a)


def _edges(triangles):
    result = Counter()
    for triangle in triangles:
        for a, b in zip(triangle, triangle[1:] + triangle[:1]):
            result[_edge(a, b)] += 1
    return result


def _hull_size(points):
    points = sorted(set(points))

    def half(values):
        out = []
        for point in values:
            while len(out) >= 2 and orient(out[-2], out[-1], point) <= 0:
                out.pop()
            out.append(point)
        return out

    return len(half(points)[:-1] + half(points[::-1])[:-1])


def _assert_empty_circumcircles(points, triangles):
    for triangle in triangles:
        for point in points:
            if point in triangle:
                continue
            assert incircle(*triangle, point) <= 0


def test_triangle_and_square_have_expected_euler_face_counts():
    for raw in (
        [(0, 0), (4, 0), (0, 3)],
        [(0, 0), (4, 0), (4, 4), (0, 4)],
    ):
        points = [(Fraction(x), Fraction(y)) for x, y in raw]
        triangles = delaunay_triangulate(raw)
        assert len(triangles) == 2 * len(points) - 2 - _hull_size(points)
        assert all(orient(*triangle) > 0 for triangle in triangles)
        _assert_empty_circumcircles(points, triangles)


def test_cocircular_square_is_valid_and_deterministic():
    points = [(0, 0), (1, 0), (1, 1), (0, 1)]
    first = delaunay_triangulate(points)
    assert first == delaunay_triangulate(points)
    assert len(first) == 2
    _assert_empty_circumcircles(
        [(Fraction(x), Fraction(y)) for x, y in points], first
    )


def test_seeded_general_position_clouds_match_planar_triangle_count_and_empty_circle():
    rng = random.Random(20261118)
    for n in range(4, 35):
        raw = [(rng.randint(-500, 500) + i / 10000,
                rng.randint(-500, 500) + i / 7000) for i in range(n)]
        points = [(Fraction(str(x)), Fraction(str(y))) for x, y in raw]
        triangles = delaunay_triangulate(raw)
        assert len(triangles) == 2 * n - 2 - _hull_size(points)
        assert {vertex for triangle in triangles for vertex in triangle} == set(points)
        assert all(orient(*triangle) > 0 for triangle in triangles)
        _assert_empty_circumcircles(points, triangles)


def test_duplicate_points_are_rejected():
    with pytest.raises(ValueError, match="duplicate"):
        delaunay_triangulate([(0, 0), (1, 0), (0, 1), (0, 0)])


@pytest.mark.parametrize("points", [
    [],
    [(0, 0), (1, 0)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 0), (1, 0), (float("nan"), 1)],
    [(0, 0), (1, 0), (float("inf"), 1)],
])
def test_invalid_or_degenerate_inputs_are_rejected(points):
    with pytest.raises(ValueError):
        delaunay_triangulate(points)


def test_returned_edges_have_manifold_planar_incidence():
    raw = [(0, 0), (5, 0), (6, 3), (3, 6), (0, 4), (2, 2)]
    triangles = delaunay_triangulate(raw)
    counts = _edges(triangles)
    assert all(count in (1, 2) for count in counts.values())
    assert sum(count == 1 for count in counts.values()) == _hull_size(
        [(Fraction(x), Fraction(y)) for x, y in raw]
    )

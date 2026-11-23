"""Independent Shapely differential checks for native Vatti scanbeam output."""
import random

import pytest
from shapely.geometry import GeometryCollection, Polygon
from shapely.ops import unary_union

from vatti_scanbeam import clip_rings, decompose_scanbeams


def _rect(x0, y0, x1, y1, *, ccw=True):
    ring = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    return ring if ccw else list(reversed(ring))


def _signed_area(ring):
    points = list(ring)
    if points and points[0] == points[-1]:
        points.pop()
    return 0.5 * sum(
        points[i][0] * points[(i + 1) % len(points)][1]
        - points[(i + 1) % len(points)][0] * points[i][1]
        for i in range(len(points))
    )


def _native_geometry(rings):
    shells = [ring for ring in rings if _signed_area(ring) > 0]
    holes = [ring for ring in rings if _signed_area(ring) < 0]
    assignments = [[] for _ in shells]
    shell_polygons = [Polygon(ring) for ring in shells]
    for hole in holes:
        probe = Polygon(hole).representative_point()
        parents = [
            (polygon.area, index)
            for index, polygon in enumerate(shell_polygons)
            if polygon.contains(probe)
        ]
        assert parents, "native output contains an orphan hole"
        assignments[min(parents)[1]].append(hole)
    polygons = [
        Polygon(shell, assignments[index])
        for index, shell in enumerate(shells)
    ]
    return unary_union(polygons) if polygons else GeometryCollection()


def _run_native(subject, clip, operation):
    decomposition = decompose_scanbeams([subject, clip])
    return clip_rings(decomposition, {0}, {1}, operation).rings


def _reference(subject, clip, operation):
    left, right = Polygon(subject), Polygon(clip)
    return {
        "intersection": left.intersection,
        "union": left.union,
        "difference": left.difference,
        "xor": left.symmetric_difference,
    }[operation](right)


@pytest.mark.parametrize(
    "operation", ("intersection", "union", "difference", "xor")
)
def test_seeded_rectangle_boolean_results_match_shapely(operation):
    rng = random.Random(20261116)
    checked = 0
    for _ in range(80):
        rings = []
        for _source in range(2):
            x0, x1 = sorted((rng.randint(-15, 15), rng.randint(-15, 15)))
            y0, y1 = sorted((rng.randint(-15, 15), rng.randint(-15, 15)))
            if x0 == x1 or y0 == y1:
                break
            rings.append([
                (x0, y0), (x1, y0), (x1, y1), (x0, y1)
            ])
        if len(rings) != 2:
            continue
        actual = _native_geometry(_run_native(rings[0], rings[1], operation))
        expected = _reference(rings[0], rings[1], operation)
        tolerance = 1e-9 * max(1.0, expected.area)
        assert actual.is_valid
        assert abs(actual.area - expected.area) <= tolerance
        assert actual.symmetric_difference(expected).area <= tolerance
        checked += 1
    assert checked >= 60


@pytest.mark.parametrize(
    "operation", ("intersection", "union", "difference", "xor")
)
def test_concave_disconnected_overlay_matches_shapely(operation):
    subject = [
        (0, 0), (10, 0), (10, 10), (7, 10),
        (7, 3), (3, 3), (3, 10), (0, 10),
    ]
    clip = [(-1, 5), (11, 5), (11, 8), (-1, 8)]
    actual = _native_geometry(_run_native(subject, clip, operation))
    expected = _reference(subject, clip, operation)
    tolerance = 1e-9 * max(1.0, expected.area)
    assert actual.is_valid
    assert actual.symmetric_difference(expected).area <= tolerance
    if operation == "intersection":
        assert actual.geom_type == "MultiPolygon"
        assert len(actual.geoms) == 2


@pytest.mark.parametrize(
    "operation", ("intersection", "union", "difference", "xor")
)
def test_hole_aware_vatti_overlay_matches_shapely(operation):
    outer = [(0, 0), (10, 0), (10, 10), (0, 10)]
    hole = [(3, 3), (3, 7), (7, 7), (7, 3)]
    clip = [(5, -1), (12, -1), (12, 12), (5, 12)]
    decomposition = decompose_scanbeams([outer, hole, clip])
    rings = clip_rings(decomposition, {0, 1}, {2}, operation).rings
    actual = _native_geometry(rings)
    left, right = Polygon(outer, [hole]), Polygon(clip)
    expected = {
        "intersection": left.intersection,
        "union": left.union,
        "difference": left.difference,
        "xor": left.symmetric_difference,
    }[operation](right)
    tolerance = 1e-9 * max(1.0, expected.area)
    assert actual.is_valid
    assert actual.symmetric_difference(expected).area <= tolerance


@pytest.mark.parametrize(
    "fill_rule,clockwise",
    [
        ("even_odd", False),
        ("non_zero", False),
        ("positive", True),
        ("negative", False),
    ],
)
@pytest.mark.parametrize("operation", ("intersection", "union", "difference", "xor"))
def test_vatti_fill_rules_match_independent_polygon_oracle(
    fill_rule, clockwise, operation
):
    subject = _rect(0, 0, 5, 4, ccw=not clockwise)
    clip = _rect(3, -1, 7, 3, ccw=not clockwise)
    decomposition = decompose_scanbeams([subject, clip])
    actual_rings = clip_rings(
        decomposition, {0}, {1}, operation, fill_rule=fill_rule
    ).rings
    actual = _native_geometry(actual_rings)
    left, right = Polygon(subject), Polygon(clip)
    expected = {
        "intersection": left.intersection,
        "union": left.union,
        "difference": left.difference,
        "xor": left.symmetric_difference,
    }[operation](right)
    tolerance = 1e-9 * max(1.0, expected.area)
    assert actual.is_valid
    assert actual.symmetric_difference(expected).area <= tolerance

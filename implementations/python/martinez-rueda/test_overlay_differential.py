"""Independent differential checks for the native Martinez overlay."""
import random

import pytest
from shapely.geometry import GeometryCollection, Polygon
from shapely.ops import unary_union

from martinez_sweep import boolean_overlay_rings


def _native_geometry(result):
    parts = [
        Polygon(item["shell"], item["holes"])
        for item in result["polygons"]
    ]
    return unary_union(parts) if parts else GeometryCollection()


def _reference_operation(a, b, operation):
    left = Polygon(a[0], a[1:])
    right = Polygon(b[0], b[1:])
    return {
        "intersection": left.intersection,
        "union": left.union,
        "difference": left.difference,
        "symmetric_difference": left.symmetric_difference,
    }[operation](right)


@pytest.mark.parametrize(
    "operation",
    ("intersection", "union", "difference", "symmetric_difference"),
)
def test_seeded_rectangle_overlay_matches_shapely(operation):
    rng = random.Random(20261116)
    checked = 0
    for _ in range(80):
        rectangles = []
        for _source in range(2):
            x0, x1 = sorted((rng.randint(-12, 12), rng.randint(-12, 12)))
            y0, y1 = sorted((rng.randint(-12, 12), rng.randint(-12, 12)))
            if x1 == x0 or y1 == y0:
                break
            rectangles.append([[
                (x0, y0), (x1, y0), (x1, y1), (x0, y1)
            ]])
        if len(rectangles) != 2:
            continue
        native = boolean_overlay_rings(rectangles, operation=operation)
        reference = _reference_operation(
            rectangles[0], rectangles[1], operation
        )
        actual = _native_geometry(native)
        assert actual.is_valid
        tolerance = 1e-9 * max(1.0, reference.area)
        assert abs(actual.area - reference.area) <= tolerance
        assert actual.symmetric_difference(reference).area <= tolerance
        checked += 1
    assert checked >= 60


@pytest.mark.parametrize(
    "operation",
    ("intersection", "union", "difference", "symmetric_difference"),
)
def test_shared_and_coincident_edges_match_shapely(operation):
    cases = [
        # Partial overlap with two coincident horizontal edge intervals.
        (
            [[(0, 0), (2, 0), (2, 2), (0, 2)]],
            [[(1, 0), (3, 0), (3, 2), (1, 2)]],
        ),
        # Adjacent polygons share one complete vertical edge.
        (
            [[(0, 0), (2, 0), (2, 2), (0, 2)]],
            [[(2, 0), (4, 0), (4, 2), (2, 2)]],
        ),
        # Identical geometry with reversed input orientation.
        (
            [[(0, 0), (3, 0), (3, 2), (0, 2)]],
            [[(0, 2), (3, 2), (3, 0), (0, 0)]],
        ),
    ]
    for a, b in cases:
        native = boolean_overlay_rings([a, b], operation=operation)
        reference = _reference_operation(a, b, operation)
        actual = _native_geometry(native)
        tolerance = 1e-9 * max(1.0, reference.area)
        assert actual.is_valid
        assert actual.symmetric_difference(reference).area <= tolerance


@pytest.mark.parametrize(
    "operation", ("intersection", "union", "difference", "symmetric_difference")
)
def test_vertex_and_partial_shared_edge_contacts_match_shapely(operation):
    fixtures = [
        # Point-only contact: union and XOR must retain two components.
        (
            [[(0, 0), (2, 0), (2, 2), (0, 2)]],
            [[(2, 2), (4, 2), (4, 4), (2, 4)]],
        ),
        # Partial shared vertical edge terminating at a shell vertex.
        (
            [[(0, 0), (4, 0), (4, 4), (0, 4)]],
            [[(4, 2), (6, 2), (6, 4), (4, 4)]],
        ),
        # A narrow face smaller than the public epsilon.
        (
            [[(0, 0), (2, 0), (2, 2), (0, 2)]],
            [[(2, 0), (2 + 1e-12, 0), (2 + 1e-12, 2), (2, 2)]],
        ),
    ]
    for a, b in fixtures:
        native = boolean_overlay_rings([a, b], operation=operation)
        actual = _native_geometry(native)
        reference = _reference_operation(a, b, operation)
        tolerance = 1e-9 * max(1.0, reference.area)
        assert actual.is_valid
        assert actual.symmetric_difference(reference).area <= tolerance


@pytest.mark.parametrize(
    "operation", ("intersection", "union", "difference", "symmetric_difference")
)
def test_hole_and_island_overlay_matches_shapely(operation):
    shell = [(0, 0), (10, 0), (10, 10), (0, 10)]
    hole = [(3, 3), (3, 7), (7, 7), (7, 3)]
    island = [(4, 4), (6, 4), (6, 6), (4, 6)]
    subject = [shell, hole]
    clip = [island]
    native = boolean_overlay_rings([subject, clip], operation=operation)
    actual = _native_geometry(native)
    left, right = Polygon(shell, [hole]), Polygon(island)
    expected = {
        "intersection": left.intersection,
        "union": left.union,
        "difference": left.difference,
        "symmetric_difference": left.symmetric_difference,
    }[operation](right)
    assert actual.is_valid
    assert actual.symmetric_difference(expected).area <= 1e-9

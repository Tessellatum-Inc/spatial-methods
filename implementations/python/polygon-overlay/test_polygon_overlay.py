import pytest
from shapely.geometry import LineString, MultiPolygon, Polygon
from polygon_overlay import describe_result, overlay

A = Polygon([(0, 0), (4, 0), (4, 3), (0, 3)])
B = Polygon([(2, -1), (5, -1), (5, 2), (2, 2)])


@pytest.mark.parametrize(("operation", "expected"), [
    ("intersection", 4.0), ("union", 17.0),
    ("difference", 8.0), ("symmetric_difference", 13.0),
])
def test_rectangle_overlay_areas(operation, expected):
    result = overlay(A, B, operation)
    assert result.is_valid
    assert result.area == pytest.approx(expected)


def test_union_intersection_area_identity():
    assert overlay(A, B, "union").area + overlay(A, B, "intersection").area == pytest.approx(A.area + B.area)


def test_difference_intersection_area_identity():
    assert overlay(A, B, "difference").area + overlay(A, B, "intersection").area == pytest.approx(A.area)


def test_disjoint_union_is_multipart():
    distant = Polygon([(10, 10), (12, 10), (12, 12), (10, 12)])
    result = overlay(A, distant, "union")
    assert isinstance(result, MultiPolygon) and len(result.geoms) == 2


def test_disjoint_intersection_is_empty():
    distant = Polygon([(10, 10), (12, 10), (12, 12), (10, 12)])
    assert overlay(A, distant, "intersection").is_empty


def test_containment_difference_creates_hole():
    inner = Polygon([(1, 1), (3, 1), (3, 2), (1, 2)])
    result = overlay(A, inner, "difference")
    assert len(result.interiors) == 1
    assert result.area == pytest.approx(10.0)


def test_edge_touch_intersection_is_line():
    adjacent = Polygon([(4, 0), (6, 0), (6, 3), (4, 3)])
    result = overlay(A, adjacent, "intersection")
    assert isinstance(result, LineString)
    assert result.length == pytest.approx(3.0) and result.area == 0


def test_point_touch_intersection_is_point():
    touching = Polygon([(4, 3), (6, 3), (6, 5), (4, 5)])
    result = overlay(A, touching, "intersection")
    assert result.geom_type == "Point" and result.area == 0


def test_polygon_hole_is_preserved():
    donut = Polygon([(0, 0), (6, 0), (6, 6), (0, 6)],
                    holes=[[(2, 2), (4, 2), (4, 4), (2, 4)]])
    clip = Polygon([(1, 1), (5, 1), (5, 5), (1, 5)])
    result = overlay(donut, clip, "intersection")
    assert result.area == pytest.approx(12.0) and result.is_valid


def test_multipolygon_input_is_supported():
    parts = MultiPolygon([
        Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
        Polygon([(3, 0), (4, 0), (4, 1), (3, 1)]),
    ])
    clip = Polygon([(-1, -1), (5, -1), (5, 2), (-1, 2)])
    assert overlay(parts, clip, "intersection").area == pytest.approx(2.0)


def test_invalid_polygon_is_rejected():
    bow_tie = Polygon([(0, 0), (2, 2), (0, 2), (2, 0)])
    with pytest.raises(ValueError, match="invalid"):
        overlay(bow_tie, A, "intersection")


def test_non_polygonal_input_is_rejected():
    with pytest.raises(TypeError, match="Polygon or MultiPolygon"):
        overlay(A.boundary, B, "intersection")


def test_unknown_operation_is_rejected():
    with pytest.raises(ValueError, match="operation must be"):
        overlay(A, B, "xor")


@pytest.mark.parametrize("grid", [-1, float("nan"), float("inf")])
def test_invalid_precision_grid_is_rejected(grid):
    with pytest.raises(ValueError, match="finite non-negative"):
        overlay(A, B, "intersection", grid_size=grid)


def test_fixed_precision_grid_is_applied():
    result = overlay(A, B, "intersection", grid_size=0.5)
    assert result.is_valid and result.area == pytest.approx(4.0)


def test_result_description_reports_actual_dimension():
    line = overlay(A, Polygon([(4, 0), (6, 0), (6, 3), (4, 3)]), "intersection")
    report = describe_result(line)
    assert report["geometry_type"] == "LineString"
    assert report["area"] == 0.0 and report["is_valid"] is True

def test_seeded_axis_aligned_rectangle_overlay_against_independent_oracle():
    """Check 500 rectangle pairs against interval-arithmetic area formulas."""
    import random

    rng = random.Random(20261115)
    for _ in range(500):
        ax0, ax1 = sorted((rng.uniform(-100, 100), rng.uniform(-100, 100)))
        ay0, ay1 = sorted((rng.uniform(-100, 100), rng.uniform(-100, 100)))
        bx0, bx1 = sorted((rng.uniform(-100, 100), rng.uniform(-100, 100)))
        by0, by1 = sorted((rng.uniform(-100, 100), rng.uniform(-100, 100)))
        # Avoid degenerate rectangles without conditioning the overlap pattern.
        if ax1 - ax0 < 1e-6 or ay1 - ay0 < 1e-6:
            continue
        if bx1 - bx0 < 1e-6 or by1 - by0 < 1e-6:
            continue

        left = Polygon([(ax0, ay0), (ax1, ay0), (ax1, ay1), (ax0, ay1)])
        right = Polygon([(bx0, by0), (bx1, by0), (bx1, by1), (bx0, by1)])
        iw = max(0.0, min(ax1, bx1) - max(ax0, bx0))
        ih = max(0.0, min(ay1, by1) - max(ay0, by0))
        intersection_area = iw * ih
        area_a = (ax1 - ax0) * (ay1 - ay0)
        area_b = (bx1 - bx0) * (by1 - by0)
        union_area = area_a + area_b - intersection_area

        inter = overlay(left, right, "intersection")
        union = overlay(left, right, "union")
        difference = overlay(left, right, "difference")
        symmetric = overlay(left, right, "symmetric_difference")

        assert inter.area == pytest.approx(intersection_area, rel=1e-10, abs=1e-9)
        assert union.area == pytest.approx(union_area, rel=1e-10, abs=1e-9)
        assert difference.area == pytest.approx(area_a - intersection_area, rel=1e-10, abs=1e-9)
        assert symmetric.area == pytest.approx(area_a + area_b - 2 * intersection_area,
                                               rel=1e-10, abs=1e-9)
        assert all(g.is_valid for g in (inter, union, difference, symmetric))


def test_seeded_overlay_metamorphic_symmetry_and_area_conservation():
    """Operation identities should hold across varied rotated rectangles."""
    import random
    from math import cos, sin

    rng = random.Random(81723)

    def rotated_rectangle(cx, cy, width, height, angle):
        c, s = cos(angle), sin(angle)
        return Polygon([
            (cx + x * c - y * s, cy + x * s + y * c)
            for x, y in [(-width / 2, -height / 2),
                         (width / 2, -height / 2),
                         (width / 2, height / 2),
                         (-width / 2, height / 2)]
        ])

    for _ in range(250):
        a = rotated_rectangle(rng.uniform(-5, 5), rng.uniform(-5, 5),
                              rng.uniform(0.2, 8), rng.uniform(0.2, 8),
                              rng.uniform(-3.14, 3.14))
        b = rotated_rectangle(rng.uniform(-5, 5), rng.uniform(-5, 5),
                              rng.uniform(0.2, 8), rng.uniform(0.2, 8),
                              rng.uniform(-3.14, 3.14))
        ab_intersection = overlay(a, b, "intersection")
        ba_intersection = overlay(b, a, "intersection")
        ab_union = overlay(a, b, "union")
        ba_union = overlay(b, a, "union")
        a_minus_b = overlay(a, b, "difference")
        b_minus_a = overlay(b, a, "difference")
        xor = overlay(a, b, "symmetric_difference")

        assert ab_intersection.symmetric_difference(ba_intersection).area == pytest.approx(0.0, abs=1e-8)
        assert ab_union.symmetric_difference(ba_union).area == pytest.approx(0.0, abs=1e-8)
        assert ab_union.area + ab_intersection.area == pytest.approx(a.area + b.area, rel=1e-9, abs=1e-8)
        assert a_minus_b.area + ab_intersection.area == pytest.approx(a.area, rel=1e-9, abs=1e-8)
        assert b_minus_a.area + ab_intersection.area == pytest.approx(b.area, rel=1e-9, abs=1e-8)
        assert xor.area == pytest.approx(a_minus_b.area + b_minus_a.area, rel=1e-9, abs=1e-8)




def test_cascaded_union_matches_union_of_overlapping_polygons():
    from polygon_overlay import cascaded_union
    polygons = [
        Polygon([(0, 0), (3, 0), (3, 2), (0, 2)]),
        Polygon([(2, 0), (5, 0), (5, 2), (2, 2)]),
        Polygon([(4, 0), (7, 0), (7, 2), (4, 2)]),
    ]
    result = cascaded_union(polygons)
    assert result.is_valid
    assert result.area == pytest.approx(14.0)
    assert result.equals(overlay(overlay(polygons[0], polygons[1], "union"),
                                 polygons[2], "union"))


def test_cascaded_union_keeps_disjoint_components_and_holes():
    from polygon_overlay import cascaded_union
    outer = Polygon([(0, 0), (6, 0), (6, 6), (0, 6)])
    inner = Polygon([(2, 2), (4, 2), (4, 4), (2, 4)])
    distant = Polygon([(10, 0), (11, 0), (11, 1), (10, 1)])
    result = cascaded_union([outer.difference(inner), distant])
    assert result.is_valid
    assert result.area == pytest.approx(33.0)
    assert result.geom_type == "MultiPolygon"


def test_cascaded_union_rejects_empty_or_invalid_inputs():
    from polygon_overlay import cascaded_union
    with pytest.raises(ValueError, match="at least one"):
        cascaded_union([])
    with pytest.raises(ValueError, match="invalid"):
        cascaded_union([Polygon([(0, 0), (2, 2), (0, 2), (2, 0)])])


def test_cascaded_union_rejects_invalid_grid():
    from polygon_overlay import cascaded_union
    with pytest.raises(ValueError, match="finite non-negative"):
        cascaded_union([A, B], grid_size=-1)

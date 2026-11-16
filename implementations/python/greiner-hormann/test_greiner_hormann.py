import random
import pytest
from greiner_hormann import greiner_hormann_intersection, _area


def total_area(rings):
    return sum(abs(_area(ring)) for ring in rings)


def test_overlapping_rectangles():
    a = [(0, 0), (6, 0), (6, 4), (0, 4)]
    b = [(2, -1), (5, -1), (5, 5), (2, 5)]
    result = greiner_hormann_intersection(a, b)
    assert len(result) == 1
    assert total_area(result) == pytest.approx(12.0)
    expected = [(2.0, 0.0), (5.0, 0.0), (5.0, 4.0), (2.0, 4.0)]
    assert any(result[0] == expected[i:] + expected[:i] for i in range(len(expected)))


def test_concave_subject_can_produce_disconnected_intersection():
    # The horizontal clip crosses the two arms of this U-shaped polygon.
    u = [(0, 0), (6, 0), (6, 6), (4, 6), (4, 2), (2, 2), (2, 6), (0, 6)]
    horizontal = [(-1, 3), (7, 3), (7, 5), (-1, 5)]
    result = greiner_hormann_intersection(u, horizontal)
    assert len(result) == 2
    assert total_area(result) == pytest.approx(8.0)


def test_containment_returns_inner_polygon():
    outer = [(0, 0), (8, 0), (8, 8), (0, 8)]
    inner = [(2, 2), (4, 2), (4, 4), (2, 4)]
    assert total_area(greiner_hormann_intersection(outer, inner)) == pytest.approx(4.0)


def test_disjoint_returns_empty():
    a = [(0, 0), (1, 0), (1, 1), (0, 1)]
    b = [(3, 3), (4, 3), (4, 4), (3, 4)]
    assert greiner_hormann_intersection(a, b) == []


def test_clockwise_input_is_normalized():
    a = [(0, 0), (6, 0), (6, 4), (0, 4)]
    b = [(2, -1), (5, -1), (5, 5), (2, 5)]
    assert total_area(greiner_hormann_intersection(a[::-1], b[::-1])) == pytest.approx(12.0)


def test_vertex_touch_is_explicitly_rejected():
    a = [(0, 0), (2, 0), (2, 2), (0, 2)]
    b = [(2, 2), (4, 2), (4, 4), (2, 4)]
    with pytest.raises(NotImplementedError, match="vertex-touch"):
        greiner_hormann_intersection(a, b)


def test_invalid_self_crossing_ring_is_rejected():
    bow_tie = [(0, 0), (2, 2), (0, 2), (2, 0)]
    square = [(0, 0), (3, 0), (3, 3), (0, 3)]
    with pytest.raises(ValueError, match="simple ring"):
        greiner_hormann_intersection(bow_tie, square)


def test_seeded_axis_aligned_rectangle_intersections_against_interval_oracle():
    rng = random.Random(221119)
    for _ in range(1000):
        ax0, ax1 = sorted((rng.uniform(-30, 30), rng.uniform(-30, 30)))
        ay0, ay1 = sorted((rng.uniform(-30, 30), rng.uniform(-30, 30)))
        bx0, bx1 = sorted((rng.uniform(-30, 30), rng.uniform(-30, 30)))
        by0, by1 = sorted((rng.uniform(-30, 30), rng.uniform(-30, 30)))
        if min(ax1 - ax0, ay1 - ay0, bx1 - bx0, by1 - by0) < 1e-4:
            continue
        a = [(ax0, ay0), (ax1, ay0), (ax1, ay1), (ax0, ay1)]
        b = [(bx0, by0), (bx1, by0), (bx1, by1), (bx0, by1)]
        expected = max(0.0, min(ax1, bx1) - max(ax0, bx0)) * max(
            0.0, min(ay1, by1) - max(ay0, by0))
        result = greiner_hormann_intersection(a, b)
        assert total_area(result) == pytest.approx(expected, rel=1e-9, abs=1e-8)


def test_seeded_rotated_rectangles_against_shapely_area_oracle():
    from math import cos, sin
    from shapely.geometry import Polygon
    rng = random.Random(90017)
    for _ in range(250):
        def rectangle():
            cx, cy = rng.uniform(-4, 4), rng.uniform(-4, 4)
            w, h, angle = rng.uniform(0.5, 7), rng.uniform(0.5, 7), rng.uniform(-3, 3)
            c, s = cos(angle), sin(angle)
            return [(cx + x*c - y*s, cy + x*s + y*c)
                    for x, y in [(-w/2, -h/2), (w/2, -h/2),
                                 (w/2, h/2), (-w/2, h/2)]]
        a, b = rectangle(), rectangle()
        actual = total_area(greiner_hormann_intersection(a, b))
        expected = Polygon(a).intersection(Polygon(b)).area
        assert actual == pytest.approx(expected, rel=1e-8, abs=1e-7)



def test_seeded_concave_u_intersections_against_disconnected_area_oracle():
    """Randomized concave cases where one intersection splits into two faces."""
    rng = random.Random(20261115)
    checked = 0
    for _ in range(300):
        width = rng.uniform(8.0, 30.0)
        height = rng.uniform(8.0, 25.0)
        arm = rng.uniform(0.5, width * 0.2)
        base = rng.uniform(1.0, height * 0.35)
        lower = rng.uniform(base + 0.1, height * 0.65)
        upper = rng.uniform(lower + 0.1, height - 0.1)
        u_shape = [
            (0.0, 0.0), (width, 0.0), (width, height),
            (width - arm, height), (width - arm, base),
            (arm, base), (arm, height), (0.0, height),
        ]
        strip = [
            (-1.0, lower), (width + 1.0, lower),
            (width + 1.0, upper), (-1.0, upper),
        ]
        result = greiner_hormann_intersection(u_shape, strip)
        assert len(result) == 2
        expected = 2.0 * arm * (upper - lower)
        assert total_area(result) == pytest.approx(expected, rel=1e-8, abs=1e-8)
        checked += 1
    assert checked == 300


@pytest.mark.parametrize("bad_ring", [
    [(0, 0), (1, 0), (float("nan"), 1)],
    [(0, 0), (1, 0), (float("inf"), 1)],
    [(0, 0), (1, 1)],
])
def test_rejects_nonfinite_or_too_short_rings(bad_ring):
    square = [(0, 0), (2, 0), (2, 2), (0, 2)]
    with pytest.raises(ValueError):
        greiner_hormann_intersection(bad_ring, square)

import pytest
from polygon_clipping import clip_convex_polygon, signed_area

SUBJECT = [(0, 0), (6, 0), (6, 4), (0, 4)]
WINDOW = [(2, -1), (5, -1), (5, 5), (2, 5)]


def test_overlap_has_expected_vertices_and_area():
    result = clip_convex_polygon(SUBJECT, WINDOW)
    assert result == [(2.0, 0.0), (5.0, 0.0), (5.0, 4.0), (2.0, 4.0)]
    assert signed_area(result) == pytest.approx(12.0)


def test_clockwise_inputs_are_normalized():
    result = clip_convex_polygon(SUBJECT[::-1], WINDOW[::-1])
    assert signed_area(result) == pytest.approx(12.0)


def test_containment_returns_inner_polygon():
    inner = [(1, 1), (2, 1), (2, 2), (1, 2)]
    assert signed_area(clip_convex_polygon(inner, SUBJECT)) == pytest.approx(1.0)


def test_disjoint_polygons_return_empty():
    distant = [(10, 10), (12, 10), (12, 12), (10, 12)]
    assert clip_convex_polygon(SUBJECT, distant) == []


def test_shared_edge_only_contact_returns_empty():
    adjacent = [(6, 0), (8, 0), (8, 4), (6, 4)]
    assert clip_convex_polygon(SUBJECT, adjacent) == []


def test_point_only_contact_returns_empty():
    touching = [(6, 4), (8, 4), (8, 6), (6, 6)]
    assert clip_convex_polygon(SUBJECT, touching) == []


def test_concave_input_is_rejected():
    concave = [(0, 0), (4, 0), (2, 1), (4, 4), (0, 4)]
    with pytest.raises(ValueError, match="convex"):
        clip_convex_polygon(concave, WINDOW)


def test_zero_area_input_is_rejected():
    with pytest.raises(ValueError, match="non-zero area"):
        clip_convex_polygon([(0, 0), (1, 1), (2, 2)], WINDOW)


def test_negative_epsilon_is_rejected():
    with pytest.raises(ValueError, match="non-negative"):
        clip_convex_polygon(SUBJECT, WINDOW, epsilon=-1)

def test_seeded_rectangle_clips_against_independent_interval_oracle():
    """Exercise all overlap patterns with a closed-form rectangle oracle."""
    import random

    rng = random.Random(20261116)
    for _ in range(1000):
        ax0, ax1 = sorted((rng.uniform(-50, 50), rng.uniform(-50, 50)))
        ay0, ay1 = sorted((rng.uniform(-50, 50), rng.uniform(-50, 50)))
        bx0, bx1 = sorted((rng.uniform(-50, 50), rng.uniform(-50, 50)))
        by0, by1 = sorted((rng.uniform(-50, 50), rng.uniform(-50, 50)))
        if min(ax1 - ax0, ay1 - ay0, bx1 - bx0, by1 - by0) < 1e-5:
            continue

        subject = [(ax0, ay0), (ax1, ay0), (ax1, ay1), (ax0, ay1)]
        window = [(bx0, by0), (bx1, by0), (bx1, by1), (bx0, by1)]
        expected_width = max(0.0, min(ax1, bx1) - max(ax0, bx0))
        expected_height = max(0.0, min(ay1, by1) - max(ay0, by0))
        expected_area = expected_width * expected_height

        result = clip_convex_polygon(subject, window)
        assert signed_area(result) == pytest.approx(expected_area, rel=1e-10, abs=1e-9)
        if expected_area == 0:
            assert result == []
        else:
            assert len(result) >= 3
            assert signed_area(result) > 0


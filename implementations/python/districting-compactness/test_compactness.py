import math
import pytest
from compactness import polygon_compactness, minimum_enclosing_circle


def test_square_compactness_matches_analytic_scores():
    result = polygon_compactness([(0, 0), (2, 0), (2, 2), (0, 2)])
    assert result["area"] == pytest.approx(4)
    assert result["perimeter"] == pytest.approx(8)
    assert result["polsby_popper"] == pytest.approx(math.pi / 4)
    assert result["reock"] == pytest.approx(2 / math.pi)
    assert result["schwartzberg_ratio"] == pytest.approx(2 / math.sqrt(math.pi))
    assert result["minimum_enclosing_circle"]["radius"] == pytest.approx(math.sqrt(2))


def test_compactness_is_orientation_and_ring_closure_invariant():
    ring = [(0, 0), (4, 0), (4, 2), (0, 2)]
    a = polygon_compactness(ring)
    b = polygon_compactness(list(reversed(ring)) + [ring[-1]])
    assert b["area"] == pytest.approx(a["area"])
    assert b["perimeter"] == pytest.approx(a["perimeter"])
    assert b["polsby_popper"] == pytest.approx(a["polsby_popper"])
    assert b["reock"] == pytest.approx(a["reock"])


def test_near_circular_polygon_has_high_compactness():
    ring = [(math.cos(2*math.pi*i/80), math.sin(2*math.pi*i/80)) for i in range(80)]
    result = polygon_compactness(ring)
    assert result["polsby_popper"] > .99
    assert result["reock"] > .99
    assert result["schwartzberg_ratio"] == pytest.approx(1, abs=.01)


def test_minimum_enclosing_circle_handles_acute_and_collinear_points():
    circle = minimum_enclosing_circle([(0, 0), (2, 0), (1, 2)])
    assert circle["center"] == pytest.approx((1, .75))
    assert circle["radius"] == pytest.approx(1.25)
    line = minimum_enclosing_circle([(0, 0), (2, 0), (1, 0)])
    assert line["center"] == pytest.approx((1, 0))
    assert line["radius"] == pytest.approx(1)


@pytest.mark.parametrize("ring", [
    [(0, 0), (1, 1), (2, 2)],
    [(0, 0), (1, 1), (0, 0)],
    [(0, 0), (1, 0), (float("nan"), 1)],
])
def test_compactness_rejects_degenerate_or_invalid_rings(ring):
    with pytest.raises(ValueError):
        polygon_compactness(ring)

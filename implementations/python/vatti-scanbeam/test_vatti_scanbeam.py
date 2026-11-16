import pytest
from vatti_scanbeam import decompose_scanbeams


def test_rectangle_has_two_scanbeams_and_one_local_minimum():
    ring = [(0, 0), (4, 0), (4, 3), (0, 3)]
    result = decompose_scanbeams([ring])
    assert result.scanbeams == (0.0, 3.0)
    assert len(result.bounds) == 2
    assert len(result.horizontals) == 2
    assert len(result.minima) == 1
    minimum = result.minima[0]
    assert minimum.y == 0
    assert minimum.left_bound.lower == (0.0, 0.0)
    assert minimum.right_bound.lower == (4.0, 0.0)
    assert len(minimum.horizontal_edges) == 1


def test_clockwise_reversal_preserves_minimum_geometry():
    ccw = [(0, 0), (5, 0), (5, 4), (0, 4)]
    cw = list(reversed(ccw))
    a, b = decompose_scanbeams([ccw]), decompose_scanbeams([cw])
    assert a.scanbeams == b.scanbeams
    assert len(a.minima) == len(b.minima) == 1
    assert {a.minima[0].left_bound.lower, a.minima[0].right_bound.lower} == {
        b.minima[0].left_bound.lower, b.minima[0].right_bound.lower}


def test_non_horizontal_minimum_has_two_bounds():
    ring = [(2, 0), (5, 3), (4, 6), (0, 5), (-1, 2)]
    result = decompose_scanbeams([ring])
    assert len(result.minima) == 1
    assert result.minima[0].y == 0
    assert result.minima[0].horizontal_edges == ()


def test_horizontal_bottom_plateau_forms_one_minimum():
    ring = [(0, 0), (2, 0), (4, 0), (5, 3), (0, 3)]
    result = decompose_scanbeams([ring])
    assert len(result.minima) == 1
    assert len(result.minima[0].horizontal_edges) == 2
    assert {result.minima[0].left_bound.lower, result.minima[0].right_bound.lower} == {
        (0.0, 0.0), (4.0, 0.0)}


def test_two_local_minima_are_reported():
    ring = [(0, 2), (2, 0), (4, 2), (6, 0), (8, 2), (8, 5), (0, 5)]
    result = decompose_scanbeams([ring])
    assert len(result.minima) == 2


def test_invalid_rings_and_coordinates_are_rejected():
    with pytest.raises(ValueError):
        decompose_scanbeams([[(0, 0), (1, 1)]])
    with pytest.raises(ValueError, match="finite"):
        decompose_scanbeams([[(0, 0), (1, 0), (0, float("nan"))]])
    with pytest.raises(ValueError, match="repeated"):
        decompose_scanbeams([[(0, 0), (2, 0), (2, 2), (0, 2), (2, 0)]])

import pytest
from vatti_clipping import boolean_clip

A = [(0, 0), (6, 0), (6, 4), (0, 4)]
B = [(2, -1), (5, -1), (5, 5), (2, 5)]

def area(ring):
    return abs(sum(ring[i][0] * ring[(i + 1) % len(ring)][1]
                   - ring[(i + 1) % len(ring)][0] * ring[i][1]
                   for i in range(len(ring))) / 2)

def net_area(polygons):
    return sum(area(p.shell) - sum(area(h) for h in p.holes) for p in polygons)

@pytest.mark.parametrize(("operation", "expected"), [
    ("intersection", 12.0), ("union", 30.0),
    ("difference", 12.0), ("xor", 18.0)])
def test_rectangle_boolean_areas(operation, expected):
    assert net_area(boolean_clip([A], [B], operation, scale=1000)) == pytest.approx(expected)

def test_disconnected_intersection_returns_multiple_components():
    subject = [(0, 0), (10, 0), (10, 2), (0, 2)]
    clips = [[(2, -1), (4, -1), (4, 3), (2, 3)],
             [(6, -1), (8, -1), (8, 3), (6, 3)]]
    result = boolean_clip([subject], clips, "intersection")
    assert len(result) == 2
    assert net_area(result) == pytest.approx(8.0)

def test_difference_preserves_hole_hierarchy():
    outer = [(0, 0), (10, 0), (10, 10), (0, 10)]
    inner = [(3, 3), (7, 3), (7, 7), (3, 7)]
    result = boolean_clip([outer], [inner], "difference")
    assert len(result) == 1 and len(result[0].holes) == 1
    assert net_area(result) == pytest.approx(84.0)

def test_nested_island_is_separate_component():
    outer = [(0, 0), (12, 0), (12, 12), (0, 12)]
    hole = [(2, 2), (10, 2), (10, 10), (2, 10)]
    island = [(4, 4), (8, 4), (8, 8), (4, 8)]
    result = boolean_clip([outer], [hole, island], "difference")
    assert len(result) == 2
    assert sorted(net_area([p]) for p in result) == pytest.approx([16.0, 80.0])

def test_fill_rule_resolves_self_crossing_ring():
    bow_tie = [(0, 0), (4, 4), (0, 4), (4, 0)]
    result = boolean_clip([bow_tie], [], "union", fill_rule="even_odd")
    assert len(result) == 2
    assert net_area(result) == pytest.approx(8.0)

def test_invalid_contract_values_are_rejected():
    with pytest.raises(ValueError, match="operation"):
        boolean_clip([A], [B], "buffer")
    with pytest.raises(ValueError, match="fill_rule"):
        boolean_clip([A], [B], "union", fill_rule="winding")
    with pytest.raises(ValueError, match="positive integer"):
        boolean_clip([A], [B], "union", scale=0)

def test_precision_grid_collapse_is_reported():
    tiny = [(0, 0), (0.0001, 0), (0, 0.0001)]
    with pytest.raises(ValueError, match="collapses"):
        boolean_clip([tiny], [], "union", scale=10)

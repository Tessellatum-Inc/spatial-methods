import pytest
from shapely.geometry import LineString, Polygon
from topological_relations import de9im, rcc8

OUTER = Polygon([(0, 0), (10, 0), (10, 10), (0, 10)])
INNER = Polygon([(2, 2), (4, 2), (4, 4), (2, 4)])
TANGENT = Polygon([(0, 2), (4, 2), (4, 4), (0, 4)])
DISJOINT = Polygon([(20, 20), (22, 20), (22, 22), (20, 22)])
ADJACENT = Polygon([(10, 0), (12, 0), (12, 10), (10, 10)])
OVERLAP = Polygon([(5, 5), (12, 5), (12, 12), (5, 12)])

@pytest.mark.parametrize(("a", "b", "expected"), [
    (OUTER, DISJOINT, "DC"),
    (OUTER, ADJACENT, "EC"),
    (OUTER, OVERLAP, "PO"),
    (OUTER, OUTER, "EQ"),
    (TANGENT, OUTER, "TPP"),
    (INNER, OUTER, "NTPP"),
    (OUTER, TANGENT, "TPPi"),
    (OUTER, INNER, "NTPPi"),
])
def test_all_rcc8_relations(a, b, expected):
    assert rcc8(a, b) == expected

def test_de9im_returns_nine_intersection_cells():
    matrix = de9im(OUTER, ADJACENT)
    assert len(matrix) == 9
    assert matrix[0] == "F"

def test_directional_relations_are_inverse_pairs():
    assert rcc8(TANGENT, OUTER) == "TPP"
    assert rcc8(OUTER, TANGENT) == "TPPi"
    assert rcc8(INNER, OUTER) == "NTPP"
    assert rcc8(OUTER, INNER) == "NTPPi"

def test_invalid_polygon_rejected():
    bow_tie = Polygon([(0, 0), (2, 2), (0, 2), (2, 0)])
    with pytest.raises(ValueError, match="valid"):
        rcc8(bow_tie, OUTER)

def test_empty_and_non_region_inputs_rejected():
    with pytest.raises(ValueError, match="empty"):
        rcc8(Polygon(), OUTER)
    with pytest.raises(TypeError, match="Polygon or MultiPolygon"):
        rcc8(LineString([(0, 0), (1, 1)]), OUTER)


@pytest.mark.parametrize(("a", "b", "expected"), [
    (OUTER, Polygon([(20, 20), (22, 20), (22, 22), (20, 22)]), "NE"),
    (OUTER, Polygon([(20, 2), (22, 2), (22, 4), (20, 4)]), "E"),
    (OUTER, Polygon([(2, 20), (4, 20), (4, 22), (2, 22)]), "N"),
    (OUTER, Polygon([(-2, 2), (0, 2), (0, 4), (-2, 4)]), "W"),
    (OUTER, Polygon([(2, -2), (4, -2), (4, 0), (2, 0)]), "S"),
    (OUTER, Polygon([(2, 2), (4, 2), (4, 4), (2, 4)]), "OVERLAPPING"),
])
def test_bounding_box_cardinal_directions(a, b, expected):
    from topological_relations import cardinal_direction
    assert cardinal_direction(a, b) == expected


def test_cardinal_direction_inverse_pairs():
    from topological_relations import cardinal_direction
    east = Polygon([(20, 2), (22, 2), (22, 4), (20, 4)])
    assert cardinal_direction(OUTER, east) == "E"
    assert cardinal_direction(east, OUTER) == "W"


def test_cardinal_direction_rejects_empty_geometry():
    from topological_relations import cardinal_direction
    with pytest.raises(ValueError, match="empty"):
        cardinal_direction(Polygon(), OUTER)

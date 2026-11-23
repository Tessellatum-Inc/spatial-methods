import pytest

from point_in_polygon import PointLocation, locate_point


SQUARE = [(0, 0), (4, 0), (4, 4), (0, 4)]


def test_point_inside_square():
    assert locate_point((2, 2), SQUARE) is PointLocation.INSIDE


def test_point_outside_square():
    assert locate_point((5, 2), SQUARE) is PointLocation.OUTSIDE


@pytest.mark.parametrize("point", [(0, 2), (4, 2), (2, 0), (2, 4), (0, 0)])
def test_point_on_boundary_is_reported_separately(point):
    assert locate_point(point, SQUARE) is PointLocation.BOUNDARY


def test_implicitly_closed_ring():
    assert locate_point((1, 1), SQUARE) is PointLocation.INSIDE


def test_explicitly_closed_ring():
    closed = SQUARE + [SQUARE[0]]
    assert locate_point((1, 1), closed) is PointLocation.INSIDE


def test_concave_polygon():
    concave = [(0, 0), (4, 0), (4, 1), (1, 1), (1, 4), (0, 4)]
    assert locate_point((0.5, 3), concave) is PointLocation.INSIDE
    assert locate_point((3, 3), concave) is PointLocation.OUTSIDE


def test_ray_through_concave_vertex_uses_half_open_crossing_rule():
    concave = [(0, 0), (4, 0), (4, 4), (2, 2), (0, 4)]
    # The horizontal ray from (1, 2) passes through the concave vertex (2, 2).
    assert locate_point((1, 2), concave) is PointLocation.INSIDE
    assert locate_point((5, 2), concave) is PointLocation.OUTSIDE


def test_ring_requires_three_distinct_vertices():
    with pytest.raises(ValueError, match="three distinct"):
        locate_point((0, 0), [(0, 0), (1, 1), (0, 0)])


def test_winding_number_orientation_and_boundary_contract():
    from point_in_polygon import winding_number, locate_point_winding
    assert winding_number((2, 2), SQUARE) == 1
    assert winding_number((2, 2), list(reversed(SQUARE))) == -1
    assert locate_point_winding((2, 2), SQUARE) is PointLocation.INSIDE
    assert locate_point_winding((5, 2), SQUARE) is PointLocation.OUTSIDE
    assert locate_point_winding((4, 2), SQUARE) is PointLocation.BOUNDARY
    with pytest.raises(ValueError, match="boundary"):
        winding_number((4, 2), SQUARE)


def test_winding_number_handles_concavity_and_reversed_rings():
    from point_in_polygon import winding_number, locate_point_winding
    concave = [(0, 0), (4, 0), (4, 1), (1, 1), (1, 4), (0, 4)]
    assert locate_point_winding((0.5, 3), concave) is PointLocation.INSIDE
    assert locate_point_winding((3, 3), concave) is PointLocation.OUTSIDE
    assert winding_number((0.5, 3), concave) == 1
    assert winding_number((0.5, 3), list(reversed(concave))) == -1


def test_winding_number_matches_even_odd_for_seeded_simple_radial_polygons():
    import math
    import random
    from point_in_polygon import locate_point_winding
    rng = random.Random(20261115)
    for _ in range(150):
        angles = sorted(rng.random() * 2 * math.pi for _ in range(12))
        ring = []
        for angle in angles:
            radius = rng.uniform(2.0, 8.0)
            ring.append((radius * math.cos(angle), radius * math.sin(angle)))
        for _ in range(30):
            point = (rng.uniform(-9, 9), rng.uniform(-9, 9))
            parity = locate_point(point, ring)
            winding = locate_point_winding(point, ring)
            assert winding is parity


def test_winding_number_rejects_nonfinite_inputs():
    from point_in_polygon import winding_number, locate_point_winding
    with pytest.raises(ValueError, match="finite"):
        winding_number((float("nan"), 0), SQUARE)
    with pytest.raises(ValueError, match="finite"):
        locate_point_winding((0, 0), [(0, 0), (1, 0), (0, float("inf"))])


def test_exact_predicates_handle_near_boundary_decimal_values_without_tolerance():
    from point_in_polygon import (
        locate_point_exact, locate_point_winding_exact, winding_number_exact,
    )
    ring = [(0, 0), (10, 0), (10, 10), (0, 10)]
    assert locate_point_exact((5, "0.00000000000000000001"), ring) is PointLocation.INSIDE
    assert locate_point_exact((5, "-0.00000000000000000001"), ring) is PointLocation.OUTSIDE
    assert locate_point_exact((5, 0), ring) is PointLocation.BOUNDARY
    assert locate_point_winding_exact((5, "0.00000000000000000001"), ring) is PointLocation.INSIDE
    assert winding_number_exact((5, 5), ring) == 1


def test_exact_predicates_preserve_large_integer_coordinate_distinctions():
    from point_in_polygon import locate_point_exact, locate_point_winding_exact
    base = 10**18
    ring = [(base, base), (base + 4, base), (base + 4, base + 4), (base, base + 4)]
    assert locate_point_exact((base + 2, base + 2), ring) is PointLocation.INSIDE
    assert locate_point_winding_exact((base + 4, base + 2), ring) is PointLocation.BOUNDARY


def test_exact_predicates_reject_nonfinite_and_boolean_coordinates():
    from point_in_polygon import locate_point_exact, winding_number_exact
    with pytest.raises(ValueError, match="finite"):
        locate_point_exact((float("nan"), 0), SQUARE)
    with pytest.raises(ValueError, match="finite"):
        winding_number_exact((0, 0), [(0, 0), (1, 0), (0, float("inf"))])
    with pytest.raises(ValueError, match="boolean"):
        locate_point_exact((True, 0), SQUARE)


def test_exact_winding_and_even_odd_agree_on_seeded_simple_polygons():
    import math
    import random
    from point_in_polygon import locate_point_exact, locate_point_winding_exact
    rng = random.Random(20261118)
    for _ in range(100):
        angles = sorted(rng.random() * 2 * math.pi for _ in range(10))
        ring = [(round((2 + rng.random() * 5) * math.cos(a), 6),
                 round((2 + rng.random() * 5) * math.sin(a), 6))
                for a in angles]
        for _ in range(20):
            point = (round(rng.uniform(-8, 8), 6), round(rng.uniform(-8, 8), 6))
            assert locate_point_exact(point, ring) is locate_point_winding_exact(point, ring)

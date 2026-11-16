from fractions import Fraction

import pytest

from convex_decomposition import convex_decompose, hertel_mehlhorn_decompose
from ear_clipping import polygon_area


def area2(ring):
    return sum(ring[i][0] * ring[(i + 1) % len(ring)][1]
               - ring[(i + 1) % len(ring)][0] * ring[i][1]
               for i in range(len(ring)))


def is_convex(ring):
    turns = [
        (ring[(i + 1) % len(ring)][0] - ring[i][0])
        * (ring[(i + 2) % len(ring)][1] - ring[(i + 1) % len(ring)][1])
        - (ring[(i + 1) % len(ring)][1] - ring[i][1])
        * (ring[(i + 2) % len(ring)][0] - ring[(i + 1) % len(ring)][0])
        for i in range(len(ring))
    ]
    return all(turn >= 0 for turn in turns) and area2(ring) > 0


def test_square_merges_two_triangles_into_one_piece():
    square = [(0, 0), (4, 0), (4, 3), (0, 3)]
    pieces = convex_decompose(square)
    assert len(pieces) == 1
    assert pieces[0] == [
        (Fraction(0), Fraction(0)), (Fraction(4), Fraction(0)),
        (Fraction(4), Fraction(3)), (Fraction(0), Fraction(3))
    ]


def test_concave_l_shape_is_partitioned_into_convex_pieces():
    polygon = [(0, 0), (3, 0), (3, 1), (1, 1), (1, 3), (0, 3)]
    pieces = convex_decompose(polygon)
    assert len(pieces) >= 2
    assert all(is_convex(piece) for piece in pieces)
    assert sum((abs(area2(piece)) for piece in pieces), Fraction(0)) == 10


def test_clockwise_input_is_normalized():
    polygon = [(0, 0), (0, 2), (2, 2), (2, 0)]
    pieces = convex_decompose(polygon)
    assert len(pieces) == 1
    assert area2(pieces[0]) > 0


def test_triangle_is_already_convex():
    triangle = [(0, 0), (3, 0), (1, 2)]
    pieces = convex_decompose(triangle)
    assert len(pieces) == 1
    assert len(pieces[0]) == 3


@pytest.mark.parametrize("invalid", [
    [(0, 0), (2, 2), (0, 2), (2, 0)],
    [(0, 0), (1, 0), (2, 0)],
])
def test_invalid_polygon_is_rejected(invalid):
    with pytest.raises(ValueError):
        convex_decompose(invalid)


def test_generator_input_is_supported():
    # A single-use generator for the polygon ring is consumed only once.
    vertices = (point for point in [(0, 0), (2, 0), (2, 2), (0, 2)])
    pieces = convex_decompose(vertices)
    assert len(pieces) == 1


def test_many_reflex_vertices_use_adjacency_worklist_and_preserve_partition_area():
    import math

    # A simple star-shaped radial ring with alternating radii creates many
    # reflex vertices while keeping a known interior and no self-crossings.
    ring = []
    for i in range(24):
        angle = 2 * math.pi * i / 24
        radius = 10 if i % 2 == 0 else 6
        ring.append((Fraction(str(radius * math.cos(angle))),
                    Fraction(str(radius * math.sin(angle)))))
    pieces = convex_decompose(ring)
    assert len(pieces) > 1
    assert all(is_convex(piece) for piece in pieces)
    assert sum((abs(area2(piece)) for piece in pieces), Fraction(0)) == 2 * polygon_area(ring)


def test_hertel_mehlhorn_pass_returns_convex_partition_for_concave_ring():
    polygon = [(0, 0), (5, 0), (5, 1), (3, 1), (3, 3), (1, 3), (1, 5), (0, 5)]
    pieces = hertel_mehlhorn_decompose(polygon)
    assert len(pieces) >= 2
    assert all(is_convex(piece) for piece in pieces)
    assert sum((abs(area2(piece)) for piece in pieces), Fraction(0)) == 26


def test_hertel_mehlhorn_pass_is_deterministic_and_handles_convex_input():
    polygon = [(0, 0), (4, 0), (4, 3), (0, 3)]
    first = hertel_mehlhorn_decompose(polygon)
    second = hertel_mehlhorn_decompose(polygon)
    assert first == second
    assert len(first) == 1
    assert is_convex(first[0])


def test_hertel_mehlhorn_pass_handles_generator_input():
    polygon = [(0, 0), (3, 0), (3, 2), (1, 2), (1, 4), (0, 4)]
    pieces = hertel_mehlhorn_decompose(iter(polygon))
    assert all(is_convex(piece) for piece in pieces)
    assert sum((abs(area2(piece)) for piece in pieces), Fraction(0)) == 16

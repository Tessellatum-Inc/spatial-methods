import pytest
from monotone_triangulation import triangulate, triangle_area, polygon_area, orient


def _check(ring):
    triangles = triangulate(ring)
    assert len(triangles) == len(ring) - 2
    assert all(orient(*triangle) > 0 for triangle in triangles)
    assert sum((triangle_area(t) for t in triangles), 0) == polygon_area(ring)
    return triangles


def test_rectangle():
    _check([(0, 0), (5, 1), (6, 4), (4, 7), (1, 6)])


def test_concave_monotone_polygon():
    ring = [(0, 0), (6, 1), (5, 3), (7, 6), (4, 8), (2, 7), (3, 4), (1, 2)]
    _check(ring)


def test_clockwise_ring_is_normalized():
    ring = [(1, 2), (3, 4), (2, 7), (4, 8), (7, 6), (5, 3), (6, 1), (0, 0)]
    _check(list(reversed(ring)))


def test_non_monotone_polygon_is_rejected():
    with pytest.raises(ValueError, match="not y-monotone"):
        triangulate([(0, 0), (5, 1), (3, 3), (5, 5), (0, 6), (2, 3)])


def test_equal_y_is_explicitly_rejected():
    with pytest.raises(ValueError, match="distinct vertex y"):
        triangulate([(0, 0), (4, 0), (5, 4), (2, 6), (0, 4)])


def test_self_intersection_is_rejected():
    with pytest.raises(ValueError, match="not a simple polygon"):
        triangulate([(0, 0), (4, 4), (0, 4), (3, 0), (5, 6)])


def test_general_u_polygon_is_partitioned_into_monotone_pieces():
    from monotone_triangulation import partition_y_monotone, triangulate_general

    ring = [(0, 0), (6, 0.2), (6, 6.3), (5.2, 6.0),
            (4.8, 1.5), (1.8, 1.7), (1.2, 5.8), (0, 6.1)]
    pieces = partition_y_monotone(ring)
    assert len(pieces) >= 2
    assert all(len(piece) >= 3 for piece in pieces)
    assert sum((polygon_area(piece) for piece in pieces), 0) == polygon_area(ring)
    triangles = triangulate_general(ring)
    assert len(triangles) == len(ring) - 2
    assert all(orient(*triangle) > 0 for triangle in triangles)
    assert sum((triangle_area(t) for t in triangles), 0) == polygon_area(ring)


def test_general_partition_accepts_clockwise_input():
    from monotone_triangulation import partition_y_monotone, triangulate_general

    ring = [(0, 0), (6, 0.2), (6, 6.3), (5.2, 6.0),
            (4.8, 1.5), (1.8, 1.7), (1.2, 5.8), (0, 6.1)]
    pieces = partition_y_monotone(list(reversed(ring)))
    assert len(pieces) >= 2
    assert len(triangulate_general(list(reversed(ring)))) == len(ring) - 2


def test_general_partition_rejects_equal_y_event_ties():
    from monotone_triangulation import partition_y_monotone

    with pytest.raises(ValueError, match="distinct vertex y"):
        partition_y_monotone([(0, 0), (4, 0), (5, 4), (2, 6), (0, 4)])


def _strictly_inside_triangle(point, triangle):
    a, b, c = triangle
    turns = [orient(a, b, point), orient(b, c, point), orient(c, a, point)]
    return all(value > 0 for value in turns) or all(value < 0 for value in turns)


def _proper_cross(a, b, c, d):
    return (orient(a, b, c) * orient(a, b, d) < 0 and
            orient(c, d, a) * orient(c, d, b) < 0)


def _assert_triangle_mesh(ring, triangles):
    # Every input boundary edge appears once; every internal edge appears twice.
    from collections import Counter
    edge_counts = Counter()
    for triangle in triangles:
        for i in range(3):
            a, b = triangle[i], triangle[(i + 1) % 3]
            edge_counts[tuple(sorted((a, b)))] += 1
    boundary = {
        tuple(sorted((tuple(map(lambda x: __import__("fractions").Fraction(str(x)), ring[i])),
                      tuple(map(lambda x: __import__("fractions").Fraction(str(x)), ring[(i + 1) % len(ring)])))))
        for i in range(len(ring))
    }
    assert {edge for edge, count in edge_counts.items() if count == 1} == boundary
    assert all(count in (1, 2) for count in edge_counts.values())
    # Distinct triangle interiors may neither cross nor contain one another.
    for i, first in enumerate(triangles):
        for second in triangles[i + 1:]:
            assert not any(_proper_cross(first[k], first[(k + 1) % 3],
                                         second[j], second[(j + 1) % 3])
                           for k in range(3) for j in range(3))
            assert not any(_strictly_inside_triangle(
                (sum(p[0] for p in tri) / 3, sum(p[1] for p in tri) / 3), other)
                for tri, other in ((first, second), (second, first)))


def test_general_partition_matches_independent_ear_clipping_invariants():
    from monotone_triangulation import triangulate_general
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ear-clipping"))
    from ear_clipping import triangulate as ear_triangulate

    ring = [(0, 0), (6, 0.2), (6, 6.3), (5.2, 6.0),
            (4.8, 1.5), (1.8, 1.7), (1.2, 5.8), (0, 6.1)]
    ours = triangulate_general(ring)
    independent = ear_triangulate(ring)
    assert len(ours) == len(independent) == len(ring) - 2
    assert sum((triangle_area(t) for t in ours), 0) == polygon_area(ring)
    assert sum((abs(orient(*t)) / 2 for t in independent), 0) == polygon_area(ring)
    _assert_triangle_mesh(ring, ours)
    _assert_triangle_mesh(ring, independent)


def test_partition_sweep_on_multiple_reflex_vertices():
    from monotone_triangulation import partition_y_monotone, triangulate_general

    ring = [(0, 0), (10, 0.3), (10, 9.7), (8.5, 9.2),
            (8.0, 2.1), (6.2, 2.4), (5.7, 8.8),
            (4.1, 8.4), (3.6, 1.6), (1.4, 1.9),
            (0.9, 9.1), (0, 8.7)]
    pieces = partition_y_monotone(ring)
    assert len(pieces) >= 3
    triangles = triangulate_general(ring)
    assert len(triangles) == len(ring) - 2
    _assert_triangle_mesh(ring, triangles)


def test_general_partition_rejects_collinear_event_vertex():
    from monotone_triangulation import partition_y_monotone

    with pytest.raises(ValueError, match="consecutive collinear"):
        partition_y_monotone([(0, 0), (5, 1), (4, 2), (3, 3), (1, 5), (0, 4)])


def test_general_triangulation_accepts_one_shot_vertex_iterables():
    from monotone_triangulation import triangulate_general

    ring = [(0, 0), (6, 0.2), (6, 6.3), (5.2, 6.0),
            (4.8, 1.5), (1.8, 1.7), (1.2, 5.8), (0, 6.1)]
    triangles = triangulate_general(iter(ring))
    assert len(triangles) == len(ring) - 2
    assert sum((triangle_area(t) for t in triangles), 0) == polygon_area(ring)

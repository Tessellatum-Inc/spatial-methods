import pytest
from monotone_triangulation import triangulate, triangle_area, polygon_area, orient


def _check(ring):
    triangles = triangulate(ring)
    assert len(triangles) == len(ring) - 2
    assert all(orient(*triangle) > 0 for triangle in triangles)
    assert sum((triangle_area(t) for t in triangles), 0) == polygon_area(ring)
    return triangles


def test_rectangle():
    _check([(0, 0), (5, 0), (6, 4), (4, 7), (1, 6)])


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

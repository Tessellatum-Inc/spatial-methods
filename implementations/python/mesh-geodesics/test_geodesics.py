import math
import pytest
from geodesics import mesh_edge_distances, mesh_edge_shortest_path


def test_flat_square_mesh_edge_route():
    vertices = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)]
    faces = [(0, 1, 2), (0, 2, 3)]
    path, length = mesh_edge_shortest_path(vertices, faces, 0, 2)
    assert path == [0, 2]
    assert length == pytest.approx(math.sqrt(2))


def test_distances_respect_disconnected_components():
    vertices = [(0, 0, 0), (1, 0, 0), (3, 0, 0), (4, 0, 0)]
    faces = [(0, 1, 2)]
    d = mesh_edge_distances(vertices, faces, 0)
    assert d[0] == 0
    assert math.isinf(d[3])


def test_shortest_path_uses_valid_edge_route():
    vertices = [(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)]
    faces = [(0, 1, 2), (0, 2, 3)]
    path, length = mesh_edge_shortest_path(vertices, faces, 1, 3)
    # Both equal-length routes are valid; tie-breaking follows face order.
    assert path in ([1, 2, 3], [1, 0, 3])
    assert length == pytest.approx(2.0)


@pytest.mark.parametrize("faces", [[(0, 0, 1)], [(0, 1, 9)], [(0, 1)]])
def test_invalid_faces_rejected(faces):
    with pytest.raises(ValueError):
        mesh_edge_distances([(0, 0, 0), (1, 0, 0), (0, 1, 0)], faces, 0)


def test_invalid_source_rejected():
    with pytest.raises(ValueError):
        mesh_edge_distances([(0, 0, 0), (1, 0, 0), (0, 1, 0)], [(0, 1, 2)], 3)

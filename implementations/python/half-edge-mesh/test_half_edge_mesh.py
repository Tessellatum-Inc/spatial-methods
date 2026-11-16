import pytest
from half_edge_mesh import HalfEdgeMesh


def test_single_triangle_has_three_boundary_edges():
    mesh = HalfEdgeMesh.from_triangles(3, [(0, 1, 2)])
    assert len(mesh.halfedges) == 3
    assert len(mesh.boundary_edges()) == 3
    assert mesh.face_cycle(0) == (0, 1, 2)
    assert [mesh.destination(i) for i in range(3)] == [1, 2, 0]


def test_two_triangles_share_symmetric_twins_and_are_adjacent():
    mesh = HalfEdgeMesh.from_triangles(4, [(0, 1, 2), (2, 1, 3)])
    shared = [i for i, h in enumerate(mesh.halfedges) if h.twin is not None]
    assert len(shared) == 2
    assert mesh.halfedges[shared[0]].twin == shared[1]
    assert mesh.adjacent_faces(0) == (1,)
    assert mesh.adjacent_faces(1) == (0,)
    assert len(mesh.boundary_edges()) == 4


def test_disconnected_components_and_isolated_vertices_are_supported():
    mesh = HalfEdgeMesh.from_triangles(7, [(0, 1, 2), (3, 4, 5)])
    assert mesh.vertex_edge[6] is None
    assert mesh.incident_faces(3) == (1,)
    assert mesh.adjacent_faces(0) == ()


def test_closed_tetrahedral_surface_has_no_boundary():
    mesh = HalfEdgeMesh.from_triangles(4, [(0, 2, 1), (0, 1, 3),
                                           (1, 2, 3), (2, 0, 3)])
    assert mesh.boundary_edges() == ()
    assert all(len(mesh.adjacent_faces(i)) == 3 for i in range(4))


@pytest.mark.parametrize("faces, message", [
    ([(0, 1)], "not triangular"),
    ([(0, 1, 1)], "repeats a vertex"),
    ([(0, 1, 5)], "out-of-range"),
    ([(0, 1, 2), (0, 1, 3)], "inconsistent winding"),
    ([(0, 1, 2), (1, 0, 3), (0, 1, 4)], "more than two"),
    ([(0, 1, 2), (0, 1, 2)], "duplicate geometric"),
    ([(0, 1, 2), (0, 2, 1)], "duplicate geometric"),
])
def test_invalid_topology_is_rejected(faces, message):
    with pytest.raises(ValueError, match=message):
        HalfEdgeMesh.from_triangles(5, faces)


def test_out_of_range_queries_raise():
    mesh = HalfEdgeMesh.from_triangles(3, [(0, 1, 2)])
    with pytest.raises(IndexError):
        mesh.destination(3)
    with pytest.raises(IndexError):
        mesh.face_cycle(1)
    with pytest.raises(IndexError):
        mesh.incident_faces(3)


def test_empty_mesh_is_valid():
    mesh = HalfEdgeMesh.from_triangles(0, [])
    assert mesh.halfedges == ()
    assert mesh.vertex_edge == ()


def test_bow_tie_vertex_with_disconnected_triangle_fans_is_rejected():
    with pytest.raises(ValueError, match="non-manifold link"):
        HalfEdgeMesh.from_triangles(5, [(0, 1, 2), (0, 3, 4)])

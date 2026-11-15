import pytest
from winged_edge_mesh import WingedEdgeMesh


def test_builds_polygon_mesh_with_left_right_face_and_wings():
    mesh = WingedEdgeMesh.from_faces(4, ((0,1,2),(1,3,2)))
    shared = mesh.edge(1,2)
    assert shared.left_face is not None and shared.right_face is not None
    assert shared.left_prev is not None and shared.left_next is not None
    assert len(mesh.boundary_edges()) == 4
    assert len(mesh.incident_edges(1)) == 3


def test_single_polygon_has_boundary_edges():
    mesh = WingedEdgeMesh.from_faces(4, ((0,1,2,3),))
    assert len(mesh.edges) == 4
    assert len(mesh.boundary_edges()) == 4


def test_rejects_nonmanifold_edge():
    with pytest.raises(ValueError, match="non-manifold"):
        WingedEdgeMesh.from_faces(5, ((0,1,2),(1,0,3),(0,1,4)))


def test_rejects_inconsistent_winding():
    with pytest.raises(ValueError, match="inconsistent"):
        WingedEdgeMesh.from_faces(4, ((0,1,2),(0,1,3)))


@pytest.mark.parametrize("faces", [((0,1),), ((0,1,1),), ((0,1,4),)])
def test_rejects_invalid_faces(faces):
    with pytest.raises(ValueError):
        WingedEdgeMesh.from_faces(4, faces)

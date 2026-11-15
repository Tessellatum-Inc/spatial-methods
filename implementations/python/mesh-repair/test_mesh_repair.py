import pytest
from mesh_repair import repair_triangle_mesh


def test_removes_duplicate_and_collapsed_faces_and_compacts_vertices():
    vertices = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (8, 8, 8)]
    faces = [(0, 1, 2), (2, 1, 0), (0, 0, 1)]
    out_v, out_f, report = repair_triangle_mesh(vertices, faces)
    assert len(out_v) == 3
    assert len(out_f) == 1
    assert report["removed_duplicate_faces"] == 1
    assert report["removed_collapsed_faces"] == 1
    assert report["removed_unreferenced_vertices"] == 1


def test_welding_collapses_near_duplicate_vertex_and_removes_duplicate_face():
    vertices = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (1e-5, 0, 0)]
    out_v, out_f, report = repair_triangle_mesh(
        vertices, [(0, 1, 2), (3, 1, 2)], weld_tolerance=1e-4)
    assert len(out_v) == 3
    assert len(out_f) == 1
    assert report["welded_vertices"] == 1
    assert report["removed_duplicate_faces"] == 1


def test_orients_adjacent_faces_consistently():
    vertices = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0)]
    # Both faces initially traverse shared edge 1->2.
    out_v, out_f, report = repair_triangle_mesh(
        vertices, [(0, 1, 2), (1, 2, 3)])
    edges = {}
    for fi, tri in enumerate(out_f):
        for k, u in enumerate(tri):
            v = tri[(k+1) % 3]
            edges.setdefault(tuple(sorted((u, v))), []).append((u, v))
    shared = edges[tuple(sorted((1, 2)))]
    assert shared[0] == shared[1][::-1]
    assert report["flipped_faces"] == 1


def test_disconnected_components_are_oriented_independently():
    vertices = [(0,0,0),(1,0,0),(0,1,0),(3,0,0),(4,0,0),(3,1,0)]
    _, faces, report = repair_triangle_mesh(vertices, [(0,1,2),(3,5,4)])
    assert len(faces) == 2
    assert report["face_components"] == 2


def test_non_manifold_edge_is_rejected():
    vertices = [(0,0,0),(1,0,0),(0,1,0),(0,-1,0),(0,0,1)]
    with pytest.raises(ValueError, match="non-manifold edge"):
        repair_triangle_mesh(vertices, [(0,1,2),(1,0,3),(0,1,4)])


@pytest.mark.parametrize("vertices, faces, kwargs, message", [
    ([(0,0)], [], {}, "three coordinates"),
    ([(float("nan"),0,0)], [], {}, "non-finite"),
    ([(0,0,0)], [(0,1,2)], {}, "out-of-range"),
    ([(0,0,0),(1,0,0)], [(0,1)], {}, "triangular"),
    ([(0,0,0)], [], {"weld_tolerance": -1}, "non-negative"),
])
def test_invalid_inputs(vertices, faces, kwargs, message):
    with pytest.raises(ValueError, match=message):
        repair_triangle_mesh(vertices, faces, **kwargs)


def test_empty_mesh_is_supported():
    assert repair_triangle_mesh([], [])[:2] == ((), ())

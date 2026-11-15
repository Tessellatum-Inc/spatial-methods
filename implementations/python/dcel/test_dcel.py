import pytest
from dcel import DCEL

def rect(x0,y0,x1,y1,reverse=False):
    p=[(x0,y0),(x1,y0),(x1,y1),(x0,y1),(x0,y0)]
    return list(reversed(p)) if reverse else p

def test_single_face_has_twin_exterior_cycle():
    d=DCEL.from_faces({"a":[rect(0,0,2,2)]})
    assert d.validate()
    assert len(d.vertices)==4 and len(d.halfedges)==8
    assert len(d.faces["a"].boundary_cycles)==1
    assert len(d.unbounded_cycles)==1
    assert d.unbounded_face.id is None
    assert d.unbounded_face.boundary_cycles is d.unbounded_cycles

def test_adjacent_faces_share_twins_and_have_consistent_cycles():
    d=DCEL.from_faces({"west":[rect(0,0,1,1)],"east":[rect(1,0,2,1,True)]})
    assert d.validate()
    shared=[e for e in d.halfedges if d.vertices[e.origin].point==(1.0,0.0)
            and d.vertices[e.target].point==(1.0,1.0)]
    assert len(shared)==1
    assert d.halfedges[shared[0].twin].face=="west" or d.halfedges[shared[0].twin].face=="east"
    assert len(d.vertices)==6
    assert len(d.unbounded_cycles)==1

def test_multiple_disconnected_faces_have_separate_exterior_components():
    d=DCEL.from_faces({"a":[rect(0,0,1,1)],"b":[rect(3,0,4,1)]})
    assert d.validate()
    assert len(d.unbounded_cycles)==2
    assert len(d.unbounded_face.boundary_cycles)==2

def test_rejects_bad_rings_and_duplicate_orientation():
    with pytest.raises(ValueError): DCEL.from_faces({"x":[[(0,0),(1,0),(1,1),(0,1)]]})
    with pytest.raises(ValueError):
        DCEL.from_faces({"a":[rect(0,0,1,1)],"b":[rect(0,0,1,1)]})

def test_rejects_repeated_ring_vertex():
    with pytest.raises(ValueError):
        DCEL.from_faces({"x":[[(0,0),(2,0),(2,2),(1,1),(0,2),(2,0),(0,0)]]})

def test_rejects_nonfinite_coordinates():
    with pytest.raises(ValueError):
        DCEL.from_faces({"x":[[(0,0),(1,0),(1,float("inf")),(0,1),(0,0)]]})


def test_rejects_zero_area_ring():
    with pytest.raises(ValueError, match="non-zero signed area"):
        DCEL.from_faces({"flat": [[(0, 0), (1, 0), (2, 0), (0, 0)]]})


def test_rejects_self_intersecting_ring_with_nonzero_signed_area():
    # The non-adjacent first and third edges cross; signed area is non-zero.
    ring = [(0, 0), (4, 4), (0, 3), (3, 0), (0, 0)]
    with pytest.raises(ValueError, match="non-adjacent edges intersect"):
        DCEL.from_faces({"crossed": [ring]})



def test_rejects_crossing_boundaries_between_distinct_faces():
    faces = {
        "a": [[(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)]],
        "b": [[(2, -1), (5, -1), (5, 2), (2, 2), (2, -1)]],
    }
    with pytest.raises(ValueError, match="noded"):
        DCEL.from_faces(faces)


def test_rejects_t_junction_where_vertex_hits_unsplit_edge():
    faces = {
        "a": [[(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)]],
        "b": [[(2, 4), (3, 5), (1, 5), (2, 4)]],
    }
    with pytest.raises(ValueError, match="noded"):
        DCEL.from_faces(faces)


def test_rejects_partial_collinear_shared_boundary():
    faces = {
        "a": [[(0, 0), (4, 0), (4, 4), (0, 4), (0, 0)]],
        "b": [[(2, 4), (5, 4), (5, 6), (2, 6), (2, 4)]],
    }
    with pytest.raises(ValueError, match="collinear overlaps"):
        DCEL.from_faces(faces)


def test_rejects_crossing_edges_between_faces_that_are_not_noded():
    a = [(0, 0), (3, 0), (3, 1), (0, 1), (0, 0)]
    b = [(1, -1), (2, -1), (2, 2), (1, 2), (1, -1)]
    with pytest.raises(ValueError, match="must be noded"):
        DCEL.from_faces({"a": [a], "b": [b]})


def test_rejects_t_junction_between_face_boundaries():
    a = [(0, 0), (3, 0), (3, 2), (0, 2), (0, 0)]
    b = [(1, 0), (2, -1), (2, -2), (1, -2), (1, 0)]
    with pytest.raises(ValueError, match="must be noded"):
        DCEL.from_faces({"a": [a], "b": [b]})


def test_rejects_partial_collinear_shared_edge_overlap():
    a = [(0, 0), (3, 0), (3, 2), (0, 2), (0, 0)]
    b = [(1, 0), (2, 0), (2, -1), (1, -1), (1, 0)]
    with pytest.raises(ValueError, match="partial collinear overlaps"):
        DCEL.from_faces({"a": [a], "b": [b]})

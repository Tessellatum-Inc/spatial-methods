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

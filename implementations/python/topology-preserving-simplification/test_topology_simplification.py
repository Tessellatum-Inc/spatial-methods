import pytest
from topology_simplification import simplify_ring, _simple

def test_closed_ring_and_collinear_vertex():
    ring=[(0,0),(2,0),(4,0),(4,4),(0,4),(0,0)]
    out=simplify_ring(ring,0.1)
    assert out[0]==out[-1] and len(out)==5
    assert _simple(out[:-1])

def test_open_concave_ring_stays_simple_and_ccw():
    ring=[(0,0),(4,0),(4,4),(2.1,2),(0,4),(0,2)]
    out=simplify_ring(ring,0.5)
    assert out[0]!=out[-1] and _simple(out)
    assert sum(out[i][0]*out[(i+1)%len(out)][1]-out[(i+1)%len(out)][0]*out[i][1] for i in range(len(out)))>0

def test_rejects_invalid_rings():
    with pytest.raises(ValueError,match="simple"):
        simplify_ring([(0,0),(3,3),(0,3),(3,0)],1)
    with pytest.raises(ValueError,match="simple"):
        simplify_ring([(0,0),(1,0),(2,0)],1)

def test_rejects_invalid_threshold_and_coordinates():
    with pytest.raises(ValueError,match="area_threshold"):
        simplify_ring([(0,0),(1,0),(0,1)],-1)
    with pytest.raises(ValueError,match="finite"):
        simplify_ring([(0,0),(1,0),(float("nan"),1)],1)

def test_retains_at_least_three_vertices():
    out=simplify_ring([(0,0),(4,0),(2,3),(0,4),(-2,2)],1e6)
    assert len(out)>=3 and _simple(out)

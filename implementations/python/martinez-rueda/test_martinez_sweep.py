import pytest
from martinez_sweep import sweep_split_segments

def test_overlapping_rectangles_split_crossed_edges():
    a=[(0,0),(4,0),(4,3),(0,3)]; b=[(2,-1),(5,-1),(5,2),(2,2)]
    r=sweep_split_segments([[a],[b]])
    assert len(r["intersection_events"])==2
    assert len(r["split_segments"])==12

def test_disjoint_rectangles_have_no_crossings():
    a=[(0,0),(1,0),(1,1),(0,1)]; b=[(3,0),(4,0),(4,1),(3,1)]
    r=sweep_split_segments([[a],[b]])
    assert not r["intersection_events"] and len(r["split_segments"])==8

def test_concave_ring_multiple_crossings():
    a=[(0,0),(6,0),(6,6),(4,6),(4,2),(2,2),(2,6),(0,6)]
    b=[(-1,3),(7,3),(7,5),(-1,5)]
    assert len(sweep_split_segments([[a],[b]])["intersection_events"])==4

def test_shared_endpoint_is_not_proper_crossing():
    a=[(0,0),(2,0),(2,2),(0,2)]; b=[(2,2),(4,2),(4,4),(2,4)]
    assert not sweep_split_segments([[a],[b]])["intersection_events"]

def test_collinear_overlap_rejected():
    a=[(0,0),(2,0),(2,2),(0,2)]; b=[(1,0),(3,0),(3,2),(1,2)]
    with pytest.raises(NotImplementedError): sweep_split_segments([[a],[b]])

def test_invalid_input_rejected():
    with pytest.raises(ValueError): sweep_split_segments([ [[(0,0),(0,0),(1,1)]] ])
    sq=[(0,0),(1,0),(1,1),(0,1)]
    with pytest.raises(ValueError): sweep_split_segments([[sq],[sq]],epsilon=0)

def test_seeded_rectangle_crossing_counts():
    import random
    rng=random.Random(48)
    for _ in range(150):
        x0,x1=sorted((rng.uniform(-5,5),rng.uniform(-5,5)))
        y0,y1=sorted((rng.uniform(-5,5),rng.uniform(-5,5)))
        u0,u1=sorted((rng.uniform(-5,5),rng.uniform(-5,5)))
        v0,v1=sorted((rng.uniform(-5,5),rng.uniform(-5,5)))
        if min(x1-x0,y1-y0,u1-u0,v1-v0)<1e-4: continue
        a=[(x0,y0),(x1,y0),(x1,y1),(x0,y1)]
        b=[(u0,v0),(u1,v0),(u1,v1),(u0,v1)]
        assert len(sweep_split_segments([[a],[b]])["intersection_events"]) in (0,2,4)

import pytest
from martinez_sweep import (sweep_split_segments, classify_boundary_fragments, fragment_area_contribution, boolean_overlay_rings)

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

def test_boolean_fragment_classification_matches_rectangle_areas():
    a=[(0,0),(4,0),(4,3),(0,3)]
    b=[(2,-1),(5,-1),(5,2),(2,2)]
    expected={"intersection":4.0,"union":17.0,"difference":8.0,"symmetric_difference":13.0}
    for operation,area in expected.items():
        result=classify_boundary_fragments([[a],[b]],operation=operation)
        assert fragment_area_contribution(result["selected_fragments"])==pytest.approx(area)


def test_containment_classification_handles_hole_orientation_for_difference():
    outer=[(0,0),(6,0),(6,6),(0,6)]
    inner=[(2,2),(4,2),(4,4),(2,4)]
    diff=classify_boundary_fragments([[outer],[inner]],operation="difference")
    assert fragment_area_contribution(diff["selected_fragments"])==pytest.approx(32.0)
    inter=classify_boundary_fragments([[outer],[inner]],operation="intersection")
    assert fragment_area_contribution(inter["selected_fragments"])==pytest.approx(4.0)


def test_classification_rejects_multiple_ring_inputs_until_hole_roles_exist():
    a=[(0,0),(4,0),(4,4),(0,4)]
    with pytest.raises(NotImplementedError):
        classify_boundary_fragments([[a,a],[a]])

def test_stitched_boolean_results_match_rectangle_areas_and_components():
    a=[(0,0),(4,0),(4,3),(0,3)]
    b=[(2,-1),(5,-1),(5,2),(2,2)]
    expected={'intersection':(4.0,1),'union':(17.0,1),'difference':(8.0,1),'symmetric_difference':(13.0,2)}
    for op,(area,count) in expected.items():
        result=boolean_overlay_rings([[a],[b]],operation=op)
        assert result['area']==pytest.approx(area)
        assert len(result['rings'])==count
        assert all(len(ring)>=3 for ring in result['rings'])

def test_containment_stitches_hole_with_opposite_orientation():
    outer=[(0,0),(6,0),(6,6),(0,6)]
    inner=[(2,2),(4,2),(4,4),(2,4)]
    diff=boolean_overlay_rings([[outer],[inner]],operation='difference')
    assert diff['area']==pytest.approx(32.0)
    assert len(diff['rings'])==2
    assert sorted((1 if sum(diff['rings'][i][j][0]*diff['rings'][i][(j+1)%len(diff['rings'][i])][1]-diff['rings'][i][(j+1)%len(diff['rings'][i])][0]*diff['rings'][i][j][1] for j in range(len(diff['rings'][i])))>0 else -1) for i in range(2))==[-1,1]
    union=boolean_overlay_rings([[outer],[inner]],operation='union')
    assert union['area']==pytest.approx(36.0) and len(union['rings'])==1
    inter=boolean_overlay_rings([[outer],[inner]],operation='intersection')
    assert inter['area']==pytest.approx(4.0) and len(inter['rings'])==1
    xor=boolean_overlay_rings([[outer],[inner]],operation='symmetric_difference')
    assert xor['area']==pytest.approx(32.0) and len(xor['rings'])==2

def test_disjoint_union_stitches_two_components_and_intersection_is_empty():
    a=[(0,0),(1,0),(1,1),(0,1)]
    b=[(3,0),(4,0),(4,1),(3,1)]
    assert len(boolean_overlay_rings([[a],[b]],operation='union')['rings'])==2
    assert boolean_overlay_rings([[a],[b]],operation='intersection')['rings']==()

def test_stitching_accepts_clockwise_input_rings():
    a=[(0,3),(4,3),(4,0),(0,0)]
    b=[(2,2),(5,2),(5,-1),(2,-1)]
    assert boolean_overlay_rings([[a],[b]],operation='intersection')['area']==pytest.approx(4.0)

def test_concave_intersection_stitches_two_disconnected_components():
    a=[(0,0),(6,0),(6,6),(4,6),(4,2),(2,2),(2,6),(0,6)]
    b=[(-1,3),(7,3),(7,5),(-1,5)]
    result=boolean_overlay_rings([[a],[b]],operation='intersection')
    assert result['area']==pytest.approx(8.0)
    assert len(result['rings'])==2

def test_self_crossing_ring_is_rejected():
    bowtie=[(0,0),(2,2),(0,2),(2,0)]
    other=[(3,0),(4,0),(4,1),(3,1)]
    with pytest.raises(ValueError): boolean_overlay_rings([[bowtie],[other]])

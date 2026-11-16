import pytest
from martinez_sweep import (sweep_split_segments, classify_boundary_fragments, fragment_area_contribution, boolean_overlay_rings, _YIntervalStatus, Segment, _intersection)

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
    # Both horizontal edges of b cross all four arms of the concave ring.
    assert len(sweep_split_segments([[a],[b]])["intersection_events"])==8

def test_shared_endpoint_is_not_proper_crossing():
    a=[(0,0),(2,0),(2,2),(0,2)]; b=[(2,2),(4,2),(4,4),(2,4)]
    result=sweep_split_segments([[a],[b]])
    assert not result["intersection_events"]
    assert any(event.kind=="contact" for event in result["node_events"])

def test_collinear_overlap_is_split_at_both_bundle_endpoints():
    a=[(0,0),(2,0),(2,2),(0,2)]
    b=[(1,0),(3,0),(3,2),(1,2)]
    result=sweep_split_segments([[a],[b]])
    # Both shared horizontal edges are noded at x=1 and x=2.
    assert len(result["split_segments"]) == 12
    assert result["intersection_events"] == ()

@pytest.mark.parametrize("operation,expected_area,expected_rings", [
    ("intersection", 2.0, 1),
    ("union", 6.0, 1),
    ("difference", 2.0, 1),
    ("symmetric_difference", 4.0, 2),
])
def test_partial_collinear_overlap_boolean_results(operation, expected_area, expected_rings):
    a=[(0,0),(2,0),(2,2),(0,2)]
    b=[(1,0),(3,0),(3,2),(1,2)]
    result=boolean_overlay_rings([[a],[b]], operation=operation)
    assert result["area"] == pytest.approx(expected_area)
    assert len(result["rings"]) == expected_rings

@pytest.mark.parametrize("operation,expected_area,expected_rings", [
    ("intersection", 4.0, 1),
    ("union", 4.0, 1),
    ("difference", 0.0, 0),
    ("symmetric_difference", 0.0, 0),
])
def test_identical_coincident_polygons_are_bundled_once(operation, expected_area, expected_rings):
    a=[(0,0),(2,0),(2,2),(0,2)]
    b=list(reversed(a))
    result=boolean_overlay_rings([[a],[b]], operation=operation)
    assert result["area"] == pytest.approx(expected_area)
    assert len(result["rings"]) == expected_rings

@pytest.mark.parametrize("operation,expected_area,expected_rings", [
    ("intersection", 0.0, 0),
    ("union", 8.0, 1),
    ("difference", 4.0, 1),
    ("symmetric_difference", 8.0, 1),
])
def test_adjacent_polygons_with_shared_edge_all_boolean_operations(
    operation, expected_area, expected_rings
):
    a=[(0,0),(2,0),(2,2),(0,2)]
    b=[(2,0),(4,0),(4,2),(2,2)]
    result=boolean_overlay_rings([[a],[b]], operation=operation)
    assert result["area"] == pytest.approx(expected_area)
    assert len(result["rings"]) == expected_rings


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


def test_invalid_touching_shell_hole_ring_collection_is_rejected():
    a=[(0,0),(4,0),(4,4),(0,4)]
    with pytest.raises(ValueError):
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

def test_polygon_input_hole_and_island_inside_hole():
    shell=[(0,0),(10,0),(10,10),(0,10)]
    hole=[(3,3),(3,7),(7,7),(7,3)]
    island=[(4,4),(6,4),(6,6),(4,6)]
    union=boolean_overlay_rings([[shell,hole],[island]],operation='union')
    assert union['area']==pytest.approx(88.0)
    assert len(union['rings'])==3
    inter=boolean_overlay_rings([[shell,hole],[island]],operation='intersection')
    assert inter['rings']==()
    diff=boolean_overlay_rings([[shell,hole],[island]],operation='difference')
    assert diff['area']==pytest.approx(84.0)
    assert len(diff['rings'])==2

def test_invalid_hole_outside_shell_is_rejected():
    shell=[(0,0),(5,0),(5,5),(0,5)]
    hole=[(6,6),(6,7),(7,7),(7,6)]
    other=[(10,10),(11,10),(11,11),(10,11)]
    with pytest.raises(ValueError): boolean_overlay_rings([[shell,hole],[other]])

def test_y_interval_sweep_status_prunes_x_overlapping_but_y_disjoint_segments():
    a=[(0,0),(10,0),(10,1),(0,1)]
    b=[(0,10),(10,10),(10,11),(0,11)]
    result=sweep_split_segments([[a],[b]])
    assert result["candidate_pairs_tested"]==0
    assert result["intersection_events"]==()
    assert len(result["split_segments"])==8

def test_y_interval_treap_matches_brute_force_after_insertions_and_removals():
    import random
    rng=random.Random(901)
    status=_YIntervalStatus()
    intervals={}
    for sid in range(250):
        low=rng.uniform(-100,100)
        high=low+rng.uniform(0.01,20)
        intervals[sid]=(low,high)
        status.insert(sid,low,high)
    for _ in range(100):
        low=rng.uniform(-100,100)
        high=low+rng.uniform(0.01,20)
        expected={sid for sid,(a,b) in intervals.items() if a<=high and b>=low}
        assert set(status.overlaps(low,high))==expected
    removed=set(rng.sample(list(intervals),80))
    for sid in removed:
        status.remove(sid)
        intervals.pop(sid)
    for _ in range(100):
        low=rng.uniform(-100,100)
        high=low+rng.uniform(0.01,20)
        expected={sid for sid,(a,b) in intervals.items() if a<=high and b>=low}
        assert set(status.overlaps(low,high))==expected


def test_boolean_overlay_exposes_polygon_shell_hole_grouping():
    outer=[(0,0),(6,0),(6,6),(0,6)]
    inner=[(2,2),(4,2),(4,4),(2,4)]
    result=boolean_overlay_rings([[outer],[inner]],operation="difference")
    assert len(result["rings"])==2
    assert len(result["polygons"])==1
    assert result["polygons"][0]["shell"] in result["rings"]
    assert result["polygons"][0]["holes"] == tuple(
        ring for ring in result["rings"] if ring is not result["polygons"][0]["shell"]
    )
    assert len(result["polygons"][0]["holes"])==1


def test_island_inside_hole_is_a_separate_polygon_component():
    shell=[(0,0),(10,0),(10,10),(0,10)]
    hole=[(3,3),(3,7),(7,7),(7,3)]
    island=[(4,4),(6,4),(6,6),(4,6)]
    result=boolean_overlay_rings([[shell,hole],[island]],operation="union")
    assert result["area"]==pytest.approx(88.0)
    assert len(result["polygons"])==2
    assert sorted(len(poly["holes"]) for poly in result["polygons"])==[0,1]
    assert sum(abs(sum(
        poly["shell"][i][0]*poly["shell"][(i+1)%len(poly["shell"])][1]
        -poly["shell"][(i+1)%len(poly["shell"])][0]*poly["shell"][i][1]
        for i in range(len(poly["shell"]))
    ))/2 for poly in result["polygons"])==pytest.approx(104.0)


def test_polygon_component_assembly_rejects_orphan_hole():
    from martinez_sweep import assemble_polygon_components
    orphan=[(2,2),(2,4),(4,4),(4,2)]
    with pytest.raises(ValueError,match="no containing shell"):
        assemble_polygon_components((orphan,))


def test_exact_rational_predicate_detects_crossing_below_epsilon_area_scale():
    # The determinant is 2e-20, smaller than epsilon, but the segments
    # properly cross. A dimensionally inconsistent determinant-vs-epsilon
    # comparison used to classify these as parallel.
    a=Segment(0,0,0,(0.0,0.0),(1e-10,1e-10))
    b=Segment(1,0,0,(0.0,1e-10),(1e-10,0.0))
    hit=_intersection(a,b,1e-10)
    assert hit is not None
    t,u,p,proper=hit
    assert float(t)==pytest.approx(0.5)
    assert float(u)==pytest.approx(0.5)
    assert p==(5e-11,5e-11)
    assert proper


def test_exact_predicate_handles_near_parallel_but_nonparallel_segments():
    a=Segment(0,0,0,(0.0,0.0),(1.0,1e-12))
    b=Segment(1,0,0,(0.0,1e-12),(1.0,0.0))
    hit=_intersection(a,b,1e-14)
    assert hit is not None
    assert hit[2]==pytest.approx((0.5,5e-13))


def test_exact_predicate_keeps_collinear_overlap_rejection():
    a=Segment(0,0,0,(0.0,0.0),(2.0,0.0))
    b=Segment(1,0,0,(1.0,0.0),(3.0,0.0))
    with pytest.raises(NotImplementedError,match="collinear"):
        _intersection(a,b,1e-10)


def test_seeded_exact_segment_predicates_against_independent_integer_oracle():
    from fractions import Fraction
    import random

    rng=random.Random(20261116)
    checked=0
    for sid in range(1200):
        points=[(rng.randint(-1000,1000),rng.randint(-1000,1000)) for _ in range(4)]
        a,b,c,d=points
        if a==b or c==d:
            continue
        rx,ry=b[0]-a[0],b[1]-a[1]
        sx,sy=d[0]-c[0],d[1]-c[1]
        den=rx*sy-ry*sx
        if den==0:
            continue
        qx,qy=c[0]-a[0],c[1]-a[1]
        t=Fraction(qx*sy-qy*sx,den)
        u=Fraction(qx*ry-qy*rx,den)
        expected=0<=t<=1 and 0<=u<=1
        hit=_intersection(
            Segment(0,0,0,a,b),Segment(1,0,0,c,d),1e-12
        )
        assert (hit is not None)==expected
        if expected:
            assert float(hit[0])==pytest.approx(float(t),abs=1e-12)
            assert float(hit[1])==pytest.approx(float(u),abs=1e-12)
            assert hit[2]==pytest.approx(
                (float(Fraction(a[0])+t*rx),float(Fraction(a[1])+t*ry)),
                abs=1e-9,
            )
        checked+=1
    assert checked>=1000


def test_exact_ring_predicates_detect_tiny_self_crossing_below_area_epsilon():
    from martinez_sweep import _ring_is_simple
    scale=1e-12
    ring=[(0.0,0.0),(2*scale,2*scale),(0.0,2*scale),(2*scale,0.0)]
    assert not _ring_is_simple(ring,1e-10)


def test_exact_point_in_ring_handles_small_scale_and_boundary():
    from martinez_sweep import _inside
    scale=1e-12
    ring=[(0.0,0.0),(4*scale,0.0),(4*scale,4*scale),(0.0,4*scale)]
    assert _inside((2*scale,2*scale),ring)
    assert not _inside((0.0,2*scale),ring)
    assert not _inside((5*scale,2*scale),ring)


def test_exact_point_in_ring_handles_large_coordinates_and_horizontal_edges():
    from martinez_sweep import _inside
    base=1e15
    ring=[(base,base),(base+8,base),(base+8,base+8),(base,base+8)]
    assert _inside((base+4,base+4),ring)
    assert not _inside((base+4,base),ring)
    assert not _inside((base+9,base+4),ring)


def test_exact_segment_intersection_does_not_report_disjoint_collinear_edges():
    from martinez_sweep import _segments_intersect_exact
    assert not _segments_intersect_exact((0,0),(1,0),(2,0),(3,0))
    assert _segments_intersect_exact((0,0),(2,0),(1,0),(3,0))


def test_exact_ring_validation_rejects_adjacent_collinear_backtracking():
    from martinez_sweep import _ring_is_simple
    ring=[(0,0),(3,0),(1,0),(1,2),(0,2)]
    assert not _ring_is_simple(ring,1e-10)


def test_exact_signed_area_accepts_valid_ring_below_area_epsilon():
    from martinez_sweep import _signed_area_exact, sweep_split_segments
    scale=1e-12
    ring=[(0.0,0.0),(scale,0.0),(scale,scale),(0.0,scale)]
    assert _signed_area_exact(ring)>0
    result=sweep_split_segments([[ring]],epsilon=1e-10)
    assert len(result["segments"])==4
    assert len(result["split_segments"])==4


def test_exact_signed_area_preserves_orientation_at_large_coordinate_offset():
    from martinez_sweep import _signed_area_exact
    base=1e15
    ccw=[(base,base),(base+4,base),(base+4,base+4),(base,base+4)]
    assert _signed_area_exact(ccw)==16
    assert _signed_area_exact(list(reversed(ccw)))==-16


def test_distinct_intersections_closer_than_epsilon_keep_separate_split_fragments():
    from martinez_sweep import sweep_split_segments
    delta=1e-11
    a=[(0.0,0.0),(1.0,0.0),(1.0,1.0),(0.0,1.0)]
    b=[(0.5,-1.0),(0.5+delta,-1.0),(0.5+delta,2.0),(0.5,2.0)]
    result=sweep_split_segments([[a],[b]],epsilon=1e-10)
    bottom=[f for f in result["split_segments"]
            if f.source==0 and f.ring==0 and f.index==0]
    assert len(bottom)==3
    assert bottom[0].b[0] < bottom[1].a[0] or bottom[0].b[0] == bottom[1].a[0]
    assert bottom[1].b[0] > bottom[1].a[0]
    assert bottom[1].b[0] < bottom[2].a[0] or bottom[1].b[0] == bottom[2].a[0]


def test_exact_point_in_ring_accepts_fraction_coordinates():
    from fractions import Fraction
    from martinez_sweep import _inside
    ring=[(0,0),(2,0),(2,2),(0,2)]
    assert _inside((Fraction(1,2),Fraction(3,2)),ring)
    assert not _inside((Fraction(2),Fraction(1)),ring)


def test_x_window_expiry_heap_preserves_disjoint_sweep_results():
    # Both polygons are valid, but their x-ranges are separated by a wide gap.
    a=[(0,0),(10,0),(10,10),(0,10)]
    b=[(100,0),(110,0),(110,10),(100,10)]
    result=sweep_split_segments([[a],[b]])
    assert result["candidate_pairs_tested"]==0
    assert len(result["split_segments"])==8
    assert result["intersection_events"]==()


def test_split_parameters_are_exact_fractions():
    from fractions import Fraction
    a=[(0,0),(4,0),(4,4),(0,4)]
    b=[(1,-1),(3,-1),(3,5),(1,5)]
    result=sweep_split_segments([[a],[b]])
    fragments=[f for f in result["split_segments"] if f.source==0 and f.index==0]
    assert len(fragments)==3
    assert all(isinstance(f.t0,Fraction) and isinstance(f.t1,Fraction)
               for f in fragments)


def test_side_probes_do_not_jump_across_faces_narrower_than_epsilon():
    # The clip is a 1e-12-wide rectangle: much narrower than the default
    # 1e-10 epsilon. Exact clearance-bounded probes must preserve it.
    subject=[(0,0),(2,0),(2,2),(0,2)]
    clip=[(2,0),(2+1e-12,0),(2+1e-12,2),(2,2)]
    union=boolean_overlay_rings([[subject],[clip]],operation="union")
    intersection=boolean_overlay_rings([[subject],[clip]],operation="intersection")
    difference=boolean_overlay_rings([[subject],[clip]],operation="difference")
    assert union["area"] == pytest.approx(4.0+2e-12,abs=1e-14)
    assert len(union["rings"]) == 1
    assert intersection["area"] == pytest.approx(0.0,abs=1e-14)
    assert difference["area"] == pytest.approx(4.0,abs=1e-14)


def test_sweep_retains_exact_rational_intersection_nodes():
    from fractions import Fraction
    a=[(0,0),(3,0),(3,3),(0,3)]
    b=[(1,-1),(2,-1),(2,4),(1,4)]
    result=sweep_split_segments([[a],[b]])
    nodes=[
        point for fragment in result["split_segments"]
        for point in (fragment.a,fragment.b)
        if point[0] in (Fraction(1),Fraction(2))
    ]
    assert nodes
    assert all(isinstance(value,Fraction) for point in nodes for value in point)
    assert (Fraction(1),Fraction(0)) in nodes
    assert (Fraction(2),Fraction(0)) in nodes


def test_overlay_preserves_large_integer_coordinate_precision():
    from fractions import Fraction
    base=10**18
    a=[(base,base),(base+8,base),(base+8,base+8),(base,base+8)]
    b=[(base+4,base-2),(base+10,base-2),(base+10,base+6),(base+4,base+6)]
    result=boolean_overlay_rings([[a],[b]],operation="intersection")
    assert result["area"] == pytest.approx(24.0)
    assert len(result["rings"]) == 1
    assert all(isinstance(value,Fraction)
               for ring in result["rings"] for point in ring for value in point)


def test_exact_overlap_smaller_than_epsilon_is_not_discarded():
    from fractions import Fraction
    a=[(0,0),(2,0),(2,2),(0,2)]
    b=[(2-1e-12,0),(4,0),(4,2),(2-1e-12,2)]
    result=sweep_split_segments([[a],[b]],epsilon=1e-10)
    assert len(result["intersection_events"]) == 0
    shared_bottom=[
        f for f in result["split_segments"]
        if f.source==0 and f.index==0
    ]
    assert len(shared_bottom)==2
    assert shared_bottom[0].b[0] == Fraction(str(2-1e-12))
    assert shared_bottom[1].b[0] == Fraction(2)


def test_near_miss_smaller_than_epsilon_is_not_a_false_intersection():
    a=[(0,0),(2,0),(2,2),(0,2)]
    b=[(2+1e-12,0),(4,0),(4,2),(2+1e-12,2)]
    result=sweep_split_segments([[a],[b]],epsilon=1e-10)
    assert result["intersection_events"] == ()
    assert len(result["split_segments"]) == 8
    overlay=boolean_overlay_rings([[a],[b]],operation="union",epsilon=1e-10)
    assert overlay["area"] == pytest.approx(8.0 - 2e-12,abs=1e-14)
    assert len(overlay["rings"]) == 2


def test_collinear_bundle_endpoints_are_coalesced_into_node_events():
    a=[(0,0),(2,0),(2,2),(0,2)]
    b=[(1,0),(3,0),(3,2),(1,2)]
    result=sweep_split_segments([[a],[b]])
    contacts=[event for event in result["node_events"] if event.kind=="contact"]
    assert len(contacts)==4
    assert all(len(event.segment_ids)==3 for event in contacts)


def test_contour_face_walk_uses_exact_polar_order_for_nearly_collinear_rays():
    from fractions import Fraction
    from martinez_sweep import _polar_compare
    almost_horizontal=(Fraction(1),Fraction(1,10**40))
    horizontal=(Fraction(1),Fraction(0))
    assert _polar_compare(horizontal,almost_horizontal) < 0
    assert _polar_compare(almost_horizontal,horizontal) > 0



def test_multiway_endpoint_touch_groups_all_four_incident_edges():
    # Two triangles meet at one vertex. Four edge-pair contacts must become
    # one exact node event containing all four incident edge identifiers.
    left=[(0,0),(-2,-1),(-2,1)]
    right=[(0,0),(2,-1),(2,1)]
    result=sweep_split_segments([[left],[right]])
    node=next(event for event in result["node_events"]
              if event.point==(0,0))
    assert node.kind=="contact"
    assert len(node.segment_ids)==4
    assert len(set(node.segment_ids))==4


def test_three_way_proper_crossing_is_one_exact_node_event():
    # One boundary edge from each of three valid polygons passes through the
    # origin. Pairwise reports must be coalesced into one 3-edge event.
    horizontal=[(-1,0),(1,0),(0,-2)]
    rising=[(-1,-1),(1,1),(2,-1)]
    falling=[(-1,1),(1,-1),(-2,-1)]
    result=sweep_split_segments([[horizontal],[rising],[falling]])
    node=next(event for event in result["node_events"]
              if event.point==(0,0))
    assert node.kind=="intersection"
    assert len(node.segment_ids)==3
    assert len(set(node.segment_ids))==3
    # Every participating edge is split at the exact shared coordinate.
    for sid in node.segment_ids:
        fragments=[f for f in result["split_segments"]
                   if result["segments"][sid].source==f.source
                   and result["segments"][sid].ring==f.ring
                   and result["segments"][sid].index==f.index]
        assert any(f.a==(0,0) or f.b==(0,0) for f in fragments)

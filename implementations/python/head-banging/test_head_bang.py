import pytest
from head_bang import head_bang, _weighted_median

def test_weighted_median_even_split_uses_midpoint():
    assert _weighted_median([1,9],[1,1])==pytest.approx(5)

def test_low_and_high_spikes_are_clipped_to_screens():
    pts=[(0,0),(-1,0),(1,0)]
    low=head_bang(pts,[1,2,9],n_neighbors=2,max_triples=1,max_deviation_degrees=0)
    high=head_bang(pts,[10,2,9],n_neighbors=2,max_triples=1,max_deviation_degrees=0)
    assert low["smoothed_values"]==pytest.approx([2,2,9])
    assert high["smoothed_values"]==pytest.approx([9,2,9])
    assert low["triples"][0]==[(1,2)]

def test_value_between_screens_is_preserved():
    r=head_bang([(0,0),(-1,0),(1,0)],[5,2,9],n_neighbors=2,max_triples=1,max_deviation_degrees=0)
    assert r["smoothed_values"]==pytest.approx([5,2,9])

def test_weighted_target_can_resist_adjustment():
    r=head_bang([(0,0),(-1,0),(1,0)],[1,2,9],[10,1,1],n_neighbors=2,max_triples=1,max_deviation_degrees=0)
    assert r["smoothed_values"][0]==pytest.approx(1)

def test_weighted_endpoints_can_override_target():
    r=head_bang([(0,0),(-1,0),(1,0)],[1,2,9],[1,10,10],n_neighbors=2,max_triples=1,max_deviation_degrees=0)
    assert r["smoothed_values"][0]==pytest.approx(2)

def test_no_qualifying_triples_leave_values_unchanged():
    r=head_bang([(0,0),(1,0),(0,1)],[100,1,2],n_neighbors=2,max_deviation_degrees=0)
    assert r["smoothed_values"]==[100,1,2]
    assert all(not t for t in r["triples"])

def test_max_triples_caps_pairs_and_ties_are_deterministic():
    pts=[(0,0),(-1,0),(1,0),(-2,0),(2,0)]
    a=head_bang(pts,[10,1,9,2,8],n_neighbors=4,max_triples=1,max_deviation_degrees=0)
    b=head_bang(pts,[10,1,9,2,8],n_neighbors=4,max_triples=1,max_deviation_degrees=0)
    assert len(a["triples"][0])==1
    assert a==b

def test_convergence_metadata_is_returned():
    r=head_bang([(0,0),(-1,0),(1,0)],[1,2,9],n_neighbors=2,max_triples=1,max_deviation_degrees=0)
    assert r["iterations"]>=1 and r["converged"]

@pytest.mark.parametrize("args",[
    ([],[],None), ([(0,0)],[],None), ([(0,0),(1,1)],[1],[1]),
    ([(0,0),(0,0)],[1,2],None), ([(0,float("nan"))],[1],None),
    ([(0,0),(1,1)],[1,float("inf")],None), ([(0,0),(1,1)],[1,2],[1,0])
])
def test_invalid_inputs_rejected(args):
    with pytest.raises(ValueError): head_bang(args[0],args[1],args[2])

def test_invalid_parameters_rejected():
    pts=[(0,0),(-1,0),(1,0)];values=[1,2,9]
    with pytest.raises(ValueError):head_bang(pts,values,n_neighbors=1)
    with pytest.raises(ValueError):head_bang(pts,values,max_triples=0)
    with pytest.raises(ValueError):head_bang(pts,values,max_deviation_degrees=91)
    with pytest.raises(ValueError):head_bang(pts,values,max_iterations=0)
    with pytest.raises(ValueError):head_bang(pts,values,tolerance=-1)


def test_two_point_pattern_has_no_triples_and_is_unchanged():
    result = head_bang([(0, 0), (1, 1)], [4, 9])
    assert result["smoothed_values"] == [4.0, 9.0]
    assert result["neighbors"] == [[1], [0]]
    assert result["converged"]


def test_iteration_limit_reports_nonconvergence_when_value_still_changes():
    result = head_bang(
        [(0, 0), (-1, 0), (1, 0)], [1, 2, 9],
        n_neighbors=2, max_triples=1, max_deviation_degrees=0,
        max_iterations=1,
    )
    assert result["smoothed_values"][0] == pytest.approx(2)
    assert not result["converged"]

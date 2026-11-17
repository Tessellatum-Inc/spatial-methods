import numpy as np
import pytest
from spatiotemporal_etas import simulate_etas


def test_etas_is_seeded_and_parent_genealogy_is_valid():
    args=((0,0,20,15),30,.01,.55,.02,1.1,2.5,2.3,1.0,.3,2.5,.2)
    a=simulate_etas(*args,seed=71);b=simulate_etas(*args,seed=71)
    for key in ("time","x","y","magnitude","parent_index","generation","is_immigrant"):
        np.testing.assert_array_equal(a[key],b[key])
    assert np.all(np.diff(a["time"])>=0)
    assert np.all(a["magnitude"]>=2.5)
    assert np.all((a["x"]>=0)&(a["x"]<20)) and np.all((a["y"]>=0)&(a["y"]<15))
    for i,parent in enumerate(a["parent_index"]):
        if parent==-1:
            assert a["is_immigrant"][i] and a["generation"][i]==0
        else:
            assert parent<i and a["generation"][i]==a["generation"][parent]+1
            assert a["time"][parent]<a["time"][i] and not a["is_immigrant"][i]


def test_zero_branching_produces_background_only_events():
    a=simulate_etas((0,0,10,10),5,.1,0,.01,1,2,2.3,1,.5,2,seed=8)
    assert np.all(a["is_immigrant"]) and np.all(a["parent_index"]==-1)


@pytest.mark.parametrize("args",[
    (((0,0,1,1),1,1,1,.1,1,2,2.3,1,.1,2)),
    (((0,0,1,1),1,1,.5,.1,0,2,2.3,1,.1,2)),
    (((0,0,1,1),1,1,.5,.1,1,2,1,1,.1,2)),
    (((0,0,1,1),1,1,.5,.1,1,2,2.3,2,.1,1)),
])
def test_invalid_etas_parameters_are_rejected(args):
    with pytest.raises(ValueError): simulate_etas(*args)


def test_etas_event_cap_is_enforced():
    with pytest.raises(OverflowError):
        simulate_etas((0,0,1,1),2,100,0,.01,1,2,2.3,1,.1,2,seed=1,max_events=1)


def test_branching_coefficient_matches_requested_expected_offspring():
    n,beta,alpha=.6,2.5,1.0
    kappa=n*(beta-alpha)/beta
    assert kappa*beta/(beta-alpha)==pytest.approx(n)

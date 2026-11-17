import numpy as np
import pytest
from space_time_k import space_time_k_function

def test_two_event_k_matches_hand_computed_translation_weight():
    out=space_time_k_function([[1,1],[3,4]],[2,4],[4],[2],window=(0,0,10,10),time_window=(0,10))
    expected=2*100*10/(2*1)/(0.56*0.8)
    assert out["K"][0,0]==pytest.approx(expected)

def test_k_is_monotone_in_radius_and_absolute_time_lag():
    out=space_time_k_function([[1,1],[2,1],[8,8],[8,7]],[1,2,8,9],[0,2,10],[0,2,10],window=(0,0,10,10),time_window=(0,10))
    assert np.all(np.diff(out["K"],axis=0)>=-1e-12)
    assert np.all(np.diff(out["K"],axis=1)>=-1e-12)

def test_k_is_invariant_to_event_order():
    p=np.array([[1,1],[2,1],[8,8],[8,7]],float);t=np.array([1,2,8,9],float)
    a=space_time_k_function(p,t,[2,5],[1,5],window=(0,0,10,10),time_window=(0,10))
    ix=[2,0,3,1];b=space_time_k_function(p[ix],t[ix],[2,5],[1,5],window=(0,0,10,10),time_window=(0,10))
    np.testing.assert_allclose(a["K"],b["K"])

@pytest.mark.parametrize("p,t,r,tau,w,tw",[
    ([[0,0]],[0],[1],[1],(0,0,1,1),(0,1)),
    ([[0,0],[1,1]],[0],[1],[1],(0,0,1,1),(0,1)),
    ([[0,0],[1,1]],[0,2],[1],[1],(0,0,1,1),(0,1)),
    ([[0,0],[1,1]],[0,1],[-1],[1],(0,0,1,1),(0,1)),
    ([[0,0],[1,1]],[0,1],[1],[-1],(0,0,1,1),(0,1)),
])
def test_invalid_inputs(p,t,r,tau,w,tw):
    with pytest.raises(ValueError):space_time_k_function(p,t,r,tau,window=w,time_window=tw)

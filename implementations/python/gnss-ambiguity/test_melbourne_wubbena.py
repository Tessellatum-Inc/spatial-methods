import numpy as np
import pytest
from combinations import melbourne_wubbena
from melbourne_wubbena import detect_melbourne_wubbena_slips

F1,F2=1575.42e6,1227.60e6

def test_mw_combination_uses_cycles_and_weighted_code_ranges():
    l1=[100.,101.];l2=[80.,80.]
    p1=[2.1e7,2.1e7];p2=[2.1e7,2.1e7]
    out=melbourne_wubbena(l1,l2,p1,p2,F1,F2)
    assert out[1]-out[0]==pytest.approx(1.0)
    assert out[0]==pytest.approx((l1[0]-l2[0])-((F1-F2)/299792458.0)*2.1e7)

def test_mw_validation():
    with pytest.raises(ValueError): melbourne_wubbena([1],[2,3],[4],[5],F1,F2)
    with pytest.raises(ValueError): melbourne_wubbena([np.nan],[2],[4],[5],F1,F2)
    with pytest.raises(ValueError): melbourne_wubbena([1],[2],[4],[5],F1,F1)

def test_mw_detector_flags_step_and_starts_new_arc():
    y=np.r_[np.zeros(12),np.ones(1),np.ones(12)]
    r=detect_melbourne_wubbena_slips(y,initial_sigma=.1,sigma_multiplier=4)
    assert r["flags"][12]
    assert not np.any(r["flags"][13:])

def test_mw_detector_gap_reset_and_irregular_epochs():
    t=np.r_[np.arange(6.),np.arange(100.,106.)]
    y=np.r_[np.zeros(6),np.ones(6)]
    r=detect_melbourne_wubbena_slips(y,epochs=t,max_gap=10,initial_sigma=.1)
    assert r["gap_resets"][6]
    assert not r["flags"][6]
    assert not np.any(r["flags"][7:])

def test_mw_detector_rejects_bad_inputs():
    with pytest.raises(ValueError): detect_melbourne_wubbena_slips([1])
    with pytest.raises(ValueError): detect_melbourne_wubbena_slips([1,2],sigma_multiplier=0)
    with pytest.raises(ValueError): detect_melbourne_wubbena_slips([1,2],epochs=[0,0])

import numpy as np
import pytest
from cycle_slips import detect_geometry_free_slips

def test_quadratic_trend_and_single_jump():
    t=np.arange(30,dtype=float)
    y=0.002*t*t+0.01*t
    y[18:]+=0.35
    r=detect_geometry_free_slips(y,epochs=t,window=7,threshold=0.08)
    assert r["flags"][18]
    assert not np.any(r["flags"][:18])
    assert not np.any(r["flags"][19:])

def test_irregular_epochs():
    t=np.cumsum(np.r_[0.,np.linspace(0.8,1.2,19)])
    y=0.01*t*t
    y[12:]+=0.5
    r=detect_geometry_free_slips(y,t,window=6,threshold=0.1)
    assert r["flags"][12]

def test_gap_resets_history():
    t=np.r_[np.arange(10.),np.arange(100.,110.)]
    y=np.r_[np.arange(10.)*.01,np.arange(10.)*.01]
    r=detect_geometry_free_slips(y,t,window=4,threshold=.1,max_gap=5)
    assert not np.any(r["flags"][10:])
    assert np.all(np.isnan(r["residuals"][10:14]))

def test_invalid_inputs():
    with pytest.raises(ValueError): detect_geometry_free_slips([1,2,3])
    with pytest.raises(ValueError): detect_geometry_free_slips(np.arange(8.),window=2)
    with pytest.raises(ValueError): detect_geometry_free_slips(np.arange(8.),epochs=[0,1,2,3,4,5,6,5])
    with pytest.raises(ValueError): detect_geometry_free_slips(np.arange(8.),threshold=0)

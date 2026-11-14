import numpy as np
import pytest
from beta_convergence import beta_convergence


def test_beta_convergence_recovers_negative_slope_and_speed():
    rng=np.random.default_rng(5); y0=np.exp(np.linspace(1,3,40))
    growth=.08-.18*np.log(y0)+rng.normal(0,.004,size=40)
    y1=y0*np.exp(growth*5)
    r=beta_convergence(y0,y1,periods=5)
    assert r["beta"]==pytest.approx(-.18,abs=.02)
    assert r["convergence_speed_per_period"]==pytest.approx(-np.log1p(r["beta"])/5)
    assert r["half_life_periods"]>0
    assert r["specification"]=="absolute"
    assert np.all(np.isfinite(r["hc1_standard_errors"]))


def test_conditional_convergence_accepts_controls():
    rng=np.random.default_rng(6); y0=np.exp(np.linspace(1,3,30))
    z=rng.normal(size=30)
    growth=.1-.12*np.log(y0)+.04*z+rng.normal(0,.003,size=30)
    y1=y0*np.exp(growth*3)
    r=beta_convergence(y0,y1,periods=3,controls=z)
    assert r["specification"]=="conditional"
    assert r["coefficients"].shape==(3,)
    assert r["n_parameters"]==3


@pytest.mark.parametrize("y0,y1,T,C",[
    ([1,2,3],[1,2,3],1,None),
    ([1,2,3,4],[1,2,3,4],0,None),
    ([1,2,3,4],[1,2,3,4],1,np.ones((4,3))),
    ([1,2,3,4],[1,2,3,4],1,np.array([1,2])),
    ([1,2,3,4],[1,2,0,4],1,None),
])
def test_beta_convergence_rejects_invalid_data(y0,y1,T,C):
    with pytest.raises(ValueError): beta_convergence(y0,y1,T,C)


def test_nonconvergent_slope_has_no_speed_or_half_life():
    y0=np.exp(np.arange(8.)); y1=y0*np.exp(.01+.05*np.log(y0))
    r=beta_convergence(y0,y1)
    assert r["beta"]>0
    assert r["convergence_speed_per_period"] is None
    assert r["half_life_periods"] is None

import numpy as np
import pytest
from fay_herriot import fay_herriot

def test_fay_herriot_returns_finite_empirical_bayes_estimates():
    rng=np.random.default_rng(12); n=80
    x0=np.linspace(-2,2,n); x=np.column_stack([np.ones(n),x0])
    d=np.full(n,.25); truth=3+1.7*x0+rng.normal(0,.8,n)
    direct=truth+rng.normal(0,np.sqrt(d))
    r=fay_herriot(direct,d,x)
    assert np.isfinite(r["estimate"]).all()
    assert np.isfinite(r["beta"]).all()
    assert r["between_area_variance"]>=0
    assert np.all((r["shrinkage_factor"]>=0)&(r["shrinkage_factor"]<=1))
    assert np.all(r["conditional_random_effect_variance"]>=0)
    assert r["variance_estimator"]=="REML"

def test_fay_herriot_shrinks_noisy_direct_estimates_toward_regression():
    y=np.array([0.,10.,0.,10.,0.,10.])
    d=np.full(6,100.)
    x=np.ones((6,1))
    r=fay_herriot(y,d,x)
    assert np.allclose(r["estimate"],np.mean(y),atol=1e-5)
    assert np.all(r["shrinkage_factor"]<.1)

def test_fay_herriot_supports_ml_option():
    y=np.array([1.,2.,1.5,3.,2.5,4.])
    d=np.full(6,.2); x=np.column_stack([np.ones(6),np.arange(6.)])
    r=fay_herriot(y,d,x,reml=False)
    assert r["variance_estimator"]=="ML"
    assert r["between_area_variance"]>=0

def test_fay_herriot_rejects_invalid_design_and_variances():
    with pytest.raises(ValueError,match="sampling_variances"):
        fay_herriot([1,2,3],[1,0,1],np.ones((3,1)))
    with pytest.raises(ValueError,match="full column rank"):
        fay_herriot([1,2,3,4],[1,1,1,1],np.ones((4,2)))
    with pytest.raises(ValueError,match="covariates"):
        fay_herriot([1,2,3],[1,1,1],[[1],[np.nan],[1]])

import numpy as np
import pytest
from least_squares_collocation import least_squares_collocation


def setup_case():
    x=np.array([0.,1.,2.,3.])
    d=np.abs(x[:,None]-x[None,:])
    C=np.exp(-d/1.5)
    R=np.eye(4)*.1
    xt=np.array([.5,1.5,2.5])
    dt=np.abs(xt[:,None]-x[None,:])
    C0=np.exp(-dt/1.5)
    C00=np.exp(-np.abs(xt[:,None]-xt[None,:])/1.5)
    return x,C,R,C0,C00


def test_lsc_predicts_constant_trend_and_returns_uncertainty():
    x,C,R,C0,C00=setup_case()
    H=np.ones((4,1)); H0=np.ones((3,1)); y=np.full(4,7.0)
    r=least_squares_collocation(y,H,C,R,C0,C00,H0)
    np.testing.assert_allclose(r["trend_parameters"],[7.0],atol=1e-10)
    np.testing.assert_allclose(r["prediction"],7.0,atol=1e-10)
    assert np.all(r["prediction_standard_deviation"]>=0)
    assert np.min(np.linalg.eigvalsh(r["prediction_covariance"]))>=-1e-10


def test_lsc_interpolates_exactly_at_observed_site_without_noise():
    x,C,_,_,_=setup_case()
    R=np.zeros_like(C)
    H=np.ones((4,1)); y=np.array([1.,2.,1.5,3.])
    # Predict at the second observation: its cross covariance is row 1 of C.
    r=least_squares_collocation(y,H,C,R,C[1:2],C[1:2,1:2],np.ones((1,1)))
    assert r["prediction"][0]==pytest.approx(y[1],abs=1e-9)
    assert r["prediction_covariance"][0,0]==pytest.approx(0,abs=1e-9)


def test_lsc_supports_correlated_observation_noise_and_multiple_trend_terms():
    x,C,R,C0,C00=setup_case()
    R[0,1]=R[1,0]=.02
    H=np.column_stack([np.ones(4),x])
    H0=np.column_stack([np.ones(3),[.5,1.5,2.5]])
    y=2+0.5*x+np.array([.1,-.1,.05,0])
    r=least_squares_collocation(y,H,C,R,C0,C00,H0)
    assert r["trend_parameters"].shape==(2,)
    assert r["prediction"].shape==(3,)


def test_lsc_rejects_inconsistent_dimensions_and_singular_models():
    x,C,R,C0,C00=setup_case()
    with pytest.raises(ValueError): least_squares_collocation([1,2],np.ones((4,1)),C,R,C0,C00)
    with pytest.raises(ValueError): least_squares_collocation(np.ones(4),np.ones((4,1)),C,R,C0[:,:2],C00)
    with pytest.raises(ValueError): least_squares_collocation(np.ones(4),np.column_stack([np.ones(4),np.ones(4)]),C,R,C0,C00)
    with pytest.raises(ValueError): least_squares_collocation(np.ones(4),np.ones((4,1)),C,-C,C0,C00)

import numpy as np
import pytest
from mnf_transform import mnf_transform, estimate_noise_covariance

def test_supplied_noise_covariance_and_ordering():
    rng=np.random.default_rng(12)
    latent=rng.normal(size=(20,24,2))
    mixing=np.array([[1.,.2],[.5,1.],[.2,-.4]])
    noise=rng.normal(scale=.08,size=(20,24,3))
    cube=latent@mixing.T+noise
    result=mnf_transform(cube,noise_covariance=np.eye(3)*.01,n_components=2)
    assert result["scores"].shape==(20,24,2)
    assert np.all(np.diff(result["eigenvalues"])<=0)
    assert np.all(np.isfinite(result["loadings"]))

def test_mask_preserves_invalid_as_nan():
    x=np.random.default_rng(2).normal(size=(8,9,3))
    mask=np.ones((8,9),bool); mask[0,0]=False
    out=mnf_transform(x,noise_covariance=np.eye(3),mask=mask)
    assert np.isnan(out["scores"][0,0]).all()
    assert np.isfinite(out["scores"][mask]).all()

def test_difference_noise_estimator():
    rng=np.random.default_rng(3)
    x=np.zeros((30,30,2)); x+=rng.normal(size=x.shape)
    cov=estimate_noise_covariance(x)
    assert cov.shape==(2,2)
    assert np.linalg.eigvalsh(cov).min()>0

def test_reject_indefinite_noise():
    x=np.random.default_rng(1).normal(size=(5,6,2))
    with pytest.raises(ValueError):
        mnf_transform(x,noise_covariance=np.array([[1,2],[2,1]]))

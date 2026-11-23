import math
import numpy as np
import pytest
from approximate_inference import laplace_approximation,slice_sample

def test_laplace_recovers_multivariate_gaussian_mode_covariance_and_evidence():
    precision=np.array([[3.,.5],[.5,2.]])
    mean=np.array([1.,-2.]);constant=-.7
    def logp(x):
        d=x-mean
        return constant-.5*d@precision@d
    result=laplace_approximation(logp,[0.,0.])
    np.testing.assert_allclose(result.mode,mean,atol=1e-5)
    np.testing.assert_allclose(result.covariance,np.linalg.inv(precision),rtol=1e-4,atol=1e-5)
    sign,logdet=np.linalg.slogdet(precision)
    expected=constant+len(mean)/2*math.log(2*math.pi)-.5*logdet
    assert result.log_evidence==pytest.approx(expected,abs=1e-4)

def test_laplace_rejects_non_concave_mode():
    with pytest.raises(ValueError,match="positive definite"):
        laplace_approximation(lambda x: .5*x[0]**2,[0.])

def test_slice_sampler_matches_standard_normal_moments():
    samples=slice_sample(lambda x:-.5*float(x@x),[0.,0.],n_samples=12000,burn_in=1000,width=1.5,seed=5)
    np.testing.assert_allclose(samples.mean(axis=0),[0,0],atol=.08)
    np.testing.assert_allclose(samples.var(axis=0),[1,1],atol=.12)

def test_slice_sampler_is_reproducible_and_validates():
    a=slice_sample(lambda x:-.5*float(x@x),[0.],n_samples=30,burn_in=5,seed=2)
    b=slice_sample(lambda x:-.5*float(x@x),[0.],n_samples=30,burn_in=5,seed=2)
    np.testing.assert_array_equal(a,b)
    with pytest.raises(ValueError): slice_sample(lambda x:0,[0],n_samples=0)
    with pytest.raises(ValueError): laplace_approximation(lambda x:0,[np.nan])

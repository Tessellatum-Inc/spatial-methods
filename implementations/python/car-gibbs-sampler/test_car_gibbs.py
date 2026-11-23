import numpy as np
import pytest
from car_gibbs import car_gibbs

def test_two_node_rho_zero_matches_independent_gaussian_posterior():
    w=np.array([[0.,1.],[1.,0.]])
    samples=car_gibbs(w,[1.,-1.],[1.,1.],rho=0,precision=1,n_samples=30000,burn_in=2000,seed=4)
    np.testing.assert_allclose(samples.mean(axis=0),[.5,-.5],atol=.025)
    np.testing.assert_allclose(samples.var(axis=0),[.5,.5],atol=.03)

def test_proper_car_sampler_is_reproducible_and_handles_missing_data():
    w=np.array([[0.,1.,0.],[1.,0.,1.],[0.,1.,0.]])
    a=car_gibbs(w,[1.,np.nan,0.],[.5,np.nan,.5],rho=.4,precision=2,n_samples=50,burn_in=20,seed=9)
    b=car_gibbs(w,[1.,np.nan,0.],[.5,np.nan,.5],rho=.4,precision=2,n_samples=50,burn_in=20,seed=9)
    np.testing.assert_array_equal(a,b)
    assert a.shape==(50,3) and np.isfinite(a).all()

def test_invalid_graph_and_improper_rho_rejected():
    with pytest.raises(ValueError,match="symmetric"):
        car_gibbs([[0,1],[0,0]],[1,1],[1,1])
    with pytest.raises(ValueError,match="positive degree"):
        car_gibbs([[0,0],[0,0]],[1,1],[1,1])
    with pytest.raises(ValueError,match="positive definite"):
        car_gibbs([[0,1],[1,0]],[1,1],[1,1],rho=2)

def test_invalid_observations_and_sampling_options():
    w=[[0,1],[1,0]]
    with pytest.raises(ValueError,match="variances"):
        car_gibbs(w,[1,2],[1,0])
    with pytest.raises(ValueError,match="n_samples"):
        car_gibbs(w,[1,2],[1,1],n_samples=0)
    with pytest.raises(ValueError,match="initial"):
        car_gibbs(w,[1,2],[1,1],initial=[0])

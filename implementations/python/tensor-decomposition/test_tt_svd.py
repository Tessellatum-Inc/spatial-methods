import numpy as np
import pytest
from tt_svd import tt_svd, tt_reconstruct, tt_complete

def test_tt_svd_exact_reconstruction_when_rank_not_capped():
    rng=np.random.default_rng(2)
    x=rng.normal(size=(3,4,2,3))
    model=tt_svd(x)
    np.testing.assert_allclose(tt_reconstruct(model["cores"]),x,rtol=1e-11,atol=1e-11)
    assert model["ranks"][0]==model["ranks"][-1]==1

def test_tt_svd_rank_one_and_zero_tensor():
    a=np.arange(1.,4);b=np.array([2.,-1.]);c=np.array([1.,3.,4.])
    x=np.einsum("i,j,k->ijk",a,b,c)
    model=tt_svd(x,max_rank=1)
    np.testing.assert_allclose(tt_reconstruct(model["cores"]),x,rtol=1e-10,atol=1e-10)
    zero=tt_svd(np.zeros((2,3,4)),max_rank=1)
    np.testing.assert_allclose(tt_reconstruct(zero["cores"]),0)

def test_tt_rank_cap_bounds_internal_ranks():
    x=np.random.default_rng(4).normal(size=(5,4,3,2))
    m=tt_svd(x,max_rank=2)
    assert max(m["ranks"][1:-1])<=2
    assert m["relative_error"]>0

def test_tt_reconstruction_rejects_bad_cores():
    with pytest.raises(ValueError): tt_reconstruct([np.ones((2,3,1)),np.ones((1,2,1))])
    with pytest.raises(ValueError): tt_reconstruct([np.ones((1,3,2)),np.ones((1,2,1))])

def test_tt_svd_rejects_bad_inputs():
    with pytest.raises(ValueError): tt_svd(np.ones(4))
    with pytest.raises(ValueError): tt_svd(np.ones((2,2)),max_rank=0)
    with pytest.raises(ValueError): tt_svd(np.ones((2,2)),tolerance=-1)

def test_completion_preserves_observations_and_returns_finite_values():
    rng=np.random.default_rng(10)
    x=np.einsum("i,j,k->ijk",rng.uniform(.5,2,4),rng.uniform(.5,2,3),rng.uniform(.5,2,5))
    mask=rng.random(x.shape)>.35
    raw=x.copy(); raw[~mask]=np.nan
    result=tt_complete(raw,mask,max_rank=1,max_iter=30,tolerance=1e-9)
    assert np.all(np.isfinite(result["completed"]))
    np.testing.assert_array_equal(result["completed"][mask],x[mask])
    assert result["observed_rmse"]==0
    assert result["iterations"]<=30

def test_completion_validation():
    with pytest.raises(ValueError): tt_complete(np.ones((2,2)),np.zeros((2,2),bool),1)
    with pytest.raises(ValueError): tt_complete(np.ones((2,2)),np.ones((2,2),bool),1)
    with pytest.raises(ValueError): tt_complete(np.array([[1,np.nan],[2,3]]),np.array([[1,1],[1,0]],bool),1)

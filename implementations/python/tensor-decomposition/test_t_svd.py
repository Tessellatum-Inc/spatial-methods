import numpy as np
import pytest
from t_svd import t_svd, t_svd_reconstruct, t_svd_truncate

def test_full_t_svd_reconstructs_real_tensor():
    x=np.random.default_rng(3).normal(size=(5,4,6))
    factors=t_svd(x)
    got=t_svd_reconstruct(*factors)
    assert np.allclose(got,x,atol=1e-10)

def test_truncated_t_svd_has_expected_shapes_and_no_worse_error_than_zero_fit():
    x=np.random.default_rng(9).normal(size=(8,6,5))
    approx,factors=t_svd_truncate(x,2)
    u,s,vh=factors
    assert u.shape==(8,2,5) and s.shape==(2,2,5) and vh.shape==(2,6,5)
    assert np.linalg.norm(x-approx)<np.linalg.norm(x)

def test_exact_tubal_rank_one_recovery_for_outer_product_tubes():
    a=np.arange(1.,5.)[:,None,None]; b=np.arange(1.,4.)[None,:,None]; c=np.array([1.,2.,-1.,.5])[None,None,:]
    x=a*b*c
    approx,_=t_svd_truncate(x,1)
    assert np.allclose(approx,x,atol=1e-10)

def test_invalid_tensor_and_rank():
    with pytest.raises(ValueError): t_svd(np.ones((3,3)))
    with pytest.raises(ValueError): t_svd(np.ones((3,3,2)),tubal_rank=0)
    with pytest.raises(ValueError): t_svd(np.ones((3,3,2)),tubal_rank=4)

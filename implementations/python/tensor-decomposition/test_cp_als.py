import numpy as np
import pytest
from cp_als import cp_als

def reconstruct(result):
    a,b,c=result["factors"]
    return np.einsum("r,ir,jr,kr->ijk",result["weights"],a,b,c)

def test_rank_one_tensor_reconstruction():
    a=np.array([1.,2.,3.,4.]); b=np.array([2.,-1.,3.]); c=np.array([1.,.5])
    x=np.einsum("i,j,k->ijk",a,b,c)
    r=cp_als(x,1,max_iter=500,tolerance=1e-10,seed=3)
    assert np.linalg.norm(x-reconstruct(r))/np.linalg.norm(x)<1e-5

def test_deterministic_initialization():
    x=np.arange(24,dtype=float).reshape(3,4,2)
    a=cp_als(x,1,seed=9); b=cp_als(x,1,seed=9)
    np.testing.assert_allclose(a["error_history"],b["error_history"])

def test_zero_tensor():
    r=cp_als(np.zeros((2,3,2)),1)
    assert r["error_history"]==[0.0]
    np.testing.assert_allclose(reconstruct(r),0)

@pytest.mark.parametrize("x,rank",[
    (np.ones((3,3)),1),
    (np.ones((2,2,2)),0),
    (np.ones((2,2,2)),True),
    (np.full((2,2,2),np.nan),1),
])
def test_invalid_inputs(x,rank):
    with pytest.raises(ValueError): cp_als(x,rank)

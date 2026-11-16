import numpy as np
from nfindr_endmembers import nfindr

def test_selects_observed_pure_pixel_vertices():
    E=np.array([[1.,0.,0.],[0.,1.,0.],[0.,0.,1.],[.2,.3,.4]])
    A=np.vstack((np.eye(3),np.random.default_rng(3).dirichlet([1,1,1],size=97)))
    cube=(A@E.T).reshape(10,10,4)
    out=nfindr(cube,3,max_iter=5,seed=1)
    assert out["endmembers"].shape==(4,3)
    assert len(set(out["pixel_indices"]))==3
    assert np.all(np.isfinite(out["endmembers"]))

def test_mask_is_respected():
    cube=np.random.default_rng(8).random((8,8,4)); mask=np.ones((8,8),bool); mask[0]=False
    out=nfindr(cube,3,mask=mask)
    assert np.all(out["pixel_indices"]>=8)

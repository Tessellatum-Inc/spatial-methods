import numpy as np
import pytest
from graph_fused_lasso import graph_fused_lasso

def test_graph_fused_lasso_returns_location_coefficients_and_converges():
    rng=np.random.default_rng(2)
    loc=np.repeat(np.arange(3),80)
    x=rng.normal(size=(len(loc),1))
    true=np.array([1.0,1.1,1.0])
    y=true[loc]*x[:,0]+rng.normal(scale=.05,size=len(loc))
    r=graph_fused_lasso(x,y,loc,3,[(0,1),(1,2)],lambda_l1=0,
                        lambda_fused=2,rho=1,max_iter=4000)
    assert r["coefficients"].shape==(3,1)
    assert r["converged"]
    assert np.ptp(r["coefficients"][:,0])<.15

def test_l1_penalty_shrinks_coefficients():
    rng=np.random.default_rng(3)
    loc=np.zeros(100,dtype=int); x=rng.normal(size=(100,1)); y=2*x[:,0]
    fit=graph_fused_lasso(x,y,loc,1,[],lambda_l1=5,lambda_fused=0)
    assert abs(fit["coefficients"][0,0])<2

def test_graph_fused_lasso_accepts_no_edges_and_validates():
    x=np.ones((4,1)); y=np.arange(4.); loc=np.zeros(4,dtype=int)
    r=graph_fused_lasso(x,y,loc,1,[])
    assert r["coefficients"].shape==(1,1)
    with pytest.raises(ValueError): graph_fused_lasso(x,y,loc,1,[(0,0)])
    with pytest.raises(ValueError): graph_fused_lasso(x,y,loc,1,[(0,1),(1,0)])
    with pytest.raises(ValueError): graph_fused_lasso(x,y,loc,0,[])

def test_disconnected_graph_does_not_fuse_components():
    rng=np.random.default_rng(5)
    loc=np.repeat([0,1],100); x=np.ones((200,1))
    y=np.r_[np.full(100,1.),np.full(100,3.)]+rng.normal(0,.02,200)
    r=graph_fused_lasso(x,y,loc,2,[],lambda_fused=10,lambda_l1=0)
    assert r["coefficients"][1,0]-r["coefficients"][0,0]>1.5

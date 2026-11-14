import numpy as np
import pytest
from lloyd import lloyd_cvt

def test_two_cluster_centroids():
    x=np.array([[0.,0.],[0.,2.],[10.,0.],[10.,2.]])
    z=np.array([[1.,1.],[9.,1.]])
    r=lloyd_cvt(x,z)
    np.testing.assert_allclose(r["centers"],[[0.,1.],[10.,1.]])
    assert r["objective"]==pytest.approx(4.0)
    assert r["assignments"].tolist()==[0,0,1,1]

def test_weighted_centroid_moves_to_weighted_mean():
    x=np.array([[0.],[10.],[20.]])
    r=lloyd_cvt(x,np.array([[1.]]),weights=np.array([1.,2.,1.]))
    np.testing.assert_allclose(r["centers"],[[10.]])
    assert r["objective"]==pytest.approx(200.0)

def test_deterministic_and_empty_seed_retained():
    x=np.array([[0.],[1.],[2.]])
    z=np.array([[0.],[100.]])
    a=lloyd_cvt(x,z); b=lloyd_cvt(x,z)
    np.testing.assert_allclose(a["centers"],b["centers"])
    assert np.all(np.isfinite(a["centers"]))

@pytest.mark.parametrize("args",[
    (np.array([1.,2.]),np.array([[1.]])),
    (np.array([[np.nan]]),np.array([[1.]])),
    (np.array([[1.]]),np.array([[np.inf]])),
])
def test_invalid_coordinates(args):
    with pytest.raises(ValueError): lloyd_cvt(*args)

def test_invalid_weights_and_controls():
    x=np.array([[0.],[1.]])
    z=np.array([[0.]])
    with pytest.raises(ValueError): lloyd_cvt(x,z,weights=[0,0])
    with pytest.raises(ValueError): lloyd_cvt(x,z,weights=[1,-1])
    with pytest.raises(ValueError): lloyd_cvt(x,z,max_iter=0)

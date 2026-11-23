import numpy as np
from vca_endmembers import vca

def test_reproducible_and_returns_scene_spectra():
    rng=np.random.default_rng(5)
    E=np.array([[1.,.1,.2],[.1,1.,.2],[.2,.1,1.],[.3,.4,.2]])
    A=rng.dirichlet([2,2,2],size=300)
    cube=(A@E.T).reshape(15,20,4)
    a=vca(cube,3,seed=17); b=vca(cube,3,seed=17)
    assert np.array_equal(a["pixel_indices"],b["pixel_indices"])
    assert np.allclose(a["endmembers"],b["endmembers"])
    assert np.all(np.isfinite(a["endmembers"]))
    assert np.all(a["pixel_indices"]<cube.shape[0]*cube.shape[1])

def test_masked_pixels_not_selected():
    x=np.random.default_rng(4).random((8,9,4))
    mask=np.ones((8,9),bool); mask[0,:]=False
    out=vca(x,3,mask=mask)
    assert np.all(out["pixel_indices"]>=9)

def test_one_endmember():
    x=np.random.default_rng(2).random((5,6,3))
    assert vca(x,1)["endmembers"].shape==(3,1)

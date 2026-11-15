import numpy as np
from fcls_unmixing import fcls_unmix

def test_recovers_noise_free_mixtures():
    E=np.array([[1.,.1,.2],[.1,1.,.2],[.2,.1,1.],[.3,.4,.2]])
    rng=np.random.default_rng(10)
    A=rng.dirichlet([2,2,2],size=30)
    cube=(A@E.T).reshape(5,6,4)
    out=fcls_unmix(cube,E)
    assert np.all(out["success"])
    assert np.all(out["abundances"]>=-1e-10)
    assert np.allclose(out["abundances"].sum(axis=-1),1,atol=1e-7)
    assert np.allclose(out["abundances"].reshape(-1,3),A,atol=1e-4)

def test_single_endmember():
    cube=np.ones((2,3,4))
    out=fcls_unmix(cube,np.ones((4,1)))
    assert np.allclose(out["abundances"],1)
    assert np.all(out["success"])

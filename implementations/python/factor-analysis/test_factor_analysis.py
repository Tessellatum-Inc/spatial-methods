import numpy as np
import pytest
from factor_analysis import principal_axis_factor_analysis

def synthetic(seed=42, n=2500):
    rng=np.random.default_rng(seed)
    structure=np.array([[.90,0],[.80,0],[.70,0],[0,.90],[0,.80],[0,.70]])
    latent=rng.normal(size=(n,2))
    noise=rng.normal(size=(n,6))*np.sqrt(1-np.sum(structure**2,axis=1))
    return latent@structure.T+noise

def test_recovers_simple_two_factor_structure():
    r=principal_axis_factor_analysis(synthetic(),2)
    assert r.loadings.shape==(6,2)
    assert r.converged and r.rotation_converged
    assert np.all(np.max(np.abs(r.loadings),axis=1)>.60)
    assert np.all(np.min(np.abs(r.loadings),axis=1)<.15)
    assert r.communalities==pytest.approx(np.sum(r.loadings**2,axis=1))
    assert np.all((r.uniquenesses>=0)&(r.uniquenesses<=1))

def test_varimax_is_orthogonal_and_preserves_communalities():
    x=synthetic(seed=7,n=1200)
    a=principal_axis_factor_analysis(x,2,rotation="varimax")
    b=principal_axis_factor_analysis(x,2,rotation="none")
    assert a.rotation_matrix.T@a.rotation_matrix==pytest.approx(np.eye(2),abs=1e-8)
    assert np.sum(a.loadings**2,axis=1)==pytest.approx(np.sum(b.loadings**2,axis=1),abs=1e-7)

def test_standardization_is_invariant_to_units_and_offsets():
    x=synthetic(seed=12,n=1000)
    a=principal_axis_factor_analysis(x,2)
    y=x*np.array([10,.1,3,100,2,.5])+np.array([4,-3,10,0,8,1])
    b=principal_axis_factor_analysis(y,2)
    assert b.correlation==pytest.approx(a.correlation,abs=1e-10)
    assert np.abs(b.loadings)==pytest.approx(np.abs(a.loadings),abs=1e-7)

def test_deterministic():
    x=synthetic(seed=21,n=500)
    a=principal_axis_factor_analysis(x,2); b=principal_axis_factor_analysis(x,2)
    assert a.loadings==pytest.approx(b.loadings)
    assert a.communalities==pytest.approx(b.communalities)

@pytest.mark.parametrize("bad", [np.ones((10,3)), np.array([[1.,2.],[2.,3.]]),
    np.array([[1.,2.],[2.,3.],[3.,np.nan]]), np.ones((5,2))])
def test_invalid_or_degenerate_data_rejected(bad):
    with pytest.raises(ValueError): principal_axis_factor_analysis(bad,1)

def test_invalid_controls_rejected():
    x=synthetic(n=100)
    for k in (0,6,1.5,True):
        with pytest.raises(ValueError): principal_axis_factor_analysis(x,k)
    with pytest.raises(ValueError): principal_axis_factor_analysis(x,2,rotation="promax")
    with pytest.raises(ValueError): principal_axis_factor_analysis(x,2,max_iter=0)
    with pytest.raises(ValueError): principal_axis_factor_analysis(x,2,tolerance=0)

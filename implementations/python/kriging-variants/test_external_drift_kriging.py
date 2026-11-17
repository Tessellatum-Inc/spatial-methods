import numpy as np
import pytest
from external_drift_kriging import external_drift_kriging_predict


def test_external_drift_reproduces_a_supplied_covariate_trend():
    points=np.array([(x,y) for x in range(5) for y in range(4)],dtype=float)
    targets=np.array([[.5,.5],[2.2,1.7],[4.,3.]])
    def covariates(xy):
        return np.column_stack((xy[:,0]**2+.3*xy[:,1],np.sin(xy[:,1])))
    ext,ext_target=covariates(points),covariates(targets)
    values=4+2.5*ext[:,0]-1.2*ext[:,1]
    expected=4+2.5*ext_target[:,0]-1.2*ext_target[:,1]
    result=external_drift_kriging_predict(points,values,targets,ext,ext_target)
    np.testing.assert_allclose(result["prediction"],expected,atol=1e-8)
    np.testing.assert_allclose(result["weights"].sum(axis=1),1.,atol=1e-9)
    assert np.all(result["variance"]>=0)


def test_external_drift_matches_independent_augmented_system():
    points=np.array([(0,0),(1,0),(0,1),(1,1),(2,0),(2,1)],float)
    target=np.array([[.4,.7]])
    ext=np.column_stack((points[:,0]**2,points[:,1]))
    ext_target=np.column_stack((target[:,0]**2,target[:,1]))
    values=1+2*ext[:,0]-3*ext[:,1]+np.array([.1,-.2,.2,.05,-.1,.15])
    result=external_drift_kriging_predict(points,values,target,ext,ext_target,
        model="gaussian",partial_sill=1.2,range_=2,nugget=.05)
    d=np.linalg.norm(points[:,None]-points[None,:],axis=2)
    c=1.2*np.exp(-3*(d/2)**2);c.flat[::len(points)+1]+=.05
    cross=1.2*np.exp(-3*(np.linalg.norm(points-target[0],axis=1)/2)**2)
    p=np.column_stack((np.ones(len(points)),ext))
    pt=np.r_[1.,ext_target[0]]
    system=np.block([[c,p],[p.T,np.zeros((p.shape[1],p.shape[1]))]])
    oracle=np.linalg.solve(system,np.r_[cross,pt])
    assert result["prediction"][0]==pytest.approx(oracle[:len(points)]@values)
    assert result["variance"][0]==pytest.approx(1.2-oracle[:len(points)]@cross-oracle[len(points):]@pt)


def test_external_drift_rejects_rank_deficiency_and_bad_shapes():
    points=np.array([(x,y) for x in range(3) for y in range(3)],float)
    target=np.array([[.5,.5]])
    with pytest.raises(ValueError,match="rank deficient"):
        external_drift_kriging_predict(points,np.arange(9.),target,np.ones((9,1)),np.ones((1,1)))
    with pytest.raises(ValueError,match="shape"):
        external_drift_kriging_predict(points,np.arange(9.),target,np.ones((9,2)),np.ones((1,1)))

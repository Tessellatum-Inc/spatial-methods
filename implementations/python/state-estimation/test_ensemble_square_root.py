import numpy as np
import pytest
from ensemble_square_root import etkf_analysis


def test_etkf_matches_kalman_mean_and_covariance():
    rng=np.random.default_rng(10)
    E=rng.normal(size=(3,80))
    H=np.array([[1.,0.,1.],[0.,1.,-1.]])
    R=np.array([[.4,.1],[.1,.7]])
    y=np.array([.8,-.4])
    out=etkf_analysis(E,y,H,R)
    Pf=np.cov(E,bias=False)
    K=Pf@H.T@np.linalg.inv(H@Pf@H.T+R)
    expected_mean=E.mean(axis=1)+K@(y-H@E.mean(axis=1))
    expected_cov=Pf-K@H@Pf
    np.testing.assert_allclose(out["analysis_mean"],expected_mean,atol=1e-10)
    np.testing.assert_allclose(out["analysis_covariance"],expected_cov,atol=1e-10)
    np.testing.assert_allclose(out["analysis_ensemble"].mean(axis=1),expected_mean,atol=1e-10)


def test_etkf_is_deterministic_and_does_not_perturb_observations():
    rng=np.random.default_rng(2); E=rng.normal(size=(4,20))
    H=np.eye(4); R=np.eye(4)*.2; y=np.arange(4.)
    a=etkf_analysis(E,y,H,R); b=etkf_analysis(E,y,H,R)
    np.testing.assert_array_equal(a["analysis_ensemble"],b["analysis_ensemble"])
    np.testing.assert_allclose(a["analysis_anomalies"].mean(axis=1),0,atol=1e-12)


def test_more_informative_observations_do_not_increase_covariance():
    rng=np.random.default_rng(7); E=rng.normal(size=(3,60))
    H=np.eye(3); y=np.zeros(3)
    prior=np.linalg.eigvalsh(np.cov(E))
    post=np.linalg.eigvalsh(etkf_analysis(E,y,H,np.eye(3)*.1)["analysis_covariance"])
    assert np.all(post<=prior+1e-10)


@pytest.mark.parametrize("E,y,H,R",[
    (np.ones((2,2)),[1],[[1,0]],[[1]]),
    (np.ones((2,3)),[1,2],[[1,0]],np.eye(2)),
    (np.ones((2,3)),[1],[[1,0]],[[0]]),
    (np.ones((2,3)),[1],[[1,0]],[[1,2],[2,1]]),
])
def test_etkf_rejects_invalid_inputs(E,y,H,R):
    with pytest.raises(ValueError): etkf_analysis(E,y,H,R)

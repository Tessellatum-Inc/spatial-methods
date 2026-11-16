import numpy as np
import pytest
from nonlinear_filters import ekf_step, ekf_filter, ukf_step, ukf_filter


def test_ekf_matches_linear_kalman_update():
    F = np.array([[1.0, 1.0], [0.0, 1.0]])
    H = np.array([[1.0, 0.0]])
    f = lambda x: F @ x
    h = lambda x: H @ x
    x0 = np.array([0.0, 1.0])
    P0 = np.eye(2)
    Q = np.diag([0.01, 0.02])
    R = np.array([[0.2]])
    x, P, info = ekf_step(x0, P0, np.array([1.1]), f, h,
                           lambda _: F, lambda _: H, Q, R)
    xp = F @ x0
    Pp = F @ P0 @ F.T + Q
    K = Pp @ H.T @ np.linalg.inv(H @ Pp @ H.T + R)
    np.testing.assert_allclose(x, xp + K @ (1.1 - H @ xp))
    np.testing.assert_allclose(P, (np.eye(2)-K@H)@Pp@(np.eye(2)-K@H).T+K@R@K.T)
    assert np.all(np.linalg.eigvalsh(P) > 0)
    assert info["innovation"].shape == (1,)


def test_ukf_matches_linear_kalman_mean_and_covariance():
    F = np.array([[1.0, 1.0], [0.0, 1.0]])
    H = np.array([[1.0, 0.0]])
    f = lambda x: F @ x
    h = lambda x: H @ x
    x0, P0 = np.array([0.0, 1.0]), np.eye(2)
    Q, R = np.diag([0.01, 0.02]), np.array([[0.2]])
    x, P, _ = ukf_step(x0, P0, np.array([1.1]), f, h, Q, R,
                        alpha=0.5, beta=2.0, kappa=0.0)
    xp = F @ x0
    Pp = F @ P0 @ F.T + Q
    K = Pp @ H.T @ np.linalg.inv(H @ Pp @ H.T + R)
    np.testing.assert_allclose(x, xp + K @ (1.1 - H @ xp), atol=1e-9)
    np.testing.assert_allclose(P, Pp - K @ H @ Pp, atol=1e-9)


def test_ukf_handles_nonlinear_scalar_observation():
    f = lambda x: x.copy()
    h = lambda x: np.array([x[0] ** 2])
    x, P, info = ukf_step(np.array([1.0]), np.array([[0.2]]),
                           np.array([1.1]), f, h, np.array([[0.01]]),
                           np.array([[0.1]]), alpha=0.3)
    assert np.isfinite(x).all() and np.isfinite(P).all()
    assert P[0, 0] > 0
    assert info["innovation"].shape == (1,)


def test_filter_runners_return_one_state_per_observation():
    obs = np.array([[1.0], [1.2], [1.1]])
    f = lambda x: x.copy()
    h = lambda x: x.copy()
    jac_f = lambda _: np.eye(1)
    jac_h = lambda _: np.eye(1)
    Q, R = np.array([[0.01]]), np.array([[0.1]])
    e = ekf_filter(obs, np.array([0.0]), np.array([[1.0]]), f, h, jac_f, jac_h, Q, R)
    u = ukf_filter(obs, np.array([0.0]), np.array([[1.0]]), f, h, Q, R, alpha=0.5)
    assert e["means"].shape == u["means"].shape == (3, 1)
    assert e["covariances"].shape == u["covariances"].shape == (3, 1, 1)


@pytest.mark.parametrize("bad", [np.array([np.nan]), np.array([np.inf])])
def test_rejects_nonfinite_observations(bad):
    with pytest.raises(ValueError):
        ukf_step(np.array([0.0]), np.array([[1.0]]), bad,
                 lambda x: x, lambda x: x, np.array([[0.1]]), np.array([[0.1]]))


def test_ekf_rejects_bad_jacobian_shape():
    with pytest.raises(ValueError):
        ekf_step(np.array([0.0]), np.array([[1.0]]), np.array([1.0]),
                 lambda x: x, lambda x: x, lambda x: np.ones((2, 2)),
                 lambda x: np.ones((1, 1)), np.array([[0.1]]), np.array([[0.1]]))

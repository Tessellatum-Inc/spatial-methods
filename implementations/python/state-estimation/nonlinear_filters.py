"""Extended and scaled-unscented Kalman filters for additive-noise models."""
from __future__ import annotations
import numpy as np


def _covariance(value, size, name):
    a = np.asarray(value, dtype=float)
    if a.shape != (size, size) or not np.all(np.isfinite(a)):
        raise ValueError(f"{name} must be a finite square matrix of size {size}")
    a = 0.5 * (a + a.T)
    if np.linalg.eigvalsh(a).min() < -1e-10:
        raise ValueError(f"{name} must be positive semidefinite")
    return a


def _state(value, name):
    a = np.asarray(value, dtype=float)
    if a.ndim != 1 or a.size == 0 or not np.all(np.isfinite(a)):
        raise ValueError(f"{name} must be a nonempty finite vector")
    return a


def _solve_spd(a, b):
    """Solve SPD system without explicitly forming an inverse."""
    try:
        L = np.linalg.cholesky(a)
        return np.linalg.solve(L.T, np.linalg.solve(L, b))
    except np.linalg.LinAlgError as exc:
        raise ValueError("innovation covariance must be positive definite; check noise and model") from exc


def ekf_step(mean, covariance, observation, transition, observation_model,
             transition_jacobian, observation_jacobian, Q, R):
    """One EKF predict/update step for discrete additive-noise dynamics.

    x[k+1] = transition(x[k]) + w, z[k] = observation_model(x[k]) + v.
    Jacobians are evaluated at the prior mean and predicted mean respectively.
    Uses the Joseph covariance update. No control input or correlated noise.
    """
    x = _state(mean, "mean")
    n = x.size
    P = _covariance(covariance, n, "P")
    Q = _covariance(Q, n, "Q")
    xp = _state(transition(x), "transition output")
    if xp.size != n:
        raise ValueError("transition must preserve state dimension")
    F = np.asarray(transition_jacobian(x), dtype=float)
    if F.shape != (n, n) or not np.all(np.isfinite(F)):
        raise ValueError("transition_jacobian must be finite and square")
    Pp = F @ P @ F.T + Q
    Pp = 0.5 * (Pp + Pp.T)
    z = _state(observation, "observation")
    zp = _state(observation_model(xp), "predicted observation")
    m = zp.size
    if z.size != m:
        raise ValueError("observation dimension does not match observation model")
    R = _covariance(R, m, "R")
    H = np.asarray(observation_jacobian(xp), dtype=float)
    if H.shape != (m, n) or not np.all(np.isfinite(H)):
        raise ValueError("observation_jacobian has incompatible shape or nonfinite values")
    innovation = z - zp
    S = H @ Pp @ H.T + R
    K = _solve_spd(S, H @ Pp).T
    updated = xp + K @ innovation
    I_KH = np.eye(n) - K @ H
    Pu = I_KH @ Pp @ I_KH.T + K @ R @ K.T
    Pu = 0.5 * (Pu + Pu.T)
    return updated, Pu, {"predicted_mean": xp, "predicted_covariance": Pp,
                         "innovation": innovation, "innovation_covariance": S,
                         "gain": K}


def ekf_filter(observations, initial_mean, initial_covariance, transition,
              observation_model, transition_jacobian, observation_jacobian, Q, R):
    """Run EKF over observations; returns filtered means/covariances and diagnostics."""
    zs = np.asarray(observations, dtype=float)
    if zs.ndim != 2 or zs.shape[0] == 0 or not np.all(np.isfinite(zs)):
        raise ValueError("observations must be a nonempty finite 2-D array")
    x = _state(initial_mean, "initial_mean")
    P = _covariance(initial_covariance, x.size, "initial_covariance")
    means, covariances, diagnostics = [], [], []
    for z in zs:
        x, P, info = ekf_step(x, P, z, transition, observation_model,
                              transition_jacobian, observation_jacobian, Q, R)
        means.append(x.copy()); covariances.append(P.copy()); diagnostics.append(info)
    return {"means": np.asarray(means), "covariances": np.asarray(covariances),
            "diagnostics": diagnostics}


def _sigma_points(mean, covariance, alpha, beta, kappa):
    n = mean.size
    lam = alpha * alpha * (n + kappa) - n
    scale = n + lam
    if scale <= 0:
        raise ValueError("alpha, beta and kappa produce nonpositive sigma-point scale")
    P = _covariance(covariance, n, "P")
    try:
        # Small diagonal jitter only handles round-off near semidefinite boundaries.
        L = np.linalg.cholesky(P + np.eye(n) * 1e-12)
    except np.linalg.LinAlgError as exc:
        raise ValueError("UKF covariance must admit a stable Cholesky factor") from exc
    offsets = np.sqrt(scale) * L
    points = np.vstack([mean, mean + offsets.T, mean - offsets.T])
    wm = np.full(2 * n + 1, 1.0 / (2.0 * scale))
    wc = wm.copy()
    wm[0] = lam / scale
    wc[0] = lam / scale + (1.0 - alpha * alpha + beta)
    return points, wm, wc


def _weighted_covariance(points, mean, weights):
    d = points - mean
    return (d.T * weights) @ d


def ukf_step(mean, covariance, observation, transition, observation_model,
             Q, R, alpha=1e-3, beta=2.0, kappa=0.0):
    """One scaled-UKF predict/update step for additive-noise nonlinear models.

    Uses 2n+1 state sigma points and additive Q/R. Observation dimension may
    differ from state dimension. Angle wrapping, augmented-noise UKF, controls,
    and correlated process/measurement noise are intentionally not implicit.
    """
    x = _state(mean, "mean")
    n = x.size
    P = _covariance(covariance, n, "P")
    Q = _covariance(Q, n, "Q")
    R = np.asarray(R, dtype=float)
    if R.ndim != 2 or R.shape[0] != R.shape[1] or not np.all(np.isfinite(R)):
        raise ValueError("R must be a finite square matrix")
    R = _covariance(R, R.shape[0], "R")
    if not np.isfinite(alpha) or alpha <= 0 or not np.isfinite(beta) or not np.isfinite(kappa):
        raise ValueError("alpha must be positive and beta/kappa finite")
    points, wm, wc = _sigma_points(x, P, alpha, beta, kappa)
    propagated = np.asarray([_state(transition(p), "transition output") for p in points])
    if propagated.shape != (2 * n + 1, n):
        raise ValueError("transition must preserve state dimension")
    xp = wm @ propagated
    Pp = _weighted_covariance(propagated, xp, wc) + Q
    Pp = 0.5 * (Pp + Pp.T)

    # Additive process noise is part of the predicted-state distribution.
    # Re-centre sigma points on (xp, Pp) before applying the observation
    # function; reusing transition-only points would omit Q from S and the
    # state/observation cross-covariance, breaking the linear Kalman limit.
    measurement_points, _, _ = _sigma_points(xp, Pp, alpha, beta, kappa)
    predicted_obs = np.asarray([
        _state(observation_model(p), "predicted observation")
        for p in measurement_points
    ])
    m = predicted_obs.shape[1]
    if R.shape != (m, m):
        raise ValueError("R dimension does not match observation model")
    zp = wm @ predicted_obs
    dz = predicted_obs - zp
    dx = measurement_points - xp
    S = (dz.T * wc) @ dz + R
    cross = (dx.T * wc) @ dz
    z = _state(observation, "observation")
    if z.size != m:
        raise ValueError("observation dimension does not match observation model")
    K = _solve_spd(S, cross.T).T
    innovation = z - zp
    xu = xp + K @ innovation
    Pu = Pp - K @ S @ K.T
    Pu = 0.5 * (Pu + Pu.T)
    # Reject material loss of positive semidefiniteness rather than hiding it.
    if np.linalg.eigvalsh(Pu).min() < -1e-8:
        raise ValueError("UKF update produced a non-PSD covariance; review scaling and model")
    return xu, Pu, {"predicted_mean": xp, "predicted_covariance": Pp,
                    "predicted_observation": zp, "innovation": innovation,
                    "innovation_covariance": S, "gain": K}


def ukf_filter(observations, initial_mean, initial_covariance, transition,
              observation_model, Q, R, alpha=1e-3, beta=2.0, kappa=0.0):
    """Run scaled UKF over a sequence of observations."""
    zs = np.asarray(observations, dtype=float)
    if zs.ndim != 2 or zs.shape[0] == 0 or not np.all(np.isfinite(zs)):
        raise ValueError("observations must be a nonempty finite 2-D array")
    x = _state(initial_mean, "initial_mean")
    P = _covariance(initial_covariance, x.size, "initial_covariance")
    means, covariances, diagnostics = [], [], []
    for z in zs:
        x, P, info = ukf_step(x, P, z, transition, observation_model, Q, R,
                              alpha=alpha, beta=beta, kappa=kappa)
        means.append(x.copy()); covariances.append(P.copy()); diagnostics.append(info)
    return {"means": np.asarray(means), "covariances": np.asarray(covariances),
            "diagnostics": diagnostics}

"""Spatial advection-diffusion and linear data-assimilation teaching models."""
from __future__ import annotations
from numbers import Integral
import numpy as np


def _array(value, name, ndim):
    a = np.asarray(value, dtype=float)
    if a.ndim != ndim or not np.isfinite(a).all():
        raise ValueError(f"{name} must be a finite {ndim}-dimensional array")
    return a


def _covariance(value, name, n, positive_definite=False):
    a = _array(value, name, 2)
    if a.shape != (n, n) or not np.allclose(a, a.T, rtol=1e-10, atol=1e-12):
        raise ValueError(f"{name} must be symmetric with shape ({n}, {n})")
    eig = np.linalg.eigvalsh((a + a.T) / 2)
    tol = 1e-10 * max(1.0, float(np.max(np.abs(eig))))
    invalid = eig.min() <= tol if positive_definite else eig.min() < -tol
    if invalid:
        qualifier = "positive definite" if positive_definite else "positive semidefinite"
        raise ValueError(f"{name} must be {qualifier}")
    return a


def periodic_advection_diffusion_operator(n_cells, cell_width, time_step, velocity, diffusivity):
    """One explicit upwind-advection/centred-diffusion step on a uniform periodic grid."""
    if isinstance(n_cells, bool) or not isinstance(n_cells, Integral) or n_cells < 3:
        raise ValueError("n_cells must be an integer of at least 3")
    dx, dt, u, kappa = map(float, (cell_width, time_step, velocity, diffusivity))
    if not all(np.isfinite(v) for v in (dx, dt, u, kappa)) or dx <= 0 or dt <= 0 or kappa < 0:
        raise ValueError("grid spacing/time step must be positive; parameters finite and diffusivity non-negative")
    c, r = abs(u) * dt / dx, kappa * dt / dx**2
    if c + 2*r > 1 + 1e-12:
        raise ValueError("time step violates explicit advection-diffusion stability bound")
    F = np.zeros((n_cells, n_cells))
    for i in range(n_cells):
        left, right = (i-1) % n_cells, (i+1) % n_cells
        F[i, i] = 1 - c - 2*r
        F[i, left] += r
        F[i, right] += r
        F[i, left if u >= 0 else right] += c
    return F


def periodic_point_observation_operator(n_cells, cell_width, sensor_positions):
    """Periodic linear interpolation from uniform cell-centred states to point sensors."""
    if isinstance(n_cells, bool) or not isinstance(n_cells, Integral) or n_cells < 3:
        raise ValueError("n_cells must be an integer of at least 3")
    dx = float(cell_width)
    pos = _array(sensor_positions, "sensor_positions", 1)
    if not np.isfinite(dx) or dx <= 0 or pos.size == 0:
        raise ValueError("cell_width must be positive and sensor_positions non-empty")
    q = np.mod(pos, n_cells*dx) / dx
    left = np.floor(q).astype(int)
    frac = q-left
    H = np.zeros((pos.size, n_cells))
    rows = np.arange(pos.size)
    H[rows, left] = 1-frac
    H[rows, (left+1) % n_cells] += frac
    return H


def run_linear_spatial_assimilation(initial_mean, initial_covariance, transition_matrix,
                                    process_covariance, observations, *, forecast_steps=0):
    """Run sequential forecast-analysis updates; each item is None or (y,H,R)."""
    mean = _array(initial_mean, "initial_mean", 1).copy()
    n = mean.size
    if n == 0:
        raise ValueError("initial_mean must not be empty")
    P = _covariance(initial_covariance, "initial_covariance", n).copy()
    F = _array(transition_matrix, "transition_matrix", 2)
    if F.shape != (n,n):
        raise ValueError("transition_matrix must match state dimension")
    Q = _covariance(process_covariance, "process_covariance", n)
    if isinstance(forecast_steps, bool) or not isinstance(forecast_steps, Integral) or forecast_steps < 0:
        raise ValueError("forecast_steps must be a non-negative integer")
    fm, fp, am, ap, innovations, innovation_covariances = [], [], [], [], [], []
    for k, item in enumerate(observations):
        mean = F @ mean
        P = F @ P @ F.T + Q
        P = (P + P.T)/2
        fm.append(mean.copy()); fp.append(P.copy())
        if item is None:
            innovations.append(np.empty(0)); innovation_covariances.append(np.empty((0,0)))
        else:
            if not isinstance(item, (tuple,list)) or len(item) != 3:
                raise ValueError(f"observation {k} must be None or (y,H,R)")
            y = _array(item[0], f"observations[{k}].y", 1)
            H = _array(item[1], f"observations[{k}].H", 2)
            if y.size == 0 or H.shape != (y.size,n):
                raise ValueError(f"observation {k} dimensions do not match state")
            R = _covariance(item[2], f"observations[{k}].R", y.size, True)
            d = y-H@mean
            S = H@P@H.T+R
            S = (S+S.T)/2
            try:
                K = np.linalg.solve(S, H@P).T
            except np.linalg.LinAlgError as exc:
                raise ValueError(f"observation {k} innovation covariance is singular") from exc
            mean = mean+K@d
            A = np.eye(n)-K@H
            P = A@P@A.T+K@R@K.T
            P = (P+P.T)/2
            innovations.append(d.copy()); innovation_covariances.append(S.copy())
        am.append(mean.copy()); ap.append(P.copy())
    ffm, ffp = [], []
    for _ in range(int(forecast_steps)):
        mean = F@mean
        P = F@P@F.T+Q
        P = (P+P.T)/2
        ffm.append(mean.copy()); ffp.append(P.copy())
    stack = lambda rows, shape: np.stack(rows) if rows else np.empty(shape)
    return {
        "forecast_means": stack(fm,(0,n)), "forecast_covariances": stack(fp,(0,n,n)),
        "analysis_means": stack(am,(0,n)), "analysis_covariances": stack(ap,(0,n,n)),
        "innovations": innovations, "innovation_covariances": innovation_covariances,
        "free_forecast_means": stack(ffm,(0,n)),
        "free_forecast_covariances": stack(ffp,(0,n,n)),
    }


def periodic_nonuniform_advection_diffusion_operator(cell_widths, time_step,
                                                       face_velocities, face_diffusivities):
    """Conservative explicit finite-volume step on a periodic nonuniform 1-D grid.

    State entries are cell-centred concentrations. Face i is the right face
    between cells i and (i+1) modulo n. Advection uses upwind face values;
    diffusion uses the centre-to-centre gradient. Face velocity and diffusivity
    may vary spatially. The step is accepted only if its transition matrix is
    non-negative (within round-off tolerance).
    """
    widths = _array(cell_widths, "cell_widths", 1)
    n = widths.size
    if n < 3 or np.any(widths <= 0):
        raise ValueError("cell_widths must contain at least three positive values")
    dt = float(time_step)
    if not np.isfinite(dt) or dt <= 0:
        raise ValueError("time_step must be positive and finite")
    velocity = _array(face_velocities, "face_velocities", 1)
    diffusivity = _array(face_diffusivities, "face_diffusivities", 1)
    if velocity.shape != (n,) or diffusivity.shape != (n,) or np.any(diffusivity < 0):
        raise ValueError("face velocity and diffusivity must have one value per face; diffusivity non-negative")
    distances = 0.5 * (widths + np.roll(widths, -1))
    L = np.zeros((n,n))
    for i in range(n):
        j = (i+1) % n
        u, k, distance = velocity[i], diffusivity[i], distances[i]
        a = max(u, 0.0) + k/distance
        b = min(u, 0.0) - k/distance
        L[i,i] -= a/widths[i]
        L[i,j] -= b/widths[i]
        L[j,i] += a/widths[j]
        L[j,j] += b/widths[j]
    F = np.eye(n) + dt*L
    if np.min(F) < -1e-12:
        raise ValueError("time step violates finite-volume positivity/stability bound")
    F[F < 0] = 0.0
    return F


def periodic_nonuniform_point_observation_operator(cell_widths, sensor_positions):
    """Linear interpolation from nonuniform periodic cell centres to point sensors."""
    widths = _array(cell_widths, "cell_widths", 1)
    n = widths.size
    pos = _array(sensor_positions, "sensor_positions", 1)
    if n < 3 or np.any(widths <= 0) or pos.size == 0:
        raise ValueError("need at least three positive cell widths and one sensor")
    length = float(widths.sum())
    centres = np.cumsum(widths) - 0.5*widths
    q = np.mod(pos, length)
    H = np.zeros((pos.size,n))
    for row, point in enumerate(q):
        right = int(np.searchsorted(centres, point, side="right"))
        if right == 0:
            li, ri = n-1, 0
            lx, rx = centres[-1]-length, centres[0]
        elif right == n:
            li, ri = n-1, 0
            lx, rx = centres[-1], centres[0]+length
        else:
            li, ri = right-1, right
            lx, rx = centres[li], centres[ri]
        fraction = (point-lx)/(rx-lx)
        H[row,li] = 1.0-fraction
        H[row,ri] += fraction
    return H


def verify_spatial_forecasts(forecast_means, heldout_observations):
    """Score free forecasts against separate held-out (y,H) observations by lead."""
    forecasts = _array(forecast_means, "forecast_means", 2)
    if forecasts.shape[0] != len(heldout_observations) or forecasts.shape[1] == 0:
        raise ValueError("forecast_means and heldout_observations must have matching non-empty leads")
    scores = []
    for lead, item in enumerate(heldout_observations):
        if item is None:
            scores.append({"lead": lead+1, "count": 0, "bias": np.nan, "mae": np.nan, "rmse": np.nan})
            continue
        if not isinstance(item, (tuple,list)) or len(item) != 2:
            raise ValueError(f"heldout observation {lead} must be None or (y,H)")
        y = _array(item[0], f"heldout_observations[{lead}].y", 1)
        H = _array(item[1], f"heldout_observations[{lead}].H", 2)
        if y.size == 0 or H.shape != (y.size,forecasts.shape[1]):
            raise ValueError(f"heldout observation {lead} dimensions do not match forecast state")
        error = H@forecasts[lead]-y
        scores.append({
            "lead": lead+1, "count": int(error.size),
            "bias": float(np.mean(error)), "mae": float(np.mean(np.abs(error))),
            "rmse": float(np.sqrt(np.mean(error**2))),
        })
    return scores

"""Dense universal kriging with polynomial drift and explicit variogram parameters."""
from __future__ import annotations
import numpy as np
from variogram_models import variogram_model


def _drift(coordinates, center, scale, order):
    q = (coordinates-center)/scale
    x, y = q[:,0], q[:,1]
    cols = [np.ones(len(q))]
    if order >= 1:
        cols.extend([x,y])
    if order >= 2:
        cols.extend([x*x,x*y,y*y])
    return np.column_stack(cols)


def universal_kriging(observation_coordinates, values, target_coordinates, *,
                      variogram="spherical", nugget=0.0,
                      partial_sill=1.0, range_=1.0, drift_order=1):
    """Predict at targets using a universal-kriging covariance system.

    Coordinates are planar and share units with range_. Drift order 0 is
    ordinary kriging (unknown constant mean); order 1 is linear; order 2 is
    quadratic. Variogram parameters are supplied, not fitted.
    """
    obs = np.asarray(observation_coordinates, dtype=float)
    z = np.asarray(values, dtype=float)
    target = np.asarray(target_coordinates, dtype=float)
    if obs.ndim != 2 or obs.shape[1] != 2 or len(obs) == 0 or not np.all(np.isfinite(obs)):
        raise ValueError("observation_coordinates must be a non-empty finite (n, 2) array")
    if z.shape != (len(obs),) or not np.all(np.isfinite(z)):
        raise ValueError("values must be finite and match observations")
    if target.ndim != 2 or target.shape[1] != 2 or not np.all(np.isfinite(target)):
        raise ValueError("target_coordinates must be a finite (m, 2) array")
    if drift_order not in (0,1,2):
        raise ValueError("drift_order must be 0, 1 or 2")
    n_terms = {0:1,1:3,2:6}[drift_order]
    if len(obs) < n_terms:
        raise ValueError("not enough observations for the requested drift order")
    if not np.isfinite([nugget,partial_sill,range_]).all() or nugget < 0 or partial_sill < 0 or range_ <= 0:
        raise ValueError("nugget and partial_sill must be non-negative and range_ positive")
    center = obs.mean(axis=0)
    scale = obs.std(axis=0)
    scale[scale <= np.finfo(float).eps] = 1.0
    f = _drift(obs, center, scale, drift_order)
    ft = _drift(target, center, scale, drift_order)
    if np.linalg.matrix_rank(f) < n_terms:
        raise ValueError("observation geometry is rank deficient for the requested drift")
    distance = np.linalg.norm(obs[:,None,:]-obs[None,:,:], axis=2)
    sill = float(nugget+partial_sill)
    gamma = variogram_model(distance, model=variogram, nugget=nugget,
                            partial_sill=partial_sill, range_=range_)
    covariance = sill-gamma
    system = np.block([[covariance, f],
                       [f.T, np.zeros((n_terms,n_terms))]])
    if np.linalg.matrix_rank(system) < system.shape[0]:
        raise ValueError("kriging system is singular; check geometry and variogram parameters")
    predictions = np.empty(len(target), dtype=float)
    variances = np.empty(len(target), dtype=float)
    for i, point in enumerate(target):
        d = np.linalg.norm(obs-point, axis=1)
        gamma0 = variogram_model(d, model=variogram, nugget=nugget,
                                 partial_sill=partial_sill, range_=range_)
        c0 = sill-gamma0
        rhs = np.r_[c0, ft[i]]
        solution = np.linalg.solve(system, rhs)
        weights, multipliers = solution[:len(obs)], solution[len(obs):]
        predictions[i] = float(weights @ z)
        variance = sill-float(weights @ c0)-float(multipliers @ ft[i])
        if variance < -1e-7*max(1.0,sill):
            raise RuntimeError("computed kriging variance is materially negative")
        variances[i] = max(0.0,variance)
    return {"prediction": predictions, "variance": variances,
            "drift_order": int(drift_order), "variogram": variogram,
            "n_observations": int(len(obs))}

"""Average direct, indirect and total impacts for SAR and SDM models."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class Impact:
    direct: float
    indirect: float
    total: float
    impact_matrix: tuple[tuple[float, ...], ...]


def spatial_impacts(
    weights: Sequence[Sequence[float]],
    rho: float,
    beta: Sequence[float],
    gamma: Sequence[float] | None = None,
) -> tuple[Impact, ...]:
    """Calculate average impacts for each covariate in a spatial Durbin model.

    For covariate r, S_r = (I-rho W)^-1 (beta_r I + gamma_r W).
    Average direct impact is trace(S_r)/N; average total impact is the
    average row sum (equivalently sum(S_r)/N); indirect is total minus direct.

    Set gamma=0 for the spatial-lag/SAR special case. Supply one gamma per
    beta; gamma=0 means no spatially lagged covariate for that term.
    """
    w = np.asarray(weights, dtype=float)
    b = np.asarray(beta, dtype=float)
    if w.ndim != 2 or w.shape[0] != w.shape[1] or w.shape[0] < 2:
        raise ValueError("weights must be a square matrix with at least two units")
    n = w.shape[0]
    if b.ndim != 1 or b.size == 0:
        raise ValueError("beta must be a nonempty one-dimensional vector")
    if gamma is None:
        g = np.zeros_like(b)
    else:
        g = np.asarray(gamma, dtype=float)
        if g.shape != b.shape:
            raise ValueError("gamma must have one value per beta coefficient")
    if not np.all(np.isfinite(w)) or not np.all(np.isfinite(b)) or not np.all(np.isfinite(g)):
        raise ValueError("weights and coefficients must be finite")
    if not np.isfinite(rho):
        raise ValueError("rho must be finite")
    identity = np.eye(n)
    system = identity - float(rho) * w
    try:
        impacts = []
        for coefficient, spatial_coefficient in zip(b, g):
            right = coefficient * identity + spatial_coefficient * w
            matrix = np.linalg.solve(system, right)
            direct = float(np.trace(matrix) / n)
            total = float(np.sum(matrix) / n)
            indirect = total - direct
            impacts.append(Impact(
                direct=direct,
                indirect=indirect,
                total=total,
                impact_matrix=tuple(tuple(float(v) for v in row) for row in matrix),
            ))
    except np.linalg.LinAlgError as exc:
        raise ValueError("I - rho W must be nonsingular") from exc
    return tuple(impacts)



@dataclass(frozen=True)
class ImpactInterval:
    estimate: float
    standard_error: float
    lower: float
    upper: float


@dataclass(frozen=True)
class ImpactUncertainty:
    direct: ImpactInterval
    indirect: ImpactInterval
    total: ImpactInterval
    accepted_draws: int
    rejected_draws: int


def spatial_impact_uncertainty(
    weights: Sequence[Sequence[float]],
    rho: float,
    beta: Sequence[float],
    covariance: Sequence[Sequence[float]],
    gamma: Sequence[float] | None = None,
    *,
    draws: int = 5000,
    confidence: float = 0.95,
    seed: int | None = None,
    condition_limit: float = 1e10,
    minimum_acceptance: float = 0.5,
) -> tuple[ImpactUncertainty, ...]:
    """Parametric Monte Carlo intervals for SAR/SDM direct, indirect and total impacts.

    The joint parameter vector is ordered [rho, beta...] when gamma is None,
    and [rho, beta..., gamma...] otherwise. Covariance must use that exact
    ordering. Draws producing an ill-conditioned I-rho W are rejected.
    """
    w = np.asarray(weights, dtype=float)
    b = np.asarray(beta, dtype=float)
    if w.ndim != 2 or w.shape[0] != w.shape[1] or w.shape[0] < 2:
        raise ValueError("weights must be a square matrix with at least two units")
    if b.ndim != 1 or b.size == 0:
        raise ValueError("beta must be a nonempty one-dimensional vector")
    if gamma is None:
        g = np.zeros_like(b)
        mean = np.concatenate([[float(rho)], b])
    else:
        g = np.asarray(gamma, dtype=float)
        if g.shape != b.shape:
            raise ValueError("gamma must have one value per beta coefficient")
        mean = np.concatenate([[float(rho)], b, g])
    cov = np.asarray(covariance, dtype=float)
    if cov.shape != (mean.size, mean.size):
        raise ValueError("covariance shape must match [rho, beta..., gamma...]")
    if not (np.all(np.isfinite(w)) and np.all(np.isfinite(mean))
            and np.all(np.isfinite(cov))):
        raise ValueError("weights, parameters and covariance must be finite")
    if not np.allclose(cov, cov.T, atol=1e-10, rtol=1e-10):
        raise ValueError("covariance must be symmetric")
    eigenvalues = np.linalg.eigvalsh((cov + cov.T) / 2.0)
    if eigenvalues.min() < -1e-10 * max(1.0, float(np.max(np.abs(eigenvalues)))):
        raise ValueError("covariance must be positive semidefinite")
    if isinstance(draws, bool) or not isinstance(draws, int) or draws < 100:
        raise ValueError("draws must be an integer of at least 100")
    if not np.isfinite(confidence) or not 0 < confidence < 1:
        raise ValueError("confidence must be strictly between zero and one")
    if not np.isfinite(condition_limit) or condition_limit <= 1:
        raise ValueError("condition_limit must be finite and greater than one")
    if not np.isfinite(minimum_acceptance) or not 0 < minimum_acceptance <= 1:
        raise ValueError("minimum_acceptance must be in (0, 1]")

    point_impacts = spatial_impacts(w, rho, b, g)
    rng = np.random.default_rng(seed)
    samples = rng.multivariate_normal(mean, cov, size=draws, check_valid="raise")
    values = [[[], [], []] for _ in range(b.size)]
    rejected = 0
    identity = np.eye(w.shape[0])
    for sample in samples:
        sampled_rho = float(sample[0])
        system = identity - sampled_rho * w
        try:
            condition_number = np.linalg.cond(system)
            if not np.isfinite(condition_number) or condition_number > condition_limit:
                rejected += 1
                continue
            sampled_beta = sample[1:1 + b.size]
            sampled_gamma = (np.zeros_like(b) if gamma is None
                             else sample[1 + b.size:1 + 2 * b.size])
            sample_impacts = spatial_impacts(w, sampled_rho, sampled_beta, sampled_gamma)
        except (ValueError, np.linalg.LinAlgError):
            rejected += 1
            continue
        for index, impact in enumerate(sample_impacts):
            values[index][0].append(impact.direct)
            values[index][1].append(impact.indirect)
            values[index][2].append(impact.total)

    accepted = draws - rejected
    if accepted < int(np.ceil(draws * minimum_acceptance)):
        raise ValueError("too few valid parameter draws; inspect covariance and spatial-parameter support")
    tail = (1.0 - confidence) / 2.0
    results = []
    for index, point in enumerate(point_impacts):
        intervals = []
        for component, estimate in zip(values[index],
                                       (point.direct, point.indirect, point.total)):
            array = np.asarray(component, dtype=float)
            intervals.append(ImpactInterval(
                estimate=float(estimate),
                standard_error=float(np.std(array, ddof=1)),
                lower=float(np.quantile(array, tail)),
                upper=float(np.quantile(array, 1.0 - tail)),
            ))
        results.append(ImpactUncertainty(
            direct=intervals[0],
            indirect=intervals[1],
            total=intervals[2],
            accepted_draws=accepted,
            rejected_draws=rejected,
        ))
    return tuple(results)


@dataclass(frozen=True)
class DeltaImpactUncertainty:
    """First-order delta-method uncertainty for one covariate's impacts."""
    direct: ImpactInterval
    indirect: ImpactInterval
    total: ImpactInterval


def spatial_impact_delta_uncertainty(
    weights: Sequence[Sequence[float]],
    rho: float,
    beta: Sequence[float],
    covariance: Sequence[Sequence[float]],
    gamma: Sequence[float] | None = None,
    *,
    confidence: float = 0.95,
) -> tuple[DeltaImpactUncertainty, ...]:
    """Propagate joint parameter covariance through SAR/SDM impact functions.

    Covariance ordering is [rho, beta...] for SAR or [rho, beta..., gamma...]
    for SDM. Uses the analytic Jacobian and a two-sided normal (Wald) interval.
    This is a local first-order approximation, unlike the parametric Monte
    Carlo method; it can be poor near singular spatial multipliers or with
    highly nonlinear/strongly skewed impact distributions.
    """
    from statistics import NormalDist

    w = np.asarray(weights, dtype=float)
    b = np.asarray(beta, dtype=float)
    if w.ndim != 2 or w.shape[0] != w.shape[1] or w.shape[0] < 2:
        raise ValueError("weights must be a square matrix with at least two units")
    if b.ndim != 1 or b.size == 0:
        raise ValueError("beta must be a nonempty one-dimensional vector")
    if gamma is None:
        g = np.zeros_like(b)
        mean_size = 1 + b.size
    else:
        g = np.asarray(gamma, dtype=float)
        if g.shape != b.shape:
            raise ValueError("gamma must have one value per beta coefficient")
        mean_size = 1 + 2 * b.size
    mean = np.concatenate([[float(rho)], b] if gamma is None else [[float(rho)], b, g])
    cov = np.asarray(covariance, dtype=float)
    if cov.shape != (mean_size, mean_size):
        raise ValueError("covariance shape must match [rho, beta..., gamma...]")
    if not (np.all(np.isfinite(w)) and np.all(np.isfinite(mean))
            and np.all(np.isfinite(cov))):
        raise ValueError("weights, parameters and covariance must be finite")
    if not np.allclose(cov, cov.T, atol=1e-10, rtol=1e-10):
        raise ValueError("covariance must be symmetric")
    eigenvalues = np.linalg.eigvalsh((cov + cov.T) / 2.0)
    if eigenvalues.min() < -1e-10 * max(1.0, float(np.max(np.abs(eigenvalues)))):
        raise ValueError("covariance must be positive semidefinite")
    if not np.isfinite(confidence) or not 0 < confidence < 1:
        raise ValueError("confidence must be strictly between zero and one")

    n = w.shape[0]
    identity = np.eye(n)
    system = identity - float(rho) * w
    try:
        multiplier = np.linalg.solve(system, identity)
        normal_critical = NormalDist().inv_cdf((1.0 + confidence) / 2.0)
        results = []
        for index, (coefficient, spatial_coefficient) in enumerate(zip(b, g)):
            right = coefficient * identity + spatial_coefficient * w
            impact_matrix = multiplier @ right
            derivative_rho = multiplier @ w @ impact_matrix
            derivative_beta = multiplier
            derivative_gamma = multiplier @ w
            jac_direct = np.zeros(mean_size)
            jac_total = np.zeros(mean_size)
            jac_direct[0] = np.trace(derivative_rho) / n
            jac_total[0] = np.sum(derivative_rho) / n
            jac_direct[1 + index] = np.trace(derivative_beta) / n
            jac_total[1 + index] = np.sum(derivative_beta) / n
            if gamma is not None:
                gamma_index = 1 + b.size + index
                jac_direct[gamma_index] = np.trace(derivative_gamma) / n
                jac_total[gamma_index] = np.sum(derivative_gamma) / n
            direct = float(np.trace(impact_matrix) / n)
            total = float(np.sum(impact_matrix) / n)
            indirect = total - direct
            jac_indirect = jac_total - jac_direct
            intervals = []
            for estimate, gradient in (
                (direct, jac_direct), (indirect, jac_indirect), (total, jac_total)
            ):
                variance = float(gradient @ cov @ gradient)
                tolerance = 1e-10 * max(1.0, float(np.max(np.abs(cov))))
                if variance < -tolerance:
                    raise ValueError("delta-method variance is negative; inspect covariance")
                standard_error = float(np.sqrt(max(0.0, variance)))
                intervals.append(ImpactInterval(
                    estimate=estimate,
                    standard_error=standard_error,
                    lower=estimate - normal_critical * standard_error,
                    upper=estimate + normal_critical * standard_error,
                ))
            results.append(DeltaImpactUncertainty(
                direct=intervals[0], indirect=intervals[1], total=intervals[2]
            ))
    except np.linalg.LinAlgError as exc:
        raise ValueError("I - rho W must be nonsingular") from exc
    return tuple(results)

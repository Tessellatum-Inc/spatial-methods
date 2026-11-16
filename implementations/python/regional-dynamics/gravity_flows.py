"""Constrained gravity and entropy-maximising spatial interaction models."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class GravityBalanceResult:
    flows: np.ndarray
    converged: bool
    iterations: int
    row_error: float
    column_error: float


def _inputs(origins, destinations, impedance):
    o = np.asarray(origins, dtype=float)
    d = np.asarray(destinations, dtype=float)
    f = np.asarray(impedance, dtype=float)
    if o.ndim != 1 or d.ndim != 1 or o.size == 0 or d.size == 0:
        raise ValueError("origins and destinations must be non-empty vectors")
    if f.shape != (o.size, d.size):
        raise ValueError("impedance must have shape (n_origins, n_destinations)")
    if not np.isfinite(o).all() or not np.isfinite(d).all() or not np.isfinite(f).all():
        raise ValueError("margins and impedance must be finite")
    if np.any(o < 0) or np.any(d < 0) or np.any(f < 0):
        raise ValueError("margins and impedance must be non-negative")
    return o, d, f


def unconstrained_gravity(origins, destinations, impedance):
    """Return O_i * D_j * f(c_ij), with neither margin constrained."""
    o, d, f = _inputs(origins, destinations, impedance)
    return o[:, None] * d[None, :] * f


def production_constrained_gravity(origins, destinations, impedance):
    """Allocate every origin total across destinations; row sums equal origins."""
    o, d, f = _inputs(origins, destinations, impedance)
    weights = f * d[None, :]
    denominator = weights.sum(axis=1)
    if np.any((o > 0) & (denominator <= 0)):
        raise ValueError("a positive origin has no reachable positive-attraction destination")
    probabilities = np.divide(
        weights, denominator[:, None], out=np.zeros_like(weights),
        where=denominator[:, None] > 0,
    )
    return o[:, None] * probabilities


def attraction_constrained_gravity(origins, destinations, impedance):
    """Allocate origin mass to each destination; column sums equal destinations."""
    o, d, f = _inputs(origins, destinations, impedance)
    weights = f * o[:, None]
    denominator = weights.sum(axis=0)
    if np.any((d > 0) & (denominator <= 0)):
        raise ValueError("a positive destination has no reachable positive-production origin")
    probabilities = np.divide(
        weights, denominator[None, :], out=np.zeros_like(weights),
        where=denominator[None, :] > 0,
    )
    return probabilities * d[None, :]


def doubly_constrained_gravity(
    origins, destinations, impedance, *, tolerance=1e-10, max_iter=10000
):
    """Fit doubly constrained flows by iterative proportional fitting (RAS).

    Origin and destination totals must agree. Structural zeros in impedance
    remain zero. A non-converged result is returned with diagnostics rather
    than silently described as balanced.
    """
    o, d, f = _inputs(origins, destinations, impedance)
    if not np.isfinite(tolerance) or tolerance <= 0:
        raise ValueError("tolerance must be finite and positive")
    if not isinstance(max_iter, int) or max_iter < 1:
        raise ValueError("max_iter must be a positive integer")
    if not np.isclose(o.sum(), d.sum(), rtol=1e-9, atol=1e-12):
        raise ValueError("total origin production must equal total destination attraction")

    seed = o[:, None] * d[None, :] * f
    if np.any((o > 0) & (seed.sum(axis=1) == 0)):
        raise ValueError("a positive origin has no feasible destination")
    if np.any((d > 0) & (seed.sum(axis=0) == 0)):
        raise ValueError("a positive destination has no feasible origin")

    flows = seed.copy()
    total = float(o.sum())
    if total == 0:
        return GravityBalanceResult(flows, True, 0, 0.0, 0.0)

    row_error = column_error = float("inf")
    for iteration in range(1, max_iter + 1):
        row_sums = flows.sum(axis=1)
        row_scale = np.divide(o, row_sums, out=np.ones_like(o), where=row_sums > 0)
        flows *= row_scale[:, None]

        column_sums = flows.sum(axis=0)
        column_scale = np.divide(d, column_sums, out=np.ones_like(d), where=column_sums > 0)
        flows *= column_scale[None, :]

        row_error = float(np.max(np.abs(flows.sum(axis=1) - o)) / max(total, 1.0))
        column_error = float(np.max(np.abs(flows.sum(axis=0) - d)) / max(total, 1.0))
        if max(row_error, column_error) <= tolerance:
            return GravityBalanceResult(flows, True, iteration, row_error, column_error)

    return GravityBalanceResult(flows, False, max_iter, row_error, column_error)


def entropy_maximizing_gravity(
    origins, destinations, generalized_cost, *, beta, tolerance=1e-10, max_iter=10000
):
    """Doubly constrained Wilson-style model with exponential cost deterrence.

    The seed matrix is O_i D_j exp(-beta * c_ij), and IPF enforces both
    marginal totals. This is a specified exponential-impedance variant,
    not a calibrated estimate of beta.
    """
    cost = np.asarray(generalized_cost, dtype=float)
    if not np.isfinite(beta) or beta < 0:
        raise ValueError("beta must be finite and non-negative")
    if not np.isfinite(cost).all() or np.any(cost < 0):
        raise ValueError("generalized_cost must be finite and non-negative")
    with np.errstate(under="ignore"):
        impedance = np.exp(-beta * cost)
    return doubly_constrained_gravity(
        origins, destinations, impedance, tolerance=tolerance, max_iter=max_iter
    )



def intervening_opportunities(origins, destinations, generalized_cost, *, alpha):
    """Allocate origin flows by a cumulative intervening-opportunities rule.

    Destinations are encountered in increasing generalized-cost order.
    For an origin, the probability mass assigned to a tied-cost group is
    exp(-alpha * prior_opportunities) * (1 - exp(-alpha * group_opportunities)).
    That mass is divided among destinations in the group in proportion to
    their opportunity totals. Remaining survival probability is returned as
    unallocated flow rather than silently renormalised to one.
    """
    o, d, cost = _inputs(origins, destinations, generalized_cost)
    try:
        rate = float(alpha)
    except (TypeError, ValueError):
        raise ValueError("alpha must be finite and positive") from None
    if not np.isfinite(rate) or rate <= 0:
        raise ValueError("alpha must be finite and positive")

    flows = np.zeros((o.size, d.size), dtype=float)
    unallocated = np.zeros(o.size, dtype=float)
    for i in range(o.size):
        survival = 1.0
        # Group equal costs so ties do not depend on destination column order.
        for level in np.unique(cost[i]):
            group = np.flatnonzero(cost[i] == level)
            opportunity = float(d[group].sum())
            if opportunity <= 0:
                continue
            probability = survival * (-np.expm1(-rate * opportunity))
            flows[i, group] = o[i] * probability * d[group] / opportunity
            survival *= np.exp(-rate * opportunity)
        unallocated[i] = o[i] * survival
    return {"flows": flows, "unallocated": unallocated}

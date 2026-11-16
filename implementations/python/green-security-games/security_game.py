"""Minimax Stackelberg security-game coverage allocation."""
from __future__ import annotations
import numpy as np


def minimax_patrol_allocation(attacker_values, detection_effectiveness, resources,
                              *, tolerance=1e-10, max_iterations=200):
    """Allocate fractional patrol coverage to minimize best-response attack payoff.

    Site i's expected attacker payoff is v_i*(1-e_i*x_i), where v_i is
    attack value, e_i detection effectiveness and x_i patrol coverage.
    Coverage lies in [0,1] and sum(x_i) is bounded by the resource budget.
    The minimax solution equalizes payoffs across partially covered sites.
    """
    value = np.asarray(attacker_values, dtype=float)
    effectiveness = np.asarray(detection_effectiveness, dtype=float)
    if value.ndim != 1 or value.size == 0 or effectiveness.shape != value.shape:
        raise ValueError("attacker_values and detection_effectiveness must be matching non-empty vectors")
    if not np.all(np.isfinite(value)) or np.any(value <= 0):
        raise ValueError("attacker values must be finite and positive")
    if not np.all(np.isfinite(effectiveness)) or np.any((effectiveness <= 0) | (effectiveness > 1)):
        raise ValueError("detection effectiveness must lie in (0, 1]")
    try:
        budget, tol = float(resources), float(tolerance)
    except (TypeError, ValueError):
        raise ValueError("resources and tolerance must be finite and valid") from None
    if not np.isfinite(budget) or not 0 <= budget <= len(value):
        raise ValueError("resources must lie between zero and the number of sites")
    if not np.isfinite(tol) or tol <= 0:
        raise ValueError("tolerance must be finite and positive")
    if isinstance(max_iterations, (bool, np.bool_)) or not isinstance(max_iterations, (int, np.integer)) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    if budget == 0:
        coverage = np.zeros_like(value)
        threshold = float(value.max())
    elif budget == len(value):
        coverage = np.ones_like(value)
        threshold = float(np.max(value*(1-effectiveness)))
    else:
        lower = float(np.min(value*(1-effectiveness)))
        upper = float(np.max(value))
        for _ in range(int(max_iterations)):
            threshold = 0.5*(lower+upper)
            allocation = np.clip((1.0-threshold/value)/effectiveness, 0.0, 1.0)
            if allocation.sum() > budget:
                lower = threshold
            else:
                upper = threshold
            if upper-lower <= tol*max(1.0, upper):
                break
        threshold = upper
        coverage = np.clip((1.0-threshold/value)/effectiveness, 0.0, 1.0)
        # Correct tiny bisection budget error without changing active-set order.
        excess = coverage.sum()-budget
        if excess > tol:
            active = np.flatnonzero((coverage > 0) & (coverage < 1))
            if active.size:
                coverage[active] -= excess/active.size
    payoffs = value*(1.0-effectiveness*coverage)
    return {"coverage": coverage, "attacker_payoffs": payoffs,
            "worst_case_payoff": float(payoffs.max()),
            "resources_used": float(coverage.sum()),
            "resource_budget": budget, "equalized_payoff": threshold}

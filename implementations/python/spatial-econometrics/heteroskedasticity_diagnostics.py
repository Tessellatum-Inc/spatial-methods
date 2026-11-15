"""Heteroskedasticity diagnostics for OLS spatial-regression baselines.

Implements the Koenker studentized Breusch-Pagan test and White's general
heteroskedasticity test using auxiliary regressions on squared OLS residuals.
These diagnose non-constant variance; they do not test spatial dependence.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, lgamma
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class HeteroskedasticityTest:
    statistic: float
    p_value: float
    degrees_of_freedom: int
    auxiliary_r_squared: float


@dataclass(frozen=True)
class HeteroskedasticityDiagnostics:
    coefficients: tuple[float, ...]
    residuals: tuple[float, ...]
    sigma2_mle: float
    koenker_bp: HeteroskedasticityTest
    white: HeteroskedasticityTest


def _chi_square_sf(value: float, df: int) -> float:
    """Chi-square survival function via regularized upper incomplete gamma."""
    # Numerical Recipes series/continued-fraction evaluation of Q(df/2, value/2).
    a = df / 2.0
    x = max(0.0, value / 2.0)
    if x == 0.0:
        return 1.0
    if x < a + 1.0:
        term = total = 1.0 / a
        ap = a
        for _ in range(10000):
            ap += 1.0
            term *= x / ap
            total += term
            if abs(term) <= abs(total) * 1e-14:
                break
        lower = total * np.exp(-x + a * np.log(x) - lgamma(a))
        return float(np.clip(1.0 - lower, 0.0, 1.0))
    b = x + 1.0 - a
    c = 1.0 / np.finfo(float).tiny
    d = 1.0 / b
    h = d
    for i in range(1, 10000):
        an = -i * (i - a)
        b += 2.0
        d = an * d + b
        if abs(d) < np.finfo(float).tiny:
            d = np.finfo(float).tiny
        c = b + an / c
        if abs(c) < np.finfo(float).tiny:
            c = np.finfo(float).tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) <= 1e-14:
            break
    upper = np.exp(-x + a * np.log(x) - lgamma(a)) * h
    return float(np.clip(upper, 0.0, 1.0))


def _auxiliary_test(squared_residuals: np.ndarray,
                    auxiliary_design: np.ndarray) -> HeteroskedasticityTest:
    n = squared_residuals.size
    rank = int(np.linalg.matrix_rank(auxiliary_design))
    if rank < 2:
        raise ValueError("auxiliary design must identify at least one variance regressor")
    fitted = auxiliary_design @ np.linalg.lstsq(
        auxiliary_design, squared_residuals, rcond=None
    )[0]
    centred = squared_residuals - float(np.mean(squared_residuals))
    total = float(centred @ centred)
    if total <= np.finfo(float).eps:
        raise ValueError("squared residuals have no variation")
    residual = squared_residuals - fitted
    r_squared = float(np.clip(1.0 - (residual @ residual) / total, 0.0, 1.0))
    statistic = float(n * r_squared)
    df = rank - 1
    return HeteroskedasticityTest(
        statistic=statistic,
        p_value=_chi_square_sf(statistic, df),
        degrees_of_freedom=df,
        auxiliary_r_squared=r_squared,
    )


def heteroskedasticity_diagnostics(
    y: Sequence[float],
    x: Sequence[Sequence[float]],
) -> HeteroskedasticityDiagnostics:
    """Run Koenker studentized BP and White tests after OLS.

    Koenker BP regresses squared OLS residuals on the original design.
    White's test augments the design with all unique squares and pairwise
    products of nonconstant regressors. Constant columns are detected and
    represented once. Both LM statistics are n times auxiliary R-squared.
    """
    response = np.asarray(y, dtype=float)
    design = np.asarray(x, dtype=float)
    if response.ndim != 1 or response.size < 5:
        raise ValueError("y must be one-dimensional with at least five observations")
    n = response.size
    if design.ndim != 2 or design.shape[0] != n or design.shape[1] < 1:
        raise ValueError("X must be a two-dimensional matrix with one row per observation")
    if design.shape[1] >= n:
        raise ValueError("X must leave positive residual degrees of freedom")
    if not np.all(np.isfinite(response)) or not np.all(np.isfinite(design)):
        raise ValueError("y and X must contain only finite values")
    if np.linalg.matrix_rank(design) < design.shape[1]:
        raise ValueError("X must have full column rank")
    beta = np.linalg.lstsq(design, response, rcond=None)[0]
    residual = response - design @ beta
    sigma2 = float(residual @ residual / n)
    if not isfinite(sigma2) or sigma2 <= np.finfo(float).eps:
        raise ValueError("OLS must have positive variance")

    constant = np.ptp(design, axis=0) <= np.finfo(float).eps * np.maximum(
        1.0, np.max(np.abs(design), axis=0)
    ) * 16
    nonconstant = design[:, ~constant]
    if nonconstant.shape[1] == 0:
        raise ValueError("X must contain at least one nonconstant regressor")
    intercept = np.ones((n, 1))
    bp_design = np.column_stack((intercept, nonconstant))
    squared = residual ** 2
    bp = _auxiliary_test(squared, bp_design)

    white_terms = [intercept, nonconstant]
    for j in range(nonconstant.shape[1]):
        white_terms.append((nonconstant[:, j] ** 2)[:, None])
        for k in range(j + 1, nonconstant.shape[1]):
            white_terms.append((nonconstant[:, j] * nonconstant[:, k])[:, None])
    white_design = np.column_stack(white_terms)
    # Remove linearly dependent generated columns before the auxiliary fit.
    # SVD-based rank reduction keeps the fitted space unchanged.
    u, singular, _ = np.linalg.svd(white_design, full_matrices=False)
    rank = int(np.sum(singular > singular[0] * max(white_design.shape) * np.finfo(float).eps))
    white_basis = u[:, :rank]
    white = _auxiliary_test(squared, white_basis)
    return HeteroskedasticityDiagnostics(
        coefficients=tuple(float(v) for v in beta),
        residuals=tuple(float(v) for v in residual),
        sigma2_mle=sigma2,
        koenker_bp=bp,
        white=white,
    )

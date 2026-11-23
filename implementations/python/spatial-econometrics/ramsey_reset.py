"""Ramsey RESET functional-form diagnostic for OLS baselines.

The test augments the restricted OLS design with powers of fitted values and
uses a partial F test for their joint contribution. It diagnoses generic
functional-form misspecification; it is not a test for spatial dependence.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, lgamma
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class ResetResult:
    statistic: float
    p_value: float
    numerator_degrees_of_freedom: int
    denominator_degrees_of_freedom: int
    restricted_rss: float
    unrestricted_rss: float
    restricted_coefficients: tuple[float, ...]
    added_term_coefficients: tuple[float, ...]
    fitted_values: tuple[float, ...]


def _beta_continued_fraction(a: float, b: float, x: float) -> float:
    """Evaluate the continued fraction in the incomplete-beta identity."""
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    tiny = np.finfo(float).tiny / np.finfo(float).eps
    if abs(d) < tiny:
        d = tiny
    d = 1.0 / d
    h = d
    for m in range(1, 10001):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < tiny:
            d = tiny
        c = 1.0 + aa / c
        if abs(c) < tiny:
            c = tiny
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 3e-14:
            return h
    raise ArithmeticError("incomplete-beta continued fraction did not converge")


def _regularized_beta(x: float, a: float, b: float) -> float:
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    log_front = (a * np.log(x) + b * np.log1p(-x)
                 - (lgamma(a) + lgamma(b) - lgamma(a + b)))
    front = float(np.exp(log_front))
    if x < (a + 1.0) / (a + b + 2.0):
        return float(np.clip(front * _beta_continued_fraction(a, b, x) / a, 0.0, 1.0))
    return float(np.clip(1.0 - front * _beta_continued_fraction(b, a, 1.0 - x) / b,
                         0.0, 1.0))


def _f_survival(statistic: float, numerator_df: int, denominator_df: int) -> float:
    if statistic <= 0.0:
        return 1.0
    x = denominator_df / (denominator_df + numerator_df * statistic)
    return _regularized_beta(x, denominator_df / 2.0, numerator_df / 2.0)


def ramsey_reset_test(
    y: Sequence[float],
    x: Sequence[Sequence[float]],
    *,
    power: int = 3,
) -> ResetResult:
    """Run Ramsey's RESET using powers 2..power of restricted OLS fitted values.

    The restricted model is y = X beta + error. The unrestricted model adds
    y_hat**2 through y_hat**power. A partial F test evaluates their joint
    contribution. The numerator degrees of freedom equal the actual rank
    increase, so redundant fitted-value powers are not counted twice.
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
    if not isinstance(power, (int, np.integer)) or isinstance(power, bool) or power < 2:
        raise ValueError("power must be an integer of at least two")
    rank_x = int(np.linalg.matrix_rank(design))
    if rank_x != design.shape[1]:
        raise ValueError("X must have full column rank")

    beta = np.linalg.lstsq(design, response, rcond=None)[0]
    fitted = design @ beta
    restricted_residual = response - fitted
    rss_r = float(restricted_residual @ restricted_residual)
    if not isfinite(rss_r) or rss_r <= np.finfo(float).eps:
        raise ValueError("restricted OLS residual sum of squares must be positive")

    scale = max(1.0, float(np.max(np.abs(fitted))))
    normalised = fitted / scale
    added = np.column_stack([normalised ** degree for degree in range(2, power + 1)])
    unrestricted_design = np.column_stack((design, added))
    rank_u = int(np.linalg.matrix_rank(unrestricted_design))
    q = rank_u - rank_x
    df_den = n - rank_u
    if q < 1:
        raise ValueError("RESET fitted-value powers add no independent regressors")
    if df_den < 1:
        raise ValueError("RESET unrestricted model must leave residual degrees of freedom")
    coefficients = np.linalg.lstsq(unrestricted_design, response, rcond=None)[0]
    unrestricted_residual = response - unrestricted_design @ coefficients
    rss_u = float(unrestricted_residual @ unrestricted_residual)
    tolerance = np.finfo(float).eps * max(1.0, rss_r) * n * 64
    if rss_u > rss_r + tolerance:
        raise ArithmeticError("unrestricted OLS fit has larger residual sum of squares")
    rss_u = min(rss_u, rss_r)
    improvement = max(0.0, rss_r - rss_u)
    if rss_u <= np.finfo(float).eps:
        statistic = float("inf") if improvement > tolerance else 0.0
        p_value = 0.0 if np.isinf(statistic) else 1.0
    else:
        statistic = (improvement / q) / (rss_u / df_den)
        p_value = _f_survival(statistic, q, df_den)
    return ResetResult(
        statistic=float(statistic),
        p_value=float(p_value),
        numerator_degrees_of_freedom=q,
        denominator_degrees_of_freedom=df_den,
        restricted_rss=rss_r,
        unrestricted_rss=rss_u,
        restricted_coefficients=tuple(float(v) for v in beta),
        added_term_coefficients=tuple(float(v) for v in coefficients[design.shape[1]:]),
        fitted_values=tuple(float(v) for v in fitted),
    )

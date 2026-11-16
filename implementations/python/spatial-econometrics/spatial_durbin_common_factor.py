"""Likelihood-ratio test of the spatial Durbin common-factor restriction.

The null gamma + rho*beta = 0 reduces an SDM to a spatial-error model.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np

from heteroskedasticity_diagnostics import _chi_square_sf
from maximum_likelihood import spatial_durbin_mle, spatial_error_mle, _validate


@dataclass(frozen=True)
class SpatialDurbinCommonFactorResult:
    statistic: float
    p_value: float
    degrees_of_freedom: int
    rho_sdm: float
    beta_sdm: tuple[float, ...]
    gamma_sdm: tuple[float, ...]
    restriction_residuals: tuple[float, ...]
    log_likelihood_sdm: float
    log_likelihood_sem: float


def spatial_durbin_common_factor_test(
    y: Sequence[float],
    x: Sequence[Sequence[float]],
    weights: Sequence[Sequence[float]],
    *,
    grid_size: int = 201,
    tolerance: float = 1e-7,
) -> SpatialDurbinCommonFactorResult:
    """Test H0: gamma_j + rho*beta_j = 0 for identified WX columns.

    Fits unrestricted SDM and restricted SEM by concentrated Gaussian ML.
    The LR statistic is 2*(ll_SDM - ll_SEM), asymptotically chi-square with
    degrees of freedom equal to the number of linearly independent columns
    in WX after projection on X. Spatially lagged covariates collinear with
    X (notably a row-standardised intercept) are not separately identified
    and are not counted as restrictions.

    Inference is conditional on W and relies on the Gaussian ML model,
    regular identification and the usual likelihood-ratio asymptotics.
    """
    response, design, w, _ = _validate(y, x, weights)
    wx = w @ design
    current = design.copy()
    rank = np.linalg.matrix_rank(current)
    retained = []
    for j in range(design.shape[1]):
        candidate = np.column_stack((current, wx[:, j]))
        next_rank = np.linalg.matrix_rank(candidate)
        if next_rank > rank:
            retained.append(j)
            current = candidate
            rank = next_rank
    df = len(retained)
    if df == 0:
        raise ValueError("no independently identified spatially lagged covariates")

    unrestricted = spatial_durbin_mle(
        response, design, w, grid_size=grid_size, tolerance=tolerance
    )
    restricted = spatial_error_mle(
        response, design, w, grid_size=grid_size, tolerance=tolerance
    )
    difference = unrestricted.log_likelihood - restricted.log_likelihood
    numerical_tolerance = 1e-7 * max(
        1.0, abs(unrestricted.log_likelihood), abs(restricted.log_likelihood)
    )
    if difference < -numerical_tolerance:
        raise ArithmeticError(
            "unrestricted SDM likelihood fell below nested SEM likelihood; "
            "increase grid_size or inspect optimizer convergence"
        )
    statistic = float(2.0 * max(0.0, difference))
    beta = np.asarray(unrestricted.coefficients, dtype=float)
    gamma = np.asarray(unrestricted.spatial_covariate_coefficients, dtype=float)
    restrictions = gamma[retained] + unrestricted.spatial_parameter * beta[retained]
    return SpatialDurbinCommonFactorResult(
        statistic=statistic,
        p_value=_chi_square_sf(statistic, df),
        degrees_of_freedom=df,
        rho_sdm=float(unrestricted.spatial_parameter),
        beta_sdm=tuple(float(v) for v in beta),
        gamma_sdm=tuple(float(v) for v in gamma),
        restriction_residuals=tuple(float(v) for v in restrictions),
        log_likelihood_sdm=float(unrestricted.log_likelihood),
        log_likelihood_sem=float(restricted.log_likelihood),
    )

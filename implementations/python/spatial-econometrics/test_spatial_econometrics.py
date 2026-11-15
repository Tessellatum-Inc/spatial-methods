import numpy as np
import pytest

from diagnostics import spatial_lm_diagnostics
from impacts import spatial_impacts


CHAIN = np.array([
    [0., 1., 0., 0.],
    [1., 0., 1., 0.],
    [0., 1., 0., 1.],
    [0., 0., 1., 0.],
])


def test_spatial_lm_diagnostics_match_hand_computed_components():
    x = np.column_stack([np.ones(6), np.arange(6, dtype=float)])
    y = np.array([1.0, 2.2, 2.8, 4.4, 4.7, 6.3])
    w = np.zeros((6, 6))
    for i in range(5):
        w[i, i + 1] = w[i + 1, i] = 1.0
    result = spatial_lm_diagnostics(y, x, w)
    beta = np.linalg.lstsq(x, y, rcond=None)[0]
    e = y - x @ beta
    sigma2 = e @ e / len(y)
    trace = np.trace(w.T @ w + w @ w)
    lm_error = (e @ w @ e / sigma2) ** 2 / trace
    wxb = w @ (x @ beta)
    m_wxb = wxb - x @ np.linalg.lstsq(x, wxb, rcond=None)[0]
    denominator = m_wxb @ m_wxb / sigma2 + trace
    lm_lag = (e @ w @ y / sigma2) ** 2 / denominator
    assert result.lm_error.statistic == pytest.approx(lm_error)
    assert result.lm_lag.statistic == pytest.approx(lm_lag)
    assert 0 <= result.lm_error.p_value <= 1
    assert 0 <= result.lm_lag.p_value <= 1


def test_spatial_lm_diagnostics_uses_supplied_design():
    x = np.column_stack([np.ones(4), [0., 1., 2., 3.]])
    y = [1., 2.1, 2.9, 4.2]
    result = spatial_lm_diagnostics(y, x, CHAIN)
    assert len(result.coefficients) == 2
    assert len(result.residuals) == 4
    assert result.trace_term > 0
    assert result.lag_denominator >= result.trace_term


@pytest.mark.parametrize("bad_y,bad_x,bad_w", [
    ([1, 2], [[1], [1]], [[0, 1], [1, 0]]),
    ([1, 2, 3], [[1], [1]], [[0, 1], [1, 0]]),
    ([1, 2, 3], [[1], [1], [1]], [[0, 1], [1, 0]]),
    ([1, float("nan"), 3], [[1], [1], [1]], [[0, 1, 0], [1, 0, 1], [0, 1, 0]]),
    ([1, 2, 3], [[1], [1], [1]], [[0, -1, 0], [-1, 0, -1], [0, -1, 0]]),
    ([1, 2, 3], [[1], [1], [1]], [[1, 0, 0], [0, 0, 1], [0, 1, 0]]),
])
def test_spatial_lm_diagnostics_reject_invalid_inputs(bad_y, bad_x, bad_w):
    with pytest.raises(ValueError):
        spatial_lm_diagnostics(bad_y, bad_x, bad_w)


def test_spatial_lm_diagnostics_rejects_collinear_design_and_perfect_fit():
    with pytest.raises(ValueError, match="full column rank"):
        spatial_lm_diagnostics([1, 2, 3], [[1, 1], [1, 1], [1, 1]],
                               [[0, 1, 0], [1, 0, 1], [0, 1, 0]])
    with pytest.raises(ValueError, match="residual variance"):
        spatial_lm_diagnostics([1, 2, 3], [[1], [2], [3]],
                               [[0, 1, 0], [1, 0, 1], [0, 1, 0]])


def test_sar_impacts_reduce_to_beta_when_rho_and_gamma_are_zero():
    impacts = spatial_impacts(CHAIN, 0.0, [2.5, -1.0])
    assert [item.direct for item in impacts] == pytest.approx([2.5, -1.0])
    assert [item.indirect for item in impacts] == pytest.approx([0.0, 0.0])
    assert [item.total for item in impacts] == pytest.approx([2.5, -1.0])


def test_spatial_lag_impacts_include_feedback_spillovers():
    impact, = spatial_impacts(CHAIN, 0.2, [2.0])
    matrix = np.linalg.inv(np.eye(4) - 0.2 * CHAIN) * 2.0
    np.testing.assert_allclose(np.asarray(impact.impact_matrix), matrix)
    assert impact.direct == pytest.approx(np.trace(matrix) / 4)
    assert impact.total == pytest.approx(np.sum(matrix) / 4)
    assert impact.indirect == pytest.approx(impact.total - impact.direct)


def test_sdm_impacts_include_lagged_covariate_effects():
    impact, = spatial_impacts(CHAIN, 0.15, [1.5], [0.75])
    matrix = np.linalg.solve(np.eye(4) - 0.15 * CHAIN,
                             1.5 * np.eye(4) + 0.75 * CHAIN)
    np.testing.assert_allclose(np.asarray(impact.impact_matrix), matrix)
    assert impact.total == pytest.approx(np.sum(matrix) / 4)


def test_spatial_impacts_validate_shapes_and_singularity():
    with pytest.raises(ValueError, match="gamma"):
        spatial_impacts(CHAIN, 0.1, [1.0, 2.0], [0.5])
    with pytest.raises(ValueError, match="nonsingular"):
        spatial_impacts(np.ones((2, 2)), 1.0, [1.0])
    with pytest.raises(ValueError, match="finite"):
        spatial_impacts([[0, float("nan")], [1, 0]], 0.1, [1.0])

def test_spatial_lag_2sls_recovers_parameters_on_synthetic_sar_data():
    from spatial_2sls import spatial_lag_2sls
    rng = np.random.default_rng(2026)
    n = 80
    weights = np.zeros((n, n))
    for i in range(n - 1):
        weights[i, i + 1] = weights[i + 1, i] = 1.0
    row_sums = weights.sum(axis=1)
    weights = weights / row_sums[:, None]
    x_value = rng.normal(size=n)
    x = np.column_stack([np.ones(n), x_value])
    beta = np.array([1.2, 0.8])
    rho = 0.3
    error = rng.normal(scale=0.15, size=n)
    y = np.linalg.solve(np.eye(n) - rho * weights, x @ beta + error)
    result = spatial_lag_2sls(y, x, weights, instrument_orders=1)
    assert result.rho == pytest.approx(rho, abs=0.18)
    assert result.beta == pytest.approx(beta, abs=0.18)
    assert len(result.residuals) == n
    assert result.instruments_used >= 3


def test_spatial_lag_2sls_rejects_underidentified_and_invalid_inputs():
    from spatial_2sls import spatial_lag_2sls
    x = np.column_stack([np.ones(4), [0., 1., 2., 3.]])
    w = CHAIN
    with pytest.raises(ValueError, match="instrument_orders"):
        spatial_lag_2sls([1., 2., 3., 4.], x, w, instrument_orders=0)
    with pytest.raises(ValueError, match="finite"):
        spatial_lag_2sls([1., 2., float("nan"), 4.], x, w)
    with pytest.raises(ValueError):
        spatial_lag_2sls([1., 2., 3., 4.], x, np.zeros((4, 4)))


def _row_standardised_chain(n):
    weights = np.zeros((n, n))
    for i in range(n - 1):
        weights[i, i + 1] = weights[i + 1, i] = 1.0
    return weights / weights.sum(axis=1, keepdims=True)


def test_spatial_lag_mle_recovers_synthetic_sar_parameters():
    from maximum_likelihood import spatial_lag_mle
    rng = np.random.default_rng(20261115)
    n = 70
    w = _row_standardised_chain(n)
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    beta = np.array([1.3, -0.65])
    rho = 0.28
    epsilon = rng.normal(scale=0.12, size=n)
    y = np.linalg.solve(np.eye(n) - rho * w, x @ beta + epsilon)
    fit = spatial_lag_mle(y, x, w, grid_size=161)
    assert fit.model == "SAR"
    assert fit.spatial_parameter == pytest.approx(rho, abs=0.14)
    assert fit.coefficients == pytest.approx(beta, abs=0.15)
    assert fit.sigma2_mle > 0
    assert np.isfinite(fit.log_likelihood)
    assert len(fit.fitted) == n
    assert len(fit.residuals) == n
    assert fit.rho_bounds[0] < fit.spatial_parameter < fit.rho_bounds[1]
    assert fit.evaluations > 161


def test_spatial_error_mle_recovers_synthetic_sem_parameters():
    from maximum_likelihood import spatial_error_mle
    rng = np.random.default_rng(771)
    n = 70
    w = _row_standardised_chain(n)
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    beta = np.array([0.9, 0.75])
    lam = 0.36
    innovation = rng.normal(scale=0.15, size=n)
    error = np.linalg.solve(np.eye(n) - lam * w, innovation)
    y = x @ beta + error
    fit = spatial_error_mle(y, x, w, grid_size=161)
    assert fit.model == "SEM"
    assert fit.spatial_parameter == pytest.approx(lam, abs=0.18)
    assert fit.coefficients == pytest.approx(beta, abs=0.16)
    assert fit.sigma2_mle > 0
    assert np.isfinite(fit.log_likelihood)
    assert len(fit.fitted) == n
    assert len(fit.residuals) == n


def test_spatial_mle_rejects_invalid_inputs_and_grid_settings():
    from maximum_likelihood import spatial_lag_mle, spatial_error_mle
    x = np.column_stack([np.ones(5), np.arange(5, dtype=float)])
    w = np.zeros((5, 5))
    for i in range(4):
        w[i, i + 1] = w[i + 1, i] = 1.0
    with pytest.raises(ValueError, match="at least five"):
        spatial_lag_mle([1., 2., 3., 4.], np.ones((4, 1)), CHAIN)
    with pytest.raises(ValueError, match="grid_size"):
        spatial_error_mle([1., 2., 3., 4., 5.], x, w, grid_size=5)
    with pytest.raises(ValueError, match="tolerance"):
        spatial_error_mle([1., 2., 3., 4., 5.], x, w, tolerance=0.0)
    with pytest.raises(ValueError, match="full column rank"):
        spatial_lag_mle([1., 2., 3., 4., 5.], np.ones((5, 2)), w)
    with pytest.raises(ValueError, match="finite"):
        spatial_error_mle([1., 2., float("nan"), 4., 5.], x, w)


def test_spatial_lm_robust_scores_match_bera_yoon_adjustments():
    from diagnostics import spatial_lm_diagnostics
    x = np.column_stack([np.ones(6), np.arange(6, dtype=float)])
    y = np.array([1.0, 2.2, 2.8, 4.4, 4.7, 6.3])
    w = np.zeros((6, 6))
    for i in range(5):
        w[i, i + 1] = w[i + 1, i] = 1.0
    result = spatial_lm_diagnostics(y, x, w)
    beta = np.linalg.lstsq(x, y, rcond=None)[0]
    e = y - x @ beta
    sigma2 = e @ e / len(y)
    trace = np.trace(w.T @ w + w @ w)
    wxb = w @ (x @ beta)
    residualised = wxb - x @ np.linalg.lstsq(x, wxb, rcond=None)[0]
    d = residualised @ residualised / sigma2 + trace
    d_lag = e @ (w @ y) / sigma2
    d_error = e @ (w @ e) / sigma2
    expected_lag = (d_lag - d_error) ** 2 / (d - trace)
    expected_error = (d_error - trace * d_lag / d) ** 2 / (trace * (1 - trace / d))
    assert result.robust_lm_lag is not None
    assert result.robust_lm_error is not None
    assert result.robust_lm_lag.statistic == pytest.approx(expected_lag)
    assert result.robust_lm_error.statistic == pytest.approx(expected_error)
    assert 0 <= result.robust_lm_lag.p_value <= 1
    assert 0 <= result.robust_lm_error.p_value <= 1


def test_spatial_lm_robust_tests_are_unavailable_when_not_identified():
    from diagnostics import spatial_lm_diagnostics
    n = 6
    w = np.zeros((n, n))
    for i in range(n):
        w[i, (i - 1) % n] = 0.5
        w[i, (i + 1) % n] = 0.5
    x = np.ones((n, 1))
    y = np.array([1.0, 2.0, 1.5, 3.0, 2.5, 4.0])
    result = spatial_lm_diagnostics(y, x, w)
    assert result.lag_denominator == pytest.approx(result.trace_term)
    assert result.robust_lm_lag is None
    assert result.robust_lm_error is None


def _row_standardised_path(n):
    weights = np.zeros((n, n))
    for i in range(n - 1):
        weights[i, i + 1] = weights[i + 1, i] = 1.0
    return weights / weights.sum(axis=1, keepdims=True)


def test_spatial_durbin_2sls_recovers_synthetic_sdm_parameters():
    from spatial_durbin_2sls import spatial_durbin_2sls
    rng = np.random.default_rng(91827)
    n = 250
    w = _row_standardised_path(n)
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    beta = np.array([1.1, 0.85])
    gamma = np.array([0.0, -0.3])
    rho = 0.24
    innovation = rng.normal(scale=0.03, size=n)
    wx = w @ x
    y = np.linalg.solve(
        np.eye(n) - rho * w,
        x @ beta + wx @ gamma + innovation,
    )
    fit = spatial_durbin_2sls(y, x, w, instrument_orders=5)
    assert fit.rho == pytest.approx(rho, abs=0.12)
    assert fit.beta == pytest.approx(beta, abs=0.12)
    assert fit.gamma[0] == pytest.approx(0.0, abs=1e-10)
    assert fit.gamma[1] == pytest.approx(gamma[1], abs=0.08)
    assert fit.instruments_used >= fit.regressors
    assert len(fit.fitted) == n
    assert len(fit.residuals) == n
    assert np.all(np.isfinite(fit.residuals))


def test_spatial_durbin_2sls_validates_inputs_and_instrument_order():
    from spatial_durbin_2sls import spatial_durbin_2sls
    n = 8
    w = _row_standardised_path(n)
    x = np.column_stack([np.ones(n), np.arange(n, dtype=float)])
    y = np.arange(n, dtype=float) + np.array([0.1, -0.2, 0.1, 0.2, -0.1, 0.1, -0.1, 0.0])
    with pytest.raises(ValueError, match="instrument_orders"):
        spatial_durbin_2sls(y, x, w, instrument_orders=1)
    with pytest.raises(ValueError, match="finite"):
        spatial_durbin_2sls([1., 2., 3., 4., 5., 6., 7., float("nan")], x, w)
    with pytest.raises(ValueError, match="full column rank"):
        spatial_durbin_2sls(y, np.ones((n, 2)), w)


def test_spatial_durbin_2sls_rejects_underidentified_complete_graph():
    from spatial_durbin_2sls import spatial_durbin_2sls
    n = 12
    w = (np.ones((n, n)) - np.eye(n)) / (n - 1)
    x = np.column_stack([np.ones(n), np.linspace(-1.0, 1.0, n)])
    y = np.array([1.0, 1.7, 1.2, 2.4, 1.9, 3.1, 2.7, 3.6, 3.0, 4.1, 3.8, 4.7])
    with pytest.raises(ValueError, match="underidentified SDM"):
        spatial_durbin_2sls(y, x, w, instrument_orders=4)


def test_spatial_durbin_mle_recovers_synthetic_sdm_parameters():
    from maximum_likelihood import spatial_durbin_mle
    rng = np.random.default_rng(20261115)
    n = 90
    w = _row_standardised_path(n)
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    beta = np.array([1.0, 0.7])
    gamma = np.array([0.0, -0.25])
    rho = 0.22
    epsilon = rng.normal(scale=0.16, size=n)
    y = np.linalg.solve(
        np.eye(n) - rho * w,
        x @ beta + (w @ x) @ gamma + epsilon,
    )
    fit = spatial_durbin_mle(y, x, w, grid_size=161)
    assert fit.model == "SDM"
    assert fit.spatial_parameter == pytest.approx(rho, abs=0.17)
    assert fit.coefficients == pytest.approx(beta, abs=0.20)
    assert fit.spatial_covariate_coefficients[0] == pytest.approx(0.0, abs=1e-10)
    assert fit.spatial_covariate_coefficients[1] == pytest.approx(gamma[1], abs=0.20)
    assert fit.sigma2_mle > 0
    assert np.isfinite(fit.log_likelihood)
    assert len(fit.fitted) == n
    assert len(fit.residuals) == n


def test_spatial_durbin_mle_rejects_rank_deficient_augmented_design():
    from maximum_likelihood import spatial_durbin_mle
    n = 12
    w = (np.ones((n, n)) - np.eye(n)) / (n - 1)
    x = np.column_stack([np.ones(n), np.linspace(-1.0, 1.0, n)])
    y = np.array([1.0, 1.7, 1.2, 2.4, 1.9, 3.1, 2.7, 3.6, 3.0, 4.1, 3.8, 4.7])
    # On a complete row-standardised graph, WX is in span(X), so the SDM
    # collapses to SAR and gamma is not separately identified.
    fit = spatial_durbin_mle(y, x, w, grid_size=41)
    assert fit.spatial_covariate_coefficients == pytest.approx((0.0, 0.0))
    with pytest.raises(ValueError, match="grid_size"):
        spatial_durbin_mle(y, x, w, grid_size=10)


def test_spatial_sarar_mle_recovers_synthetic_sarar_parameters():
    from maximum_likelihood import spatial_sarar_mle
    rng = np.random.default_rng(20261116)
    n = 75
    w = _row_standardised_chain(n)
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    beta = np.array([1.2, -0.55])
    rho, lam = 0.22, 0.38
    innovation = rng.normal(scale=0.12, size=n)
    spatial_error = np.linalg.solve(np.eye(n) - lam * w, innovation)
    y = np.linalg.solve(np.eye(n) - rho * w, x @ beta + spatial_error)
    fit = spatial_sarar_mle(y, x, w, grid_size=31, tolerance=1e-6)
    assert fit.model == "SARAR"
    assert fit.spatial_parameter == pytest.approx(rho, abs=0.12)
    assert fit.error_parameter == pytest.approx(lam, abs=0.20)
    assert fit.coefficients == pytest.approx(beta, abs=0.18)
    assert fit.sigma2_mle > 0
    assert np.isfinite(fit.log_likelihood)
    assert len(fit.fitted) == n
    assert len(fit.residuals) == n
    assert fit.evaluations > 31 ** 2


def test_spatial_sarar_mle_validates_search_controls():
    from maximum_likelihood import spatial_sarar_mle
    n = 10
    w = _row_standardised_chain(n)
    x = np.column_stack([np.ones(n), np.arange(n, dtype=float)])
    y = np.array([1.0, 1.7, 1.2, 2.4, 1.9, 3.1, 2.7, 3.6, 3.0, 4.1])
    with pytest.raises(ValueError, match="grid_size"):
        spatial_sarar_mle(y, x, w, grid_size=5)
    with pytest.raises(ValueError, match="coordinate_iterations"):
        spatial_sarar_mle(y, x, w, coordinate_iterations=0)
    with pytest.raises(ValueError, match="tolerance"):
        spatial_sarar_mle(y, x, w, tolerance=0.0)


def test_spatial_impact_uncertainty_zero_covariance_collapses_to_point_impacts():
    from impacts import spatial_impact_uncertainty
    rho, beta, gamma = 0.15, [1.5], [0.4]
    mean = np.array([rho, beta[0], gamma[0]])
    result, = spatial_impact_uncertainty(
        CHAIN, rho, beta, np.zeros((3, 3)), gamma,
        draws=200, seed=123,
    )
    point, = spatial_impacts(CHAIN, rho, beta, gamma)
    assert result.accepted_draws == 200
    assert result.rejected_draws == 0
    assert result.direct.estimate == pytest.approx(point.direct)
    assert result.indirect.estimate == pytest.approx(point.indirect)
    assert result.total.estimate == pytest.approx(point.total)
    assert result.direct.standard_error == pytest.approx(0.0, abs=1e-12)
    assert result.direct.lower == pytest.approx(point.direct)
    assert result.direct.upper == pytest.approx(point.direct)


def test_spatial_impact_uncertainty_uses_joint_parameter_covariance():
    from impacts import spatial_impact_uncertainty
    w = _row_standardised_chain(8)
    covariance = np.diag([0.0025, 0.01, 0.01, 0.01, 0.01])
    result, = spatial_impact_uncertainty(
        w, 0.2, [1.0, 0.5], covariance, [0.0, 0.2],
        draws=1200, seed=77,
    )
    assert result.accepted_draws + result.rejected_draws == 1200
    assert result.direct.standard_error > 0
    assert result.indirect.standard_error > 0
    assert result.total.lower < result.total.upper
    assert result.direct.lower < result.direct.estimate < result.direct.upper


def test_spatial_impact_uncertainty_validates_covariance_and_draw_controls():
    from impacts import spatial_impact_uncertainty
    with pytest.raises(ValueError, match="covariance shape"):
        spatial_impact_uncertainty(CHAIN, 0.1, [1.0], np.eye(2), draws=100)
    with pytest.raises(ValueError, match="positive semidefinite"):
        spatial_impact_uncertainty(CHAIN, 0.1, [1.0], [[1.0, 2.0], [2.0, 1.0]], draws=100)
    with pytest.raises(ValueError, match="draws"):
        spatial_impact_uncertainty(CHAIN, 0.1, [1.0], np.eye(2), draws=10)


def _row_standardised_line(n):
    matrix = np.zeros((n, n))
    for i in range(n - 1):
        matrix[i, i + 1] = matrix[i + 1, i] = 1.0
    return matrix / matrix.sum(axis=1, keepdims=True)


def test_slx_ols_recovers_spatial_covariate_effects():
    from slx_sdem import spatial_lx_ols
    rng = np.random.default_rng(4421)
    n = 120
    w = _row_standardised_line(n)
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    beta = np.array([1.1, 0.7])
    gamma = np.array([0.0, -0.45])
    y = x @ beta + (w @ x) @ gamma + rng.normal(scale=0.08, size=n)
    fit = spatial_lx_ols(y, x, w)
    assert fit.coefficients == pytest.approx(beta, abs=0.06)
    assert fit.spatial_covariate_coefficients == pytest.approx(gamma, abs=0.08)
    assert fit.spatial_covariate_coefficients[0] == 0.0
    assert len(fit.residuals) == n
    assert fit.sigma2_ols > 0


def test_sdem_mle_recovers_spatial_error_and_lagged_covariate_effects():
    from slx_sdem import spatial_dem_mle
    rng = np.random.default_rng(77219)
    n = 100
    w = _row_standardised_line(n)
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    beta = np.array([0.8, 0.55])
    gamma = np.array([0.0, -0.35])
    lam = 0.28
    innovation = rng.normal(scale=0.1, size=n)
    error = np.linalg.solve(np.eye(n) - lam * w, innovation)
    y = x @ beta + (w @ x) @ gamma + error
    fit = spatial_dem_mle(y, x, w, grid_size=61)
    assert fit.error_parameter == pytest.approx(lam, abs=0.2)
    assert fit.coefficients == pytest.approx(beta, abs=0.15)
    assert fit.spatial_covariate_coefficients == pytest.approx(gamma, abs=0.2)
    assert fit.spatial_covariate_coefficients[0] == 0.0
    assert np.isfinite(fit.log_likelihood)
    assert len(fit.fitted) == n


def test_slx_sdem_reject_invalid_inputs_and_search_controls():
    from slx_sdem import spatial_lx_ols, spatial_dem_mle
    n = 10
    w = _row_standardised_line(n)
    x = np.column_stack([np.ones(n), np.arange(n, dtype=float)])
    y = np.array([1.0, 2.2, 2.8, 4.4, 4.7, 6.3, 7.1, 8.2, 8.8, 10.1])
    with pytest.raises(ValueError, match="finite"):
        spatial_lx_ols([1, 2, 3, 4, 5, 6, 7, 8, float("nan"), 10], x, w)
    with pytest.raises(ValueError, match="full column rank"):
        spatial_lx_ols(y, np.ones((n, 2)), w)
    with pytest.raises(ValueError, match="grid_size"):
        spatial_dem_mle(y, x, w, grid_size=5)

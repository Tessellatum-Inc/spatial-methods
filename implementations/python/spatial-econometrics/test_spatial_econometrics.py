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
        spatial_impacts([[0.0, 1.0], [1.0, 0.0]], 1.0, [1.0])
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
    results = spatial_impact_uncertainty(
        w, 0.2, [1.0, 0.5], covariance, [0.0, 0.2],
        draws=1200, seed=77,
    )
    assert len(results) == 2
    result = results[0]
    assert result.accepted_draws + result.rejected_draws == 1200
    assert result.direct.standard_error > 0
    assert result.indirect.standard_error > 0
    assert result.total.lower < result.total.upper
    assert result.direct.lower < result.direct.estimate < result.direct.upper


def test_spatial_impact_uncertainty_validates_covariance_and_draw_controls():
    from impacts import spatial_impact_uncertainty
    with pytest.raises(ValueError, match="covariance shape"):
        spatial_impact_uncertainty(CHAIN, 0.1, [1.0], np.eye(3), draws=100)
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


def _symmetric_grid_adjacency(rows, cols):
    n = rows * cols
    a = np.zeros((n, n))
    for row in range(rows):
        for col in range(cols):
            i = row * cols + col
            if row + 1 < rows:
                j = (row + 1) * cols + col
                a[i, j] = a[j, i] = 1.0
            if col + 1 < cols:
                j = row * cols + col + 1
                a[i, j] = a[j, i] = 1.0
    return a


def test_proper_car_mle_recovers_synthetic_dependence_and_regression():
    from proper_car import proper_car_mle
    rng = np.random.default_rng(18031)
    adjacency = _symmetric_grid_adjacency(8, 8)
    n = adjacency.shape[0]
    degree = adjacency.sum(axis=1)
    alpha = 0.32
    tau = 3.5
    precision_base = np.diag(degree) - alpha * adjacency
    chol = np.linalg.cholesky(precision_base)
    error = np.linalg.solve(chol.T, rng.normal(size=n)) / np.sqrt(tau)
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    beta = np.array([1.4, -0.65])
    y = x @ beta + error
    fit = proper_car_mle(y, x, adjacency, grid_size=101)
    assert fit.alpha == pytest.approx(alpha, abs=0.22)
    assert fit.coefficients == pytest.approx(beta, abs=0.22)
    assert fit.tau > 0
    assert fit.variance_scale == pytest.approx(1.0 / fit.tau)
    np.testing.assert_allclose(fit.conditional_variances, 1.0 / (fit.tau * adjacency.sum(axis=1)))
    assert np.isfinite(fit.log_likelihood)
    assert len(fit.residuals) == n
    assert fit.alpha_bounds[0] < fit.alpha < fit.alpha_bounds[1]


def test_proper_car_mle_alpha_zero_and_precision_are_valid():
    from proper_car import proper_car_mle
    rng = np.random.default_rng(2801)
    adjacency = _symmetric_grid_adjacency(5, 6)
    n = adjacency.shape[0]
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    y = x @ np.array([0.5, 1.2]) + rng.normal(scale=0.25, size=n)
    fit = proper_car_mle(y, x, adjacency)
    assert np.isfinite(fit.alpha)
    assert np.isfinite(fit.log_likelihood)
    assert fit.tau > 0
    assert fit.evaluations > 0


def test_proper_car_mle_rejects_invalid_graphs_and_controls():
    from proper_car import proper_car_mle
    n = 12
    x = np.column_stack([np.ones(n), np.arange(n, dtype=float)])
    y = np.linspace(0.1, 2.0, n) + np.sin(np.arange(n))
    adjacency = _symmetric_grid_adjacency(3, 4)
    with pytest.raises(ValueError, match="symmetric"):
        proper_car_mle(y, x, adjacency + np.triu(np.ones((n, n)), 1) * 0.1)
    isolated = adjacency.copy()
    isolated[0, :] = 0.0
    isolated[:, 0] = 0.0
    with pytest.raises(ValueError, match="positive degree"):
        proper_car_mle(y, x, isolated)
    with pytest.raises(ValueError, match="grid_size"):
        proper_car_mle(y, x, adjacency, grid_size=10)
    with pytest.raises(ValueError, match="full column rank"):
        proper_car_mle(y, np.ones((n, 2)), adjacency)



def _icar_test_adjacency():
    adjacency = np.zeros((7, 7))
    for i in range(4):
        adjacency[i, i + 1] = adjacency[i + 1, i] = 1.0
    adjacency[5, 6] = adjacency[6, 5] = 1.0
    return adjacency


def test_icar_sample_enforces_componentwise_sum_to_zero_and_reproducibility():
    from icar import icar_sample
    adjacency = _icar_test_adjacency()
    first = icar_sample(adjacency, precision=2.5, rng=731)
    second = icar_sample(adjacency, precision=2.5, rng=731)
    assert first.field == second.field
    assert first.n_components == 2
    assert first.component_labels[:5] == (0, 0, 0, 0, 0)
    assert first.component_labels[5:] == (1, 1)
    field = np.asarray(first.field)
    assert field[:5].sum() == pytest.approx(0.0, abs=1e-12)
    assert field[5:].sum() == pytest.approx(0.0, abs=1e-12)
    assert np.isfinite(first.log_pseudodeterminant)
    assert first.precision == 2.5


def test_icar_sample_respects_precision_scale_and_returns_finite_field():
    from icar import icar_sample
    adjacency = _symmetric_grid_adjacency(4, 4)
    sample = icar_sample(adjacency, precision=4.0, rng=912)
    field = np.asarray(sample.field)
    assert sample.n_components == 1
    assert field.sum() == pytest.approx(0.0, abs=1e-11)
    assert np.all(np.isfinite(field))
    assert sample.log_pseudodeterminant > 0


def test_icar_sample_rejects_invalid_graphs_and_precision():
    from icar import icar_sample
    adjacency = _symmetric_grid_adjacency(3, 4)
    with pytest.raises(ValueError, match="symmetric"):
        icar_sample(adjacency + np.triu(np.ones_like(adjacency), 1) * 0.1)
    isolated = adjacency.copy()
    isolated[0, :] = 0.0
    isolated[:, 0] = 0.0
    with pytest.raises(ValueError, match="positive degree"):
        icar_sample(isolated)
    with pytest.raises(ValueError, match="precision"):
        icar_sample(adjacency, precision=0.0)


def test_spatial_hac_ols_reduces_to_hc0_when_no_distinct_pairs_overlap():
    from spatial_hac import spatial_hac_ols
    rng = np.random.default_rng(128)
    n = 30
    coordinates = np.column_stack([np.arange(n, dtype=float) * 10.0, np.zeros(n)])
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    y = x @ np.array([1.2, -0.4]) + rng.normal(size=n)
    fit = spatial_hac_ols(y, x, coordinates, bandwidth=1.0,
                          small_sample_correction=False)
    beta = np.linalg.lstsq(x, y, rcond=None)[0]
    residual = y - x @ beta
    bread = np.linalg.inv(x.T @ x)
    expected = bread @ ((x * residual[:, None]).T @ (x * residual[:, None])) @ bread
    np.testing.assert_allclose(fit.covariance, expected, atol=1e-12)
    assert fit.nonzero_off_diagonal_pairs == 0
    assert fit.coefficients == pytest.approx(beta)


def test_spatial_hac_ols_includes_nearby_cross_products_and_is_symmetric():
    from spatial_hac import spatial_hac_ols
    rng = np.random.default_rng(882)
    n = 40
    coordinates = np.column_stack([np.arange(n, dtype=float), np.zeros(n)])
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    common = rng.normal(size=n)
    error = common * 0.35 + rng.normal(scale=0.5, size=n)
    y = x @ np.array([0.7, 0.9]) + error
    fit = spatial_hac_ols(y, x, coordinates, bandwidth=3.5)
    covariance = np.asarray(fit.covariance)
    np.testing.assert_allclose(covariance, covariance.T, atol=1e-12)
    assert fit.nonzero_off_diagonal_pairs > 0
    assert np.all(np.asarray(fit.standard_errors) >= 0)
    assert np.linalg.eigvalsh(covariance).min() > -1e-10
    assert fit.small_sample_correction is True


def test_spatial_hac_ols_rejects_invalid_inputs():
    from spatial_hac import spatial_hac_ols
    x = np.column_stack([np.ones(8), np.arange(8, dtype=float)])
    y = np.linspace(1.0, 3.0, 8) + np.sin(np.arange(8))
    coordinates = np.column_stack([np.arange(8, dtype=float), np.zeros(8)])
    with pytest.raises(ValueError, match="bandwidth"):
        spatial_hac_ols(y, x, coordinates, bandwidth=0.0)
    with pytest.raises(ValueError, match="planar"):
        spatial_hac_ols(y, x, np.arange(8, dtype=float), bandwidth=2.0)
    with pytest.raises(ValueError, match="full column rank"):
        spatial_hac_ols(y, np.ones((8, 2)), coordinates, bandwidth=2.0)


def test_spatial_lag_gmm_recovers_synthetic_heteroskedastic_sar_parameters():
    from spatial_gmm import spatial_lag_gmm
    rng = np.random.default_rng(12)
    n = 100
    w = _row_standardised_chain(n)
    x_value = rng.normal(size=n)
    x = np.column_stack([np.ones(n), x_value])
    beta = np.array([1.1, 0.7])
    rho = 0.25
    error = rng.normal(size=n) * (0.12 + 0.12 * np.abs(x_value))
    y = np.linalg.solve(np.eye(n) - rho * w, x @ beta + error)
    fit = spatial_lag_gmm(y, x, w, instrument_orders=2)
    assert fit.rho == pytest.approx(rho, abs=0.10)
    assert fit.beta == pytest.approx(beta, abs=0.10)
    assert len(fit.standard_errors) == 3
    assert np.all(np.asarray(fit.standard_errors) > 0)
    covariance = np.asarray(fit.covariance)
    np.testing.assert_allclose(covariance, covariance.T, atol=1e-12)
    assert np.linalg.eigvalsh(covariance).min() >= -1e-10
    assert fit.instruments_used == 4
    assert fit.j_degrees_of_freedom == 1
    assert fit.j_statistic >= 0
    assert fit.second_step_objective >= 0
    assert fit.first_step_objective >= 0


def test_spatial_lag_gmm_returns_zero_j_for_exactly_identified_model():
    from spatial_gmm import spatial_lag_gmm
    rng = np.random.default_rng(91)
    n = 60
    w = _row_standardised_chain(n)
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    y = np.linalg.solve(np.eye(n) - 0.2 * w,
                        x @ np.array([0.8, -0.3]) + rng.normal(scale=0.2, size=n))
    # A two-column X with one independent WX column gives three instruments
    # for the three structural regressors: the model is exactly identified.
    fit = spatial_lag_gmm(y, x, w, instrument_orders=1)
    assert fit.instruments_used == fit.regressors
    assert fit.j_degrees_of_freedom == 0
    assert fit.j_statistic == pytest.approx(0.0, abs=1e-12)


def test_spatial_lag_gmm_rejects_invalid_or_underidentified_inputs():
    from spatial_gmm import spatial_lag_gmm
    x = np.ones((8, 1))
    y = np.sin(np.arange(8, dtype=float))
    w = np.zeros((8, 8))
    for i in range(7):
        w[i, i + 1] = w[i + 1, i] = 1.0
    w = w / w.sum(axis=1, keepdims=True)
    with pytest.raises(ValueError, match="instrument_orders"):
        spatial_lag_gmm(y, x, w, instrument_orders=0)
    with pytest.raises(ValueError, match="finite"):
        spatial_lag_gmm([1, 2, 3, 4, 5, 6, float("nan"), 8], x, w)
    with pytest.raises(ValueError, match="identify"):
        spatial_lag_gmm(y, x, w, instrument_orders=1)


def test_spatial_error_gmm_recovers_synthetic_kp_parameters():
    from spatial_error_gmm import spatial_error_gmm
    rng = np.random.default_rng(2718)
    n = 120
    w = _row_standardised_chain(n)
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    beta = np.array([1.25, -0.55])
    lam = 0.38
    innovation = rng.normal(scale=0.35, size=n)
    error = np.linalg.solve(np.eye(n) - lam * w, innovation)
    y = x @ beta + error
    fit = spatial_error_gmm(y, x, w, grid_size=501)
    assert fit.lambda_ == pytest.approx(lam, abs=0.16)
    assert fit.beta == pytest.approx(beta, abs=0.15)
    assert fit.innovation_variance > 0
    assert len(fit.filtered_innovations) == n
    assert len(fit.standard_errors) == 2
    covariance = np.asarray(fit.covariance)
    np.testing.assert_allclose(covariance, covariance.T, atol=1e-12)
    assert np.linalg.eigvalsh(covariance).min() > 0
    assert fit.moment_objective >= 0
    assert len(fit.moment_residuals) == 3


def test_spatial_error_gmm_handles_zero_spatial_error_and_custom_bounds():
    from spatial_error_gmm import spatial_error_gmm
    rng = np.random.default_rng(44)
    n = 100
    w = _row_standardised_chain(n)
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    y = x @ np.array([0.7, 1.1]) + rng.normal(scale=0.2, size=n)
    fit = spatial_error_gmm(y, x, w, rho_bounds=(-0.8, 0.8), grid_size=301)
    assert abs(fit.lambda_) < 0.35
    assert fit.rho_bounds == (-0.8, 0.8)


def test_spatial_error_gmm_rejects_invalid_inputs():
    from spatial_error_gmm import spatial_error_gmm
    n = 12
    w = _row_standardised_chain(n)
    x = np.column_stack([np.ones(n), np.arange(n, dtype=float)])
    y = np.sin(np.arange(n, dtype=float))
    with pytest.raises(ValueError, match="grid_size"):
        spatial_error_gmm(y, x, w, grid_size=10)
    with pytest.raises(ValueError, match="full column rank"):
        spatial_error_gmm(y, np.ones((n, 2)), w)
    with pytest.raises(ValueError, match="finite"):
        spatial_error_gmm([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, float("nan")], x, w)
    with pytest.raises(ValueError, match="zero diagonal"):
        bad = w.copy()
        bad[0, 0] = 0.1
        spatial_error_gmm(y, x, bad)


def test_spatial_lag_instrument_diagnostics_reports_classical_and_hc1_strength():
    from instrument_diagnostics import spatial_lag_instrument_diagnostics
    rng = np.random.default_rng(7021)
    n = 180
    w = _row_standardised_chain(n)
    x_value = rng.normal(size=n)
    x = np.column_stack([np.ones(n), x_value])
    innovation = rng.normal(scale=0.35, size=n)
    y = np.linalg.solve(np.eye(n) - 0.55 * w, x @ np.array([0.8, 1.2]) + innovation)
    result = spatial_lag_instrument_diagnostics(y, x, w, instrument_orders=2)
    assert result.partial_r_squared > 0.1
    assert result.classical_partial_f > 10
    assert result.robust_wald_f > 0
    assert result.excluded_instruments == 2
    assert result.instruments_used == 4
    assert result.classical_f_numerator_df == 2
    assert result.classical_f_denominator_df == n - 4
    assert len(result.first_stage_standard_errors_hc1) == 4
    assert 0 <= result.partial_r_squared <= 1


def test_spatial_lag_instrument_diagnostics_flags_weak_relevance_without_rule_of_thumb():
    from instrument_diagnostics import spatial_lag_instrument_diagnostics
    rng = np.random.default_rng(7022)
    n = 160
    w = _row_standardised_chain(n)
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    y = rng.normal(size=n)
    result = spatial_lag_instrument_diagnostics(y, x, w, instrument_orders=2)
    assert result.partial_r_squared < 0.12
    assert result.classical_partial_f < 10
    assert result.robust_wald_f >= 0


def test_spatial_lag_instrument_diagnostics_drops_redundant_lagged_intercept():
    from instrument_diagnostics import spatial_lag_instrument_diagnostics
    rng = np.random.default_rng(7023)
    n = 80
    w = _row_standardised_chain(n)
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    y = rng.normal(size=n)
    result = spatial_lag_instrument_diagnostics(y, x, w, instrument_orders=3)
    assert result.instruments_used < x.shape[1] * 4
    assert result.excluded_instruments == result.instruments_used - x.shape[1]


def test_spatial_lag_instrument_diagnostics_rejects_invalid_or_unidentified_inputs():
    from instrument_diagnostics import spatial_lag_instrument_diagnostics
    n = 40
    w = _row_standardised_chain(n)
    y = np.arange(n, dtype=float)
    with pytest.raises(ValueError, match="no independent excluded"):
        spatial_lag_instrument_diagnostics(y, np.ones((n, 1)), w)
    with pytest.raises(ValueError, match="instrument_orders"):
        spatial_lag_instrument_diagnostics(y, np.column_stack([np.ones(n), y]), w,
                                           instrument_orders=0)
    bad = w.copy()
    bad[0, 0] = np.nan
    with pytest.raises(ValueError, match="finite"):
        spatial_lag_instrument_diagnostics(y, np.column_stack([np.ones(n), y]), bad)


def test_spatial_lag_anderson_rubin_matches_classical_and_hc1_joint_tests():
    from spatial_lag_anderson_rubin import spatial_lag_anderson_rubin
    rng = np.random.default_rng(9182)
    n = 100
    w = _row_standardised_chain(n)
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    rho = 0.28
    y = np.linalg.solve(np.eye(n) - rho * w,
                        x @ np.array([1.0, -0.6]) + rng.normal(scale=0.25, size=n))
    result = spatial_lag_anderson_rubin(y, x, w, rho, instrument_orders=2)
    assert result.rho_null == rho
    assert result.classical_f >= 0
    assert result.robust_wald_chi2 >= 0
    assert result.excluded_instruments == result.instruments_used - x.shape[1]
    assert result.classical_f_numerator_df == result.excluded_instruments
    assert result.classical_f_denominator_df == n - result.instruments_used
    assert result.robust_wald_degrees_of_freedom == result.excluded_instruments
    assert len(result.transformed_coefficients) == result.instruments_used
    assert result.transformed_residual_variance > 0

    # Independently reconstruct the homoskedastic restricted/unrestricted F.
    z_columns = [x]
    lagged = x.copy()
    for _ in range(2):
        lagged = w @ lagged
        z_columns.append(lagged)
    z = np.column_stack(z_columns)
    keep = []
    current = np.empty((n, 0))
    rank = 0
    for j in range(z.shape[1]):
        candidate = np.column_stack([current, z[:, j]])
        next_rank = np.linalg.matrix_rank(candidate, tol=1e-10)
        if next_rank > rank:
            keep.append(j)
            current, rank = candidate, next_rank
    z = z[:, keep]
    y0 = y - rho * (w @ y)
    restricted = y0 - x @ np.linalg.lstsq(x, y0, rcond=None)[0]
    unrestricted = y0 - z @ np.linalg.lstsq(z, y0, rcond=None)[0]
    q = z.shape[1] - x.shape[1]
    expected_f = ((restricted @ restricted - unrestricted @ unrestricted) / q) / (
        unrestricted @ unrestricted / (n - z.shape[1])
    )
    assert result.classical_f == pytest.approx(expected_f)


def test_spatial_lag_anderson_rubin_is_candidate_specific_and_handles_weak_relevance():
    from spatial_lag_anderson_rubin import spatial_lag_anderson_rubin
    rng = np.random.default_rng(9183)
    n = 90
    w = _row_standardised_chain(n)
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    rho = 0.35
    y = np.linalg.solve(np.eye(n) - rho * w,
                        x @ np.array([0.7, 0.4]) + rng.normal(scale=0.2, size=n))
    at_null = spatial_lag_anderson_rubin(y, x, w, rho, instrument_orders=2)
    away = spatial_lag_anderson_rubin(y, x, w, -0.2, instrument_orders=2)
    assert away.classical_f > at_null.classical_f


def test_spatial_lag_anderson_rubin_rejects_invalid_or_unidentified_inputs():
    from spatial_lag_anderson_rubin import spatial_lag_anderson_rubin
    n = 40
    w = _row_standardised_chain(n)
    x = np.column_stack([np.ones(n), np.arange(n, dtype=float)])
    y = np.sin(np.arange(n, dtype=float))
    with pytest.raises(ValueError, match="rho_null"):
        spatial_lag_anderson_rubin(y, x, w, float("nan"))
    with pytest.raises(ValueError, match="instrument_orders"):
        spatial_lag_anderson_rubin(y, x, w, 0.2, instrument_orders=0)
    with pytest.raises(ValueError, match="finite"):
        bad = w.copy()
        bad[0, 0] = np.nan
        spatial_lag_anderson_rubin(y, x, bad, 0.2)
    with pytest.raises(ValueError, match="no independent excluded"):
        spatial_lag_anderson_rubin(y, np.ones((n, 1)), w, 0.2)


def test_heteroskedastic_spatial_error_gm_recovers_dependence_with_varying_innovation_variance():
    from heteroskedastic_spatial_error_gm import heteroskedastic_spatial_error_gm
    rng = np.random.default_rng(2718)
    n = 120
    w = _row_standardised_chain(n)
    rho = 0.38
    innovation_scale = 0.15 + 0.2 * np.abs(rng.normal(size=n))
    innovation = rng.normal(size=n) * innovation_scale
    disturbance = np.linalg.solve(np.eye(n) - rho * w, innovation)
    fit = heteroskedastic_spatial_error_gm(disturbance, w, grid_size=501)
    assert fit.lambda_ == pytest.approx(rho, abs=0.16)
    assert fit.moment_objective >= 0
    assert len(fit.moment_residuals) == 2
    assert len(fit.gamma_matrix) == 2
    assert np.all(np.isfinite(np.asarray(fit.gamma_matrix)))
    assert fit.evaluations > 501


def test_heteroskedastic_spatial_error_gm_rejects_invalid_inputs_and_bounds():
    from heteroskedastic_spatial_error_gm import heteroskedastic_spatial_error_gm
    n = 40
    w = _row_standardised_chain(n)
    residuals = np.sin(np.arange(n, dtype=float))
    with pytest.raises(ValueError, match="grid_size"):
        heteroskedastic_spatial_error_gm(residuals, w, grid_size=10)
    with pytest.raises(ValueError, match="nonsingularity"):
        heteroskedastic_spatial_error_gm(residuals, w, rho_bounds=(-1.0, 0.9))
    with pytest.raises(ValueError, match="finite"):
        heteroskedastic_spatial_error_gm([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
                                          13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                                          23, 24, 25, 26, 27, 28, 29, 30, 31, 32,
                                          33, 34, 35, 36, 37, 38, 39, float("nan")], w)


def test_heteroskedastic_spatial_error_gm_expansion_matches_original_zero_diagonal_moments():
    from heteroskedastic_spatial_error_gm import heteroskedastic_spatial_error_gm
    rng = np.random.default_rng(2719)
    n = 90
    w = _row_standardised_chain(n)
    residual_predictor = rng.normal(size=n) * (0.5 + np.abs(rng.normal(size=n)))
    fit = heteroskedastic_spatial_error_gm(residual_predictor, w)
    innovation = residual_predictor - fit.lambda_ * (w @ residual_predictor)
    spatial_innovation = w @ innovation
    column_squared_norms = np.sum(w * w, axis=0)
    direct = np.array([
        (spatial_innovation @ spatial_innovation
         - np.dot(column_squared_norms, innovation * innovation)) / n,
        (spatial_innovation @ innovation) / n,
    ])
    np.testing.assert_allclose(fit.moment_residuals, direct, atol=1e-12)


def test_heteroskedastic_spatial_error_gm_uses_oriented_moment_for_asymmetric_weights():
    from heteroskedastic_spatial_error_gm import heteroskedastic_spatial_error_gm
    rng = np.random.default_rng(4412)
    n = 60
    w = _row_standardised_chain(n)
    assert not np.allclose(w, w.T)
    u = rng.normal(size=n) * (0.5 + np.linspace(0.0, 1.0, n))
    fit = heteroskedastic_spatial_error_gm(u, w)
    expected_gamma_2 = float(u @ (w @ u) / n)
    transposed_gamma_2 = float((w @ u) @ u / n)
    assert fit.gamma[1] == pytest.approx(expected_gamma_2)
    # A scalar quadratic form is invariant to transposition, even when W is not symmetric.
    assert expected_gamma_2 == pytest.approx(transposed_gamma_2)


def test_spatial_sarar_gtsls_three_step_recovers_synthetic_heteroskedastic_model():
    from spatial_sarar_gtsls import spatial_sarar_gtsls
    rng = np.random.default_rng(4413)
    n = 180
    w = _row_standardised_chain(n)
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    beta = np.array([1.1, -0.7])
    rho, lam = 0.22, 0.28
    innovation_scale = 0.12 + 0.10 * np.abs(x[:, 1])
    innovation = rng.normal(size=n) * innovation_scale
    error = np.linalg.solve(np.eye(n) - lam * w, innovation)
    y = np.linalg.solve(np.eye(n) - rho * w, x @ beta + error)
    fit = spatial_sarar_gtsls(y, x, w, instrument_orders=3, grid_size=501)
    assert fit.rho == pytest.approx(rho, abs=0.18)
    assert fit.lambda_ == pytest.approx(lam, abs=0.22)
    assert fit.beta == pytest.approx(beta, abs=0.2)
    assert len(fit.standard_errors_hc1_conditional) == x.shape[1] + 1
    assert np.all(np.asarray(fit.standard_errors_hc1_conditional) >= 0)
    assert fit.instruments_used >= x.shape[1] + 1
    assert fit.first_stage_rank == fit.instruments_used
    assert fit.transformed_stage_rank == x.shape[1] + 1
    assert np.all(np.isfinite(fit.filtered_residuals))
    assert np.asarray(fit.covariance_joint_kp).shape == (x.shape[1] + 2, x.shape[1] + 2)
    assert len(fit.standard_errors_joint_kp) == x.shape[1] + 2
    assert np.all(np.asarray(fit.standard_errors_joint_kp) >= 0)
    assert np.all(np.isfinite(fit.covariance_joint_kp))


def test_spatial_sarar_gtsls_rejects_invalid_or_underidentified_inputs():
    from spatial_sarar_gtsls import spatial_sarar_gtsls
    n = 20
    w = _row_standardised_chain(n)
    x = np.ones((n, 1))
    y = np.sin(np.arange(n, dtype=float))
    with pytest.raises(ValueError, match="instrument_orders"):
        spatial_sarar_gtsls(y, x, w, instrument_orders=0)
    with pytest.raises(ValueError, match="finite"):
        bad = y.copy()
        bad[0] = np.nan
        spatial_sarar_gtsls(bad, x, w)


def test_spatial_lag_2sls_hac_matches_hand_computed_conley_sandwich():
    from spatial_2sls_hac import spatial_lag_2sls_hac
    rng = np.random.default_rng(6127)
    n = 80
    w = _row_standardised_chain(n)
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    beta = np.array([0.8, -0.45])
    rho = 0.24
    innovation = rng.normal(size=n) * (0.12 + 0.08 * np.abs(x[:, 1]))
    y = np.linalg.solve(np.eye(n) - rho * w, x @ beta + innovation)
    coordinates = np.column_stack([np.arange(n, dtype=float) * 1000.0,
                                   np.zeros(n)])
    bandwidth = 2500.0
    fit = spatial_lag_2sls_hac(y, x, w, coordinates, bandwidth=bandwidth,
                               instrument_orders=2)
    instruments = np.column_stack([x, w @ x, w @ (w @ x)])
    # Reproduce stable independent-column selection used by the estimator.
    from spatial_2sls_hac import _independent_columns
    h = _independent_columns(instruments)
    regressors = np.column_stack([w @ y, x])
    projected = h @ np.linalg.solve(h.T @ h, h.T @ regressors)
    cross = projected.T @ regressors
    residuals = y - regressors @ np.asarray(fit.coefficients)
    distances = np.abs(np.arange(n)[:, None] - np.arange(n)[None, :]) * 1000.0
    scaled = distances / bandwidth
    kernel = np.where(scaled < 1.0, (1.0 - scaled) ** 4 * (4.0 * scaled + 1.0), 0.0)
    scores = projected * residuals[:, None]
    bread = np.linalg.inv(cross)
    expected = bread @ (scores.T @ kernel @ scores) @ bread.T
    expected *= n / (n - regressors.shape[1])
    np.testing.assert_allclose(fit.covariance, expected, rtol=1e-9, atol=1e-11)
    assert fit.rho == pytest.approx(rho, abs=0.18)
    assert len(fit.standard_errors) == x.shape[1] + 1
    assert fit.nonzero_off_diagonal_pairs > 0
    assert fit.instruments_used >= x.shape[1] + 1


def test_spatial_lag_2sls_hac_rejects_invalid_geometry_and_identification():
    from spatial_2sls_hac import spatial_lag_2sls_hac
    n = 12
    w = _row_standardised_chain(n)
    x = np.column_stack([np.ones(n), np.arange(n, dtype=float)])
    y = np.sin(np.arange(n, dtype=float))
    coords = np.column_stack([np.arange(n, dtype=float), np.zeros(n)])
    with pytest.raises(ValueError, match="bandwidth"):
        spatial_lag_2sls_hac(y, x, w, coords, bandwidth=0)
    with pytest.raises(ValueError, match="coordinates"):
        spatial_lag_2sls_hac(y, x, w, np.ones((n, 3)), bandwidth=2)
    with pytest.raises(ValueError, match="instrument_orders"):
        spatial_lag_2sls_hac(y, x, w, coords, bandwidth=2, instrument_orders=0)
    with pytest.raises(ValueError, match="finite"):
        bad = coords.copy()
        bad[0, 0] = np.nan
        spatial_lag_2sls_hac(y, x, w, bad, bandwidth=2)



def test_spatial_sarar_joint_covariance_matches_independent_kp_matrix_construction():
    from spatial_sarar_gtsls import spatial_sarar_gtsls
    rng = np.random.default_rng(77123)
    n = 90
    w = _row_standardised_chain(n)
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    beta = np.array([0.9, -0.55])
    rho, lam = 0.2, 0.25
    innovation = rng.normal(size=n) * (0.1 + 0.07 * np.abs(x[:, 1]))
    u = np.linalg.solve(np.eye(n) - lam * w, innovation)
    y = np.linalg.solve(np.eye(n) - rho * w, x @ beta + u)
    fit = spatial_sarar_gtsls(y, x, w, instrument_orders=2, grid_size=401)

    # Independently reconstruct the KP (2010) plug-in covariance from
    # equations (21), (25)-(29), using the fitted first-stage GM parameter.
    h_blocks = [x]
    lagged = x.copy()
    for _ in range(2):
        lagged = w @ lagged
        h_blocks.append(lagged)
    h = np.column_stack(h_blocks)
    keep, current, rank = [], np.empty((n, 0)), 0
    for j in range(h.shape[1]):
        candidate = np.column_stack([current, h[:, j]])
        next_rank = np.linalg.matrix_rank(candidate, tol=1e-10)
        if next_rank > rank:
            keep.append(j)
            current, rank = candidate, next_rank
    h = h[:, keep]
    z = np.column_stack([x, w @ y])
    p0 = np.linalg.solve(h.T @ h / n, h.T @ z / n)
    p0 = p0 @ np.linalg.inv((h.T @ z / n).T @ np.linalg.solve(h.T @ h / n, h.T @ z / n))
    first_delta = p0.T @ h.T @ y / n
    u0 = y - z @ first_delta
    transform = np.eye(n) - fit.lambda_ * w
    f0 = np.linalg.solve(transform.T, h)
    t0 = f0 @ p0
    a1 = w.T @ w
    a1 -= np.diag(np.diag(a1))
    sym_a = [a1 + a1.T, w + w.T]
    a_vectors = []
    for a in sym_a:
        alpha = (-z).T @ transform.T @ a @ transform @ u0 / n
        a_vectors.append(t0 @ alpha)
    a_stack = np.column_stack(a_vectors)
    eps_hat = transform @ u0
    sigma = eps_hat ** 2
    sigma_matrix = np.diag(sigma)
    psi_gm = np.empty((2, 2))
    for r in range(2):
        for q in range(2):
            psi_gm[r, q] = (
                np.trace(sym_a[r] @ sigma_matrix @ sym_a[q] @ sigma_matrix) / (2*n)
                + a_vectors[r] @ (sigma * a_vectors[q]) / n
            )
    psi_dd = h.T @ (sigma[:, None] * h) / n
    psi_dr = h.T @ (sigma[:, None] * a_stack) / n
    psi = np.block([[psi_dd, psi_dr], [psi_dr.T, psi_gm]])
    zstar = transform @ z
    qhh = h.T @ h / n
    qhz = h.T @ zstar / n
    pstar = np.linalg.solve(qhh, qhz) @ np.linalg.inv(qhz.T @ np.linalg.solve(qhh, qhz))
    j = np.array([1.0, 2.0 * fit.lambda_])
    gm_map = j / (j @ j)
    mapping = np.zeros((x.shape[1] + 2, h.shape[1] + 2))
    mapping[:x.shape[1] + 1, :h.shape[1]] = pstar.T
    mapping[-1, h.shape[1]:] = gm_map
    expected = mapping @ psi @ mapping.T
    np.testing.assert_allclose(fit.covariance_joint_kp, expected, rtol=1e-8, atol=1e-10)
    np.testing.assert_allclose(fit.covariance_joint_kp,
                               np.asarray(fit.covariance_joint_kp).T, atol=1e-12)


def test_spatial_sarar_joint_covariance_rejects_incompatible_inputs():
    from spatial_sarar_joint_covariance import spatial_sarar_joint_covariance
    n = 20
    w = _row_standardised_chain(n)
    x = np.column_stack([np.ones(n), np.arange(n, dtype=float)])
    y = np.sin(np.arange(n, dtype=float))
    h = np.column_stack([x, w @ x])
    with pytest.raises(ValueError, match="finite"):
        spatial_sarar_joint_covariance(y, x, w, h, float("nan"),
                                       np.zeros(n), [0.0, 0.0, 0.0])
    with pytest.raises(ValueError, match="dimensions"):
        spatial_sarar_joint_covariance(y, x, w, h, 0.2,
                                       np.zeros(n - 1), [0.0, 0.0, 0.0])


def test_global_morans_i_permutation_matches_independent_manual_simulation():
    from morans_i_permutation import morans_i_permutation
    rng = np.random.default_rng(901)
    n = 24
    w = _row_standardised_chain(n)
    values = rng.normal(size=n)
    result = morans_i_permutation(values, w, permutations=199,
                                  alternative="two-sided", seed=77)
    centred = values - values.mean()
    scale = n / w.sum() / (centred @ centred)
    observed = scale * (centred @ w @ centred)
    manual_rng = np.random.default_rng(77)
    manual = []
    for _ in range(199):
        permuted = manual_rng.permutation(centred)
        manual.append(scale * (permuted @ w @ permuted))
    manual = np.asarray(manual)
    extreme = np.count_nonzero(
        np.abs(manual + 1.0 / (n - 1))
        >= abs(observed + 1.0 / (n - 1)) - np.finfo(float).eps * 32
    )
    assert result.statistic == pytest.approx(observed)
    assert result.expected_value == pytest.approx(-1.0 / (n - 1))
    np.testing.assert_allclose(result.simulations, manual)
    assert result.permutation_mean == pytest.approx(manual.mean())
    assert result.permutation_standard_deviation == pytest.approx(manual.std(ddof=1))
    assert result.p_value == pytest.approx((extreme + 1) / 200)


def test_global_morans_i_permutation_supports_one_sided_and_asymmetric_weights():
    from morans_i_permutation import morans_i_permutation
    n = 18
    w = _row_standardised_chain(n)
    assert not np.allclose(w, w.T)
    values = np.arange(n, dtype=float) ** 2
    greater = morans_i_permutation(values, w, permutations=299,
                                    alternative="greater", seed=11)
    less = morans_i_permutation(values, w, permutations=299,
                                alternative="less", seed=11)
    assert 0 < greater.p_value <= 1
    assert 0 < less.p_value <= 1
    assert greater.simulations == less.simulations
    assert greater.p_value != less.p_value


def test_global_morans_i_permutation_rejects_invalid_inputs():
    from morans_i_permutation import morans_i_permutation
    n = 12
    w = _row_standardised_chain(n)
    values = np.arange(n, dtype=float)
    with pytest.raises(ValueError, match="at least three"):
        morans_i_permutation([1.0, 2.0], np.zeros((2, 2)))
    with pytest.raises(ValueError, match="N-by-N"):
        morans_i_permutation(values, np.zeros((n - 1, n - 1)))
    with pytest.raises(ValueError, match="positive variance"):
        morans_i_permutation(np.ones(n), w)
    with pytest.raises(ValueError, match="positive finite sum"):
        morans_i_permutation(values, np.zeros((n, n)))
    with pytest.raises(ValueError, match="zero"):
        bad = w.copy()
        bad[0, 0] = 0.1
        morans_i_permutation(values, bad)
    with pytest.raises(ValueError, match="permutations"):
        morans_i_permutation(values, w, permutations=10)
    with pytest.raises(ValueError, match="alternative"):
        morans_i_permutation(values, w, alternative="upper")



def test_local_morans_i_matches_manual_conditional_permutations_and_bh():
    from local_morans_i_permutation import local_morans_i_permutation, _benjamini_hochberg
    rng = np.random.default_rng(221)
    n = 16
    w = _row_standardised_chain(n)
    values = rng.normal(size=n)
    result = local_morans_i_permutation(values, w, permutations=199,
                                        adjustment="bh", seed=19)
    z = values - values.mean()
    m2 = z @ z / n
    expected_i = -(z ** 2) * w.sum(axis=1) / ((n - 1) * m2)
    np.testing.assert_allclose(result.local_i, z * (w @ z) / m2)
    np.testing.assert_allclose(result.expected_value, expected_i)
    manual_rng = np.random.default_rng(19)
    raw = []
    for i in range(n):
        idx = np.arange(n) != i
        draws = []
        for _ in range(199):
            permuted = manual_rng.permutation(z[idx])
            draws.append(z[i] * (w[i, idx] @ permuted) / m2)
        draws = np.asarray(draws)
        extreme = np.count_nonzero(
            np.abs(draws - expected_i[i])
            >= abs(result.local_i[i] - expected_i[i]) - np.finfo(float).eps * 32
        )
        raw.append((extreme + 1) / 200)
    np.testing.assert_allclose(result.p_values, raw)
    np.testing.assert_allclose(result.adjusted_p_values, _benjamini_hochberg(np.asarray(raw)))


def test_local_morans_i_handles_islands_and_cluster_labels():
    from local_morans_i_permutation import local_morans_i_permutation
    n = 20
    w = _row_standardised_chain(n)
    w[0, :] = 0.0
    values = np.r_[np.ones(10) * 2.0, np.ones(10) * -2.0]
    result = local_morans_i_permutation(values, w, permutations=199,
                                        adjustment="none", seed=3)
    assert result.cluster_labels[0] == "island"
    assert np.isnan(result.p_values[0])
    assert np.all(np.isfinite(result.p_values[1:]))
    assert set(result.cluster_labels[1:]).issubset(
        {"HH", "LL", "HL", "LH", "not-significant"}
    )


def test_local_morans_i_supports_asymmetric_weights_and_rejects_invalid_inputs():
    from local_morans_i_permutation import local_morans_i_permutation
    n = 14
    w = _row_standardised_chain(n)
    assert not np.allclose(w, w.T)
    values = np.arange(n, dtype=float) ** 2
    fit = local_morans_i_permutation(values, w, permutations=99,
                                     alternative="greater", seed=4)
    assert fit.alternative == "greater"
    with pytest.raises(ValueError, match="N-by-N"):
        local_morans_i_permutation(values, np.zeros((n - 1, n - 1)))
    with pytest.raises(ValueError, match="positive variance"):
        local_morans_i_permutation(np.ones(n), w)
    with pytest.raises(ValueError, match="permutations"):
        local_morans_i_permutation(values, w, permutations=10)
    with pytest.raises(ValueError, match="alpha"):
        local_morans_i_permutation(values, w, alpha=1.0)
    with pytest.raises(ValueError, match="adjustment"):
        local_morans_i_permutation(values, w, adjustment="bonferroni")


def test_heteroskedasticity_diagnostics_match_independent_auxiliary_regressions():
    from heteroskedasticity_diagnostics import heteroskedasticity_diagnostics
    rng = np.random.default_rng(613)
    n = 180
    x = np.column_stack((np.ones(n), rng.normal(size=n), rng.normal(size=n)))
    scale = np.exp(0.35 * x[:, 1])
    y = 1.2 + 0.8 * x[:, 1] - 0.4 * x[:, 2] + rng.normal(size=n) * scale
    result = heteroskedasticity_diagnostics(y, x)
    beta = np.linalg.lstsq(x, y, rcond=None)[0]
    residual = y - x @ beta
    squared = residual ** 2
    def lm(aux):
        fitted = aux @ np.linalg.lstsq(aux, squared, rcond=None)[0]
        centred = squared - squared.mean()
        r2 = 1 - ((squared - fitted) @ (squared - fitted)) / (centred @ centred)
        return n * r2
    bp_x = x
    white_x = np.column_stack((x, x[:, 1] ** 2, x[:, 1] * x[:, 2], x[:, 2] ** 2))
    assert result.koenker_bp.statistic == pytest.approx(lm(bp_x))
    assert result.white.statistic == pytest.approx(lm(white_x))
    assert result.koenker_bp.degrees_of_freedom == 2
    assert result.white.degrees_of_freedom == 5
    assert 0 <= result.koenker_bp.p_value <= 1
    assert 0 <= result.white.p_value <= 1


def test_white_test_handles_redundant_generated_terms():
    from heteroskedasticity_diagnostics import heteroskedasticity_diagnostics
    rng = np.random.default_rng(71)
    n = 120
    a = rng.normal(size=n)
    x = np.column_stack((np.ones(n), a, a ** 2))
    y = 1 + 0.4 * a + rng.normal(size=n) * (1 + 0.2 * np.abs(a))
    fit = heteroskedasticity_diagnostics(y, x)
    assert fit.white.degrees_of_freedom >= 1
    assert np.isfinite(fit.white.statistic)


def test_heteroskedasticity_diagnostics_rejects_invalid_inputs():
    from heteroskedasticity_diagnostics import heteroskedasticity_diagnostics
    with pytest.raises(ValueError, match="at least five"):
        heteroskedasticity_diagnostics([1, 2, 3, 4], np.ones((4, 1)))
    with pytest.raises(ValueError, match="full column rank"):
        x = np.column_stack((np.ones(20), np.arange(20), np.arange(20)))
        heteroskedasticity_diagnostics(np.arange(20) + np.sin(np.arange(20)), x)
    with pytest.raises(ValueError, match="positive variance"):
        x = np.column_stack((np.ones(20), np.arange(20)))
        heteroskedasticity_diagnostics(2 + 3 * np.arange(20), x)


def test_chi_square_survival_function_known_critical_values():
    from heteroskedasticity_diagnostics import _chi_square_sf
    assert _chi_square_sf(3.841458820694124, 1) == pytest.approx(0.05, abs=2e-8)
    assert _chi_square_sf(5.991464547107979, 2) == pytest.approx(0.05, abs=2e-8)
    assert _chi_square_sf(0.0, 3) == pytest.approx(1.0)


def test_ramsey_reset_matches_independent_nested_ols_comparison():
    from ramsey_reset import ramsey_reset_test
    rng = np.random.default_rng(919)
    n = 240
    z = rng.normal(size=n)
    x = np.column_stack((np.ones(n), z))
    y = 1.0 + 1.4 * z + 0.9 * z ** 2 + rng.normal(scale=0.6, size=n)
    result = ramsey_reset_test(y, x, power=3)
    beta = np.linalg.lstsq(x, y, rcond=None)[0]
    yhat = x @ beta
    augmented = np.column_stack((x, yhat ** 2, yhat ** 3))
    rss_r = np.sum((y - yhat) ** 2)
    gamma = np.linalg.lstsq(augmented, y, rcond=None)[0]
    rss_u = np.sum((y - augmented @ gamma) ** 2)
    q = np.linalg.matrix_rank(augmented) - np.linalg.matrix_rank(x)
    df = n - np.linalg.matrix_rank(augmented)
    expected_f = ((rss_r - rss_u) / q) / (rss_u / df)
    assert result.statistic == pytest.approx(expected_f, rel=1e-9)
    assert result.restricted_rss == pytest.approx(rss_r)
    assert result.unrestricted_rss == pytest.approx(rss_u)
    assert result.numerator_degrees_of_freedom == q
    assert result.denominator_degrees_of_freedom == df
    assert result.p_value < 0.001


def test_ramsey_reset_f_survival_known_critical_values():
    from ramsey_reset import _f_survival
    assert _f_survival(3.936142, 1, 100) == pytest.approx(0.05, abs=2e-5)
    assert _f_survival(3.087296, 2, 100) == pytest.approx(0.05, abs=2e-5)
    assert _f_survival(0.0, 3, 40) == pytest.approx(1.0)


def test_ramsey_reset_rejects_invalid_and_unidentified_models():
    from ramsey_reset import ramsey_reset_test
    rng = np.random.default_rng(44)
    x = np.column_stack((np.ones(30), np.arange(30, dtype=float)))
    y = 1 + 0.5 * np.arange(30) + rng.normal(size=30)
    with pytest.raises(ValueError, match="power"):
        ramsey_reset_test(y, x, power=1)
    with pytest.raises(ValueError, match="full column rank"):
        ramsey_reset_test(y, np.column_stack((x, x[:, 1])), power=2)
    with pytest.raises(ValueError, match="finite"):
        bad = y.copy()
        bad[0] = np.nan
        ramsey_reset_test(bad, x)
    with pytest.raises(ValueError, match="positive"):
        ramsey_reset_test(1 + 2 * x[:, 1], x)


def test_spatial_parameter_profile_interval_inverts_sar_likelihood_ratio():
    from spatial_mle_inference import spatial_parameter_profile_interval, _profile_log_likelihood
    rng = np.random.default_rng(55101)
    n = 70
    w = _row_standardised_chain(n)
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    y = np.linalg.solve(np.eye(n) - 0.3 * w,
                        x @ np.array([1.0, 0.65]) + rng.normal(scale=0.2, size=n))
    result = spatial_parameter_profile_interval(y, x, w, model="SAR", grid_size=161)
    assert result.model == "SAR"
    assert result.lower < result.estimate < result.upper
    assert not result.lower_truncated and not result.upper_truncated
    for endpoint in (result.lower, result.upper):
        ll = _profile_log_likelihood(y, x, w, endpoint, "SAR")
        assert 2.0 * (result.log_likelihood_maximum - ll) == pytest.approx(
            result.likelihood_ratio_cutoff, abs=2e-5
        )


def test_spatial_parameter_profile_interval_handles_sem():
    from spatial_mle_inference import spatial_parameter_profile_interval
    rng = np.random.default_rng(55102)
    n = 65
    w = _row_standardised_chain(n)
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    innovation = rng.normal(scale=0.2, size=n)
    error = np.linalg.solve(np.eye(n) - 0.25 * w, innovation)
    y = x @ np.array([0.8, -0.4]) + error
    result = spatial_parameter_profile_interval(y, x, w, model="SEM", grid_size=161)
    assert result.model == "SEM"
    assert result.lower <= result.estimate <= result.upper
    assert result.lower < result.upper
    assert result.likelihood_ratio_cutoff == pytest.approx(3.841458820694124)


def test_spatial_parameter_profile_interval_rejects_invalid_options():
    from spatial_mle_inference import spatial_parameter_profile_interval
    n = 12
    w = _row_standardised_chain(n)
    x = np.column_stack([np.ones(n), np.arange(n, dtype=float)])
    y = np.sin(np.arange(n, dtype=float))
    with pytest.raises(ValueError, match="model"):
        spatial_parameter_profile_interval(y, x, w, model="SAC")
    with pytest.raises(ValueError, match="cutoff"):
        spatial_parameter_profile_interval(y, x, w, likelihood_ratio_cutoff=0)
    with pytest.raises(ValueError, match="max_iterations"):
        spatial_parameter_profile_interval(y, x, w, max_iterations=0)


def test_spatial_lag_ar_confidence_set_matches_candidate_tests():
    from spatial_lag_anderson_rubin import spatial_lag_anderson_rubin
    from spatial_lag_ar_confidence import spatial_lag_ar_confidence_set
    n = 30
    w = _row_standardised_path(n)
    rng = np.random.default_rng(81)
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    y = np.linalg.solve(np.eye(n) - 0.2 * w, x @ [1.0, 0.7] + rng.normal(scale=0.3, size=n))
    grid = np.linspace(-0.4, 0.6, 11)
    candidate = spatial_lag_anderson_rubin(y, x, w, float(grid[5]), instrument_orders=2)
    result = spatial_lag_ar_confidence_set(y, x, w, grid, critical_value=candidate.classical_f,
                                           test="classical", instrument_orders=2)
    assert result.test == "classical"
    assert result.statistics[5] == pytest.approx(candidate.classical_f)
    assert result.accepted[5]
    assert result.grid == pytest.approx(tuple(grid))


def test_spatial_lag_ar_confidence_set_reports_grid_truncation_and_empty_sets():
    from spatial_lag_ar_confidence import spatial_lag_ar_confidence_set
    n = 30
    w = _row_standardised_path(n)
    rng = np.random.default_rng(82)
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    y = np.linalg.solve(np.eye(n) - 0.2 * w, x @ [1.0, 0.7] + rng.normal(scale=0.3, size=n))
    broad = spatial_lag_ar_confidence_set(y, x, w, np.linspace(-0.5, 0.5, 9),
                                          critical_value=1e9, test="robust", instrument_orders=2)
    assert len(broad.segments) == 1
    assert broad.segments[0].lower_grid_limited and broad.segments[0].upper_grid_limited
    empty = spatial_lag_ar_confidence_set(y, x, w, np.linspace(-0.5, 0.5, 9),
                                          critical_value=1e-12, test="robust", instrument_orders=2)
    assert not any(empty.accepted)
    assert empty.segments == ()


def test_spatial_lag_ar_confidence_set_validates_grid_and_test():
    from spatial_lag_ar_confidence import spatial_lag_ar_confidence_set
    n = 30
    w = _row_standardised_path(n)
    rng = np.random.default_rng(83)
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    y = rng.normal(size=n)
    with pytest.raises(ValueError, match="strictly increasing"):
        spatial_lag_ar_confidence_set(y, x, w, [0.0, 0.0, 1.0], critical_value=3.0)
    with pytest.raises(ValueError, match="test"):
        spatial_lag_ar_confidence_set(y, x, w, [-0.2, 0.0, 0.2], critical_value=3.0, test="unknown")
    with pytest.raises(ValueError, match="critical_value"):
        spatial_lag_ar_confidence_set(y, x, w, [-0.2, 0.0, 0.2], critical_value=0.0)



def test_spatial_impact_delta_jacobian_matches_central_finite_differences():
    from impacts import spatial_impact_delta_uncertainty
    rho, beta, gamma = 0.17, np.array([1.4]), np.array([0.6])
    covariance = np.diag([0.0025, 0.01, 0.0064])
    result, = spatial_impact_delta_uncertainty(CHAIN, rho, beta, covariance, gamma)
    theta = np.array([rho, beta[0], gamma[0]])
    def impacts_at(values):
        item, = spatial_impacts(CHAIN, values[0], [values[1]], [values[2]])
        return np.array([item.direct, item.indirect, item.total])
    numerical = np.column_stack([
        (impacts_at(theta + np.eye(3)[j] * 1e-6)
         - impacts_at(theta - np.eye(3)[j] * 1e-6)) / 2e-6
        for j in range(3)
    ])
    expected_se = np.sqrt(np.diag(numerical @ covariance @ numerical.T))
    assert [result.direct.estimate, result.indirect.estimate, result.total.estimate] == pytest.approx(
        impacts_at(theta)
    )
    assert [result.direct.standard_error, result.indirect.standard_error,
            result.total.standard_error] == pytest.approx(expected_se, rel=2e-6)


def test_spatial_impact_delta_sar_zero_rho_has_zero_spillover_uncertainty():
    from impacts import spatial_impact_delta_uncertainty
    covariance = np.diag([0.0, 0.04])
    result, = spatial_impact_delta_uncertainty(CHAIN, 0.0, [2.0], covariance)
    assert result.direct.estimate == pytest.approx(2.0)
    assert result.direct.standard_error == pytest.approx(0.2)
    assert result.indirect.estimate == pytest.approx(0.0)
    assert result.indirect.standard_error == pytest.approx(0.0)
    assert result.total.standard_error == pytest.approx(0.2)


def test_spatial_impact_delta_rejects_bad_covariance_and_confidence():
    from impacts import spatial_impact_delta_uncertainty
    with pytest.raises(ValueError, match="shape"):
        spatial_impact_delta_uncertainty(CHAIN, 0.1, [1.0], np.eye(3))
    with pytest.raises(ValueError, match="positive semidefinite"):
        spatial_impact_delta_uncertainty(CHAIN, 0.1, [1.0], [[1.0, 2.0], [2.0, 1.0]])
    with pytest.raises(ValueError, match="confidence"):
        spatial_impact_delta_uncertainty(CHAIN, 0.1, [1.0], np.eye(2), confidence=1.0)



def test_spatial_durbin_common_factor_lr_matches_nested_model_likelihoods():
    from maximum_likelihood import spatial_durbin_mle, spatial_error_mle
    from spatial_durbin_common_factor import spatial_durbin_common_factor_test
    rng = np.random.default_rng(14021)
    n = 72
    w = _row_standardised_chain(n)
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    y = np.linalg.solve(
        np.eye(n) - 0.22 * w,
        x @ [1.0, 0.7] + (w @ x) @ [0.0, -0.25]
        + rng.normal(scale=0.15, size=n),
    )
    result = spatial_durbin_common_factor_test(y, x, w, grid_size=101)
    unrestricted = spatial_durbin_mle(y, x, w, grid_size=101)
    restricted = spatial_error_mle(y, x, w, grid_size=101)
    assert result.degrees_of_freedom == 1  # WX intercept is collinear with X.
    assert result.statistic == pytest.approx(
        2.0 * (unrestricted.log_likelihood - restricted.log_likelihood), abs=1e-8
    )
    assert result.p_value == pytest.approx(
        __import__("heteroskedasticity_diagnostics")._chi_square_sf(result.statistic, 1)
    )
    assert len(result.restriction_residuals) == 1


def test_spatial_durbin_common_factor_detects_departure_from_error_restriction():
    from spatial_durbin_common_factor import spatial_durbin_common_factor_test
    rng = np.random.default_rng(14022)
    n = 100
    w = _row_standardised_chain(n)
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    y = np.linalg.solve(
        np.eye(n) - 0.18 * w,
        x @ [0.8, 0.5] + (w @ x) @ [0.0, 0.9]
        + rng.normal(scale=0.08, size=n),
    )
    result = spatial_durbin_common_factor_test(y, x, w, grid_size=121)
    assert result.degrees_of_freedom == 1
    assert result.statistic > 3.84
    assert result.p_value < 0.05


def test_spatial_durbin_common_factor_rejects_unidentified_and_bad_options():
    from spatial_durbin_common_factor import spatial_durbin_common_factor_test
    n = 12
    w = _row_standardised_chain(n)
    y = np.sin(np.arange(n, dtype=float))
    with pytest.raises(ValueError, match="no independently identified"):
        spatial_durbin_common_factor_test(y, np.ones((n, 1)), w)
    x = np.column_stack([np.ones(n), np.arange(n, dtype=float)])
    with pytest.raises(ValueError, match="grid_size"):
        spatial_durbin_common_factor_test(y, x, w, grid_size=5)



def test_spatial_parameter_profile_interval_inverts_sdm_likelihood_ratio():
    from spatial_mle_inference import spatial_parameter_profile_interval, _profile_log_likelihood
    rng = np.random.default_rng(55103)
    n = 75
    w = _row_standardised_chain(n)
    x = np.column_stack([np.ones(n), rng.normal(size=n)])
    y = np.linalg.solve(
        np.eye(n) - 0.24 * w,
        x @ [0.9, 0.55] + (w @ x) @ [0.0, -0.35]
        + rng.normal(scale=0.18, size=n),
    )
    result = spatial_parameter_profile_interval(y, x, w, model="SDM", grid_size=121)
    assert result.model == "SDM"
    assert result.lower < result.estimate < result.upper
    assert not result.lower_truncated and not result.upper_truncated
    for endpoint in (result.lower, result.upper):
        ll = _profile_log_likelihood(y, x, w, endpoint, "SDM")
        assert 2.0 * (result.log_likelihood_maximum - ll) == pytest.approx(
            result.likelihood_ratio_cutoff, abs=3e-5
        )


def test_spatial_parameter_profile_interval_sdm_rejects_unknown_model():
    from spatial_mle_inference import spatial_parameter_profile_interval
    n = 12
    w = _row_standardised_chain(n)
    x = np.column_stack([np.ones(n), np.arange(n, dtype=float)])
    y = np.sin(np.arange(n, dtype=float))
    with pytest.raises(ValueError, match="SAR.*SEM.*SDM"):
        spatial_parameter_profile_interval(y, x, w, model="SAC")


def test_icar_log_density_matches_closed_form_on_three_node_chain():
    from icar import icar_log_density
    adjacency = np.array([[0., 1., 0.], [1., 0., 1.], [0., 1., 0.]])
    field = np.array([1., 0., -1.])
    result = icar_log_density(adjacency, field, precision=2.0)
    # The two positive Laplacian eigenvalues are 1 and 3.
    expected = 0.5 * np.log(12.0) - np.log(2.0 * np.pi) - 2.0
    assert result.log_density == pytest.approx(expected, abs=1e-12)
    assert result.quadratic_energy == pytest.approx(2.0)
    assert result.constrained_dimension == 2
    assert result.n_components == 1
    assert result.log_pseudodeterminant_precision == pytest.approx(np.log(12.0))


def test_icar_log_density_handles_disconnected_component_constraints():
    from icar import icar_log_density
    adjacency = np.zeros((6, 6))
    adjacency[0, 1] = adjacency[1, 0] = 1.0
    adjacency[1, 2] = adjacency[2, 1] = 1.0
    adjacency[3, 4] = adjacency[4, 3] = 1.0
    adjacency[4, 5] = adjacency[5, 4] = 1.0
    field = np.array([1., 0., -1., 2., 0., -2.])
    result = icar_log_density(adjacency, field, precision=0.5)
    assert result.n_components == 2
    assert result.constrained_dimension == 4
    assert result.component_sums == pytest.approx((0.0, 0.0))
    with pytest.raises(ValueError, match="component 0"):
        icar_log_density(adjacency, [1., 0., 0., 2., 0., -2.])


def test_icar_simulation_respects_each_component_constraint_and_seed():
    from icar import icar_sample
    adjacency = np.zeros((6, 6))
    adjacency[0, 1] = adjacency[1, 0] = 1.0
    adjacency[1, 2] = adjacency[2, 1] = 1.0
    adjacency[3, 4] = adjacency[4, 3] = 1.0
    adjacency[4, 5] = adjacency[5, 4] = 1.0
    first = icar_sample(adjacency, precision=1.7, rng=991)
    second = icar_sample(adjacency, precision=1.7, rng=991)
    assert first.field == second.field
    values = np.asarray(first.field)
    assert values[:3].sum() == pytest.approx(0.0, abs=1e-12)
    assert values[3:].sum() == pytest.approx(0.0, abs=1e-12)
    assert first.n_components == 2


def test_icar_log_density_rejects_invalid_inputs():
    from icar import icar_log_density
    adjacency = np.array([[0., 1., 0.], [1., 0., 1.], [0., 1., 0.]])
    with pytest.raises(ValueError, match="one value per"):
        icar_log_density(adjacency, [1., -1.])
    with pytest.raises(ValueError, match="finite"):
        icar_log_density(adjacency, [1., np.nan, -1.])
    with pytest.raises(ValueError, match="precision"):
        icar_log_density(adjacency, [1., 0., -1.], precision=0.0)
    with pytest.raises(ValueError, match="sum-to-zero"):
        icar_log_density(adjacency, [1., 0., 0.])

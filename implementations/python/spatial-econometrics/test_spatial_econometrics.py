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
    x = np.column_stack([np.ones(4), np.arange(4, dtype=float)])
    with pytest.raises(ValueError, match="at least five"):
        spatial_lag_mle([1., 2., 3., 4.], x, CHAIN)
    with pytest.raises(ValueError, match="grid_size"):
        spatial_error_mle([1., 2., 3., 4.], x, CHAIN, grid_size=5)
    with pytest.raises(ValueError, match="full column rank"):
        spatial_lag_mle([1., 2., 3., 4.], np.ones((4, 2)), CHAIN)
    with pytest.raises(ValueError, match="finite"):
        spatial_error_mle([1., 2., float("nan"), 4.], x, CHAIN)

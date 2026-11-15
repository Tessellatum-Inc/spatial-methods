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


def test_spatial_lm_diagnostics_reproducible_and_uses_supplied_design():
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
    assert impact.impact_matrix == pytest.approx(matrix)
    assert impact.total == pytest.approx(np.sum(matrix) / 4)


def test_spatial_impacts_validate_shapes_and_singularity():
    with pytest.raises(ValueError, match="gamma"):
        spatial_impacts(CHAIN, 0.1, [1.0, 2.0], [0.5])
    with pytest.raises(ValueError, match="nonsingular"):
        spatial_impacts(np.ones((2, 2)), 1.0, [1.0])
    with pytest.raises(ValueError, match="finite"):
        spatial_impacts([[0, float("nan")], [1, 0]], 0.1, [1.0])

import numpy as np
import pytest

from raim import residual_global_test, single_fault_exclusion, weighted_least_squares


def sample():
    x = np.arange(6.0)
    h = np.column_stack([np.ones_like(x), x])
    noise = np.array([0.01, -0.02, 0.01, 0.0, -0.01, 0.02])
    y = 2.0 + 3.0 * x + noise
    y[4] += 10.0
    r = np.eye(len(y)) * 0.04
    return y, h, r


def test_weighted_least_squares_recovers_clean_linear_model():
    x = np.arange(5.0)
    h = np.column_stack([np.ones_like(x), x])
    y = 4.0 - 2.0 * x
    fit = weighted_least_squares(y, h, np.eye(5))
    assert fit["estimate"] == pytest.approx([4.0, -2.0])
    assert fit["weighted_residual_sum_squares"] == pytest.approx(0.0, abs=1e-20)
    assert fit["degrees_of_freedom"] == 3


def test_global_residual_test_detects_injected_outlier():
    y, h, r = sample()
    result = residual_global_test(y, h, r, false_alarm_probability=0.01)
    assert result["alarm"]
    assert result["p_value"] < 0.01


def test_single_fault_exclusion_isolates_unique_bad_measurement():
    y, h, r = sample()
    result = single_fault_exclusion(y, h, r, false_alarm_probability=0.01)
    assert result["global_test"]["alarm"]
    assert result["status"] == "single_fault_isolated"
    assert result["excluded_index"] == 4


def test_clean_data_does_not_trigger_exclusion():
    x = np.arange(6.0)
    h = np.column_stack([np.ones_like(x), x])
    y = 1.0 + 2.0 * x
    result = single_fault_exclusion(y, h, np.eye(6), false_alarm_probability=0.01)
    assert result["status"] == "no_global_alarm"
    assert result["excluded_index"] is None


def test_invalid_dimensions_rank_covariance_and_alpha_are_rejected():
    with pytest.raises(ValueError):
        weighted_least_squares([1, 2], [[1, 1], [1, 2]], np.eye(2))
    with pytest.raises(ValueError):
        weighted_least_squares([1, 2, 3], [[1], [1], [1]], np.diag([1, 1, 0]))
    with pytest.raises(ValueError):
        residual_global_test([1, 2, 3], [[1], [1], [1]], np.eye(3), 1.0)
    with pytest.raises(ValueError):
        weighted_least_squares([1, np.nan, 3], [[1], [2], [3]], np.eye(3))

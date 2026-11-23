import numpy as np
import pytest
from downscaling import empirical_quantile_mapping, delta_change


def test_quantile_mapping_corrects_linear_distribution_bias():
    r = empirical_quantile_mapping([1, 2, 3], [0, 1, 2, 3], [10, 11, 12, 13], n_quantiles=11)
    assert r == pytest.approx([11, 12, 13])


def test_quantile_mapping_clamps_outside_calibration_range():
    assert empirical_quantile_mapping([-100, 100], [0, 1, 2], [5, 6, 7]) == pytest.approx([5, 7])


def test_quantile_mapping_handles_constant_model_calibration():
    assert empirical_quantile_mapping([4, 5, 6], [5, 5, 5], [1, 2, 3]) == pytest.approx([2, 2, 2])


def test_delta_change_additive():
    assert delta_change([10, 20], [5, 15], [6, 16]) == pytest.approx([11, 21])


def test_delta_change_multiplicative():
    assert delta_change([10, 20], [5, 15], [10, 20], mode="multiplicative") == pytest.approx([15, 30])


def test_delta_change_preserves_future_shape():
    assert np.asarray(delta_change([10, 20], [5, 15], [[6, 7], [8, 9]])) == pytest.approx(np.array([[11, 12], [13, 14]]))


@pytest.mark.parametrize("mode", ["ratio", "unknown"])
def test_delta_change_rejects_unknown_mode(mode):
    with pytest.raises(ValueError):
        delta_change([1, 2], [1, 2], [1, 2], mode=mode)


def test_multiplicative_delta_rejects_zero_model_mean():
    with pytest.raises(ValueError):
        delta_change([1, 2], [-1, 1], [2, 3], mode="multiplicative")


@pytest.mark.parametrize("bad", [[], [float("nan")], [float("inf")]])
def test_quantile_mapping_rejects_invalid_calibration(bad):
    with pytest.raises(ValueError):
        empirical_quantile_mapping([1, 2], bad, [1, 2])


def test_quantile_mapping_rejects_invalid_quantile_count():
    with pytest.raises(ValueError):
        empirical_quantile_mapping([1, 2], [1, 2], [1, 2], n_quantiles=1)

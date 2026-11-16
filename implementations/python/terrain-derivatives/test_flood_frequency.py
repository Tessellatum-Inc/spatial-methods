import numpy as np
import pytest
from flood_frequency import (
    weibull_return_periods, fit_gumbel_lmoments, gumbel_return_level,
    fit_gev_lmoments, gev_return_level, flood_frequency_table,
)


def sample():
    return np.array([42, 51, 47, 63, 58, 71, 55, 49, 66, 60, 74, 53], dtype=float)


def test_weibull_plotting_positions_are_descending_and_ranked():
    r = weibull_return_periods([1, 2, 3, 4])
    np.testing.assert_array_equal(r["magnitude"], [4, 3, 2, 1])
    np.testing.assert_allclose(r["return_period"], [5, 2.5, 5/3, 1.25])


def test_gumbel_fit_and_return_levels_increase_with_period():
    p = fit_gumbel_lmoments(sample())
    assert p["scale"] > 0
    q = gumbel_return_level([2, 10, 100], **p)
    assert np.all(np.diff(q) > 0)


def test_gev_fit_produces_finite_parameters_and_increasing_quantiles():
    p = fit_gev_lmoments(sample())
    assert p["scale"] > 0
    q = gev_return_level([2, 10, 100], **p)
    assert np.isfinite(q).all()
    assert np.all(np.diff(q) > 0)


def test_gev_gumbel_limit_agrees_with_gumbel_formula():
    args = {"location": 12.0, "scale": 3.0}
    a = gumbel_return_level([2, 10, 100], **args)
    b = gev_return_level([2, 10, 100], **args, shape=0.0)
    np.testing.assert_allclose(a, b)


def test_frequency_table_and_input_validation():
    r = flood_frequency_table(sample(), [2, 10, 50], distribution="gev")
    assert r["quantile"].shape == (3,)
    with pytest.raises(ValueError):
        fit_gev_lmoments([1, 1, 1, 1])
    with pytest.raises(ValueError):
        weibull_return_periods([1])
    with pytest.raises(ValueError):
        gumbel_return_level(1, location=0, scale=1)
    with pytest.raises(ValueError):
        flood_frequency_table(sample(), distribution="other")

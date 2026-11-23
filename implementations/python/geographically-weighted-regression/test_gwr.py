import numpy as np
import pytest
from gwr import gwr_fit

def grid_data():
    xx, yy = np.meshgrid(np.linspace(-2, 2, 7), np.linspace(-2, 2, 7))
    coords = np.column_stack([xx.ravel(), yy.ravel()])
    design = np.column_stack([np.ones(coords.shape[0]), coords])
    response = 2.0 + 3.0 * coords[:, 0] - 4.0 * coords[:, 1]
    return coords, design, response

def test_adaptive_gwr_recovers_exact_global_linear_surface():
    coords, x, y = grid_data()
    result = gwr_fit(coords, x, y, 20, adaptive=True, kernel="gaussian")
    np.testing.assert_allclose(result["coefficients"], np.tile([2, 3, -4], (len(y), 1)), atol=1e-10)
    np.testing.assert_allclose(result["fitted"], y, atol=1e-10)
    np.testing.assert_allclose(result["residuals"], 0, atol=1e-10)

def test_fixed_gaussian_bandwidth_recovers_linear_surface():
    coords, x, y = grid_data()
    result = gwr_fit(coords, x, y, 3.0, kernel="gaussian")
    np.testing.assert_allclose(result["coefficients"], np.tile([2, 3, -4], (len(y), 1)), atol=1e-10)

def test_compact_kernel_local_fit_and_diagnostics():
    coords, x, y = grid_data()
    result = gwr_fit(coords, x, y, 20, adaptive=True, kernel="bisquare")
    assert result["coefficients"].shape == (len(y), 3)
    assert np.all(result["effective_n"] > 3)
    assert np.all(result["condition_numbers"] >= 1)
    assert np.all(result["bandwidths"] > 0)

def test_sample_weights_are_applied():
    coords, x, y = grid_data()
    weights = np.ones(len(y))
    weights[0] = 0
    a = gwr_fit(coords, x, y, 4.0, kernel="gaussian")
    b = gwr_fit(coords, x, y, 4.0, kernel="gaussian", sample_weights=weights)
    np.testing.assert_allclose(a["coefficients"], b["coefficients"], atol=1e-10)

@pytest.mark.parametrize("kwargs", [
    {"bandwidth": 0.0}, {"bandwidth": -1.0}, {"bandwidth": np.nan},
    {"bandwidth": 2, "adaptive": True}, {"bandwidth": 100, "adaptive": True},
    {"bandwidth": 3, "kernel": "triangular"},
])
def test_rejects_invalid_bandwidth_or_kernel(kwargs):
    coords, x, y = grid_data()
    bandwidth = kwargs.pop("bandwidth")
    with pytest.raises(ValueError):
        gwr_fit(coords, x, y, bandwidth, **kwargs)

def test_rejects_bad_shapes_and_nonfinite_values():
    coords, x, y = grid_data()
    with pytest.raises(ValueError):
        gwr_fit(coords[:-1], x, y, 3.0)
    bad = coords.copy()
    bad[0, 0] = np.nan
    with pytest.raises(ValueError):
        gwr_fit(bad, x, y, 3.0)
    with pytest.raises(ValueError):
        gwr_fit(coords, x, y, 3.0, sample_weights=np.zeros(len(y)))

def test_rejects_local_rank_deficiency():
    coords = np.column_stack([np.arange(6.0), np.zeros(6)])
    x = np.column_stack([np.ones(6), np.arange(6.0), np.arange(6.0)])
    y = np.arange(6.0)
    with pytest.raises(ValueError, match="rank-deficient"):
        gwr_fit(coords, x, y, 1.0, kernel="gaussian")

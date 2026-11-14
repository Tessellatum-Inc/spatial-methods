import numpy as np
import pytest

from radial_spectrum import radial_average_amplitude, fit_single_layer_spectrum


def test_radial_average_returns_positive_non_dc_bins():
    y, x = np.mgrid[:48, :48]
    grid = np.sin(2 * np.pi * x / 8) + 0.4 * np.cos(2 * np.pi * y / 12) + 0.01 * np.random.default_rng(5).normal(size=x.shape)
    result = radial_average_amplitude(grid, 1, 1, n_bins=24, min_count=1)
    assert result["wavenumber"].size > 4
    assert np.all(result["wavenumber"] > 0)
    assert np.all(result["amplitude"] > 0)
    assert np.all(result["count"] >= 1)


@pytest.mark.parametrize("n", [-1, 0, 1])
def test_single_layer_fit_recovers_exact_synthetic_model(n):
    k = np.linspace(0.08, 1.2, 80)
    expected_b, expected_z = 3.7, 4.25
    amplitude = expected_b * k**n * np.exp(-k * expected_z)
    result = fit_single_layer_spectrum(k, amplitude)
    assert result["n"] == n
    assert result["B"] == pytest.approx(expected_b, rel=1e-10)
    assert result["z"] == pytest.approx(expected_z, rel=1e-10)
    assert result["rmse_log"] < 1e-10


def test_fit_can_restrict_wavenumber_band():
    k = np.linspace(0.05, 1.5, 100)
    a = 2.0 * k**0 * np.exp(-k * 2.5)
    result = fit_single_layer_spectrum(k, a, min_wavenumber=0.2, max_wavenumber=1.0)
    assert result["z"] == pytest.approx(2.5)
    assert result["n_bins"] < k.size


def test_negative_depth_is_constrained_to_zero():
    k = np.linspace(0.1, 1.0, 20)
    result = fit_single_layer_spectrum(k, np.exp(k), exponents=(0,))
    assert result["z"] == 0.0


def test_invalid_inputs_are_rejected():
    with pytest.raises(ValueError):
        radial_average_amplitude(np.ones((8, 8)), 0, 1)
    with pytest.raises(ValueError):
        fit_single_layer_spectrum([0.1, 0.2], [1, 2], min_bins=3)
    with pytest.raises(ValueError):
        fit_single_layer_spectrum(np.arange(1, 8), np.arange(1, 8), exponents=(2,))

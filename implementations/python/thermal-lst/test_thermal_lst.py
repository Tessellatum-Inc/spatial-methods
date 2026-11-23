import numpy as np
import pytest
from thermal_lst import brightness_temperature, single_channel_lst, split_window_lst


def test_planck_brightness_temperature_round_trip():
    radiance, k1, k2 = 8.0, 774.89, 1321.08
    temperature = brightness_temperature(radiance, k1, k2)
    assert temperature == pytest.approx(k2 / np.log1p(k1 / radiance))


def test_single_channel_inverts_radiative_transfer_exactly():
    k1, k2, surface_t = 774.89, 1321.08, 300.0
    eps, tau, lup, ldown = 0.97, 0.85, 1.2, 1.8
    blackbody = k1 / np.expm1(k2 / surface_t)
    sensor = tau * (eps * blackbody + (1 - eps) * ldown) + lup
    assert single_channel_lst(sensor, eps, tau, lup, ldown, k1, k2) == pytest.approx(surface_t)


def test_split_window_coefficients_apply_expected_expression():
    got = split_window_lst(300, 298, 0.98, 0.96, 1.5,
                           [1, 0.5, 0.1, 2, 0.2, 3, 0.4])
    dt = 2
    expected = 300 + .5 * dt + .1 * dt**2 + 1 + (2 + .2 * 1.5) * (1 - .97) + (3 + .4 * 1.5) * .02
    assert got == pytest.approx(expected)


def test_split_window_broadcasts_spatial_arrays():
    result = split_window_lst(np.full((2, 1), 300), np.full((1, 3), 299),
                              .98, .97, 1.0, np.zeros(7))
    assert result.shape == (2, 3)
    assert np.allclose(result, 300)


@pytest.mark.parametrize("args", [
    (0, 1, 1, 0, 0, 1, 1),
    (1, 0, 1, 0, 0, 1, 1),
    (1, 1, 0, 0, 0, 1, 1),
    (1, 1, 1, -1, 0, 1, 1),
])
def test_single_channel_invalid_physical_inputs(args):
    with pytest.raises(ValueError):
        single_channel_lst(*args)


def test_split_window_rejects_invalid_emissivity_and_coefficients():
    with pytest.raises(ValueError):
        split_window_lst(300, 299, 0, .98, 1, np.zeros(7))
    with pytest.raises(ValueError):
        split_window_lst(300, 299, .98, .98, 1, np.zeros(6))


def test_planck_rejects_nonpositive_radiance():
    with pytest.raises(ValueError):
        brightness_temperature(0, 774.89, 1321.08)

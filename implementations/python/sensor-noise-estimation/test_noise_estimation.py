import numpy as np
import pytest

from noise_estimation import (
    estimate_band_noise,
    estimate_gaussian_noise,
    haar_diagonal_detail,
)


def test_constant_and_planar_ramp_have_zero_diagonal_detail():
    y, x = np.indices((32, 40))
    assert np.allclose(haar_diagonal_detail(np.full((32, 40), 17.0)), 0)
    assert np.allclose(estimate_gaussian_noise(3 * x + 2 * y + 5), 0, atol=1e-12)


def test_seeded_white_gaussian_noise_estimate_is_close_to_sigma():
    rng = np.random.default_rng(20261118)
    sigma = 4.5
    noise = rng.normal(0, sigma, size=(512, 512))
    estimate = estimate_gaussian_noise(noise)
    assert estimate == pytest.approx(sigma, rel=0.025)


def test_smooth_signal_plus_noise_is_recovered_with_tolerance():
    rng = np.random.default_rng(83)
    y, x = np.indices((512, 512))
    smooth = 0.01 * x + 0.02 * y + 0.00001 * x * y
    sigma = 2.0
    observed = smooth + rng.normal(0, sigma, size=smooth.shape)
    assert estimate_gaussian_noise(observed) == pytest.approx(sigma, rel=0.06)


def test_band_estimates_are_independent_and_ordered():
    rng = np.random.default_rng(12)
    sigmas = [1.0, 2.5, 5.0]
    cube = np.stack([rng.normal(0, s, size=(384, 384)) for s in sigmas], axis=2)
    estimates = estimate_band_noise(cube)
    assert estimates.shape == (3,)
    assert np.allclose(estimates, sigmas, rtol=0.04)
    assert np.all(np.diff(estimates) > 0)


@pytest.mark.parametrize("image", [
    np.ones(8),
    np.ones((1, 8)),
    np.full((4, 4), np.nan),
    np.full((4, 4), np.inf),
])
def test_invalid_single_band_inputs_are_rejected(image):
    with pytest.raises(ValueError):
        estimate_gaussian_noise(image)


def test_invalid_multiband_inputs_are_rejected():
    with pytest.raises(ValueError):
        estimate_band_noise(np.ones((8, 8)))
    with pytest.raises(ValueError):
        estimate_band_noise(np.ones((8, 8, 0)))
    bad = np.ones((8, 8, 2))
    bad[0, 0, 1] = np.nan
    with pytest.raises(ValueError):
        estimate_band_noise(bad)


def test_odd_dimensions_drop_only_last_unpaired_row_and_column():
    image = np.arange(35, dtype=float).reshape(5, 7)
    assert haar_diagonal_detail(image).shape == (2, 3)

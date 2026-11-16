import numpy as np
import pytest
from continuum_removal import continuum_removal


def test_flat_spectrum_has_unit_continuum_ratio_and_zero_absorption():
    wave = np.array([400., 500., 600., 700.])
    out = continuum_removal(np.ones(4), wave)
    np.testing.assert_allclose(out["continuum_removed"], 1.0)
    np.testing.assert_allclose(out["absorption_depth"], 0.0)
    assert out["absorption_area"] == pytest.approx(0.0)


def test_absorption_feature_is_removed_and_area_is_positive():
    wave = np.linspace(400., 800., 9)
    spectrum = np.ones(9)
    spectrum[4] = 0.5
    out = continuum_removal(spectrum, wave)
    assert out["continuum"][4] == pytest.approx(1.0)
    assert out["continuum_removed"][4] == pytest.approx(0.5)
    assert out["absorption_depth"][4] == pytest.approx(0.5)
    assert out["absorption_area"] > 0


def test_multiple_spectra_keep_leading_dimensions():
    wave = np.array([1., 2., 3., 4.])
    spectra = np.array([[1., .8, 1., 1.], [2., 2., 1., 2.]])
    out = continuum_removal(spectra, wave)
    assert out["continuum"].shape == spectra.shape
    assert out["absorption_area"].shape == (2,)


@pytest.mark.parametrize("wave", [[1., 1., 2.], [1., 2.], [1., 3., 2.]])
def test_invalid_wavelengths_rejected(wave):
    with pytest.raises(ValueError):
        continuum_removal(np.ones(3), wave)


def test_nonpositive_continuum_and_negative_reflectance_rejected():
    with pytest.raises(ValueError):
        continuum_removal(np.zeros(3), [1., 2., 3.])
    with pytest.raises(ValueError):
        continuum_removal(np.array([1., -1., 1.]), [1., 2., 3.])

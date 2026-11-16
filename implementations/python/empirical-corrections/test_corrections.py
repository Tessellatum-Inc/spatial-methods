import numpy as np
import pytest
from corrections import dark_object_subtraction, c_correction, minnaert_correction


def test_dark_object_subtraction_per_band_and_mask():
    image = np.array([[[10., 20.], [11., 22.]], [[100., 200.], [12., 24.]]])
    mask = np.array([[True, True], [False, True]])
    out = dark_object_subtraction(image, valid_mask=mask, dark_percentile=0)
    np.testing.assert_allclose(out["path_radiance"], [10., 20.])
    np.testing.assert_allclose(out["corrected"][0, 0], [0., 0.])
    assert np.all(out["corrected"] >= 0)


def test_dark_object_subtraction_can_preserve_negative_values():
    out = dark_object_subtraction(np.array([[1., 3.], [2., 4.]]),
                                  dark_percentile=50, clip_negative=False)
    assert np.min(out["corrected"]) < 0


def test_c_correction_recovers_flat_surface_reflectance():
    ci = np.array([[0.2, 0.4], [0.6, 0.8]])
    cz = 0.7
    c = 0.2
    base = 0.3
    rho = base * (ci + c) / (cz + c)
    out = c_correction(rho, ci, np.full_like(ci, cz))
    np.testing.assert_allclose(out["corrected"], base, atol=1e-10)
    assert out["c_parameters"] == pytest.approx(c)


def test_minnaert_correction_and_invalid_illumination():
    ci = np.array([[0.25, 0.5], [0.0, 1.0]])
    cz = np.full((2, 2), 0.5)
    rho = np.ones((2, 2))
    out = minnaert_correction(rho, ci, cz, k=1.0)
    assert out["corrected"][0, 0] == pytest.approx(2.0)
    assert np.isnan(out["corrected"][1, 0])


def test_invalid_shapes_percentiles_and_exponents():
    with pytest.raises(ValueError):
        dark_object_subtraction(np.ones((2, 2)), dark_percentile=80)
    with pytest.raises(ValueError):
        c_correction(np.ones((2, 2)), np.ones((2, 2)), np.ones((3, 2)))
    with pytest.raises(ValueError):
        minnaert_correction(np.ones((2, 2, 3)), np.ones((2, 2)),
                            np.ones((2, 2)), k=[1, 2])

import numpy as np
import pytest
from corrections import (dark_object_subtraction, c_correction, minnaert_correction,
                          histogram_match, pseudo_invariant_feature_normalization,
                          fit_empirical_line, apply_empirical_line, scs_c_correction)


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


def test_histogram_match_maps_empirical_quantiles_and_constant_band():
    source = np.array([[0., 0.], [1., 0.], [2., 0.], [3., 0.]])
    reference = np.array([[10., 7.], [20., 7.], [30., 7.], [40., 7.]])
    out = histogram_match(source, reference, quantiles=16)["matched"]
    np.testing.assert_allclose(out[:, 0], [10., 20., 30., 40.], atol=1e-10)
    np.testing.assert_allclose(out[:, 1], 7.0)


def test_histogram_match_respects_mask_and_rejects_bad_inputs():
    source = np.array([[0., 1.], [100., 3.]])
    reference = np.array([[10., 11.], [200., 13.]])
    mask = np.array([[True, True], [False, True]])
    out = histogram_match(source, reference, valid_mask=mask, quantiles=8)["matched"]
    assert out[1, 0] == pytest.approx(13.0)
    with pytest.raises(ValueError):
        histogram_match(source, reference[:, :1])
    with pytest.raises(ValueError):
        histogram_match(source, reference, quantiles=1)


def test_pif_normalization_recovers_known_affine_band_maps():
    reference = np.array([[[2., 5.], [4., 9.], [6., 13.]],
                          [[8., 17.], [10., 21.], [12., 25.]]])
    target = np.array([[[1., 2.], [2., 4.], [3., 6.]],
                       [[4., 8.], [5., 10.], [6., 12.]]])
    out = pseudo_invariant_feature_normalization(reference, target, stable_fraction=1.0)
    np.testing.assert_allclose(out["gain"], [2., 2.])
    np.testing.assert_allclose(out["offset"], [0., 1.])
    np.testing.assert_allclose(out["normalized"], reference, atol=1e-10)
    assert out["stable_mask"].all()


def test_pif_normalization_selects_stable_subset_and_honours_mask():
    target = np.arange(24., dtype=float).reshape(3, 4, 2)
    reference = target * 2.0 + np.array([3.0, -1.0])
    reference[0, 0] += 1000.0
    mask = np.ones((3, 4), dtype=bool)
    mask[2, 3] = False
    out = pseudo_invariant_feature_normalization(reference, target,
                                                   valid_mask=mask, stable_fraction=0.75)
    assert out["stable_mask"].sum() == 9
    assert not out["stable_mask"][2, 3]
    np.testing.assert_allclose(out["gain"], [2., 2.], atol=1e-10)


def test_pif_normalization_rejects_insufficient_or_constant_data():
    with pytest.raises(ValueError):
        pseudo_invariant_feature_normalization(np.ones((2, 2)), np.ones((2, 2)))
    with pytest.raises(ValueError):
        pseudo_invariant_feature_normalization(np.ones((2, 2)), np.ones((2, 2)),
                                                stable_fraction=0)



def test_empirical_line_fits_and_applies_multiband_calibration():
    dn = np.array([[10., 20.], [20., 30.], [40., 50.], [60., 80.]])
    reflectance = dn * np.array([0.002, 0.001]) + np.array([0.01, 0.03])
    calibration = fit_empirical_line(dn, reflectance)
    np.testing.assert_allclose(calibration["gain"], [0.002, 0.001], atol=1e-12)
    np.testing.assert_allclose(calibration["offset"], [0.01, 0.03], atol=1e-12)
    np.testing.assert_allclose(calibration["r_squared"], 1.0)
    image = np.stack([dn.reshape(2, 2, 2)[:, :, 0],
                      dn.reshape(2, 2, 2)[:, :, 1]], axis=-1)
    calibrated = apply_empirical_line(image, calibration)
    np.testing.assert_allclose(calibrated, image * [0.002, 0.001] + [0.01, 0.03])


def test_empirical_line_single_band_and_explicit_clipping():
    calibration = fit_empirical_line([0, 10, 20], [0.0, 0.5, 1.0])
    image = np.array([[-5., 10.], [20., 30.]])
    result = apply_empirical_line(image, calibration, clip=(0.0, 1.0))
    np.testing.assert_allclose(result, [[0.0, 0.5], [1.0, 1.0]])


def test_empirical_line_rejects_invalid_samples_and_coefficients():
    with pytest.raises(ValueError):
        fit_empirical_line([1, 1, 1], [0.1, 0.2, 0.3])
    with pytest.raises(ValueError):
        fit_empirical_line([[1, 2], [2, 3]], [[0.1], [0.2]])
    with pytest.raises(ValueError):
        apply_empirical_line(np.ones((2, 2, 3)), {"gain": [1, 2], "offset": [0, 0]})
    with pytest.raises(ValueError):
        apply_empirical_line(np.ones((2, 2)), {"gain": [1], "offset": [0]}, clip=(2, 1))



def test_scs_c_fits_slope_adjusted_relation_and_applies_equation():
    slope = np.array([[0.0, 0.2], [0.35, 0.5]])
    ci = np.array([[0.2, 0.4], [0.6, 0.8]])
    cz = np.full((2, 2), 0.7)
    c, a = 0.25, 0.4
    rho = np.cos(slope) * (a * ci + a * c)
    out = scs_c_correction(rho, slope, ci, cz)
    assert out["c_parameters"] == pytest.approx(c)
    expected = rho * (np.cos(slope) * cz + c) / (ci + c)
    np.testing.assert_allclose(out["corrected"], expected, atol=1e-12)


def test_scs_c_multiband_mask_and_validation():
    slope = np.full((2, 2), 0.2)
    ci = np.array([[0.2, 0.4], [0.6, 0.8]])
    cz = np.full((2, 2), 0.7)
    rho = np.stack([ci + 0.2, 2 * (ci + 0.3)], axis=-1)
    mask = np.array([[True, True], [True, False]])
    out = scs_c_correction(rho, slope, ci, cz, valid_mask=mask)
    assert out["corrected"].shape == rho.shape
    assert np.isnan(out["corrected"][1, 1]).all()
    with pytest.raises(ValueError):
        scs_c_correction(np.ones((2, 2)), np.full((2, 2), np.pi / 2),
                         ci, cz)
    with pytest.raises(ValueError):
        scs_c_correction(np.ones((2, 2)), slope, np.ones((2, 2)), cz)

import numpy as np
import pytest
from corrections import (dark_object_subtraction, c_correction, minnaert_correction,
                          histogram_match, pseudo_invariant_feature_normalization)


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

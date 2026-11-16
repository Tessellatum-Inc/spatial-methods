import numpy as np
import pytest

from resampling import resample_to_shape


def test_nearest_preserves_categorical_values():
    source = np.array([[1, 2], [3, 4]])
    result = resample_to_shape(source, (4, 4), method="nearest")
    assert set(np.unique(result)) == {1, 2, 3, 4}


def test_bilinear_preserves_constant_surface():
    result = resample_to_shape(np.full((3, 4), 7.5), (8, 9))
    np.testing.assert_allclose(result, 7.5)


def test_bilinear_reproduces_planar_surface_at_mapped_centres():
    source = np.fromfunction(lambda r, c: 2 * r + 3 * c, (4, 4), dtype=float)
    result = resample_to_shape(source, (7, 7))
    np.testing.assert_allclose(result[3, 3], 7.5, atol=1e-12)


def test_strict_nodata_policy_masks_missing_positive_weight_neighbours():
    source = np.array([[1, np.nan], [3, 4]], float)
    result = resample_to_shape(source, (3, 3), nodata_policy="strict")
    assert np.isnan(result[1, 1])


def test_renormalize_policy_uses_available_bilinear_neighbours():
    source = np.array([[1, np.nan], [3, 4]], float)
    result = resample_to_shape(source, (3, 3), nodata_policy="renormalize")
    assert np.isfinite(result[1, 1])
    np.testing.assert_allclose(result[1, 1], 8 / 3)


def test_exact_source_centres_do_not_require_zero_weight_nodata_neighbours():
    source = np.array([[1, np.nan], [3, 4]], float)
    result = resample_to_shape(source, (2, 2), nodata_policy="strict")
    assert result[0, 0] == 1


@pytest.mark.parametrize("method", ["bilinear", "cubic", "lanczos"])
def test_continuous_kernels_preserve_constant_surface(method):
    source = np.full((6, 7), 12.25)
    result = resample_to_shape(source, (11, 13), method=method)
    np.testing.assert_allclose(result, 12.25, atol=1e-10)


def test_cubic_kernel_reproduces_linear_ramp_interior():
    source = np.fromfunction(lambda r, c: 2 * r - 3 * c + 5, (12, 13), dtype=float)
    result = resample_to_shape(source, (24, 26), method="cubic")
    np.testing.assert_allclose(result[10, 12], 2 * 4.75 - 3 * 5.75 + 5, atol=1e-9)


def test_lanczos_matches_independent_windowed_sinc_reference():
    source = np.fromfunction(lambda r, c: 2 * r - 3 * c + 5, (12, 13), dtype=float)
    result = resample_to_shape(source, (24, 26), method="lanczos")
    # Lanczos-3 is a truncated windowed-sinc interpolator; unlike ideal
    # infinite sinc, its discrete first moment is not exactly zero at every
    # fractional offset. Compare with a direct independent kernel sum.
    sr, sc = 4.75, 5.75
    expected_numerator = 0.0
    expected_denominator = 0.0
    for rr in range(2, 8):
        wr = np.sinc(sr - rr) * np.sinc((sr - rr) / 3)
        for cc in range(3, 9):
            wc = np.sinc(sc - cc) * np.sinc((sc - cc) / 3)
            weight = wr * wc
            expected_numerator += source[rr, cc] * weight
            expected_denominator += weight
    expected = expected_numerator / expected_denominator
    np.testing.assert_allclose(result[10, 12], expected, atol=1e-12)


@pytest.mark.parametrize("method", ["cubic", "lanczos"])
def test_strict_nodata_policy_masks_nonzero_kernel_support(method):
    source = np.ones((7, 7), dtype=float)
    source[3, 3] = np.nan
    result = resample_to_shape(source, (14, 14), method=method, nodata_policy="strict")
    assert np.isnan(result[6, 6])


@pytest.mark.parametrize("method", ["nearest", "bilinear", "cubic", "lanczos"])
def test_output_shape_and_finite_values_for_fully_valid_source(method):
    source = np.arange(30, dtype=float).reshape(5, 6)
    result = resample_to_shape(source, (8, 9), method=method)
    assert result.shape == (8, 9)
    assert np.isfinite(result).all()


def test_invalid_shape_method_and_policy_are_rejected():
    with pytest.raises(ValueError, match="positive integers"):
        resample_to_shape([[1]], (0, 2))
    with pytest.raises(ValueError, match="method"):
        resample_to_shape([[1]], (2, 2), method="spline")
    with pytest.raises(ValueError, match="nodata_policy"):
        resample_to_shape([[1]], (2, 2), nodata_policy="ignore")
    with pytest.raises(ValueError, match="2D"):
        resample_to_shape([1, 2], (2, 2))

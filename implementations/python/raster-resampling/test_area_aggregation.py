import numpy as np
import pytest

from area_aggregation import area_weighted_resample


def test_exact_two_by_two_to_one_by_one_mean():
    result = area_weighted_resample([[1, 3], [5, 7]], (1, 1))
    np.testing.assert_allclose(result, [[4.0]])


def test_aligned_aggregation_preserves_global_mean():
    source = np.arange(16, dtype=float).reshape(4, 4)
    result = area_weighted_resample(source, (2, 2))
    np.testing.assert_allclose(result, [[2.5, 4.5], [10.5, 12.5]])
    np.testing.assert_allclose(result.mean(), source.mean())


def test_non_integer_scale_factors_preserve_global_mean():
    source = np.arange(15, dtype=float).reshape(3, 5)
    result = area_weighted_resample(source, (2, 3))
    assert result.shape == (2, 3)
    np.testing.assert_allclose(result.mean(), source.mean(), atol=1e-12)


def test_nodata_strict_and_renormalize_policies():
    source = np.array([[1.0, np.nan], [3.0, 5.0]])
    strict = area_weighted_resample(source, (1, 1), nodata_policy="strict")
    renormalized = area_weighted_resample(source, (1, 1), nodata_policy="renormalize")
    assert np.isnan(strict[0, 0])
    np.testing.assert_allclose(renormalized, [[3.0]])


def test_invalid_inputs_are_rejected():
    with pytest.raises(ValueError, match="2D"):
        area_weighted_resample([1, 2], (1, 1))
    with pytest.raises(ValueError, match="positive integers"):
        area_weighted_resample([[1]], (0, 1))
    with pytest.raises(ValueError, match="nodata_policy"):
        area_weighted_resample([[1]], (1, 1), nodata_policy="ignore")

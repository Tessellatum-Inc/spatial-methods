import numpy as np
import pytest
from image_registration import phase_correlation, estimate_affine_ransac


def test_phase_correlation_recovers_integer_translation_to_apply():
    rng = np.random.default_rng(4)
    reference = rng.normal(size=(64, 64))
    moving = np.roll(reference, shift=(5, -7), axis=(0, 1))
    result = phase_correlation(reference, moving, window=False)
    assert result["shift_to_apply"] == pytest.approx((-5, 7), abs=.1)


def test_phase_correlation_subpixel_peak_and_validation():
    rng = np.random.default_rng(2)
    image = rng.normal(size=(32, 32))
    result = phase_correlation(image, image, upsample_factor=10)
    assert result["shift_to_apply"] == pytest.approx((0, 0), abs=.1)
    with pytest.raises(ValueError):
        phase_correlation(np.ones((2, 2)), np.ones((2, 2)))


def test_affine_ransac_recovers_transform_with_outliers():
    rng = np.random.default_rng(3)
    src = rng.uniform(-10, 10, size=(30, 2))
    matrix = np.array([[1.02, .03], [-.02, .98]])
    offset = np.array([4., -3.])
    dst = src @ matrix.T + offset + rng.normal(0, .01, size=src.shape)
    dst[-8:] = rng.uniform(-30, 30, size=(8, 2))
    result = estimate_affine_ransac(src, dst, residual_threshold=.1, random_state=5)
    assert result["inlier_count"] >= 20
    np.testing.assert_allclose(result["matrix"], matrix, atol=.02)
    np.testing.assert_allclose(result["offset"], offset, atol=.03)


def test_affine_ransac_rejects_degenerate_or_invalid_matches():
    with pytest.raises(ValueError):
        estimate_affine_ransac([[0,0],[1,1],[2,2]], [[0,0],[1,1],[2,2]])
    with pytest.raises(ValueError):
        estimate_affine_ransac([[0,0],[1,0],[0,1]], [[0,0],[1,0],[0,1]], residual_threshold=0)

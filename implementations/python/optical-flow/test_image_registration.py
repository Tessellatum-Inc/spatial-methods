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


from image_registration import orb_feature_matches


def test_orb_matches_translated_texture_and_affine_ransac_recovers_shift():
    import cv2
    rng = np.random.default_rng(13)
    reference = (rng.random((256, 256)) * 255).astype(np.uint8)
    reference = cv2.GaussianBlur(reference, (3, 3), 0.7)
    transform = np.array([[1., 0., 7.], [0., 1., -5.]], dtype=np.float32)
    moving = cv2.warpAffine(reference, transform, (256, 256),
                            flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    matches = orb_feature_matches(reference, moving, max_features=1500)
    assert matches["match_count"] > 30
    fit = estimate_affine_ransac(matches["source_points"], matches["target_points"],
                                 residual_threshold=1.0, random_state=4)
    assert fit["inlier_count"] > 25
    np.testing.assert_allclose(fit["matrix"], np.eye(2), atol=0.02)
    np.testing.assert_allclose(fit["offset"], [-7., 5.], atol=0.5)


def test_orb_feature_matches_rejects_blank_and_nonfinite_images():
    with pytest.raises(ValueError, match="too few features"):
        orb_feature_matches(np.zeros((32, 32)), np.zeros((32, 32)))
    bad = np.ones((32, 32))
    bad[0, 0] = np.nan
    with pytest.raises(ValueError, match="finite"):
        orb_feature_matches(bad, np.ones((32, 32)))

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


from image_registration import local_feature_matches


@pytest.mark.parametrize("detector", ["SIFT", "AKAZE"])
def test_sift_and_akaze_match_translated_texture(detector):
    import cv2
    rng = np.random.default_rng(13)
    reference = (rng.random((256, 256)) * 255).astype(np.uint8)
    reference = cv2.GaussianBlur(reference, (3, 3), 0.7)
    moving = cv2.warpAffine(reference,
        np.array([[1., 0., 7.], [0., 1., -5.]], dtype=np.float32),
        (256, 256), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    matches = local_feature_matches(reference, moving, detector=detector,
                                    max_features=1500)
    assert matches["detector"] == detector
    assert matches["match_count"] > 20
    fit = estimate_affine_ransac(matches["source_points"], matches["target_points"],
                                 residual_threshold=1.0, random_state=4)
    assert fit["inlier_count"] > 20
    np.testing.assert_allclose(fit["matrix"], np.eye(2), atol=0.03)
    np.testing.assert_allclose(fit["offset"], [-7., 5.], atol=0.6)


def test_local_feature_matching_rejects_unknown_detector():
    with pytest.raises(ValueError, match="detector must be"):
        local_feature_matches(np.ones((32, 32)), np.ones((32, 32)),
                              detector="unsupported")


from image_registration import ecc_register


def test_ecc_translation_registration_recovers_subpixel_shift():
    import cv2
    rng = np.random.default_rng(4)
    reference = (rng.random((128, 128)) * 255).astype(np.uint8)
    reference = cv2.GaussianBlur(reference, (3, 3), 0.8)
    expected = np.array([[1., 0., 1.5], [0., 1., -1.25]], dtype=np.float32)
    moving = cv2.warpAffine(reference, expected, (128, 128),
                            flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    result = ecc_register(reference, moving, motion_model="translation",
                          max_iterations=500, epsilon=1e-7)
    np.testing.assert_allclose(result["warp_matrix"], expected, atol=0.06)
    assert result["correlation"] > 0.85
    assert result["aligned"].shape == reference.shape


def test_ecc_rejects_invalid_controls_and_shapes():
    with pytest.raises(ValueError, match="matching 2D"):
        ecc_register(np.ones((16, 16)), np.ones((16, 15)))
    with pytest.raises(ValueError, match="motion_model"):
        ecc_register(np.ones((16, 16)), np.ones((16, 16)), motion_model="rigid3d")
    with pytest.raises(ValueError, match="positive odd"):
        ecc_register(np.ones((16, 16)), np.ones((16, 16)), gauss_filter_size=4)


from image_registration import local_phase_correlation_field


def test_local_phase_correlation_recovers_tiled_displacement_field():
    import cv2
    rng = np.random.default_rng(21)
    reference = (rng.random((160, 160)) * 255).astype(np.float32)
    reference = cv2.GaussianBlur(reference, (3, 3), 0.6)
    moving = cv2.warpAffine(reference,
        np.array([[1., 0., 3.], [0., 1., -2.]], dtype=np.float32),
        (160, 160), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    result = local_phase_correlation_field(reference, moving,
        window_size=48, step=32, upsample_factor=10)
    assert result["row_shift"].shape == (4, 4)
    valid = np.isfinite(result["row_shift"])
    assert valid.sum() >= 12
    np.testing.assert_allclose(np.nanmedian(result["row_shift"]), 2.0, atol=0.25)
    np.testing.assert_allclose(np.nanmedian(result["column_shift"]), -3.0, atol=0.25)


def test_local_phase_correlation_masks_textureless_windows():
    blank = np.zeros((96, 96))
    result = local_phase_correlation_field(blank, blank, window_size=32, step=32)
    assert np.isnan(result["row_shift"]).all()
    assert np.isnan(result["column_shift"]).all()
    with pytest.raises(ValueError, match="window_size"):
        local_phase_correlation_field(blank, blank, window_size=128)


from image_registration import mutual_information_translation


def test_mutual_information_translation_handles_nonlinear_radiometry():
    import cv2
    from scipy.ndimage import shift as nd_shift
    rng = np.random.default_rng(19)
    reference = rng.normal(size=(128, 128))
    reference = cv2.GaussianBlur(reference.astype(np.float32), (3, 3), 0.7)
    transformed = np.sign(reference) * np.log1p(np.abs(reference) * 2.0)
    moving = nd_shift(transformed, shift=(2.5, -3.25), order=1,
                      mode="constant", cval=0.0, prefilter=False)
    result = mutual_information_translation(reference, moving,
        max_shift=8.0, bins=32, min_overlap_fraction=0.5)
    np.testing.assert_allclose(result["shift_to_apply"], (-2.5, 3.25), atol=0.2)
    assert result["mutual_information"] > 0.8
    assert result["overlap_fraction"] > 0.9


def test_mutual_information_translation_validates_controls():
    with pytest.raises(ValueError, match="non-zero intensity"):
        mutual_information_translation(np.ones((16, 16)), np.ones((16, 16)))
    with pytest.raises(ValueError, match="bins"):
        mutual_information_translation(np.arange(256).reshape(16, 16),
                                        np.arange(256).reshape(16, 16), bins=4)

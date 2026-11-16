import numpy as np
import pytest
from ir_mad import ir_mad


def test_identical_images_have_high_no_change_weights():
    rng = np.random.default_rng(41)
    image = rng.normal(size=(12, 10, 3))
    result = ir_mad(image, image.copy())
    assert result["mad_variates"].shape == (12, 10, 3)
    assert np.nanmin(result["weights"]) > 0.99
    assert result["canonical_correlations"].shape == (3,)


def test_affine_band_response_is_removed_but_changed_patch_is_downweighted():
    rng = np.random.default_rng(7)
    reference = rng.normal(size=(30, 30, 2))
    target = reference @ np.array([[1.2, 0.15], [-0.1, 0.85]]) + [0.4, -0.2]
    target[4:11, 18:26] += np.array([5.0, -4.0])
    result = ir_mad(reference, target, max_iterations=80, tolerance=1e-7)
    changed = result["weights"][4:11, 18:26]
    stable = np.concatenate((result["weights"][:4].ravel(),
                             result["weights"][12:].ravel()))
    assert np.nanmedian(changed) < np.nanmedian(stable)
    assert np.nanmedian(result["chi_square"][4:11, 18:26]) > 1.0


def test_mask_excludes_cloud_pixels_and_preserves_nan_output():
    rng = np.random.default_rng(3)
    reference = rng.normal(size=(8, 9, 2))
    target = reference + 0.01
    mask = np.ones((8, 9), dtype=bool)
    mask[:2, :3] = False
    result = ir_mad(reference, target, valid_mask=mask)
    assert np.isnan(result["weights"][:2, :3]).all()
    assert np.isfinite(result["weights"][mask]).all()


def test_different_band_counts_are_supported():
    rng = np.random.default_rng(9)
    reference = rng.normal(size=(10, 10, 3))
    target = np.column_stack((reference.reshape(-1, 3)[:, :2],
                              reference.reshape(-1, 3)[:, 2])).reshape(10, 10, 3)
    result = ir_mad(reference, target[..., :2])
    assert result["mad_variates"].shape == (10, 10, 2)


@pytest.mark.parametrize("kwargs", [
    {"max_iterations": 0}, {"tolerance": 0}, {"ridge": -1},
    {"min_weight": 0}, {"min_weight": 2},
])
def test_invalid_controls_are_rejected(kwargs):
    image = np.arange(36.0).reshape(6, 6)
    with pytest.raises(ValueError):
        ir_mad(image, image, **kwargs)


def test_invalid_shapes_and_too_few_pixels_are_rejected():
    with pytest.raises(ValueError):
        ir_mad(np.ones((4, 4)), np.ones((4, 5)))
    with pytest.raises(ValueError):
        ir_mad(np.ones((2, 2, 3)), np.ones((2, 2, 3)))
    with pytest.raises(ValueError):
        ir_mad(np.ones((5, 5)), np.ones((5, 5)), valid_mask=np.ones((5, 5), dtype=int))

import numpy as np
import pytest
from cloud_masks import (
    landsat_qa_pixel_clear_mask, sentinel2_scl_clear_mask,
    cloud_probability_clear_mask,
)


def test_landsat_qa_pixel_masks_fill_cloud_shadow_snow_and_cirrus_bits():
    qa = np.array([1 << 6, (1 << 6) | (1 << 7), 1 << 0, 1 << 1,
                   1 << 2, 1 << 3, 1 << 4, 1 << 5], dtype=np.uint16)
    assert landsat_qa_pixel_clear_mask(qa).tolist() == [True, True, False, False, False, False, False, False]


def test_landsat_qa_pixel_options_can_retain_snow_cirrus_or_dilated_cloud():
    qa = np.array([(1 << 6) | (1 << 1), (1 << 6) | (1 << 2), (1 << 6) | (1 << 5)])
    assert landsat_qa_pixel_clear_mask(qa, mask_dilated_cloud=False).tolist() == [True, False, False]
    assert landsat_qa_pixel_clear_mask(qa, mask_cirrus=False).tolist() == [False, True, False]
    assert landsat_qa_pixel_clear_mask(qa, mask_snow=False).tolist() == [False, False, True]


def test_sentinel2_scl_clear_classes_and_optional_unclassified():
    scl = np.arange(12, dtype=np.uint8)
    assert sentinel2_scl_clear_mask(scl).tolist() == [False, False, False, False, True, True, True, False, False, False, False, False]
    assert sentinel2_scl_clear_mask(scl, include_unclassified=True)[7]


def test_sentinel2_scl_can_retain_snow_ice():
    assert sentinel2_scl_clear_mask([11], mask_snow=False).tolist() == [True]


def test_cloud_probability_threshold_is_inclusive_on_clear_side():
    assert cloud_probability_clear_mask([0, 39.9, 40, 80], threshold=40).tolist() == [True, True, False, False]


@pytest.mark.parametrize("bad", [[-1], [12], [1.0], []])
def test_scl_rejects_invalid_class_arrays(bad):
    with pytest.raises(ValueError):
        sentinel2_scl_clear_mask(bad)


def test_landsat_rejects_invalid_fields_and_non_boolean_options():
    with pytest.raises(ValueError):
        landsat_qa_pixel_clear_mask([-1])
    with pytest.raises(ValueError):
        landsat_qa_pixel_clear_mask([65536])
    with pytest.raises(ValueError):
        landsat_qa_pixel_clear_mask([64], mask_snow=1)


def test_cloud_probability_rejects_invalid_values_and_thresholds():
    with pytest.raises(ValueError):
        cloud_probability_clear_mask([-1, 50])
    with pytest.raises(ValueError):
        cloud_probability_clear_mask([10, np.nan])
    with pytest.raises(ValueError):
        cloud_probability_clear_mask([10, 50], threshold=101)

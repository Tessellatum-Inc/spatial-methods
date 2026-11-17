"""Quality-bit and scene-classification cloud/shadow mask helpers."""
import numpy as np


def _integer_array(values, name):
    array = np.asarray(values)
    if array.size == 0 or not np.issubdtype(array.dtype, np.integer) or np.issubdtype(array.dtype, np.bool_):
        raise ValueError(f"{name} must be a non-empty integer array")
    return array


def landsat_qa_pixel_clear_mask(qa_pixel, *, mask_snow=True, mask_cirrus=True,
                                mask_dilated_cloud=True, require_clear_bit=True):
    """Return clear pixels from Landsat Collection 2 QA_PIXEL bit fields.

    Masks fill, cloud and cloud-shadow flags; snow, cirrus and dilated-cloud
    flags are configurable. The clear bit is required by default. Water is
    retained as clear unless another quality flag marks it invalid.
    """
    qa = _integer_array(qa_pixel, "qa_pixel")
    if np.any(qa < 0) or np.any(qa > 65535):
        raise ValueError("qa_pixel values must fit an unsigned 16-bit field")
    for name, value in (("mask_snow", mask_snow), ("mask_cirrus", mask_cirrus),
                        ("mask_dilated_cloud", mask_dilated_cloud),
                        ("require_clear_bit", require_clear_bit)):
        if not isinstance(value, bool):
            raise ValueError(f"{name} must be boolean")
    invalid_bits = (1 << 0) | (1 << 3) | (1 << 4)
    if mask_dilated_cloud:
        invalid_bits |= 1 << 1
    if mask_cirrus:
        invalid_bits |= 1 << 2
    if mask_snow:
        invalid_bits |= 1 << 5
    clear = (qa & invalid_bits) == 0
    if require_clear_bit:
        clear &= (qa & (1 << 6)) != 0
    return clear


def sentinel2_scl_clear_mask(scl, *, include_unclassified=False, mask_snow=True):
    """Return clear pixels from Sentinel-2 Scene Classification Layer codes.

    Clear classes are vegetation (4), bare/non-vegetated (5) and water (6).
    Unclassified (7) is optional. No-data, saturated, dark, shadow, cloud,
    cirrus and (by default) snow/ice classes are not marked clear.
    """
    classes = _integer_array(scl, "scl")
    if np.any(classes < 0) or np.any(classes > 11):
        raise ValueError("Sentinel-2 SCL classes must be integers from 0 through 11")
    if not isinstance(include_unclassified, bool) or not isinstance(mask_snow, bool):
        raise ValueError("mask options must be boolean")
    clear = (classes == 4) | (classes == 5) | (classes == 6)
    if include_unclassified:
        clear |= classes == 7
    if not mask_snow:
        clear |= classes == 11
    return clear


def cloud_probability_clear_mask(probability, *, threshold=40.0):
    """Threshold a 0–100 cloud-probability layer; lower values are clearer."""
    p = np.asarray(probability, dtype=float)
    if p.size == 0 or not np.isfinite(p).all() or np.any((p < 0) | (p > 100)):
        raise ValueError("probability must be a non-empty finite array in [0, 100]")
    if isinstance(threshold, bool) or not isinstance(threshold, (int, float)) or not np.isfinite(threshold) or not 0 <= threshold <= 100:
        raise ValueError("threshold must be a finite number in [0, 100]")
    return p < float(threshold)

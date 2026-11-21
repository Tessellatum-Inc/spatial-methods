#!/usr/bin/env python3
"""Numerical primitives for the Fiji Sentinel-2 multispectral pilot.

This module deliberately separates reproducible spectral calculations from
STAC discovery and raster I/O. Arrays must be co-registered and expressed in
consistent reflectance units before indices are calculated. It does not assign
land-cover classes or claim ground truth.
"""
from __future__ import annotations

from typing import Any

import numpy as np

# Sentinel-2 Scene Classification Layer classes that are unsuitable for
# ordinary surface-reflectance index summaries.
SCL_INVALID_CLASSES = frozenset({0, 1, 3, 7, 8, 9, 10, 11})


def _as_float_array(values: Any) -> np.ndarray:
    """Convert input to float64 while preserving NaN as the nodata convention."""
    array = np.asarray(values, dtype=np.float64)
    if array.ndim == 0:
        array = array.reshape(1)
    return array


def safe_normalized_difference(
    numerator_band: Any,
    denominator_band: Any,
    *,
    epsilon: float = 1e-10,
) -> np.ndarray:
    """Return (A-B)/(A+B), setting invalid or near-zero denominators to NaN."""
    a = _as_float_array(numerator_band)
    b = _as_float_array(denominator_band)
    a, b = np.broadcast_arrays(a, b)
    denominator = a + b
    valid = np.isfinite(a) & np.isfinite(b) & (np.abs(denominator) > epsilon)
    result = np.full(a.shape, np.nan, dtype=np.float64)
    np.divide(a - b, denominator, out=result, where=valid)
    return result


def ndvi(b08: Any, b04: Any) -> np.ndarray:
    """Normalized Difference Vegetation Index: (B08-B04)/(B08+B04)."""
    return safe_normalized_difference(b08, b04)


def ndwi_mcfeeters(b03: Any, b08: Any) -> np.ndarray:
    """McFeeters NDWI: (B03-B08)/(B03+B08)."""
    return safe_normalized_difference(b03, b08)


def mndwi(b03: Any, b11: Any) -> np.ndarray:
    """Modified NDWI: (B03-B11)/(B03+B11)."""
    return safe_normalized_difference(b03, b11)


def ndbi(b11: Any, b08: Any) -> np.ndarray:
    """Normalized Difference Built-up Index: (B11-B08)/(B11+B08)."""
    return safe_normalized_difference(b11, b08)


def ndre(b8a: Any, b05: Any) -> np.ndarray:
    """Red-edge normalized difference: (B8A-B05)/(B8A+B05)."""
    return safe_normalized_difference(b8a, b05)


def scl_valid_mask(scl: Any) -> np.ndarray:
    """Boolean mask for SCL classes retained for ordinary land-surface analysis.

    Retains classes 2, 4, 5 and 6 (dark-area pixels, vegetation, bare soil,
    water). Excludes no-data, saturated/defective, cloud shadow, unclassified,
    cloud, cirrus and snow/ice classes. Class 2 is retained but should be
    interpreted cautiously in shadow-prone locations.
    """
    values = np.asarray(scl)
    return np.isfinite(values) & ~np.isin(values, tuple(SCL_INVALID_CLASSES))


def scl_quality_summary(scl: Any) -> dict[str, Any]:
    """Summarize native-grid SCL composition without resampling."""
    values = np.asarray(scl, dtype=np.float64)
    if values.ndim == 0:
        values = values.reshape(1)
    finite = np.isfinite(values)
    total = int(values.size)
    finite_count = int(finite.sum())
    counts = {
        str(class_id): int(np.count_nonzero(finite & (values == class_id)))
        for class_id in range(12)
    }
    fractions = {
        class_id: (count / total if total else float("nan"))
        for class_id, count in counts.items()
    }
    retained = scl_valid_mask(values) & finite
    cloud_shadow = finite & np.isin(values, (3, 8, 9, 10))
    return {
        "pixel_count": total,
        "finite_pixel_count": finite_count,
        "finite_fraction": finite_count / total if total else float("nan"),
        "analysis_valid_pixel_count": int(retained.sum()),
        "analysis_valid_fraction": float(retained.sum() / total) if total else float("nan"),
        "cloud_shadow_pixel_count": int(cloud_shadow.sum()),
        "cloud_shadow_fraction": float(cloud_shadow.sum() / total) if total else float("nan"),
        "class_counts": counts,
        "class_fractions": fractions,
        "mask_resolution": "native SCL 20m",
    }


def apply_valid_mask(values: Any, valid_mask: Any) -> np.ndarray:
    """Apply a boolean validity mask, returning a float array with NaN elsewhere."""
    data = _as_float_array(values)
    mask = np.asarray(valid_mask, dtype=bool)
    data, mask = np.broadcast_arrays(data, mask)
    result = data.copy()
    result[~mask] = np.nan
    return result


def summarize_window(values: Any, valid_mask: Any | None = None) -> dict[str, float | int]:
    """Summarize a point-centred window without silently treating nodata as zero."""
    data = _as_float_array(values)
    valid = np.isfinite(data)
    if valid_mask is not None:
        valid &= np.broadcast_to(np.asarray(valid_mask, dtype=bool), data.shape)
    selected = data[valid]
    total = int(data.size)
    count = int(selected.size)
    result: dict[str, float | int] = {
        "pixel_count": total,
        "valid_pixel_count": count,
        "valid_fraction": float(count / total) if total else float("nan"),
    }
    if count:
        result.update({
            "minimum": float(np.min(selected)),
            "median": float(np.median(selected)),
            "mean": float(np.mean(selected)),
            "maximum": float(np.max(selected)),
            "standard_deviation": float(np.std(selected)),
        })
    else:
        result.update({key: float("nan") for key in (
            "minimum", "median", "mean", "maximum", "standard_deviation"
        )})
    return result


def index_stack(
    bands: dict[str, Any],
    *,
    valid_mask: Any | None = None,
) -> dict[str, np.ndarray]:
    """Calculate available indices from co-registered band arrays.

    Required inputs are explicit. B08/B04/B03 are needed for NDVI and NDWI;
    B03/B11 for MNDWI; B11/B08 for NDBI; B8A/B05 for NDRE. The caller is
    responsible for resampling to a declared common grid before calling.
    """
    required = {
        "NDVI": ("B08", "B04", ndvi),
        "NDWI": ("B03", "B08", ndwi_mcfeeters),
        "MNDWI": ("B03", "B11", mndwi),
        "NDBI": ("B11", "B08", ndbi),
        "NDRE": ("B8A", "B05", ndre),
    }
    output: dict[str, np.ndarray] = {}
    for name, (first, second, function) in required.items():
        if first in bands and second in bands:
            layer = function(bands[first], bands[second])
            if valid_mask is not None:
                layer = apply_valid_mask(layer, valid_mask)
            output[name] = layer
    return output


__all__ = [
    "SCL_INVALID_CLASSES", "safe_normalized_difference", "ndvi",
    "ndwi_mcfeeters", "mndwi", "ndbi", "ndre", "scl_valid_mask",
    "apply_valid_mask", "scl_quality_summary", "summarize_window", "index_stack",
]

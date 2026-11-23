"""Local raster map algebra and categorical lookup operations."""
from __future__ import annotations
from collections.abc import Mapping, Sequence
from typing import Any
import numpy as np

_REDUCERS = {"sum", "mean", "min", "max", "product"}
_BINARY = {"add", "subtract", "multiply", "divide", "greater", "less", "equal"}

def local_map_algebra(rasters: Sequence[Sequence[Sequence[float]] | np.ndarray],
                      operation: str, *, nodata_policy: str = "propagate") -> np.ndarray:
    """Apply cellwise arithmetic/reduction to equally shaped 2D rasters."""
    if operation not in _REDUCERS | _BINARY:
        raise ValueError(f"unsupported operation: {operation}")
    if nodata_policy not in ("propagate", "ignore"):
        raise ValueError("nodata_policy must be 'propagate' or 'ignore'")
    if len(rasters) < 2:
        raise ValueError("at least two rasters are required")
    if operation in _BINARY and len(rasters) != 2:
        raise ValueError(f"{operation} requires exactly two rasters")
    arrays = [np.asarray(r, dtype=float) for r in rasters]
    if any(a.ndim != 2 or a.size == 0 for a in arrays):
        raise ValueError("every raster must be a non-empty 2D array")
    if any(a.shape != arrays[0].shape for a in arrays[1:]):
        raise ValueError("all rasters must have identical shapes")
    stack = np.stack(arrays)
    valid = np.isfinite(stack)
    count = valid.sum(axis=0)
    if operation in _REDUCERS:
        eligible = (count == len(arrays)) if nodata_policy == "propagate" else (count > 0)
        safe = np.where(valid, stack, 0.0)
        if operation == "sum":
            values = safe.sum(axis=0)
        elif operation == "mean":
            values = safe.sum(axis=0) / np.maximum(count, 1)
        elif operation == "min":
            values = np.min(np.where(valid, stack, np.inf), axis=0)
        elif operation == "max":
            values = np.max(np.where(valid, stack, -np.inf), axis=0)
        else:
            values = np.prod(np.where(valid, stack, 1.0), axis=0)
        return np.where(eligible, values, np.nan)
    eligible = valid.all(axis=0)
    left, right = stack[0], stack[1]
    with np.errstate(divide="ignore", invalid="ignore"):
        if operation == "add": values = left + right
        elif operation == "subtract": values = left - right
        elif operation == "multiply": values = left * right
        elif operation == "divide":
            values = left / right
            eligible &= right != 0
        elif operation == "greater": values = left > right
        elif operation == "less": values = left < right
        else: values = left == right
    return np.where(eligible, values, np.nan)

def categorical_lookup(raster: Sequence[Sequence[float]] | np.ndarray,
                       lookup: Mapping[Any, float], *, unknown: str = "nodata") -> np.ndarray:
    """Recode numeric classes; unknown values become NoData, stay unchanged or error."""
    data = np.asarray(raster, dtype=float)
    if data.ndim != 2 or data.size == 0:
        raise ValueError("raster must be a non-empty 2D array")
    if unknown not in ("nodata", "keep", "error"):
        raise ValueError("unknown must be 'nodata', 'keep' or 'error'")
    normalized = {}
    for key, value in lookup.items():
        try: k, v = float(key), float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError("lookup keys and values must be numeric") from exc
        if not np.isfinite(k) or not np.isfinite(v):
            raise ValueError("lookup keys and values must be finite")
        normalized[k] = v
    result = np.full(data.shape, np.nan, dtype=float)
    valid = np.isfinite(data)
    known = np.zeros(data.shape, dtype=bool)
    for key, value in normalized.items():
        match = valid & (data == key)
        result[match] = value
        known |= match
    unrecognized = valid & ~known
    if unknown == "error" and np.any(unrecognized):
        raise ValueError(f"unknown categories encountered: {np.unique(data[unrecognized]).tolist()}")
    if unknown == "keep":
        result[unrecognized] = data[unrecognized]
    return result

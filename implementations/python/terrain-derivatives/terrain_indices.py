"""Topographic wetness index from specific catchment area and slope."""
from __future__ import annotations
import numpy as np

def topographic_wetness_index(specific_catchment_area, slope_degrees, *, slope_floor_degrees: float=0.1) -> np.ndarray:
    """Return ln(a / tan(beta)); a must be positive and expressed in metres.

    Non-finite inputs and non-positive catchment area return NaN. A declared
    positive slope floor avoids an infinite index on perfectly flat cells.
    """
    area=np.asarray(specific_catchment_area,dtype=float)
    slope=np.asarray(slope_degrees,dtype=float)
    if area.shape!=slope.shape:
        raise ValueError("area and slope arrays must have the same shape")
    try:
        slope_floor_degrees = float(slope_floor_degrees)
    except (TypeError, ValueError):
        raise ValueError("slope_floor_degrees must be finite and between 0 and 90") from None
    if not np.isfinite(slope_floor_degrees) or not 0 < slope_floor_degrees < 90:
        raise ValueError("slope_floor_degrees must be finite and between 0 and 90")
    finite_slope=slope[np.isfinite(slope)]
    if ((finite_slope<0)|(finite_slope>=90)).any():
        raise ValueError("finite slope values must be in [0, 90)")
    valid=np.isfinite(area)&(area>0)&np.isfinite(slope)
    result=np.full(area.shape,np.nan,dtype=float)
    beta=np.radians(np.maximum(slope[valid],slope_floor_degrees))
    result[valid]=np.log(area[valid]/np.tan(beta))
    return result


def topographic_position_index(elevation, *, window_size: int = 3,
                               min_valid_fraction: float = 1.0) -> np.ndarray:
    """Return focal TPI = cell elevation - neighbourhood mean elevation.

    Uses a square odd-sized window including the centre. Only complete
    windows are evaluated, so the outer half-window border is NaN.
    Non-finite cells are excluded from the focal mean; a result is emitted
    only when the valid-cell fraction reaches the requested threshold and
    the centre cell itself is finite. Integral images make this O(n) in the
    number of raster cells, independent of window area.
    """
    dem = np.asarray(elevation, dtype=float)
    if dem.ndim != 2 or dem.size == 0:
        raise ValueError("elevation must be a non-empty 2D array")
    if isinstance(window_size, (bool, np.bool_)) or not isinstance(
        window_size, (int, np.integer)
    ) or window_size < 3 or window_size % 2 == 0:
        raise ValueError("window_size must be an odd integer of at least 3")
    try:
        fraction = float(min_valid_fraction)
    except (TypeError, ValueError):
        raise ValueError("min_valid_fraction must be in (0, 1]") from None
    if not np.isfinite(fraction) or not 0 < fraction <= 1:
        raise ValueError("min_valid_fraction must be in (0, 1]")

    radius = window_size // 2
    valid = np.isfinite(dem)
    values = np.where(valid, dem, 0.0)

    def window_sums(array):
        integral = np.pad(array.cumsum(axis=0).cumsum(axis=1),
                          ((1, 0), (1, 0)), mode="constant")
        return (integral[window_size:, window_size:]
                - integral[:-window_size, window_size:]
                - integral[window_size:, :-window_size]
                + integral[:-window_size, :-window_size])

    sums = window_sums(values)
    counts = window_sums(valid.astype(np.int64))
    total = window_size * window_size
    means = np.full(sums.shape, np.nan, dtype=float)
    enough = counts >= int(np.ceil(fraction * total))
    np.divide(sums, counts, out=means, where=enough & (counts > 0))

    result = np.full(dem.shape, np.nan, dtype=float)
    interior = dem[radius:-radius, radius:-radius]
    usable = np.isfinite(interior) & np.isfinite(means)
    target = result[radius:-radius, radius:-radius]
    target[usable] = interior[usable] - means[usable]
    return result


def riley_terrain_ruggedness_index(elevation, *, z_factor: float = 1.0) -> np.ndarray:
    """Return Riley et al.'s 8-neighbour terrain ruggedness index.

    TRI is the square root of the sum of squared elevation differences
    between the centre cell and its eight immediate neighbours. It is
    expressed in the elevation unit after applying z_factor. A complete
    3x3 finite neighbourhood is required.
    """
    dem = np.asarray(elevation, dtype=float)
    if dem.ndim != 2 or dem.size == 0:
        raise ValueError("elevation must be a non-empty 2D array")
    try:
        scale = float(z_factor)
    except (TypeError, ValueError):
        raise ValueError("z_factor must be finite and positive") from None
    if not np.isfinite(scale) or scale <= 0:
        raise ValueError("z_factor must be finite and positive")
    result = np.full(dem.shape, np.nan, dtype=float)
    if dem.shape[0] < 3 or dem.shape[1] < 3:
        return result
    centre = dem[1:-1, 1:-1]
    squared = np.zeros(centre.shape, dtype=float)
    valid = np.isfinite(centre)
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            neighbour = dem[1 + dr:dem.shape[0] - 1 + dr,
                            1 + dc:dem.shape[1] - 1 + dc]
            valid &= np.isfinite(neighbour)
            delta = (neighbour - centre) * scale
            squared += np.where(np.isfinite(delta), delta * delta, 0.0)
    target = result[1:-1, 1:-1]
    target[valid] = np.sqrt(squared[valid])
    return result



def hypsometric_curve(elevation, *, valid_mask=None):
    """Return an empirical hypsometric curve and hypsometric integral.

    The raster is treated as a regular grid with equal-area cells. Finite
    elevations selected by valid_mask are normalized between the observed
    minimum and maximum. Unique relative elevations are returned in
    descending order with the fraction of valid cells at or above each
    threshold. The integral is the mean normalized elevation. A zero-relief
    surface has no defined normalization.
    """
    dem = np.asarray(elevation, dtype=float)
    if dem.ndim != 2 or dem.size == 0:
        raise ValueError("elevation must be a non-empty 2D array")
    if valid_mask is None:
        selected = np.isfinite(dem)
    else:
        mask = np.asarray(valid_mask, dtype=bool)
        if mask.shape != dem.shape:
            raise ValueError("valid_mask must match elevation shape")
        selected = np.isfinite(dem) & mask
    values = dem[selected]
    if values.size < 2:
        raise ValueError("at least two valid elevation cells are required")
    low = float(values.min())
    high = float(values.max())
    relief = high - low
    if not np.isfinite(relief) or relief <= 0:
        raise ValueError("hypsometric curve requires positive terrain relief")
    levels, counts = np.unique(values, return_counts=True)
    relative = (levels - low) / relief
    cumulative = np.cumsum(counts[::-1])[::-1] / values.size
    return {
        "relative_elevation": relative[::-1].astype(float),
        "area_fraction_above": cumulative.astype(float),
        "hypsometric_integral": float(np.mean((values - low) / relief)),
        "valid_cell_count": int(values.size),
        "minimum_elevation": low,
        "maximum_elevation": high,
    }

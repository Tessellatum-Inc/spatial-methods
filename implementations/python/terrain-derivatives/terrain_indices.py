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
        "area_fraction_above": cumulative[::-1].astype(float),
        "hypsometric_integral": float(np.mean((values - low) / relief)),
        "valid_cell_count": int(values.size),
        "minimum_elevation": low,
        "maximum_elevation": high,
    }



def cut_fill_volume(existing_surface, design_surface, *, cell_size_x=1.0,
                   cell_size_y=1.0, valid_mask=None):
    """Calculate cellwise cut/fill depths and volumes between two surfaces.

    Positive cut depth means the existing surface is above the design
    surface; positive fill depth means it is below. Volumes use the
    horizontal cell area cell_size_x * cell_size_y. Both surfaces must use
    the same vertical unit, compatible with horizontal units for volume.
    Non-finite cells and cells excluded by valid_mask are omitted.
    """
    existing = np.asarray(existing_surface, dtype=float)
    design = np.asarray(design_surface, dtype=float)
    if existing.ndim != 2 or existing.size == 0:
        raise ValueError("existing_surface must be a non-empty 2D array")
    if design.shape != existing.shape:
        raise ValueError("design_surface must match existing_surface shape")
    try:
        dx, dy = float(cell_size_x), float(cell_size_y)
    except (TypeError, ValueError):
        raise ValueError("cell sizes must be finite and positive") from None
    if not np.isfinite(dx) or not np.isfinite(dy) or dx <= 0 or dy <= 0:
        raise ValueError("cell sizes must be finite and positive")
    if valid_mask is None:
        valid = np.isfinite(existing) & np.isfinite(design)
    else:
        mask = np.asarray(valid_mask, dtype=bool)
        if mask.shape != existing.shape:
            raise ValueError("valid_mask must match surface shape")
        valid = np.isfinite(existing) & np.isfinite(design) & mask

    cut = np.full(existing.shape, np.nan, dtype=float)
    fill = np.full(existing.shape, np.nan, dtype=float)
    cut[valid] = np.maximum(existing[valid] - design[valid], 0.0)
    fill[valid] = np.maximum(design[valid] - existing[valid], 0.0)
    area = dx * dy
    cut_volume = float(np.sum(cut[valid]) * area)
    fill_volume = float(np.sum(fill[valid]) * area)
    return {
        "cut_depth": cut,
        "fill_depth": fill,
        "cut_volume": cut_volume,
        "fill_volume": fill_volume,
        "net_cut_volume": cut_volume - fill_volume,
        "valid_cell_count": int(valid.sum()),
        "cell_area": area,
    }


def sky_view_factor(
    elevation,
    *,
    cell_size_x: float = 1.0,
    cell_size_y: float = 1.0,
    max_distance: float,
    azimuth_count: int = 16,
    sample_spacing: float | None = None,
) -> np.ndarray:
    """Estimate sky-view factor by radial horizon sampling.

    For each cell, sample bilinearly along evenly spaced azimuths and retain
    the maximum positive horizon angle on each ray. The approximation is
    mean(cos(horizon_angle)**2) over azimuth. A result is emitted only where
    every ray is supported to max_distance; incomplete boundary or NoData
    rays return NaN. This is a transparent local horizon approximation, not
    a full hemispherical solid-angle integration or cast-shadow model.
    """
    dem = np.asarray(elevation, dtype=float)
    if dem.ndim != 2 or dem.size == 0:
        raise ValueError("elevation must be a non-empty 2D array")
    try:
        dx, dy, distance = float(cell_size_x), float(cell_size_y), float(max_distance)
    except (TypeError, ValueError):
        raise ValueError("cell sizes and max_distance must be finite and positive") from None
    if not np.all(np.isfinite([dx, dy, distance])) or min(dx, dy, distance) <= 0:
        raise ValueError("cell sizes and max_distance must be finite and positive")
    if isinstance(azimuth_count, (bool, np.bool_)) or not isinstance(azimuth_count, (int, np.integer)) or azimuth_count < 4:
        raise ValueError("azimuth_count must be an integer of at least four")
    if sample_spacing is None:
        step = min(dx, dy) / 2.0
    else:
        try:
            step = float(sample_spacing)
        except (TypeError, ValueError):
            raise ValueError("sample_spacing must be finite and positive") from None
        if not np.isfinite(step) or step <= 0:
            raise ValueError("sample_spacing must be finite and positive")
    distances = np.arange(step, distance + step * 0.5, step)
    distances = distances[distances <= distance]
    if distances.size == 0 or distances[-1] < distance:
        distances = np.append(distances, distance)

    rows, cols = dem.shape
    result = np.full(dem.shape, np.nan, dtype=float)
    azimuths = np.arange(azimuth_count, dtype=float) * (2.0 * np.pi / azimuth_count)
    for row, col in np.ndindex(dem.shape):
        origin = dem[row, col]
        if not np.isfinite(origin):
            continue
        horizon_terms = []
        supported = True
        for azimuth in azimuths:
            dx_direction = np.sin(azimuth)
            north_direction = np.cos(azimuth)
            ray_angles = []
            for radial_distance in distances:
                sample_col = col + dx_direction * radial_distance / dx
                sample_row = row - north_direction * radial_distance / dy
                if sample_col < 0 or sample_col > cols - 1 or sample_row < 0 or sample_row > rows - 1:
                    supported = False
                    break
                c0 = min(int(np.floor(sample_col)), cols - 2)
                r0 = min(int(np.floor(sample_row)), rows - 2)
                fc, fr = sample_col - c0, sample_row - r0
                neighbours = np.array([
                    dem[r0, c0], dem[r0, c0 + 1],
                    dem[r0 + 1, c0], dem[r0 + 1, c0 + 1],
                ])
                if not np.all(np.isfinite(neighbours)):
                    supported = False
                    break
                top = neighbours[0] * (1.0 - fc) + neighbours[1] * fc
                bottom = neighbours[2] * (1.0 - fc) + neighbours[3] * fc
                sample_z = top * (1.0 - fr) + bottom * fr
                ray_angles.append(np.arctan2(sample_z - origin, radial_distance))
            if not supported:
                break
            horizon = max(0.0, float(np.max(ray_angles)))
            horizon_terms.append(np.cos(horizon) ** 2)
        if supported and len(horizon_terms) == azimuth_count:
            result[row, col] = float(np.mean(horizon_terms))
    return result


def _gaussian_smooth_masked(dem: np.ndarray, sigma_rows: float, sigma_cols: float) -> np.ndarray:
    """Separable Gaussian smoothing with normalized finite-cell weights."""
    values = np.where(np.isfinite(dem), dem, 0.0).astype(float)
    weights = np.isfinite(dem).astype(float)
    for axis, sigma in ((0, sigma_rows), (1, sigma_cols)):
        if sigma <= 1e-12:
            continue
        radius = max(1, int(np.ceil(3.0 * sigma)))
        offsets = np.arange(-radius, radius + 1, dtype=float)
        kernel = np.exp(-0.5 * (offsets / sigma) ** 2)
        kernel /= kernel.sum()
        def convolve(array):
            moved = np.moveaxis(array, axis, -1)
            padded = np.pad(moved, [(0, 0)] * (moved.ndim - 1) + [(radius, radius)], mode="reflect")
            out = np.zeros_like(moved, dtype=float)
            for j, weight in enumerate(kernel):
                out += weight * padded[..., j:j + moved.shape[-1]]
            return np.moveaxis(out, -1, axis)
        values = convolve(values)
        weights = convolve(weights)
    result = np.full(dem.shape, np.nan, dtype=float)
    np.divide(values, weights, out=result, where=weights > np.finfo(float).eps)
    return result


def local_relief_model(elevation, *, scale: float, cell_size_x: float = 1.0, cell_size_y: float = 1.0) -> np.ndarray:
    """Return DEM minus a Gaussian-smoothed background at a declared map scale.

    Finite-cell normalized convolution prevents NoData holes acting as zero
    elevations. Source NoData remains NoData in the residual. Positive values
    are locally elevated relative to the smoothed background; negative values
    are locally depressed. This is scale-dependent, not a landform classifier.
    """
    dem = np.asarray(elevation, dtype=float)
    if dem.ndim != 2 or dem.size == 0:
        raise ValueError("elevation must be a non-empty 2D array")
    try:
        scale, dx, dy = float(scale), float(cell_size_x), float(cell_size_y)
    except (TypeError, ValueError):
        raise ValueError("scale and cell sizes must be finite and positive") from None
    if not np.isfinite([scale, dx, dy]).all() or min(scale, dx, dy) <= 0:
        raise ValueError("scale and cell sizes must be finite and positive")
    smooth = _gaussian_smooth_masked(dem, scale / dy, scale / dx)
    result = dem - smooth
    result[~np.isfinite(dem)] = np.nan
    return result


def multiscale_topographic_position_index(elevation, window_sizes, *, min_valid_fraction: float = 1.0) -> dict[int, np.ndarray]:
    """Evaluate focal TPI at several distinct odd window sizes."""
    try:
        sizes = list(window_sizes)
    except TypeError:
        raise ValueError("window_sizes must be a non-empty sequence") from None
    if not sizes:
        raise ValueError("window_sizes must be a non-empty sequence")
    normalized = []
    for size in sizes:
        if isinstance(size, (bool, np.bool_)) or not isinstance(size, (int, np.integer)) or size < 3 or size % 2 == 0:
            raise ValueError("every window size must be an odd integer of at least 3")
        normalized.append(int(size))
    if len(set(normalized)) != len(normalized):
        raise ValueError("window_sizes must be unique")
    return {size: topographic_position_index(elevation, window_size=size, min_valid_fraction=min_valid_fraction) for size in normalized}

def detect_local_extrema(elevation, *, window_size=3, min_prominence=0.0):
    """Return Boolean local-maximum and local-minimum masks.

    A complete odd square window is required. A candidate must be at least
    as high/low as every neighbour and differ from at least one neighbour;
    this avoids marking a perfectly flat window as both a peak and a pit.
    min_prominence is the difference from the most extreme neighbour.
    Plateau edges may be marked; this is not connected-plateau extraction.
    """
    dem = np.asarray(elevation, dtype=float)
    if dem.ndim != 2 or dem.size == 0: raise ValueError("elevation must be a non-empty 2D array")
    if isinstance(window_size, (bool, np.bool_)) or not isinstance(window_size, (int, np.integer)) or window_size < 3 or window_size % 2 == 0:
        raise ValueError("window_size must be an odd integer of at least 3")
    try: prominence = float(min_prominence)
    except (TypeError, ValueError): raise ValueError("min_prominence must be finite and non-negative") from None
    if not np.isfinite(prominence) or prominence < 0: raise ValueError("min_prominence must be finite and non-negative")
    radius = window_size // 2
    maxima = np.zeros(dem.shape, dtype=bool); minima = np.zeros(dem.shape, dtype=bool)
    if dem.shape[0] < window_size or dem.shape[1] < window_size: return maxima, minima
    from numpy.lib.stride_tricks import sliding_window_view
    windows = sliding_window_view(dem, (window_size, window_size))
    centre = windows[:, :, radius, radius]
    valid = np.isfinite(windows).all(axis=(-1, -2))
    neighbours = windows.copy(); neighbours[:, :, radius, radius] = np.nan
    local_max = np.nanmax(neighbours, axis=(-1, -2))
    local_min = np.nanmin(neighbours, axis=(-1, -2))
    is_max = valid & (centre >= local_max) & ((centre - local_max) >= prominence) & (centre > local_min)
    is_min = valid & (centre <= local_min) & ((local_min - centre) >= prominence) & (centre < local_max)
    maxima[radius:-radius, radius:-radius] = is_max
    minima[radius:-radius, radius:-radius] = is_min
    return maxima, minima


def reservoir_stage_storage(elevation, stage_levels, *, cell_area=1.0, valid_mask=None):
    """Compute DEM-based inundated area and storage at ordered water stages.
    Cells are horizontal prisms: storage = sum(max(stage - elevation, 0))*area.
    This is a hypsometric calculation, not a hydraulic reservoir model.
    """
    dem = np.asarray(elevation, dtype=float); stages = np.asarray(stage_levels, dtype=float)
    if dem.ndim != 2 or dem.size == 0: raise ValueError("elevation must be a non-empty 2D array")
    if stages.ndim != 1 or stages.size == 0 or np.any(~np.isfinite(stages)): raise ValueError("stage_levels must be a non-empty finite 1D array")
    if np.any(np.diff(stages) <= 0): raise ValueError("stage_levels must be strictly increasing")
    try: area = float(cell_area)
    except (TypeError, ValueError): raise ValueError("cell_area must be finite and positive") from None
    if not np.isfinite(area) or area <= 0: raise ValueError("cell_area must be finite and positive")
    if valid_mask is None: valid = np.isfinite(dem)
    else:
        mask = np.asarray(valid_mask, dtype=bool)
        if mask.shape != dem.shape: raise ValueError("valid_mask must match elevation shape")
        valid = np.isfinite(dem) & mask
    if not np.any(valid): raise ValueError("at least one valid elevation cell is required")
    cells = dem[valid]; depths = np.maximum(stages[:, None] - cells[None, :], 0.0)
    return {
        "stage": stages.copy(),
        "inundated_area": np.count_nonzero(depths > 0, axis=1).astype(float) * area,
        "storage": depths.sum(axis=1) * area,
        "valid_cell_count": int(cells.size),
    }

"""Local-maximum seeded watershed segmentation of canopy height models."""
from __future__ import annotations
import numpy as np
from scipy import ndimage
from skimage.segmentation import watershed


def segment_crowns(chm, *, canopy_threshold=1.0, min_peak_height=2.0,
                   window_size=5, compactness=0.0):
    """Return crown labels and deterministic local-maximum seed coordinates.

    CHM values are heights above ground in one consistent vertical unit.
    Cells below canopy_threshold or non-finite cells are excluded. Connected
    plateaus of local maxima contribute one seed at their first highest cell.
    Watershed operates on negative CHM, so basins grow outward from treetops.
    """
    h = np.asarray(chm, dtype=float)
    if h.ndim != 2 or h.size == 0 or not np.any(np.isfinite(h)):
        raise ValueError("chm must be a nonempty 2-D array with finite cells")
    if not np.isfinite(canopy_threshold) or not np.isfinite(min_peak_height):
        raise ValueError("height thresholds must be finite")
    if min_peak_height < canopy_threshold:
        raise ValueError("min_peak_height must be >= canopy_threshold")
    if not isinstance(window_size, int) or isinstance(window_size, bool) or window_size < 3 or window_size % 2 == 0:
        raise ValueError("window_size must be an odd integer >= 3")
    if not np.isfinite(compactness) or compactness < 0:
        raise ValueError("compactness must be finite and nonnegative")
    mask = np.isfinite(h) & (h >= canopy_threshold)
    safe = np.where(np.isfinite(h), h, -np.inf)
    local = safe == ndimage.maximum_filter(safe, size=window_size, mode="nearest")
    peak_mask = local & mask & (safe >= min_peak_height)
    components, count = ndimage.label(peak_mask, structure=np.ones((3, 3), dtype=int))
    seeds = []
    markers = np.zeros(h.shape, dtype=np.int32)
    for component in range(1, count + 1):
        coords = np.argwhere(components == component)
        values = safe[components == component]
        best = coords[int(np.argmax(values))]
        seeds.append((int(best[0]), int(best[1])))
    seeds.sort()
    for marker_id, (row, col) in enumerate(seeds, start=1):
        markers[row, col] = marker_id
    if not seeds:
        return {"labels": np.zeros(h.shape, dtype=np.int32),
                "seeds": np.empty((0, 2), dtype=int)}
    labels = watershed(-safe, markers=markers, mask=mask, compactness=compactness)
    return {"labels": labels.astype(np.int32),
            "seeds": np.asarray(seeds, dtype=int)}

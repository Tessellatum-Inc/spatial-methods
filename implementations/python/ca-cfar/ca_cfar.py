"""Two-dimensional cell-averaging CFAR for intensity imagery."""
import numpy as np


def _box_sum(a, radius):
    h, w = a.shape
    ii = np.pad(a, ((1, 0), (1, 0))).cumsum(0).cumsum(1)
    r, c = np.arange(h), np.arange(w)
    r0, r1 = np.maximum(r-radius, 0), np.minimum(r+radius+1, h)
    c0, c1 = np.maximum(c-radius, 0), np.minimum(c+radius+1, w)
    return (ii[r1[:, None], c1[None, :]] - ii[r0[:, None], c1[None, :]]
            - ii[r1[:, None], c0[None, :]] + ii[r0[:, None], c0[None, :]])


def ca_cfar(intensity, guard_cells=1, training_cells=4, false_alarm_rate=1e-3):
    """Return (detections, threshold, noise_estimate).

    Square outer window radius is guard_cells + training_cells. The square
    guard region, including the cell under test, is excluded from training.
    The threshold multiplier is the exact CA-CFAR factor for independent
    exponentially distributed intensity samples. Border cells and cells
    whose training ring contains NoData are returned as False/NaN/NaN.
    """
    image = np.asarray(intensity, dtype=float)
    if image.ndim != 2 or not image.size:
        raise ValueError("intensity must be a non-empty 2D array")
    if np.isinf(image).any() or np.any(image[np.isfinite(image)] < 0):
        raise ValueError("intensity must be non-negative and finite or NaN NoData")
    for name, value in (("guard_cells", guard_cells), ("training_cells", training_cells)):
        if isinstance(value, bool) or not isinstance(value, (int, np.integer)) or value < (0 if name == "guard_cells" else 1):
            raise ValueError(f"{name} has an invalid value")
    if not np.isfinite(false_alarm_rate) or not 0 < false_alarm_rate < 1:
        raise ValueError("false_alarm_rate must be between 0 and 1")
    g, t = int(guard_cells), int(training_cells)
    outer, inner = g+t, g
    total_n = (2*outer+1)**2 - (2*inner+1)**2
    alpha = total_n * (false_alarm_rate ** (-1.0/total_n) - 1.0)
    valid = np.isfinite(image)
    values = np.where(valid, image, 0.0)
    sums = _box_sum(values, outer) - _box_sum(values, inner)
    counts = _box_sum(valid.astype(float), outer) - _box_sum(valid.astype(float), inner)
    expected = float(total_n)
    noise = np.divide(sums, counts, out=np.full_like(sums, np.nan), where=counts == expected)
    threshold = alpha * noise
    detections = np.zeros(image.shape, dtype=bool)
    margin = outer
    if image.shape[0] > 2*margin and image.shape[1] > 2*margin:
        interior = np.s_[margin:-margin, margin:-margin] if margin else np.s_[:, :]
        detections[interior] = valid[interior] & (image[interior] > threshold[interior])
    threshold[~valid] = np.nan
    noise[~valid] = np.nan
    if margin:
        threshold[:margin, :] = np.nan
        threshold[-margin:, :] = np.nan
        threshold[:, :margin] = np.nan
        threshold[:, -margin:] = np.nan
        noise[:margin, :] = np.nan
        noise[-margin:, :] = np.nan
        noise[:, :margin] = np.nan
        noise[:, -margin:] = np.nan
    return detections, threshold, noise

"""Object-level feature extraction for segmented raster imagery."""
import numpy as np


def summarize_objects(image, labels):
    """Summarize labeled image objects and their 4-neighbour adjacency.

    image may be (rows, cols) or (rows, cols, bands). Labels are integer IDs;
    negative labels are ignored as background. Each object's geometric area,
    centroid, half-open bounding box, 4-edge perimeter, compactness and
    per-band finite-value mean/std are returned. Adjacency counts shared
    horizontal/vertical pixel edges between distinct non-negative labels.
    """
    data = np.asarray(image, dtype=float)
    lab = np.asarray(labels)
    if data.ndim == 2:
        data = data[..., None]
    if data.ndim != 3 or data.shape[0] == 0 or data.shape[1] == 0 or data.shape[2] == 0:
        raise ValueError("image must be a non-empty 2D or 3D raster")
    if lab.shape != data.shape[:2] or not np.issubdtype(lab.dtype, np.integer):
        raise ValueError("labels must be an integer raster matching image rows and columns")
    if np.isinf(data).any():
        raise ValueError("image may contain NaN NoData but not infinity")
    ids = np.unique(lab[lab >= 0])
    objects = []
    for raw_id in ids:
        oid = int(raw_id)
        mask = lab == raw_id
        rows, cols = np.nonzero(mask)
        area = int(len(rows))
        perimeter = int(mask[0, :].sum() + mask[-1, :].sum()
                        + mask[:, 0].sum() + mask[:, -1].sum())
        perimeter += int(np.count_nonzero(mask[1:, :] != mask[:-1, :]))
        perimeter += int(np.count_nonzero(mask[:, 1:] != mask[:, :-1]))
        # The transition count above counts each boundary once, but also
        # includes boundaries between two labels and background. For this
        # object's perimeter, count each of its four exposed edges directly.
        padded = np.pad(mask, 1, constant_values=False)
        perimeter = int(np.count_nonzero(mask & ~padded[:-2, 1:-1])
                        + np.count_nonzero(mask & ~padded[2:, 1:-1])
                        + np.count_nonzero(mask & ~padded[1:-1, :-2])
                        + np.count_nonzero(mask & ~padded[1:-1, 2:]))
        means, stds = [], []
        for band in range(data.shape[2]):
            values = data[..., band][mask]
            values = values[np.isfinite(values)]
            means.append(float(values.mean()) if values.size else float("nan"))
            stds.append(float(values.std()) if values.size else float("nan"))
        objects.append({
            "label": oid, "area": area,
            "centroid": (float(rows.mean()), float(cols.mean())),
            "bbox": (int(rows.min()), int(cols.min()), int(rows.max()+1), int(cols.max()+1)),
            "perimeter_4": perimeter,
            "compactness": float(4*np.pi*area/(perimeter*perimeter)) if perimeter else 0.0,
            "band_mean": tuple(means), "band_std": tuple(stds),
        })
    adjacency = {}
    for a, b in ((lab[:, :-1], lab[:, 1:]), (lab[:-1, :], lab[1:, :])):
        valid = (a >= 0) & (b >= 0) & (a != b)
        for left, right in zip(a[valid].tolist(), b[valid].tolist()):
            key = tuple(sorted((int(left), int(right))))
            adjacency[key] = adjacency.get(key, 0) + 1
    edges = [{"labels": key, "shared_edges": count}
             for key, count in sorted(adjacency.items())]
    return {"objects": objects, "adjacency": edges}

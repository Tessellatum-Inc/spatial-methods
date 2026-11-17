"""Small-grid multi-label random-walker segmentation for 2D images."""
from __future__ import annotations

import math
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve


def random_walker(image, seeds, *, beta=90.0):
    """Segment a 2D image from positive integer seed labels.

    Zero in ``seeds`` denotes an unlabelled pixel. Four-neighbour edge
    conductance is exp(-beta * squared_feature_difference). The discrete
    weighted Laplacian is solved with Dirichlet conditions at seed pixels.
    Returns the assigned labels, per-class probabilities and sorted classes.
    """
    try:
        data = np.asarray(image, dtype=float)
        marker = np.asarray(seeds)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("image and seeds must be numeric arrays") from exc
    if data.ndim not in (2, 3) or min(data.shape[:2]) < 1:
        raise ValueError("image must be a non-empty 2D scalar or multichannel image")
    if not np.isfinite(data).all():
        raise ValueError("image must contain only finite values")
    if marker.shape != data.shape[:2] or marker.ndim != 2:
        raise ValueError("seeds must be a 2D array matching the image rows and columns")
    if not np.issubdtype(marker.dtype, np.integer) or np.any(marker < 0):
        raise ValueError("seeds must contain non-negative integer labels")
    if isinstance(beta, (bool, np.bool_)):
        raise ValueError("beta must be finite and non-negative")
    try:
        strength = float(beta)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("beta must be finite and non-negative") from exc
    if not math.isfinite(strength) or strength < 0:
        raise ValueError("beta must be finite and non-negative")

    classes = np.unique(marker[marker > 0])
    if len(classes) < 2:
        raise ValueError("at least two distinct positive seed labels are required")
    height, width = marker.shape
    n = height * width
    features = data.reshape(n, -1)
    marker_flat = marker.ravel()
    edge_u, edge_v, edge_w = [], [], []
    for row in range(height):
        for col in range(width):
            u = row * width + col
            for nr, nc in ((row, col + 1), (row + 1, col)):
                if nr >= height or nc >= width:
                    continue
                v = nr * width + nc
                difference = features[u] - features[v]
                squared = float(difference @ difference)
                weight = math.exp(max(-700.0, -strength * squared))
                edge_u.append(u); edge_v.append(v); edge_w.append(weight)

    edge_u = np.asarray(edge_u, dtype=int)
    edge_v = np.asarray(edge_v, dtype=int)
    edge_w = np.asarray(edge_w, dtype=float)
    diagonal = np.zeros(n, dtype=float)
    np.add.at(diagonal, edge_u, edge_w)
    np.add.at(diagonal, edge_v, edge_w)
    rows = np.concatenate((np.arange(n), edge_u, edge_v))
    cols = np.concatenate((np.arange(n), edge_v, edge_u))
    values = np.concatenate((diagonal, -edge_w, -edge_w))
    laplacian = coo_matrix((values, (rows, cols)), shape=(n, n)).tocsr()

    seed_indices = np.flatnonzero(marker_flat > 0)
    unknown_indices = np.flatnonzero(marker_flat == 0)
    probabilities = np.zeros((n, len(classes)), dtype=float)
    class_lookup = {int(value): index for index, value in enumerate(classes)}
    for index in seed_indices:
        probabilities[index, class_lookup[int(marker_flat[index])]] = 1.0
    if unknown_indices.size:
        seed_one_hot = np.zeros((len(seed_indices), len(classes)), dtype=float)
        for row, index in enumerate(seed_indices):
            seed_one_hot[row, class_lookup[int(marker_flat[index])]] = 1.0
        system = laplacian[unknown_indices][:, unknown_indices].tocsc()
        boundary = -laplacian[unknown_indices][:, seed_indices] @ seed_one_hot
        solution = np.asarray(spsolve(system, boundary), dtype=float)
        if solution.ndim == 1:
            solution = solution[:, None]
        solution = np.clip(solution, 0.0, 1.0)
        totals = solution.sum(axis=1)
        if not np.isfinite(solution).all() or np.any(totals <= 0):
            raise ValueError("random-walker system is singular or numerically unresolved")
        probabilities[unknown_indices] = solution / totals[:, None]
    probability_image = probabilities.reshape(height, width, len(classes))
    labels = classes[np.argmax(probability_image, axis=2)]
    return {"labels": labels, "probabilities": probability_image, "class_labels": classes.copy()}

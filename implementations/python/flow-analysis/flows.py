"""Exploratory clustering and density analysis for origin-destination flows."""
from __future__ import annotations
import numpy as np
from scipy.ndimage import maximum_filter
from scipy.special import roots_legendre
from sklearn.cluster import DBSCAN


def cluster_od_flows(origins, destinations, *, eps, min_samples=5,
                     origin_scale=1.0, destination_scale=1.0):
    """DBSCAN-cluster OD records in separately scaled 4D endpoint space.

    Inputs are (n, 2) coordinate arrays. eps is measured in the resulting
    scaled four-dimensional Euclidean feature space. Labels -1 denote noise.
    """
    o = np.asarray(origins, dtype=float)
    d = np.asarray(destinations, dtype=float)
    if o.ndim != 2 or o.shape[1] != 2 or d.shape != o.shape or len(o) == 0:
        raise ValueError("origins and destinations must be matching non-empty (n, 2) arrays")
    if not np.all(np.isfinite(o)) or not np.all(np.isfinite(d)):
        raise ValueError("flow coordinates must be finite")
    try:
        e, os, ds = float(eps), float(origin_scale), float(destination_scale)
        ms = int(min_samples)
    except (TypeError, ValueError):
        raise ValueError("DBSCAN controls must be numeric") from None
    if not np.isfinite(e) or e <= 0 or not np.isfinite(os) or os <= 0 or not np.isfinite(ds) or ds <= 0:
        raise ValueError("eps and endpoint scales must be finite and positive")
    if isinstance(min_samples, (bool, np.bool_)) or ms != min_samples or ms < 1:
        raise ValueError("min_samples must be a positive integer")
    features = np.column_stack((o / os, d / ds))
    return DBSCAN(eps=e, min_samples=ms).fit_predict(features)


def line_flow_kde(origins, destinations, x_grid, y_grid, *,
                  bandwidth, weights=None, quadrature_order=8,
                  chunk_size=256):
    """Estimate weighted Gaussian KDE integrated uniformly along OD segments.

    Grid coordinates are 1D ascending vectors. Each flow contributes the
    average Gaussian kernel along its straight segment, approximated with
    Gauss-Legendre quadrature. Density units are weight per coordinate-area.
    """
    o = np.asarray(origins, dtype=float)
    d = np.asarray(destinations, dtype=float)
    x = np.asarray(x_grid, dtype=float)
    y = np.asarray(y_grid, dtype=float)
    if o.ndim != 2 or o.shape[1] != 2 or d.shape != o.shape or len(o) == 0:
        raise ValueError("origins and destinations must be matching non-empty (n, 2) arrays")
    if not np.all(np.isfinite(o)) or not np.all(np.isfinite(d)):
        raise ValueError("flow coordinates must be finite")
    if x.ndim != 1 or y.ndim != 1 or len(x) == 0 or len(y) == 0:
        raise ValueError("x_grid and y_grid must be non-empty vectors")
    if not np.all(np.isfinite(x)) or not np.all(np.isfinite(y)) or (len(x)>1 and np.any(np.diff(x)<=0)) or (len(y)>1 and np.any(np.diff(y)<=0)):
        raise ValueError("grid coordinates must be finite and strictly increasing")
    try:
        h = float(bandwidth)
    except (TypeError, ValueError):
        raise ValueError("bandwidth must be finite and positive") from None
    if not np.isfinite(h) or h <= 0:
        raise ValueError("bandwidth must be finite and positive")
    if isinstance(quadrature_order, (bool, np.bool_)) or not isinstance(quadrature_order, (int, np.integer)) or quadrature_order < 1:
        raise ValueError("quadrature_order must be a positive integer")
    if isinstance(chunk_size, (bool, np.bool_)) or not isinstance(chunk_size, (int, np.integer)) or chunk_size < 1:
        raise ValueError("chunk_size must be a positive integer")
    if weights is None:
        w = np.ones(len(o), dtype=float)
    else:
        w = np.asarray(weights, dtype=float)
        if w.shape != (len(o),) or not np.all(np.isfinite(w)) or np.any(w < 0):
            raise ValueError("weights must be finite, non-negative and match the flows")
    nodes, qweights = roots_legendre(int(quadrature_order))
    t = (nodes + 1.0) / 2.0
    qweights = qweights / 2.0
    samples = o[:, None, :] + t[None, :, None] * (d-o)[:, None, :]
    points = np.stack(np.meshgrid(x, y), axis=-1).reshape(-1, 2)
    out = np.zeros(len(points), dtype=float)
    normalizer = 1.0 / (2.0 * np.pi * h*h)
    for start in range(0, len(points), int(chunk_size)):
        p = points[start:start+int(chunk_size)]
        delta = p[:, None, None, :] - samples[None, :, :, :]
        squared = np.sum(delta*delta, axis=-1)
        kernels = normalizer * np.exp(-0.5*squared/(h*h))
        per_flow = np.sum(kernels*qweights[None, None, :], axis=2)
        out[start:start+len(p)] = per_flow @ w
    return out.reshape(len(y), len(x))


def flow_density_hotspots(density, *, quantile=0.95, neighbourhood_size=3):
    """Return grid-cell local maxima at or above a density quantile."""
    z = np.asarray(density, dtype=float)
    if z.ndim != 2 or not np.any(np.isfinite(z)):
        raise ValueError("density must be a 2D array with finite values")
    try:
        q = float(quantile)
    except (TypeError, ValueError):
        raise ValueError("quantile must be in [0, 1]") from None
    if not np.isfinite(q) or not 0 <= q <= 1:
        raise ValueError("quantile must be in [0, 1]")
    if isinstance(neighbourhood_size, (bool, np.bool_)) or not isinstance(neighbourhood_size, (int, np.integer)) or neighbourhood_size < 1 or neighbourhood_size % 2 == 0:
        raise ValueError("neighbourhood_size must be a positive odd integer")
    finite = np.isfinite(z)
    threshold = float(np.quantile(z[finite], q))
    local_max = maximum_filter(np.where(finite, z, -np.inf),
                               size=int(neighbourhood_size), mode="constant",
                               cval=-np.inf)
    mask = finite & (z == local_max) & (z >= threshold)
    return {"mask": mask, "threshold": threshold,
            "rows_cols": np.argwhere(mask)}


def functional_regions_from_flows(flow_matrix, *, adjacency=None,
                                   resolution=1.0, seed=0):
    """Louvain communities from reciprocal OD flows, optionally contiguous.

    The square directed OD matrix is symmetrised by summing reciprocal flows.
    When adjacency is supplied, only its undirected zone-neighbour pairs are
    retained. This is not Intramax, CURDS or Leiden.
    """
    from community import louvain_communities
    matrix = np.asarray(flow_matrix, dtype=float)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1] or matrix.shape[0] == 0:
        raise ValueError("flow_matrix must be a non-empty square matrix")
    if not np.all(np.isfinite(matrix)) or np.any(matrix < 0):
        raise ValueError("flow_matrix must contain finite non-negative flows")
    n = matrix.shape[0]
    graph = {i: {} for i in range(n)}
    allowed = None
    if adjacency is not None:
        if len(adjacency) != n:
            raise ValueError("adjacency must contain one neighbour collection per zone")
        allowed = set()
        for i, neighbours in enumerate(adjacency):
            for j in neighbours:
                if isinstance(j, (bool, np.bool_)) or not isinstance(j, (int, np.integer)) or not 0 <= int(j) < n or int(j) == i:
                    raise ValueError("adjacency contains an invalid zone identifier")
                allowed.add((min(i, int(j)), max(i, int(j))))
    for i in range(n):
        for j in range(i + 1, n):
            if allowed is not None and (i, j) not in allowed:
                continue
            weight = matrix[i, j] + matrix[j, i]
            if weight > 0:
                graph[i][j] = float(weight)
                graph[j][i] = float(weight)
    return louvain_communities(graph, resolution=resolution, seed=seed)

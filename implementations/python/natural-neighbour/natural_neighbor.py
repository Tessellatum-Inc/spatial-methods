"""Sibson natural-neighbour interpolation by Voronoi-area clipping."""
from __future__ import annotations
import numpy as np


def _clip(poly, normal, bound, tolerance=1e-12):
    if len(poly) == 0:
        return poly
    out = []
    previous = poly[-1]
    pv = float(normal @ previous - bound)
    pin = pv <= tolerance
    for current in poly:
        cv = float(normal @ current - bound)
        cin = cv <= tolerance
        if cin != pin:
            den = pv - cv
            if abs(den) > tolerance:
                out.append(previous + (pv / den) * (current - previous))
        if cin:
            out.append(current)
        previous, pv, pin = current, cv, cin
    return np.asarray(out, dtype=float).reshape((-1, 2))


def _area(poly):
    if len(poly) < 3:
        return 0.0
    x, y = poly[:, 0], poly[:, 1]
    return float(abs(np.dot(x, np.roll(y, -1)) -
                     np.dot(y, np.roll(x, -1))) * 0.5)


def natural_neighbor(points, values, query_points):
    """Sibson interpolation for distinct planar sites and interior queries.

    Values may be scalar or multi-output. Queries outside or on the sample
    convex-hull boundary are rejected; coordinates must use a projected
    Cartesian CRS. Returns one row per query.
    """
    p = np.asarray(points, dtype=float)
    z = np.asarray(values, dtype=float)
    q = np.asarray(query_points, dtype=float)
    if p.ndim != 2 or p.shape[1] != 2 or len(p) < 3:
        raise ValueError("points must have shape (n, 2), n >= 3")
    if z.ndim not in (1, 2) or z.shape[0] != len(p):
        raise ValueError("values must have one row per point")
    if not np.all(np.isfinite(p)) or not np.all(np.isfinite(z)):
        raise ValueError("points and values must be finite")
    if len(np.unique(p, axis=0)) != len(p):
        raise ValueError("duplicate sample coordinates are not supported")
    if np.linalg.matrix_rank(p - p.mean(axis=0)) < 2:
        raise ValueError("sample points must span a two-dimensional area")
    if q.ndim == 1:
        q = q.reshape(1, -1)
    if q.ndim != 2 or q.shape[1] != 2 or not np.all(np.isfinite(q)):
        raise ValueError("query_points must have shape (m, 2) and be finite")
    scalar = z.ndim == 1
    if scalar:
        z = z[:, None]
    lo = np.minimum(p.min(axis=0), q.min(axis=0))
    hi = np.maximum(p.max(axis=0), q.max(axis=0))
    margin = 16.0 * max(float(np.max(hi - lo)), 1.0)
    xmin, ymin = lo - margin
    xmax, ymax = hi + margin
    results = []
    for point in q:
        exact = np.flatnonzero(np.all(p == point, axis=1))
        if len(exact):
            results.append(z[exact[0]])
            continue
        cell = np.array([[xmin, ymin], [xmax, ymin],
                         [xmax, ymax], [xmin, ymax]], dtype=float)
        q2 = float(point @ point)
        for site in p:
            cell = _clip(cell, 2.0 * (site - point),
                         float(site @ site - q2))
        frame_tol = 1e-9 * margin
        if (np.any(np.abs(cell[:, 0] - xmin) <= frame_tol) or
                np.any(np.abs(cell[:, 0] - xmax) <= frame_tol) or
                np.any(np.abs(cell[:, 1] - ymin) <= frame_tol) or
                np.any(np.abs(cell[:, 1] - ymax) <= frame_tol)):
            raise ValueError("query points must lie strictly inside the convex hull")
        new_area = _area(cell)
        if not np.isfinite(new_area) or new_area <= np.finfo(float).eps:
            raise ValueError("query Voronoi cell is degenerate")
        stolen = np.zeros(len(p), dtype=float)
        for i, site in enumerate(p):
            region = cell.copy()
            site2 = float(site @ site)
            for j, other in enumerate(p):
                if i == j:
                    continue
                region = _clip(region, 2.0 * (other - site),
                               float(other @ other - site2))
                if len(region) == 0:
                    break
            stolen[i] = _area(region)
        total = stolen.sum()
        if not np.isfinite(total) or total <= 0:
            raise ValueError("natural-neighbour areas could not be resolved")
        results.append((stolen / total) @ z)
    output = np.asarray(results)
    return output[:, 0] if scalar else output

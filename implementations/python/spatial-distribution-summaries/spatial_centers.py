"""Weighted planar geographic distribution summaries."""
from __future__ import annotations
from math import atan2, degrees, fsum, hypot, isfinite, sqrt
from numbers import Integral


def _validate(points, weights=None):
    try:
        raw_points = list(points)
        if any(len(p) != 2 for p in raw_points):
            raise ValueError("each point must contain exactly two coordinates")
        pts = [(float(p[0]), float(p[1])) for p in raw_points]
    except (TypeError, ValueError, IndexError) as exc:
        raise ValueError("points must be a non-empty sequence of coordinate pairs") from exc
    if not pts or any(not isfinite(x) or not isfinite(y) for x, y in pts):
        raise ValueError("at least one point with finite coordinates is required")
    if weights is None:
        w = [1.0] * len(pts)
    else:
        try:
            w = [float(v) for v in weights]
        except (TypeError, ValueError) as exc:
            raise ValueError("weights must be numeric") from exc
        if len(w) != len(pts):
            raise ValueError("one weight is required for each point")
        if any(not isfinite(v) or v < 0 for v in w):
            raise ValueError("weights must be finite and nonnegative")
    if fsum(w) <= 0:
        raise ValueError("weights must have a positive total")
    return pts, w


def mean_center(points, weights=None):
    """Return the weighted arithmetic mean of planar point coordinates."""
    pts, w = _validate(points, weights)
    total = fsum(w)
    return (
        fsum(weight * point[0] for point, weight in zip(pts, w)) / total,
        fsum(weight * point[1] for point, weight in zip(pts, w)) / total,
    )


def median_center(points, weights=None, *, tolerance=1e-10, max_iterations=10000):
    """Return the weighted geometric median using modified Weiszfeld iteration."""
    pts, w = _validate(points, weights)
    if isinstance(tolerance, bool):
        raise ValueError("tolerance must be finite and positive")
    try:
        tolerance = float(tolerance)
    except (TypeError, ValueError) as exc:
        raise ValueError("tolerance must be finite and positive") from exc
    if not isfinite(tolerance) or tolerance <= 0:
        raise ValueError("tolerance must be finite and positive")
    if isinstance(max_iterations, bool) or not isinstance(max_iterations, Integral) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    current = mean_center(pts, w)
    scale = max(1.0, max(hypot(x - current[0], y - current[1]) for x, y in pts))
    tol = float(tolerance) * scale

    for _ in range(int(max_iterations)):
        coincident, noncoincident = [], []
        for point, weight in zip(pts, w):
            if weight == 0:
                continue
            distance = hypot(point[0] - current[0], point[1] - current[1])
            if distance <= tol:
                coincident.append((point, weight))
            else:
                noncoincident.append((point, weight, distance))

        if coincident:
            coincident_weight = fsum(weight for _, weight in coincident)
            rx = fsum(weight * (point[0] - current[0]) / distance
                      for point, weight, distance in noncoincident)
            ry = fsum(weight * (point[1] - current[1]) / distance
                      for point, weight, distance in noncoincident)
            residual_norm = hypot(rx, ry)
            if residual_norm <= coincident_weight + tol:
                return current
            denom = fsum(weight / distance for _, weight, distance in noncoincident)
            tx = fsum(weight * point[0] / distance for point, weight, distance in noncoincident) / denom
            ty = fsum(weight * point[1] / distance for point, weight, distance in noncoincident) / denom
            eta = min(1.0, coincident_weight / residual_norm)
            updated = (
                (1.0 - eta) * tx + eta * current[0],
                (1.0 - eta) * ty + eta * current[1],
            )
        else:
            denom = fsum(weight / distance for _, weight, distance in noncoincident)
            updated = (
                fsum(weight * point[0] / distance for point, weight, distance in noncoincident) / denom,
                fsum(weight * point[1] / distance for point, weight, distance in noncoincident) / denom,
            )

        movement = hypot(updated[0] - current[0], updated[1] - current[1])
        current = updated
        if movement <= tol:
            return current

    raise RuntimeError("geometric median did not converge within max_iterations")


def standard_distance(points, weights=None):
    """Return weighted RMS Euclidean distance from the weighted mean center."""
    pts, w = _validate(points, weights)
    cx, cy = mean_center(pts, w)
    total = fsum(w)
    variance = fsum(
        weight * ((x - cx) ** 2 + (y - cy) ** 2)
        for (x, y), weight in zip(pts, w)
    ) / total
    return sqrt(max(0.0, variance))


def standard_deviational_ellipse(points, weights=None, *, scale=1.0):
    """Return covariance principal-axis standard deviations and orientation.

    Semiaxes are scale * sqrt(eigenvalue) for the weighted coordinate
    covariance matrix. Orientation is counterclockwise from +x in [-90, 90).
    Use scale=1.515 for an approximately 68.3-percent bivariate-normal ellipse.
    """
    pts, w = _validate(points, weights)
    if isinstance(scale, bool):
        raise ValueError("scale must be finite and positive")
    try:
        scale = float(scale)
    except (TypeError, ValueError) as exc:
        raise ValueError("scale must be finite and positive") from exc
    if not isfinite(scale) or scale <= 0:
        raise ValueError("scale must be finite and positive")
    cx, cy = mean_center(pts, w)
    total = fsum(w)
    xx = fsum(weight * (x - cx) ** 2 for (x, _), weight in zip(pts, w)) / total
    yy = fsum(weight * (y - cy) ** 2 for (_, y), weight in zip(pts, w)) / total
    xy = fsum(weight * (x - cx) * (y - cy) for (x, y), weight in zip(pts, w)) / total
    discriminant = hypot(xx - yy, 2.0 * xy)
    major_var = max(0.0, (xx + yy + discriminant) / 2.0)
    minor_var = max(0.0, (xx + yy - discriminant) / 2.0)
    angle = 0.0 if discriminant <= 1e-14 * max(xx + yy, 1e-300) else 0.5 * atan2(2.0 * xy, xx - yy)
    orientation = degrees(angle)
    if orientation >= 90.0:
        orientation -= 180.0
    return {
        "center": (cx, cy),
        "major_axis_sd": float(scale) * sqrt(major_var),
        "minor_axis_sd": float(scale) * sqrt(minor_var),
        "orientation_degrees_ccw_from_x": orientation,
        "covariance": ((xx, xy), (xy, yy)),
        "scale": float(scale),
    }

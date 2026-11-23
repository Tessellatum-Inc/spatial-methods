"""Brown-Conrady radial and tangential lens distortion in normalized coordinates."""
from __future__ import annotations
import numpy as np


def _points(points):
    p = np.asarray(points, dtype=float)
    if p.ndim < 1 or p.shape[-1] != 2 or p.size == 0 or not np.all(np.isfinite(p)):
        raise ValueError("points must be finite with final dimension (x, y)")
    return p


def distort(points, k1=0.0, k2=0.0, p1=0.0, p2=0.0, k3=0.0):
    """Apply Brown-Conrady distortion to normalized camera-plane coordinates."""
    p = _points(points)
    coeff = np.asarray([k1, k2, p1, p2, k3], dtype=float)
    if not np.all(np.isfinite(coeff)):
        raise ValueError("distortion coefficients must be finite")
    x, y = p[..., 0], p[..., 1]
    r2 = x*x + y*y
    radial = 1 + k1*r2 + k2*r2*r2 + k3*r2*r2*r2
    xd = x*radial + 2*p1*x*y + p2*(r2 + 2*x*x)
    yd = y*radial + p1*(r2 + 2*y*y) + 2*p2*x*y
    return np.stack((xd, yd), axis=-1)


def undistort(points, k1=0.0, k2=0.0, p1=0.0, p2=0.0, k3=0.0,
              max_iter=20, tolerance=1e-12):
    """Invert Brown-Conrady distortion by damp-free Newton iterations.

    Raises ValueError if the Jacobian is singular or the requested residual
    tolerance is not reached. Coefficients operate on normalized coordinates.
    """
    target = _points(points)
    coeff = np.asarray([k1, k2, p1, p2, k3, tolerance], dtype=float)
    if not np.all(np.isfinite(coeff)) or tolerance <= 0:
        raise ValueError("coefficients and positive tolerance must be finite")
    if not isinstance(max_iter, int) or isinstance(max_iter, bool) or max_iter < 1:
        raise ValueError("max_iter must be a positive integer")
    estimate = target.copy()
    for _ in range(max_iter):
        x, y = estimate[..., 0], estimate[..., 1]
        r2 = x*x + y*y
        r4, r6 = r2*r2, r2*r2*r2
        radial = 1 + k1*r2 + k2*r4 + k3*r6
        common = k1 + 2*k2*r2 + 3*k3*r4
        drdx, drdy = 2*x*common, 2*y*common
        fx = x*radial + 2*p1*x*y + p2*(r2+2*x*x) - target[..., 0]
        fy = y*radial + p1*(r2+2*y*y) + 2*p2*x*y - target[..., 1]
        j11 = radial + x*drdx + 2*p1*y + 6*p2*x
        j12 = x*drdy + 2*p1*x + 2*p2*y
        j21 = y*drdx + 2*p1*x + 2*p2*y
        j22 = radial + y*drdy + 6*p1*y + 2*p2*x
        det = j11*j22 - j12*j21
        if np.any(np.abs(det) < 1e-15):
            raise ValueError("singular distortion Jacobian during inversion")
        dx = (j22*fx - j12*fy) / det
        dy = (-j21*fx + j11*fy) / det
        estimate[..., 0] -= dx
        estimate[..., 1] -= dy
        if max(float(np.max(np.abs(dx))), float(np.max(np.abs(dy)))) <= tolerance:
            residual = distort(estimate, k1, k2, p1, p2, k3) - target
            if float(np.max(np.abs(residual))) <= tolerance * 10:
                return estimate
    residual = distort(estimate, k1, k2, p1, p2, k3) - target
    if float(np.max(np.abs(residual))) > tolerance * 10:
        raise ValueError("undistortion did not converge; check model and coefficient range")
    return estimate

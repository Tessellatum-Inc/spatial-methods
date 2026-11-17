"""Barycentric interpolation over a caller-supplied planar triangulation."""
from __future__ import annotations

import math
import numpy as np


def _finite_array(values, *, name, ndim):
    try:
        result = np.asarray(values, dtype=float)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must contain finite numeric values") from exc
    if result.ndim != ndim or not np.all(np.isfinite(result)):
        raise ValueError(f"{name} must be a finite {ndim}-dimensional array")
    return result


class TINInterpolator2D:
    """Interpolate scalar vertex values linearly over a planar triangle mesh.

    Triangles are integer indices into the supplied vertex array. Queries
    outside all triangles return None; shared-edge points use the first
    containing face in input order.
    """

    def __init__(self, vertices, values, triangles, *, tolerance=1e-12):
        points = _finite_array(vertices, name="vertices", ndim=2)
        observations = _finite_array(values, name="values", ndim=1)
        if points.shape[1] != 2 or len(points) < 3:
            raise ValueError("vertices must have shape (n, 2), with n >= 3")
        if len(observations) != len(points):
            raise ValueError("one scalar value is required for every vertex")
        if len(np.unique(points, axis=0)) != len(points):
            raise ValueError("duplicate vertex coordinates are not supported")
        raw_faces = np.asarray(triangles)
        if raw_faces.ndim != 2 or raw_faces.shape[1] != 3 or len(raw_faces) == 0:
            raise ValueError("triangles must be a non-empty (m, 3) index array")
        if raw_faces.dtype.kind not in "iu":
            raise ValueError("triangle indices must be integers")
        faces = raw_faces.astype(np.int64, copy=False)
        if np.any(faces < 0) or np.any(faces >= len(points)):
            raise ValueError("triangle index is outside the vertex array")
        if any(len(set(map(int, face))) != 3 for face in faces):
            raise ValueError("each triangle must contain three distinct vertex indices")
        canonical = [tuple(sorted(map(int, face))) for face in faces]
        if len(set(canonical)) != len(canonical):
            raise ValueError("duplicate triangles are not supported")
        if isinstance(tolerance, (bool, np.bool_)) or not isinstance(
            tolerance, (int, float, np.integer, np.floating)
        ):
            raise ValueError("tolerance must be a finite non-negative number")
        try:
            tolerance = float(tolerance)
        except (OverflowError, TypeError, ValueError) as exc:
            raise ValueError("tolerance must be a finite non-negative number") from exc
        if not math.isfinite(tolerance) or tolerance < 0:
            raise ValueError("tolerance must be a finite non-negative number")

        self.vertices_ = points.copy()
        self.values_ = observations.copy()
        self.triangles_ = faces.copy()
        self.tolerance_ = tolerance
        self._triangle_points = points[faces]
        self._denominators = []
        for triangle in self._triangle_points:
            a, b, c = triangle
            denominator = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
            if denominator == 0:
                raise ValueError("degenerate zero-area triangle")
            self._denominators.append(float(denominator))

    def predict(self, queries):
        """Return a list of interpolated floats or None outside the TIN."""
        targets = _finite_array(queries, name="queries", ndim=2)
        if targets.shape[1] != 2:
            raise ValueError("queries must have shape (m, 2)")
        predictions = []
        for x, y in targets:
            estimate = None
            for face_index, (triangle, denominator) in enumerate(
                zip(self._triangle_points, self._denominators)
            ):
                a, b, c = triangle
                wa = ((b[1] - c[1]) * (x - c[0]) + (c[0] - b[0]) * (y - c[1])) / denominator
                wb = ((c[1] - a[1]) * (x - c[0]) + (a[0] - c[0]) * (y - c[1])) / denominator
                wc = 1.0 - wa - wb
                weights = (wa, wb, wc)
                if all(weight >= -self.tolerance_ and weight <= 1 + self.tolerance_ for weight in weights):
                    clipped = np.maximum(np.asarray(weights), 0.0)
                    clipped /= clipped.sum()
                    estimate = float(np.dot(clipped, self.values_[self.triangles_[face_index]]))
                    break
            predictions.append(estimate)
        return predictions


def tin_interpolate(vertices, values, triangles, queries, *, tolerance=1e-12):
    """Convenience function for a single TIN prediction batch."""
    return TINInterpolator2D(vertices, values, triangles, tolerance=tolerance).predict(queries)

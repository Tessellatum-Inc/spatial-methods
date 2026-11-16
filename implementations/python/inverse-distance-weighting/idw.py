"""Inverse-distance weighting interpolation for planar sample points."""
import math

def _points(values, label):
    if isinstance(values, (str, bytes)) or not isinstance(values, (list, tuple)):
        raise ValueError(f"{label} must be a sequence")
    result = []
    for point in values:
        if isinstance(point, (str, bytes)) or not isinstance(point, (list, tuple)) or len(point) != 2:
            raise ValueError(f"each {label} point must contain x and y")
        x, y = point
        if any(isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v) for v in (x, y)):
            raise ValueError(f"{label} coordinates must be finite numeric values")
        result.append((float(x), float(y)))
    return result

def idw_interpolate(samples, values, queries, *, power=2.0,
                    max_neighbors=None, radius=None):
    """Predict values using normalized inverse-distance weights.

    Exact query/sample coordinate matches return the mean of all coincident
    sample values. Queries with no samples inside radius return None.
    """
    sample_points = _points(samples, "sample")
    query_points = _points(queries, "query")
    if not sample_points or len(sample_points) != len(values):
        raise ValueError("samples and values must have equal non-zero length")
    sample_values = []
    for value in values:
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
            raise ValueError("sample values must be finite numeric values")
        sample_values.append(float(value))
    if isinstance(power, bool) or not isinstance(power, (int, float)) or not math.isfinite(power) or power <= 0:
        raise ValueError("power must be finite and positive")
    if max_neighbors is not None and (isinstance(max_neighbors, bool) or not isinstance(max_neighbors, int) or max_neighbors < 1):
        raise ValueError("max_neighbors must be a positive integer or None")
    if radius is not None and (isinstance(radius, bool) or not isinstance(radius, (int, float)) or not math.isfinite(radius) or radius <= 0):
        raise ValueError("radius must be finite and positive or None")
    predictions = []
    for query in query_points:
        neighbours = []
        exact = []
        for index, (point, value) in enumerate(zip(sample_points, sample_values)):
            distance = math.hypot(point[0]-query[0], point[1]-query[1])
            if distance == 0:
                exact.append(value)
            elif radius is None or distance <= radius:
                neighbours.append((distance, index, value))
        if exact:
            predictions.append(math.fsum(exact) / len(exact))
            continue
        neighbours.sort(key=lambda item: (item[0], item[1]))
        if max_neighbors is not None:
            neighbours = neighbours[:max_neighbors]
        if not neighbours:
            predictions.append(None)
            continue
        minimum_distance = neighbours[0][0]
        weights = [(minimum_distance / distance) ** float(power) for distance, _, _ in neighbours]
        denominator = math.fsum(weights)
        predictions.append(math.fsum(weight*item[2] for weight,item in zip(weights,neighbours)) / denominator)
    return predictions

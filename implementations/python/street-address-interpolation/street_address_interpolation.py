"""Linear address-range interpolation along projected street polylines."""
from __future__ import annotations

import bisect
import math


def _integer(value, name):
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{name} must be an integer")
    return value


def interpolate_street_addresses(coordinates, start_number, end_number, *,
                                 requested_numbers=None, side="center", offset_distance=0.0):
    """Interpolate address numbers by cumulative distance along a polyline.

    Coordinates are projected planar (x, y) pairs. When no explicit numbers
    are supplied, same-parity ranges advance by two and mixed-parity ranges
    advance by one. Optional left/right offsets use the local segment normal
    and the same linear units as the coordinates.
    """
    start = _integer(start_number, "start_number")
    end = _integer(end_number, "end_number")
    if start == end:
        raise ValueError("start_number and end_number must differ")
    if side not in ("center", "left", "right"):
        raise ValueError("side must be 'center', 'left' or 'right'")
    if isinstance(offset_distance, bool):
        raise ValueError("offset_distance must be finite and non-negative")
    try:
        offset = float(offset_distance)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("offset_distance must be finite and non-negative") from exc
    if not math.isfinite(offset) or offset < 0:
        raise ValueError("offset_distance must be finite and non-negative")
    if side == "center" and offset != 0:
        raise ValueError("center side requires zero offset_distance")

    try:
        raw_points = list(coordinates)
        if len(raw_points) < 2 or any(len(point) != 2 for point in raw_points):
            raise ValueError("coordinates must contain at least two x/y pairs")
        points = [(float(point[0]), float(point[1])) for point in raw_points]
    except (TypeError, ValueError, IndexError, OverflowError) as exc:
        raise ValueError("coordinates must be finite planar x/y pairs") from exc
    if any(not math.isfinite(x) or not math.isfinite(y) for x, y in points):
        raise ValueError("coordinates must be finite")

    lengths = []
    cumulative = [0.0]
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        length = math.hypot(x1 - x0, y1 - y0)
        if length <= 0:
            raise ValueError("consecutive street vertices must be distinct")
        lengths.append(length)
        cumulative.append(cumulative[-1] + length)
    total = cumulative[-1]

    if requested_numbers is None:
        step = 2 if abs(end - start) % 2 == 0 else 1
        step *= 1 if end > start else -1
        numbers = list(range(start, end + step, step))
    else:
        numbers = [_integer(value, "requested address number") for value in requested_numbers]
        if len(numbers) != len(set(numbers)):
            raise ValueError("requested_numbers must not contain duplicates")
        if any(value < min(start, end) or value > max(start, end) for value in numbers):
            raise ValueError("requested address numbers must lie within the supplied range")

    output = []
    for number in numbers:
        fraction = (number - start) / (end - start)
        distance = fraction * total
        segment = min(bisect.bisect_left(cumulative, distance, lo=1) - 1, len(lengths) - 1)
        segment = max(0, segment)
        local_fraction = (distance - cumulative[segment]) / lengths[segment]
        x0, y0 = points[segment]
        x1, y1 = points[segment + 1]
        dx, dy = (x1 - x0) / lengths[segment], (y1 - y0) / lengths[segment]
        x = x0 + local_fraction * (x1 - x0)
        y = y0 + local_fraction * (y1 - y0)
        if side == "left":
            x -= offset * dy
            y += offset * dx
        elif side == "right":
            x += offset * dy
            y -= offset * dx
        output.append({"number": number, "x": x, "y": y, "fraction": fraction, "side": side})
    return output

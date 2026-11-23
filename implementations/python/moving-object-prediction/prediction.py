"""Moving-object prediction and continuous range queries."""
from __future__ import annotations
import math
from collections.abc import Mapping, Sequence


def _number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite number")
    try:
        result = float(value)
    except (OverflowError, ValueError) as exc:
        raise ValueError(f"{name} must be representable as a finite float") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be representable as a finite float")
    return result


def _point(value, name):
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence) or len(value) != 2:
        raise ValueError(f"{name} must be a pair of coordinates")
    return (_number(value[0], name), _number(value[1], name))


def _advance(x, y, vx, vy, dt):
    predicted = (x + vx * dt, y + vy * dt)
    if not all(math.isfinite(v) for v in predicted):
        raise ValueError("predicted coordinates overflowed finite numeric range")
    return predicted


def predict_position(position, velocity, horizon):
    """Extrapolate a 2D point using constant Cartesian velocity."""
    x, y = _point(position, "position")
    vx, vy = _point(velocity, "velocity")
    dt = _number(horizon, "horizon")
    if dt < 0:
        raise ValueError("horizon must be non-negative")
    return _advance(x, y, vx, vy, dt)


def predictive_range_query(objects: Mapping, bounds: Sequence[float], horizon: float,
                           *, uncertainty_radius: float = 0.0):
    """Return (id, predicted point, distance) for uncertainty disks intersecting a rectangle.

    Each state is (x, y, vx, vy). Results preserve mapping iteration order.
    """
    if not isinstance(objects, Mapping):
        raise ValueError("objects must be a mapping")
    if isinstance(bounds, (str, bytes)) or not isinstance(bounds, Sequence) or len(bounds) != 4:
        raise ValueError("bounds must be (xmin, ymin, xmax, ymax)")
    xmin, ymin, xmax, ymax = (_number(v, "bounds") for v in bounds)
    if xmin > xmax or ymin > ymax:
        raise ValueError("rectangle bounds must be ordered")
    dt = _number(horizon, "horizon")
    radius = _number(uncertainty_radius, "uncertainty_radius")
    if dt < 0 or radius < 0:
        raise ValueError("horizon and uncertainty_radius must be non-negative")
    results = []
    for object_id, state in objects.items():
        if isinstance(state, (str, bytes)) or not isinstance(state, Sequence) or len(state) != 4:
            raise ValueError(f"state for {object_id!r} must be (x, y, vx, vy)")
        x, y, vx, vy = (_number(v, f"state for {object_id!r}") for v in state)
        px, py = _advance(x, y, vx, vy, dt)
        nearest_x = min(max(px, xmin), xmax)
        nearest_y = min(max(py, ymin), ymax)
        distance = math.hypot(px - nearest_x, py - nearest_y)
        if distance <= radius:
            results.append((object_id, (px, py), distance))
    return results


def continuous_range_query(objects: Mapping, bounds: Sequence[float], horizon: float):
    """Find first rectangle contact for constant-velocity paths over a finite horizon.

    Returns (object_id, first_contact_position, contact_time) in mapping order.
    Uses Liang–Barsky clipping and includes closed-rectangle boundary contact.
    """
    if not isinstance(objects, Mapping):
        raise ValueError("objects must be a mapping")
    if isinstance(bounds, (str, bytes)) or not isinstance(bounds, Sequence) or len(bounds) != 4:
        raise ValueError("bounds must be (xmin, ymin, xmax, ymax)")
    xmin, ymin, xmax, ymax = (_number(v, "bounds") for v in bounds)
    if xmin > xmax or ymin > ymax:
        raise ValueError("rectangle bounds must be ordered")
    dt = _number(horizon, "horizon")
    if dt < 0:
        raise ValueError("horizon must be non-negative")
    results = []
    for object_id, state in objects.items():
        if isinstance(state, (str, bytes)) or not isinstance(state, Sequence) or len(state) != 4:
            raise ValueError(f"state for {object_id!r} must be (x, y, vx, vy)")
        x, y, vx, vy = (_number(v, f"state for {object_id!r}") for v in state)
        end_x, end_y = _advance(x, y, vx, vy, dt)
        dx, dy = end_x - x, end_y - y
        lower, upper = 0.0, 1.0
        clipped = True
        for p, q in ((-dx, x - xmin), (dx, xmax - x),
                     (-dy, y - ymin), (dy, ymax - y)):
            if p == 0:
                if q < 0:
                    clipped = False
                    break
                continue
            ratio = q / p
            if p < 0:
                lower = max(lower, ratio)
            else:
                upper = min(upper, ratio)
            if lower > upper:
                clipped = False
                break
        if clipped and 0.0 <= lower <= 1.0:
            contact_x, contact_y = x + lower * dx, y + lower * dy
            contact_time = lower * dt
            if not all(math.isfinite(v) for v in (contact_x, contact_y, contact_time)):
                raise ValueError("continuous-query result overflowed finite numeric range")
            results.append((object_id, (contact_x, contact_y), contact_time))
    return results


def _quadratic_roots(a, b, c):
    """Real roots of a*t²+b*t+c, using a cancellation-resistant formula."""
    if a == 0.0:
        return [] if b == 0.0 else [-c / b]
    discriminant = b * b - 4.0 * a * c
    if not math.isfinite(discriminant):
        raise ValueError("acceleration query root calculation overflowed")
    if discriminant < 0.0:
        return []
    root_disc = math.sqrt(discriminant)
    if root_disc == 0.0:
        return [-b / (2.0 * a)]
    q = -0.5 * (b + math.copysign(root_disc, b))
    if q == 0.0:
        return [-b / (2.0 * a)]
    return [q / a, c / q]


def continuous_acceleration_range_query(objects: Mapping, bounds: Sequence[float],
                                        horizon: float):
    """Find first closed-rectangle contact for constant-acceleration point paths.

    Each state is (x, y, vx, vy, ax, ay), with
    p(t) = p0 + v0*t + 0.5*a*t². Returns (id, position, time), preserving
    mapping order. Boundary-only tangencies count as contact. This is an exact
    quadratic-trajectory query up to floating-point root arithmetic, not a
    probabilistic uncertainty query or a spatial index.
    """
    if not isinstance(objects, Mapping):
        raise ValueError("objects must be a mapping")
    if isinstance(bounds, (str, bytes)) or not isinstance(bounds, Sequence) or len(bounds) != 4:
        raise ValueError("bounds must be (xmin, ymin, xmax, ymax)")
    xmin, ymin, xmax, ymax = (_number(v, "bounds") for v in bounds)
    if xmin > xmax or ymin > ymax:
        raise ValueError("rectangle bounds must be ordered")
    dt = _number(horizon, "horizon")
    if dt < 0:
        raise ValueError("horizon must be non-negative")

    results = []
    for object_id, state in objects.items():
        if isinstance(state, (str, bytes)) or not isinstance(state, Sequence) or len(state) != 6:
            raise ValueError(f"state for {object_id!r} must be (x, y, vx, vy, ax, ay)")
        x, y, vx, vy, ax, ay = (
            _number(v, f"state for {object_id!r}") for v in state
        )
        # Check endpoint position and velocity before solving roots; this
        # catches overflow even when the path would not intersect the query.
        end_x = x + vx * dt + 0.5 * ax * dt * dt
        end_y = y + vy * dt + 0.5 * ay * dt * dt
        end_vx, end_vy = vx + ax * dt, vy + ay * dt
        if not all(math.isfinite(v) for v in (end_x, end_y, end_vx, end_vy)):
            raise ValueError("acceleration query endpoint overflowed")
        candidates = [0.0, dt]
        for a, b, origin, lo, hi in (
            (0.5 * ax, vx, x, xmin, xmax),
            (0.5 * ay, vy, y, ymin, ymax),
        ):
            if not math.isfinite(a):
                raise ValueError("acceleration query coefficient overflowed")
            for edge in (lo, hi):
                for root in _quadratic_roots(a, b, origin - edge):
                    if math.isfinite(root) and 0.0 <= root <= dt:
                        candidates.append(root)
        candidates = sorted(set(candidates))

        def position(t):
            px = x + vx * t + 0.5 * ax * t * t
            py = y + vy * t + 0.5 * ay * t * t
            if not math.isfinite(px) or not math.isfinite(py):
                raise ValueError("acceleration query position overflowed")
            return px, py

        def inside(px, py):
            tx = 1e-12 * max(1.0, abs(px), abs(xmin), abs(xmax))
            ty = 1e-12 * max(1.0, abs(py), abs(ymin), abs(ymax))
            return xmin - tx <= px <= xmax + tx and ymin - ty <= py <= ymax + ty

        contact = None
        for index, t in enumerate(candidates):
            px, py = position(t)
            if inside(px, py):
                contact = t
                break
            if index + 1 < len(candidates):
                next_t = candidates[index + 1]
                if next_t > t:
                    mid = t + (next_t - t) / 2.0
                    mx, my = position(mid)
                    if inside(mx, my):
                        contact = t
                        break
        if contact is not None:
            px, py = position(contact)
            # Remove only root-rounding drift at a contacted boundary.
            px = min(max(px, xmin), xmax)
            py = min(max(py, ymin), ymax)
            results.append((object_id, (px, py), contact))
    return results


def dead_reckoning_update_required(reported_position, reported_velocity,
                                   elapsed_time, observed_position, *, tolerance):
    """Request a report when observed error exceeds the prediction tolerance."""
    predicted = predict_position(reported_position, reported_velocity, elapsed_time)
    observed = _point(observed_position, "observed_position")
    limit = _number(tolerance, "tolerance")
    if limit < 0:
        raise ValueError("tolerance must be non-negative")
    error = math.hypot(observed[0] - predicted[0], observed[1] - predicted[1])
    if not math.isfinite(error):
        raise ValueError("prediction error overflowed finite numeric range")
    return error > limit

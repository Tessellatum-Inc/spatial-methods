"""Headway and passenger-arrival-weighted waiting-time metrics."""

from __future__ import annotations

from math import isfinite
from statistics import mean, median, pstdev
from typing import Iterable


def headway_metrics(
    departures: Iterable[float],
    *,
    service_start: float,
    service_end: float,
) -> dict[str, object]:
    """Summarize departures and expected wait over a defined service window.

    Times use one consistent numeric unit (normally seconds after service-day
    midnight); values above 24 hours are permitted for GTFS extended service
    times. Departures are sorted internally and must be unique and lie within
    the closed service window.

    For passengers arriving uniformly at random during the window, each
    interval of length h contributes h²/(2T) to expected wait, where T is the
    full window duration. Boundary intervals from service_start to the first
    departure and from the last departure to service_end are included. With
    no departures, expected_wait is None.
    """
    try:
        start = float(service_start)
        end = float(service_end)
    except (TypeError, ValueError) as exc:
        raise ValueError("service boundaries must be finite numbers") from exc
    if not isfinite(start) or not isfinite(end) or end <= start:
        raise ValueError("service_end must be finite and greater than service_start")

    try:
        values = [float(value) for value in departures]
    except (TypeError, ValueError) as exc:
        raise ValueError("departures must be finite numeric times") from exc
    if any(not isfinite(value) for value in values):
        raise ValueError("departure times must be finite")
    if any(value < start or value > end for value in values):
        raise ValueError("every departure must lie within the service window")

    values.sort()
    if any(right <= left for left, right in zip(values, values[1:])):
        raise ValueError("departure times must be unique")

    duration = end - start
    gaps = [right - left for left, right in zip(values, values[1:])]
    result: dict[str, object] = {
        "service_start": start,
        "service_end": end,
        "service_duration": duration,
        "departure_count": len(values),
        "departures": values,
        "headways": gaps,
        "mean_headway": mean(gaps) if gaps else None,
        "median_headway": median(gaps) if gaps else None,
        "headway_cv": (pstdev(gaps) / mean(gaps)) if len(gaps) >= 2 and mean(gaps) > 0 else None,
        "expected_wait": None,
        "wait_intervals": [],
    }
    if not values:
        return result

    boundaries = [start, *values, end]
    wait_intervals = [
        right - left
        for left, right in zip(boundaries, boundaries[1:])
        if right > left
    ]
    result["wait_intervals"] = wait_intervals
    result["expected_wait"] = sum(gap * gap for gap in wait_intervals) / (2.0 * duration)
    return result

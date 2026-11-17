"""Headway and passenger-arrival-weighted waiting-time metrics."""
from __future__ import annotations
from math import isfinite
from statistics import mean, median, pstdev
from typing import Iterable


def headway_metrics(departures: Iterable[float], *, service_start: float,
                    service_end: float,
                    arrival_weights: Iterable[float] | None = None) -> dict[str, object]:
    """Summarize headways and expected wait over a closed service window.

    Optional arrival_weights are relative constant arrival rates, one per
    positive interval in wait_intervals. Without them, arrivals are uniform.
    """
    try:
        start, end = float(service_start), float(service_end)
    except (TypeError, ValueError) as exc:
        raise ValueError("service boundaries must be finite numbers") from exc
    if not isfinite(start) or not isfinite(end) or end <= start:
        raise ValueError("service_end must be finite and greater than service_start")
    try:
        values = [float(v) for v in departures]
    except (TypeError, ValueError) as exc:
        raise ValueError("departures must be finite numeric times") from exc
    if any(not isfinite(v) for v in values):
        raise ValueError("departure times must be finite")
    if any(v < start or v > end for v in values):
        raise ValueError("every departure must lie within the service window")
    values.sort()
    if any(b <= a for a, b in zip(values, values[1:])):
        raise ValueError("departure times must be unique")
    gaps = [b-a for a, b in zip(values, values[1:])]
    result: dict[str, object] = {
        "service_start": start, "service_end": end, "service_duration": end-start,
        "departure_count": len(values), "departures": values, "headways": gaps,
        "mean_headway": mean(gaps) if gaps else None,
        "median_headway": median(gaps) if gaps else None,
        "headway_cv": pstdev(gaps)/mean(gaps) if len(gaps) >= 2 and mean(gaps)>0 else None,
        "expected_wait": None, "arrival_weight_total": 0.0,
        "wait_intervals": [], "arrival_weights": [],
    }
    if not values:
        if arrival_weights is not None:
            try: supplied = list(arrival_weights)
            except TypeError as exc:
                raise ValueError("arrival_weights must be an iterable") from exc
            if supplied:
                raise ValueError("arrival_weights must have one value per positive wait interval")
        return result
    bounds = [start, *values, end]
    intervals = [b-a for a,b in zip(bounds,bounds[1:]) if b>a]
    if arrival_weights is None:
        rates = [1.0] * len(intervals)
    else:
        try: rates = [float(v) for v in arrival_weights]
        except (TypeError, ValueError) as exc:
            raise ValueError("arrival_weights must be finite non-negative rates") from exc
        if len(rates) != len(intervals):
            raise ValueError("arrival_weights must have one value per positive wait interval")
        if any(not isfinite(v) or v < 0 for v in rates):
            raise ValueError("arrival_weights must be finite non-negative rates")
    total = sum(r*g for r,g in zip(rates,intervals))
    result["wait_intervals"], result["arrival_weights"] = intervals, rates
    result["arrival_weight_total"] = total
    if total > 0:
        result["expected_wait"] = sum(r*g*g/2 for r,g in zip(rates,intervals))/total
    return result

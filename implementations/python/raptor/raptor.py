"""A compact round-based public-transport router (RAPTOR teaching baseline)."""
from __future__ import annotations
from dataclasses import dataclass
from math import isfinite
from typing import Hashable, Mapping, Sequence

@dataclass(frozen=True)
class Trip:
    """One trip on a route; times are minutes on a common service-day clock."""
    arrivals: tuple[float, ...]
    departures: tuple[float, ...]

@dataclass(frozen=True)
class Route:
    """Trips share the same ordered stop sequence and are non-overtaking."""
    stops: tuple[Hashable, ...]
    trips: tuple[Trip, ...]

def _validate(routes):
    for route in routes:
        if len(route.stops) < 2 or not route.trips:
            raise ValueError("each route needs at least two stops and one trip")
        if len(set(route.stops)) != len(route.stops):
            raise ValueError("a route stop sequence must not repeat stops")
        previous_first = float("-inf")
        for trip_index, trip in enumerate(route.trips):
            if len(trip.arrivals) != len(route.stops) or len(trip.departures) != len(route.stops):
                raise ValueError("trip time arrays must match route stop count")
            for a, d in zip(trip.arrivals, trip.departures):
                if not isfinite(a) or not isfinite(d) or a > d:
                    raise ValueError("trip times must be finite and arrival <= departure")
            if any(trip.departures[i] > trip.arrivals[i+1] for i in range(len(route.stops)-1)):
                raise ValueError("trip times must be nondecreasing along the route")
            if trip.departures[0] < previous_first:
                raise ValueError("trips must be sorted by first-stop departure")
            if trip_index > 0:
                prior = route.trips[trip_index - 1]
                if any(trip.arrivals[i] < prior.arrivals[i] or
                       trip.departures[i] < prior.departures[i]
                       for i in range(len(route.stops))):
                    raise ValueError("overtaking trips are outside this baseline's assumptions")
            previous_first = trip.departures[0]

def raptor(routes: Sequence[Route], access_times: Mapping[Hashable, float], *,
           max_transfers: int = 3,
           footpaths: Mapping[Hashable, Sequence[tuple[Hashable, float]]] | None = None):
    """Return earliest arrivals by boarding round and a predecessor trace.

    Round 0 contains access times; round 1 permits one vehicle boarding.
    Consequently max_transfers=0 still permits a direct ride. Footpaths are
    non-negative walking links applied after each transit round. For clarity,
    this reference scans all trips at each reachable boarding position; it
    favours explicit correctness over production RAPTOR's route-scan speed.
    """
    if max_transfers < 0:
        raise ValueError("max_transfers must be non-negative")
    _validate(routes)
    if not access_times:
        raise ValueError("at least one access stop is required")
    base = {}
    for stop, time in access_times.items():
        time = float(time)
        if not isfinite(time): raise ValueError("access times must be finite")
        base[stop] = time
    walks = footpaths or {}
    for origin, links in walks.items():
        for destination, duration in links:
            duration = float(duration)
            if not isfinite(duration) or duration < 0:
                raise ValueError("footpath durations must be finite and non-negative")
    def walk_closure(labels, preds, round_no):
        # Non-negative walking links; repeated relaxation handles footpath chains.
        changed = True
        while changed:
            changed = False
            for origin, links in walks.items():
                if origin not in labels: continue
                for destination, duration in links:
                    candidate = labels[origin] + float(duration)
                    if candidate < labels.get(destination, float("inf")):
                        labels[destination] = candidate
                        preds[destination] = (origin, "walk", float(duration), round_no)
                        changed = True
    # Access walking must be available before the first vehicle boarding.
    base_predecessors = {}
    walk_closure(base, base_predecessors, 0)
    rounds = [dict(base)]
    predecessors = [base_predecessors]
    for round_no in range(1, max_transfers + 2):
        previous = rounds[-1]
        current = dict(previous)
        pred = {}
        for route in routes:
            for board_index, board_stop in enumerate(route.stops[:-1]):
                ready = previous.get(board_stop)
                if ready is None: continue
                for trip in route.trips:
                    if trip.departures[board_index] < ready: continue
                    for j in range(board_index + 1, len(route.stops)):
                        stop = route.stops[j]
                        arrival = trip.arrivals[j]
                        if arrival < current.get(stop, float("inf")):
                            current[stop] = arrival
                            pred[stop] = (board_stop, route.stops[j-1], trip.departures[board_index],
                                          arrival, route.stops[board_index:j+1], round_no)
        walk_closure(current, pred, round_no)
        rounds.append(current)
        predecessors.append(pred)
    return {"rounds": rounds, "predecessors": predecessors}

"""Connection Scan Algorithm (CSA) earliest-arrival teaching baseline."""
from __future__ import annotations
from dataclasses import dataclass
from math import isfinite
from typing import Hashable, Mapping, Sequence

@dataclass(frozen=True)
class Connection:
    trip_id: Hashable
    from_stop: Hashable
    to_stop: Hashable
    departure: float
    arrival: float

def earliest_arrival(connections: Sequence[Connection],
                     access_times: Mapping[Hashable, float], *,
                     minimum_transfer: Mapping[Hashable, float] | None = None):
    """Scan departure-sorted timetable connections once.

    A connection can be boarded when its origin is reachable early enough
    under the stop's minimum transfer time, or when the passenger is already
    aboard the same trip. Returns arrival labels and predecessor connections.
    Times use one common service-day clock. The caller supplies a globally
    departure-sorted connection sequence.
    """
    if not access_times:
        raise ValueError("at least one access stop is required")
    transfers = minimum_transfer or {}
    for stop, duration in transfers.items():
        duration = float(duration)
        if not isfinite(duration) or duration < 0:
            raise ValueError("minimum transfer times must be finite and non-negative")
    arrivals = {}
    for stop, time in access_times.items():
        time = float(time)
        if not isfinite(time): raise ValueError("access times must be finite")
        arrivals[stop] = time
    onboard = set()
    # Keep access and transit labels separate: a later transit arrival must not
    # impose an interchange penalty on an earlier independent access arrival.
    transit_arrivals = {}
    predecessors = {}
    previous_departure = float("-inf")
    for connection in connections:
        dep, arr = float(connection.departure), float(connection.arrival)
        if not isfinite(dep) or not isfinite(arr) or arr < dep:
            raise ValueError("connection times must be finite and arrival >= departure")
        if dep < previous_departure:
            raise ValueError("connections must be sorted by departure time")
        previous_departure = dep
        access_ready = float(access_times.get(connection.from_stop, float("inf")))
        transit_ready = transit_arrivals.get(connection.from_stop, float("inf"))
        change = float(transfers.get(connection.from_stop, 0.0))
        can_board = access_ready <= dep or transit_ready + change <= dep
        if can_board or connection.trip_id in onboard:
            if arr < transit_arrivals.get(connection.to_stop, float("inf")):
                transit_arrivals[connection.to_stop] = arr
            if arr < arrivals.get(connection.to_stop, float("inf")):
                arrivals[connection.to_stop] = arr
                predecessors[connection.to_stop] = connection
            onboard.add(connection.trip_id)
    return {"arrival_times": arrivals, "predecessors": predecessors}

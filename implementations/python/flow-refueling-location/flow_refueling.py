"""Exact small-instance flow-refueling location model."""
from __future__ import annotations
import math
from collections.abc import Mapping
from itertools import combinations

def _finite(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError("value must be finite numeric")
    return float(value)

def _prepare(paths, weights, candidate_sites, p, vehicle_range):
    if not isinstance(paths, Mapping) or not isinstance(weights, Mapping) or set(paths) != set(weights):
        raise ValueError("paths and weights must be mappings with identical path IDs")
    if isinstance(candidate_sites, (str, bytes)):
        raise ValueError("candidate_sites must be a sequence")
    sites = list(candidate_sites)
    try:
        unique = set(sites)
    except TypeError as exc:
        raise ValueError("candidate site IDs must be hashable") from exc
    if len(unique) != len(sites) or not sites:
        raise ValueError("candidate sites must be non-empty and unique")
    if isinstance(p, bool) or not isinstance(p, int) or not 0 <= p <= len(sites):
        raise ValueError("p must be an integer between zero and candidate count")
    vehicle_range = _finite(vehicle_range, "vehicle_range")
    if vehicle_range <= 0:
        raise ValueError("vehicle_range must be positive")
    prepared = {}
    for path_id, path in paths.items():
        if not isinstance(path, Mapping) or "length" not in path or "sites" not in path:
            raise ValueError("each path must contain length and sites")
        length = _finite(path["length"], "path length")
        if length < 0 or not isinstance(path["sites"], Mapping):
            raise ValueError("path length must be non-negative and sites must be a mapping")
        positions = {}
        for site, distance in path["sites"].items():
            if site not in unique:
                raise ValueError("path contains a site outside the candidate set")
            distance = _finite(distance, "station route distance")
            if not 0 <= distance <= length:
                raise ValueError("station route distance must lie along the path")
            positions[site] = distance
        weight = _finite(weights[path_id], "path weight")
        if weight < 0:
            raise ValueError("path weights must be non-negative")
        prepared[path_id] = (length, positions, weight)
    return sites, prepared, p, vehicle_range

def _is_feasible(length, positions, selected, vehicle_range):
    ordered = sorted(positions[site] for site in selected if site in positions)
    previous = 0.0
    for station in ordered:
        if station - previous > vehicle_range:
            return False
        previous = station
    return length - previous <= vehicle_range

def flow_refueling_exact(paths, weights, candidate_sites, p, vehicle_range):
    """Maximize weighted feasible route flow by exhaustive site-set search.

    Each path supplies its length and candidate-station positions measured
    along that fixed route. A vehicle starts with a full tank, may refuel at
    any selected station on the path, and can travel at most vehicle_range
    between consecutive refuels and from either endpoint to a station.
    """
    sites, prepared, p, vehicle_range = _prepare(paths, weights, candidate_sites, p, vehicle_range)
    best_sites = None
    best_value = -1.0
    best_paths = ()
    for chosen in combinations(sites, p):
        feasible = tuple(
            path_id for path_id, (length, positions, _weight) in prepared.items()
            if _is_feasible(length, positions, chosen, vehicle_range)
        )
        value = math.fsum(prepared[path_id][2] for path_id in feasible)
        if value > best_value:
            best_sites, best_value, best_paths = chosen, value, feasible
    return {"sites": tuple(best_sites), "objective": best_value, "feasible_paths": best_paths}

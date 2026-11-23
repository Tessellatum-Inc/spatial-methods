"""Flow-capturing facility location: exact and greedy p-budget baselines."""
from __future__ import annotations

from collections.abc import Mapping
from itertools import combinations
import math


def _prepare(paths, weights, candidate_sites, p):
    if not isinstance(paths, Mapping) or not isinstance(weights, Mapping):
        raise ValueError("paths and weights must be mappings")
    if set(paths) != set(weights):
        raise ValueError("weights must be supplied for every path and no others")
    if isinstance(candidate_sites, (str, bytes)):
        raise ValueError("candidate_sites must be a sequence")
    sites = list(candidate_sites)
    if len(sites) != len(set(sites)):
        raise ValueError("candidate sites must be unique")
    if not sites:
        raise ValueError("at least one candidate site is required")
    if isinstance(p, bool) or not isinstance(p, int) or not 0 <= p <= len(sites):
        raise ValueError("p must be an integer between zero and the number of sites")
    site_set = set(sites)
    prepared = {}
    for path_id, path_sites in paths.items():
        if isinstance(path_sites, (str, bytes)):
            raise ValueError("each path must be a sequence of candidate sites")
        try:
            ordered = list(path_sites)
        except TypeError as exc:
            raise ValueError("each path must be a sequence of candidate sites") from exc
        if len(ordered) != len(set(ordered)):
            raise ValueError(f"path {path_id!r} contains duplicate candidate sites")
        if not set(ordered) <= site_set:
            raise ValueError(f"path {path_id!r} contains an unknown candidate site")
        weight = weights[path_id]
        if (isinstance(weight, bool) or not isinstance(weight, (int, float))
                or not math.isfinite(weight) or weight < 0):
            raise ValueError(f"path weight for {path_id!r} must be finite and non-negative")
        prepared[path_id] = (set(ordered), float(weight))
    return sites, prepared, p


def _score(selected, prepared):
    chosen = set(selected)
    captured = tuple(
        path_id for path_id, (sites, _weight) in prepared.items()
        if sites & chosen
    )
    value = math.fsum(prepared[path_id][1] for path_id in captured)
    return value, captured


def flow_capturing_exact(paths, weights, candidate_sites, p):
    """Find an optimal p-site FCLM solution by exhaustive enumeration.

    A path is captured when at least one selected site lies on that path.
    Path weights represent flow demand and are counted once, regardless of how
    many selected sites lie on the path. Exactly p sites are returned. Ties are
    resolved by candidate-site input order. This is exponential and intended
    for small instances or as an independent oracle.
    """
    sites, prepared, p = _prepare(paths, weights, candidate_sites, p)
    best_sites = None
    best_value = -1.0
    best_captured = ()
    for selected in combinations(sites, p):
        value, captured = _score(selected, prepared)
        if value > best_value:
            best_sites, best_value, best_captured = selected, value, captured
    return {"sites": tuple(best_sites), "objective": best_value,
            "captured_paths": best_captured}


def flow_capturing_greedy(paths, weights, candidate_sites, p):
    """Greedy maximum-new-flow selection for the monotone submodular FCLM."""
    sites, prepared, p = _prepare(paths, weights, candidate_sites, p)
    selected = []
    captured = set()
    remaining = list(sites)
    for _ in range(p):
        best_site = None
        best_gain = -1.0
        for site in remaining:
            gain = math.fsum(
                weight for path_id, (path_sites, weight) in prepared.items()
                if path_id not in captured and site in path_sites
            )
            if gain > best_gain:
                best_site, best_gain = site, gain
        selected.append(best_site)
        remaining.remove(best_site)
        captured.update(
            path_id for path_id, (path_sites, _weight) in prepared.items()
            if best_site in path_sites
        )
    value, captured_paths = _score(selected, prepared)
    return {"sites": tuple(selected), "objective": value,
            "captured_paths": captured_paths}

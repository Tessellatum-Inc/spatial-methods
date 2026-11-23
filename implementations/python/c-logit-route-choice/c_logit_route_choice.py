"""C-logit route choice with a shared-link commonality factor."""
from __future__ import annotations

import math


def _finite_scalar(value, *, name, minimum=None, strict=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be a finite numeric scalar")
    try:
        result = float(value)
    except (OverflowError, TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a finite numeric scalar") from exc
    if not math.isfinite(result):
        raise ValueError(f"{name} must be finite")
    if minimum is not None and (result <= minimum if strict else result < minimum):
        relation = "greater than" if strict else "at least"
        raise ValueError(f"{name} must be {relation} {minimum}")
    return result


def _routes_and_lengths(routes, segment_lengths):
    if isinstance(routes, (str, bytes)) or not isinstance(routes, (list, tuple)) or not routes:
        raise ValueError("routes must be a non-empty sequence of paths")
    if not isinstance(segment_lengths, dict) or not segment_lengths:
        raise ValueError("segment_lengths must be a non-empty mapping")
    lengths = {}
    for edge, value in segment_lengths.items():
        try:
            hash(edge)
        except TypeError as exc:
            raise ValueError("segment identifiers must be hashable") from exc
        lengths[edge] = _finite_scalar(value, name="segment length", minimum=0, strict=True)
    normalized = []
    for route in routes:
        if isinstance(route, (str, bytes)) or not isinstance(route, (list, tuple)) or not route:
            raise ValueError("each route must be a non-empty sequence of segment identifiers")
        try:
            route_set = set(route)
        except TypeError as exc:
            raise ValueError("segment identifiers must be hashable") from exc
        if len(route_set) != len(route):
            raise ValueError("a route must not repeat a segment identifier")
        missing = route_set - lengths.keys()
        if missing:
            raise ValueError(f"segment lengths are missing identifiers: {sorted(map(str, missing))}")
        normalized.append(tuple(route))
    return normalized, lengths


def c_logit_route_choice(routes, segment_lengths, utilities, *,
                         beta_cf=1.0, gamma=1.0):
    """Return C-logit probabilities using the length-based commonality factor.

    For route k, CF_k = log(sum_j (L_kj / sqrt(L_k L_j))**gamma),
    including j=k. Adjusted utility is V_k - beta_cf * CF_k.
    """
    paths, lengths = _routes_and_lengths(routes, segment_lengths)
    if isinstance(utilities, (str, bytes)) or not isinstance(utilities, (list, tuple)):
        raise ValueError("utilities must be a sequence")
    if len(utilities) != len(paths):
        raise ValueError("one finite utility is required for every route")
    values = [_finite_scalar(value, name="utility") for value in utilities]
    beta = _finite_scalar(beta_cf, name="beta_cf", minimum=0)
    exponent = _finite_scalar(gamma, name="gamma", minimum=0, strict=True)

    route_lengths = [
        math.fsum(lengths[edge] for edge in route) for route in paths
    ]
    shared = []
    commonality = []
    for i, route_i in enumerate(paths):
        row = []
        terms = []
        for j, route_j in enumerate(paths):
            shared_length = math.fsum(
                lengths[edge] for edge in set(route_i).intersection(route_j)
            )
            row.append(shared_length)
            ratio = shared_length / math.sqrt(route_lengths[i] * route_lengths[j])
            terms.append(ratio ** exponent)
        shared.append(tuple(row))
        commonality.append(math.log(math.fsum(terms)))

    adjusted = [
        utility - beta * factor
        for utility, factor in zip(values, commonality)
    ]
    maximum = max(adjusted)
    exponentials = [math.exp(value - maximum) for value in adjusted]
    denominator = math.fsum(exponentials)
    probabilities = [value / denominator for value in exponentials]
    return {
        "probabilities": tuple(probabilities),
        "commonality_factors": tuple(commonality),
        "adjusted_utilities": tuple(adjusted),
        "route_lengths": tuple(route_lengths),
        "shared_lengths": tuple(shared),
    }

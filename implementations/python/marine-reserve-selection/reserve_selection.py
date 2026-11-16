"""Marxan-style simulated-annealing reserve selection reference baseline."""
from __future__ import annotations
import numpy as np


def reserve_objective(selected, feature_matrix, costs, targets, *,
                      adjacency_edges=None, boundary_lengths=None,
                      boundary_modifier=0.0, shortfall_penalty=1000.0):
    """Evaluate acquisition cost, squared target shortfall and boundary cost."""
    chosen = np.asarray(selected, dtype=bool)
    features = np.asarray(feature_matrix, dtype=float)
    c = np.asarray(costs, dtype=float)
    target = np.asarray(targets, dtype=float)
    if features.ndim != 2 or chosen.shape != (features.shape[0],):
        raise ValueError("selected must match the zone dimension of feature_matrix")
    if c.shape != (features.shape[0],) or target.shape != (features.shape[1],):
        raise ValueError("costs and targets must match zones and features")
    if not np.all(np.isfinite(features)) or np.any(features < 0) or not np.all(np.isfinite(c)) or np.any(c < 0) or not np.all(np.isfinite(target)) or np.any(target < 0):
        raise ValueError("features, costs and targets must be finite and non-negative")
    coverage = features[chosen].sum(axis=0)
    shortfall = np.maximum(target-coverage, 0.0)
    boundary = 0.0
    if adjacency_edges is not None:
        edges = np.asarray(adjacency_edges)
        lengths = np.asarray(boundary_lengths, dtype=float)
        if edges.ndim != 2 or edges.shape[1] != 2 or lengths.shape != (len(edges),):
            raise ValueError("adjacency_edges must be (m, 2) and boundary_lengths length m")
        if not np.issubdtype(edges.dtype, np.integer) or np.any(edges < 0) or np.any(edges >= len(chosen)):
            raise ValueError("adjacency edge zone IDs must be valid integers")
        if not np.all(np.isfinite(lengths)) or np.any(lengths < 0):
            raise ValueError("boundary lengths must be finite and non-negative")
        boundary = float(np.sum(lengths[chosen[edges[:, 0]] != chosen[edges[:, 1]]]))
    try:
        bm, penalty = float(boundary_modifier), float(shortfall_penalty)
    except (TypeError, ValueError):
        raise ValueError("objective modifiers must be finite and non-negative") from None
    if not np.isfinite(bm) or bm < 0 or not np.isfinite(penalty) or penalty < 0:
        raise ValueError("objective modifiers must be finite and non-negative")
    acquisition = float(c[chosen].sum())
    return {"objective": acquisition + bm*boundary + penalty*float(shortfall @ shortfall),
            "acquisition_cost": acquisition, "boundary_length": boundary,
            "boundary_cost": bm*boundary, "coverage": coverage,
            "shortfall": shortfall}


def marxan_style_select(feature_matrix, costs, targets, *,
                        adjacency_edges=None, boundary_lengths=None,
                        boundary_modifier=0.0, shortfall_penalty=1000.0,
                        iterations=20000, initial_temperature=None,
                        cooling_rate=0.9995, seed=0):
    """Select zones with single-zone simulated annealing.

    The initial solution contains all zones. The best solution encountered is
    returned. This simplified solver has no separation, connectivity,
    irreplaceability, zone-status or species-specific penalty options.
    """
    features = np.asarray(feature_matrix, dtype=float)
    c = np.asarray(costs, dtype=float)
    target = np.asarray(targets, dtype=float)
    if features.ndim != 2 or features.shape[0] == 0 or features.shape[1] == 0:
        raise ValueError("feature_matrix must be a non-empty zones-by-features matrix")
    n = features.shape[0]
    if c.shape != (n,) or target.shape != (features.shape[1],):
        raise ValueError("costs and targets must match the feature matrix")
    if not np.all(np.isfinite(features)) or np.any(features < 0) or not np.all(np.isfinite(c)) or np.any(c < 0) or not np.all(np.isfinite(target)) or np.any(target < 0):
        raise ValueError("features, costs and targets must be finite and non-negative")
    if isinstance(iterations, (bool, np.bool_)) or not isinstance(iterations, (int, np.integer)) or iterations < 1:
        raise ValueError("iterations must be a positive integer")
    try:
        cooling = float(cooling_rate)
    except (TypeError, ValueError):
        raise ValueError("cooling_rate must be in (0, 1]") from None
    if not np.isfinite(cooling) or not 0 < cooling <= 1:
        raise ValueError("cooling_rate must be in (0, 1]")
    if isinstance(seed, (bool, np.bool_)) or not isinstance(seed, (int, np.integer)):
        raise ValueError("seed must be an integer")
    if initial_temperature is None:
        temperature = max(float(np.max(c)) if c.size else 1.0, 1.0)
    else:
        temperature = float(initial_temperature)
        if not np.isfinite(temperature) or temperature <= 0:
            raise ValueError("initial_temperature must be finite and positive")
    # Validate edge arguments and objective modifiers before the search.
    current = np.ones(n, dtype=bool)
    current_score = reserve_objective(
        current, features, c, target, adjacency_edges=adjacency_edges,
        boundary_lengths=boundary_lengths, boundary_modifier=boundary_modifier,
        shortfall_penalty=shortfall_penalty)
    best = current.copy()
    best_score = current_score
    rng = np.random.default_rng(int(seed))
    for _ in range(int(iterations)):
        candidate = current.copy()
        zone = int(rng.integers(n))
        candidate[zone] = ~candidate[zone]
        score = reserve_objective(
            candidate, features, c, target, adjacency_edges=adjacency_edges,
            boundary_lengths=boundary_lengths, boundary_modifier=boundary_modifier,
            shortfall_penalty=shortfall_penalty)
        delta = score["objective"] - current_score["objective"]
        if delta <= 0 or rng.random() < np.exp(-delta/max(temperature, 1e-15)):
            current, current_score = candidate, score
        if current_score["objective"] < best_score["objective"]:
            best, best_score = current.copy(), current_score
        temperature *= cooling
    return {"selected": best, **best_score,
            "met_all_targets": bool(np.all(best_score["shortfall"] <= 1e-12)),
            "iterations": int(iterations), "seed": int(seed)}

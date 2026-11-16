"""HMM map matching for planar observations and a caller-supplied road-network metric."""
from __future__ import annotations
from dataclasses import dataclass
from math import hypot, isfinite, isnan
from typing import Callable, Hashable, Mapping, Sequence

@dataclass(frozen=True)
class Candidate:
    edge_id: Hashable
    x: float
    y: float
    distance: float

@dataclass(frozen=True)
class Match:
    edge_id: Hashable
    x: float
    y: float
    emission_distance: float
    log_probability: float

def _project(point, a, b):
    px, py = map(float, point); ax, ay = map(float, a); bx, by = map(float, b)
    dx, dy = bx-ax, by-ay; denom = dx*dx + dy*dy
    t = 0.0 if denom == 0 else max(0.0, min(1.0, ((px-ax)*dx+(py-ay)*dy)/denom))
    x, y = ax+t*dx, ay+t*dy
    return x, y, hypot(px-x, py-y)

def generate_candidates(observation, roads: Mapping[Hashable, Sequence[Sequence[float]]],
                        radius: float = 50.0) -> list[Candidate]:
    """Project onto each road polyline and retain its nearest point within radius."""
    if not isfinite(radius) or radius <= 0: raise ValueError("radius must be finite and positive")
    if len(observation) != 2 or not all(isfinite(float(v)) for v in observation):
        raise ValueError("observation must be a finite planar coordinate")
    result = []
    for edge_id, line in roads.items():
        if len(line) < 2: raise ValueError(f"road {edge_id!r} needs at least two coordinates")
        best = None
        for a, b in zip(line, line[1:]):
            x, y, distance = _project(observation, a, b)
            candidate = Candidate(edge_id, x, y, distance)
            if best is None or distance < best.distance: best = candidate
        if best.distance <= radius: result.append(best)
    return sorted(result, key=lambda c: (c.distance, repr(c.edge_id)))

def match_trace(observations: Sequence[Sequence[float]],
                roads: Mapping[Hashable, Sequence[Sequence[float]]],
                network_distance: Callable[[Candidate, Candidate], float], *,
                search_radius: float = 50.0, emission_sigma: float = 10.0,
                transition_beta: float = 20.0) -> list[Match]:
    """Decode the maximum-likelihood road candidate sequence with Viterbi.

    Coordinates and all distances use a projected metric CRS. The callback
    returns legal network distance, or positive infinity for unreachable pairs.
    """
    if not isfinite(emission_sigma) or emission_sigma <= 0: raise ValueError("emission_sigma must be positive")
    if not isfinite(transition_beta) or transition_beta <= 0: raise ValueError("transition_beta must be positive")
    if not observations: return []
    obs = [tuple(map(float, p)) for p in observations]
    if any(len(p) != 2 or not all(isfinite(v) for v in p) for p in obs):
        raise ValueError("observations must be finite planar coordinate pairs")
    layers = [generate_candidates(p, roads, search_radius) for p in obs]
    for k, layer in enumerate(layers):
        if not layer: raise ValueError(f"no road candidate within search_radius at observation {k}")
    emissions = [[-(c.distance**2)/(2*emission_sigma**2) for c in layer] for layer in layers]
    scores = emissions[0][:]
    score_layers = [scores[:]]
    back = []
    for k in range(1, len(layers)):
        displacement = hypot(obs[k][0]-obs[k-1][0], obs[k][1]-obs[k-1][1])
        next_scores, parents = [], []
        for j, current in enumerate(layers[k]):
            best_score, best_parent = float("-inf"), 0
            for i, previous in enumerate(layers[k-1]):
                distance = float(network_distance(previous, current))
                if isnan(distance) or distance < 0:
                    raise ValueError("network distances must be non-negative or positive infinity")
                transition = float("-inf") if not isfinite(distance) else -abs(distance-displacement)/transition_beta
                value = scores[i] + transition + emissions[k][j]
                if value > best_score: best_score, best_parent = value, i
            next_scores.append(best_score); parents.append(best_parent)
        if all(value == float("-inf") for value in next_scores):
            raise ValueError(f"no connected candidate sequence reaches observation {k}")
        scores = next_scores; score_layers.append(scores[:]); back.append(parents)
    index = max(range(len(scores)), key=scores.__getitem__)
    indices = [index]
    for parents in reversed(back): index = parents[index]; indices.append(index)
    indices.reverse()
    return [Match(layers[k][i].edge_id, layers[k][i].x, layers[k][i].y,
                  layers[k][i].distance, score_layers[k][i]) for k, i in enumerate(indices)]

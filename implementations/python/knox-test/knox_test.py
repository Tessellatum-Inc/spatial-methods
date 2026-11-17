"""Knox test for space-time interaction using temporal-label permutations."""
from __future__ import annotations
import numpy as np


def knox_test(coordinates, times, *, spatial_threshold, temporal_threshold,
              permutations=999, random_state=None):
    """Count close-in-space/close-in-time pairs and test against permuted times.

    The one-sided alternative is excess space-time interaction. Coordinates
    and time values must be numeric; threshold units are supplied by caller.
    """
    xy = np.asarray(coordinates, dtype=float)
    t = np.asarray(times, dtype=float)
    if xy.ndim != 2 or xy.shape[0] < 2 or xy.shape[1] == 0 or not np.all(np.isfinite(xy)):
        raise ValueError("coordinates must be a finite N x D array with N >= 2")
    if t.ndim != 1 or t.size != xy.shape[0] or not np.all(np.isfinite(t)):
        raise ValueError("times must be a finite vector matching coordinate rows")
    if not np.isfinite(spatial_threshold) or spatial_threshold <= 0:
        raise ValueError("spatial_threshold must be finite and positive")
    if not np.isfinite(temporal_threshold) or temporal_threshold <= 0:
        raise ValueError("temporal_threshold must be finite and positive")
    if not isinstance(permutations, int) or isinstance(permutations, bool) or permutations < 1:
        raise ValueError("permutations must be a positive integer")
    i, j = np.triu_indices(len(t), k=1)
    spatial_close = np.linalg.norm(xy[i] - xy[j], axis=1) <= spatial_threshold
    def count_for(candidate_times):
        temporal_close = np.abs(candidate_times[i] - candidate_times[j]) <= temporal_threshold
        return int(np.count_nonzero(spatial_close & temporal_close))
    observed = count_for(t)
    rng = np.random.default_rng(random_state)
    simulated = np.empty(permutations, dtype=np.int64)
    for b in range(permutations):
        simulated[b] = count_for(rng.permutation(t))
    p_value = (1 + int(np.count_nonzero(simulated >= observed))) / (permutations + 1)
    sd = float(np.std(simulated, ddof=1)) if permutations > 1 else np.nan
    z_score = (observed - float(np.mean(simulated))) / sd if sd > 0 else np.nan
    return {"observed_pairs": observed, "null_counts": simulated,
            "null_mean": float(np.mean(simulated)), "null_sd": sd,
            "z_score": float(z_score), "p_value": float(p_value),
            "spatial_close_pairs": int(np.count_nonzero(spatial_close))}

"""Transparent deterministic and probabilistic forecast verification baselines."""
from __future__ import annotations
from math import isfinite

def _same_length(a, b):
    if len(a) == 0 or len(a) != len(b):
        raise ValueError("inputs must have the same non-zero length")

def contingency_scores(forecast, observed, threshold):
    """Return hits, misses, false alarms, correct negatives and common scores."""
    _same_length(forecast, observed)
    if not isfinite(float(threshold)):
        raise ValueError("threshold must be finite")
    f = [float(v) for v in forecast]; o = [float(v) for v in observed]
    if any(not isfinite(v) for v in f + o):
        raise ValueError("inputs must be finite")
    hits = misses = false_alarms = correct_negatives = 0
    for fv, ov in zip(f, o):
        fe, oe = fv >= threshold, ov >= threshold
        if fe and oe: hits += 1
        elif oe: misses += 1
        elif fe: false_alarms += 1
        else: correct_negatives += 1
    total = hits + misses + false_alarms + correct_negatives
    pod = hits / (hits + misses) if hits + misses else None
    far = false_alarms / (hits + false_alarms) if hits + false_alarms else None
    csi = hits / (hits + misses + false_alarms) if hits + misses + false_alarms else None
    random_hits = ((hits + misses) * (hits + false_alarms) / total) if total else 0.0
    ets_den = hits + misses + false_alarms - random_hits
    ets = (hits - random_hits) / ets_den if ets_den else None
    return {"hits": hits, "misses": misses, "false_alarms": false_alarms,
            "correct_negatives": correct_negatives, "pod": pod, "far": far,
            "csi": csi, "ets": ets}

def brier_score(probabilities, outcomes):
    """Mean squared probability error for binary outcomes."""
    _same_length(probabilities, outcomes)
    p = [float(v) for v in probabilities]; y = [float(v) for v in outcomes]
    if any(not isfinite(v) or v < 0 or v > 1 for v in p):
        raise ValueError("probabilities must be finite and in [0, 1]")
    if any(not isfinite(v) or v not in (0.0, 1.0) for v in y):
        raise ValueError("outcomes must be finite binary values")
    return sum((a-b)**2 for a,b in zip(p,y)) / len(p)

def roc_auc(scores, outcomes):
    """Rank-based ROC AUC with average ranks for tied scores."""
    _same_length(scores, outcomes)
    pairs = sorted((float(s), float(y)) for s,y in zip(scores,outcomes))
    if any(not isfinite(s) for s,_ in pairs) or any(y not in (0.0,1.0) for _,y in pairs):
        raise ValueError("scores must be finite and outcomes binary")
    positives = sum(y == 1 for _,y in pairs); negatives = len(pairs)-positives
    if not positives or not negatives:
        raise ValueError("ROC AUC requires both outcome classes")
    rank_sum = 0.0; i = 0
    while i < len(pairs):
        j = i + 1
        while j < len(pairs) and pairs[j][0] == pairs[i][0]: j += 1
        average_rank = ((i+1) + j) / 2.0
        rank_sum += average_rank * sum(y == 1 for _,y in pairs[i:j])
        i = j
    return (rank_sum - positives*(positives+1)/2) / (positives*negatives)

def _grid(values):
    rows = [list(map(float, row)) for row in values]
    if not rows or not rows[0] or any(len(row) != len(rows[0]) for row in rows):
        raise ValueError("grid must be a non-empty rectangular 2D sequence")
    if any(not isfinite(v) for row in rows for v in row):
        raise ValueError("grid values must be finite")
    return rows

def fractions_skill_score(forecast, observed, threshold, radius=1):
    """Square-neighborhood FSS; edge neighborhoods are clipped to the domain.

    radius=0 is gridpoint verification. Both fields are thresholded with >=.
    This function assumes fields are already registered on the same grid.
    """
    f = _grid(forecast); o = _grid(observed)
    if len(f) != len(o) or len(f[0]) != len(o[0]):
        raise ValueError("forecast and observed grids must have identical shapes")
    if isinstance(radius, bool) or not isinstance(radius, int) or radius < 0:
        raise ValueError("radius must be a non-negative integer")
    if not isfinite(float(threshold)):
        raise ValueError("threshold must be finite")
    rows, cols = len(f), len(f[0])
    ff = [[1.0 if v >= threshold else 0.0 for v in row] for row in f]
    oo = [[1.0 if v >= threshold else 0.0 for v in row] for row in o]
    fbs = worst = 0.0
    for i in range(rows):
        for j in range(cols):
            fvals = [ff[a][b] for a in range(max(0,i-radius), min(rows,i+radius+1))
                     for b in range(max(0,j-radius), min(cols,j+radius+1))]
            ovals = [oo[a][b] for a in range(max(0,i-radius), min(rows,i+radius+1))
                     for b in range(max(0,j-radius), min(cols,j+radius+1))]
            fp = sum(fvals)/len(fvals); op = sum(ovals)/len(ovals)
            fbs += (fp-op)**2
            worst += fp*fp + op*op
    if worst == 0:
        return 1.0 if fbs == 0 else None
    return 1.0 - fbs/worst

def crps_ensemble(ensemble, observation):
    """Empirical-distribution CRPS for a finite ensemble.

    CRPS = mean(|x_m-y|) - (1/(2 M^2)) sum_{m,n}|x_m-x_n|.
    """
    members = [float(v) for v in ensemble]
    y = float(observation)
    if not members or not isfinite(y) or any(not isfinite(v) for v in members):
        raise ValueError("ensemble and observation must be finite and ensemble non-empty")
    first = sum(abs(v-y) for v in members) / len(members)
    pairwise = sum(abs(a-b) for a in members for b in members) / (2 * len(members)**2)
    return first - pairwise

def rank_histogram(ensembles, observations):
    """Expected ensemble rank counts with ties fractionally shared.

    Returns M+1 bins for M-member ensembles. Each case contributes one total
    count; if the observation ties k members, its mass is shared equally over
    the k+1 ranks spanned by that tie.
    """
    _same_length(ensembles, observations)
    member_count = len(ensembles[0])
    if member_count < 1 or any(len(e) != member_count for e in ensembles):
        raise ValueError("all ensembles must have the same positive member count")
    counts = [0.0] * (member_count + 1)
    for ensemble, observation in zip(ensembles, observations):
        members = [float(v) for v in ensemble]
        y = float(observation)
        if not isfinite(y) or any(not isfinite(v) for v in members):
            raise ValueError("ensemble members and observations must be finite")
        lower = sum(v < y for v in members)
        ties = sum(v == y for v in members)
        mass = 1.0 / (ties + 1)
        for rank in range(lower, lower + ties + 1):
            counts[rank] += mass
    return counts

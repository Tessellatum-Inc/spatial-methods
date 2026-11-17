"""Monte Carlo uncertainty propagation, Sobol indices and positional RMSE."""
import math
import random


def _bounds(bounds):
    if not bounds:
        raise ValueError("bounds must not be empty")
    result = []
    for pair in bounds:
        if len(pair) != 2:
            raise ValueError("each bound must be (lower, upper)")
        lo, hi = map(float, pair)
        if not math.isfinite(lo) or not math.isfinite(hi) or lo >= hi:
            raise ValueError("bounds must be finite with lower < upper")
        result.append((lo, hi))
    return result


def _size(n):
    if isinstance(n, bool) or not isinstance(n, int) or n < 2:
        raise ValueError("n must be an integer >= 2")


def _evaluate(model, rows):
    out = [float(model(row)) for row in rows]
    if any(not math.isfinite(x) for x in out):
        raise ValueError("model outputs must be finite scalars")
    return out


def _sample(bounds, n, rng):
    return [[lo + rng.random()*(hi-lo) for lo, hi in bounds] for _ in range(n)]


def positional_rmse(reference, estimated):
    """Return per-axis bias/RMSE and pooled coordinate RMSE."""
    a, b = [list(map(float, row)) for row in reference], [list(map(float, row)) for row in estimated]
    if not a or len(a) != len(b) or len(a[0]) < 1:
        raise ValueError("coordinate arrays must have equal non-zero shape")
    d = len(a[0])
    if any(len(row) != d for row in a+b) or any(not math.isfinite(x) for row in a+b for x in row):
        raise ValueError("coordinates must be finite with consistent dimensions")
    errors = [[y-x for x,y in zip(ar,br)] for ar,br in zip(a,b)]
    bias = [sum(row[j] for row in errors)/len(errors) for j in range(d)]
    axis_rmse = [math.sqrt(sum(row[j]**2 for row in errors)/len(errors)) for j in range(d)]
    pooled = math.sqrt(sum(x*x for row in errors for x in row)/(len(errors)*d))
    return {"n":len(a), "dimension":d, "bias":bias, "axis_rmse":axis_rmse, "pooled_rmse":pooled}


def monte_carlo_uniform(model, bounds, n, seed=None):
    """Propagate independent uniform inputs; report samples and scalar summaries."""
    domain = _bounds(bounds)
    _size(n)
    rows = _sample(domain, n, random.Random(seed))
    outputs = _evaluate(model, rows)
    ordered = sorted(outputs)
    mean = sum(outputs)/n
    variance = sum((x-mean)**2 for x in outputs)/(n-1)
    def quantile(p):
        pos = (n-1)*p
        lo, hi = int(pos), math.ceil(pos)
        return ordered[lo] + (ordered[hi]-ordered[lo])*(pos-lo)
    return {"samples":outputs, "mean":mean, "variance":variance,
            "standard_deviation":math.sqrt(variance),
            "quantiles":{str(p):quantile(p) for p in (0.025,0.5,0.975)}}


def sobol_first_total(model, bounds, n, seed=None):
    """Estimate first-order and total Sobol indices using Saltelli pick-freeze.

    Independent uniform inputs are assumed. Returns first-order S1 and total
    ST indices; estimates can be noisy and may fall slightly outside [0,1].
    """
    domain = _bounds(bounds)
    _size(n)
    rng = random.Random(seed)
    a, b = _sample(domain,n,rng), _sample(domain,n,rng)
    ya, yb = _evaluate(model,a), _evaluate(model,b)
    mean = sum(ya+yb)/(2*n)
    variance = sum((x-mean)**2 for x in ya+yb)/(2*n-1)
    if variance <= 0:
        raise ValueError("model output variance must be positive")
    first, total = [], []
    for j in range(len(domain)):
        ab = [row.copy() for row in a]
        for i in range(n):
            ab[i][j] = b[i][j]
        yab = _evaluate(model,ab)
        first.append(sum(yb[i]*(yab[i]-ya[i]) for i in range(n))/(n*variance))
        total.append(sum((ya[i]-yab[i])**2 for i in range(n))/(2*n*variance))
    return {"first_order":first,"total_order":total,"output_variance":variance,"n":n}

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


def _matrix(values, name):
    try:
        rows = [list(map(float, row)) for row in values]
    except (TypeError, ValueError):
        raise ValueError(f"{name} must be a non-empty rectangular numeric matrix") from None
    if not rows or not rows[0] or any(len(row) != len(rows[0]) for row in rows):
        raise ValueError(f"{name} must be a non-empty rectangular numeric matrix")
    if any(not math.isfinite(x) for row in rows for x in row):
        raise ValueError(f"{name} must contain only finite values")
    return rows


def _minimum_symmetric_eigenvalue(matrix):
    """Jacobi eigenvalue iteration for a small real symmetric matrix."""
    a = [row[:] for row in matrix]
    n = len(a)
    if n == 1:
        return a[0][0]
    scale = max(1.0, max(abs(x) for row in a for x in row))
    threshold = 1e-14 * scale
    for _ in range(50 * n * n):
        p, q, largest = 0, 1, 0.0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(a[i][j]) > largest:
                    p, q, largest = i, j, abs(a[i][j])
        if largest <= threshold:
            return min(a[i][i] for i in range(n))
        app, aqq, apq = a[p][p], a[q][q], a[p][q]
        tau = (aqq - app) / (2.0 * apq)
        t = math.copysign(1.0, tau) / (abs(tau) + math.sqrt(1.0 + tau*tau))
        c = 1.0 / math.sqrt(1.0 + t*t)
        s = t*c
        a[p][p] = app - t*apq
        a[q][q] = aqq + t*apq
        a[p][q] = a[q][p] = 0.0
        for k in range(n):
            if k not in (p, q):
                akp, akq = a[k][p], a[k][q]
                a[k][p] = a[p][k] = c*akp - s*akq
                a[k][q] = a[q][k] = s*akp + c*akq
    raise ValueError("covariance PSD check did not converge")


def covariance_propagation(jacobian, covariance, tolerance=1e-10):
    """Propagate a joint input covariance through a supplied Jacobian.

    jacobian has shape (n_outputs, n_inputs); covariance has shape
    (n_inputs, n_inputs). Returns J C J^T and marginal standard uncertainties.
    The first-order approximation assumes the Jacobian is evaluated at a
    suitable expansion point. No distributional or nonlinear effects are
    estimated by this function.
    """
    j = _matrix(jacobian, "jacobian")
    c = _matrix(covariance, "covariance")
    n = len(j[0])
    if len(c) != n or any(len(row) != n for row in c):
        raise ValueError("covariance shape must match the Jacobian input dimension")
    try:
        tolerance = float(tolerance)
    except (TypeError, ValueError):
        raise ValueError("tolerance must be finite and non-negative") from None
    if not math.isfinite(tolerance) or tolerance < 0:
        raise ValueError("tolerance must be finite and non-negative")
    scale = max(1.0, max(abs(x) for row in c for x in row))
    symmetry_tol = tolerance * scale
    for i in range(n):
        for k in range(n):
            if abs(c[i][k] - c[k][i]) > symmetry_tol:
                raise ValueError("covariance must be symmetric")
    c = [[0.5*(c[i][k] + c[k][i]) for k in range(n)] for i in range(n)]
    if _minimum_symmetric_eigenvalue(c) < -symmetry_tol:
        raise ValueError("covariance must be positive semidefinite")
    b = [[sum(j[r][k]*c[k][m] for k in range(n)) for m in range(n)]
         for r in range(len(j))]
    out = [[sum(b[r][k]*j[s][k] for k in range(n))
            for s in range(len(j))] for r in range(len(j))]
    out = [[0.5*(out[r][s] + out[s][r]) for s in range(len(j))]
           for r in range(len(j))]
    diagonal = [out[i][i] for i in range(len(out))]
    if any(x < -symmetry_tol for x in diagonal):
        raise ArithmeticError("propagated covariance has a materially negative variance")
    standard = [math.sqrt(max(0.0, x)) for x in diagonal]
    return {"covariance": out, "standard_uncertainties": standard}

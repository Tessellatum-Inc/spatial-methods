"""Exact-constraint GLS for full-rank stochastic models with datum defects.

Observation covariance must be symmetric positive definite. Exact constraints
must remove all parameter-space rank defects. Singular observation covariance
is a separate problem and is not handled here.
"""
from __future__ import annotations

from covariance_gls import (
    _matrix, _square, cholesky, matmul, matvec, transpose,
    solve_lower, solve_upper_from_lower,
)


def _solve(a, b, *, tolerance=1e-12):
    """Solve a general square system with partial pivoting."""
    a = [row[:] for row in _square(a, "system matrix")]
    b = [float(v) for v in b]
    n = len(a)
    if len(b) != n:
        raise ValueError("right-hand side length does not match system")
    scale = max(1.0, max(abs(v) for row in a for v in row))
    for k in range(n):
        pivot = max(range(k, n), key=lambda i: abs(a[i][k]))
        if abs(a[pivot][k]) <= tolerance * scale:
            raise ValueError("constrained normal system is singular; constraints may not remove all datum defects")
        a[k], a[pivot] = a[pivot], a[k]
        b[k], b[pivot] = b[pivot], b[k]
        for i in range(k + 1, n):
            factor = a[i][k] / a[k][k]
            for j in range(k, n):
                a[i][j] -= factor * a[k][j]
            b[i] -= factor * b[k]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(a[i][j] * x[j] for j in range(i + 1, n))) / a[i][i]
    return x


def _inverse(a):
    a = _square(a, "matrix")
    n = len(a)
    columns = [_solve(a, [1.0 if i == j else 0.0 for i in range(n)])
               for j in range(n)]
    return [[columns[j][i] for j in range(n)] for i in range(n)]


def constrained_gls(a, y, q, c, d):
    """Solve min (y-Ax)'Q^-1(y-Ax), subject to Cx=d.

    Returns (estimate, constrained_parameter_covariance, residuals,
    lagrange_multipliers). Q must be SPD; C must remove every datum defect.
    The covariance is the upper-left block of the inverse KKT matrix, for
    fixed Q and exact constraints. No variance-factor scaling is applied.
    """
    a = _matrix(a, "design matrix")
    q = _square(q, "observation covariance")
    c = _matrix(c, "constraint matrix")
    y = [float(v) for v in y]
    d = [float(v) for v in d]
    m, n = len(a), len(a[0])
    k = len(c)
    if len(y) != m or len(q) != m or len(c[0]) != n or len(d) != k:
        raise ValueError("observation, design, covariance or constraint dimensions differ")
    if k == 0:
        raise ValueError("at least one exact constraint is required")
    lq = cholesky(q)
    aw = transpose([solve_lower(lq, [a[i][j] for i in range(m)])
                    for j in range(n)])
    yw = solve_lower(lq, y)
    at = transpose(aw)
    normal = matmul(at, aw)
    rhs = matvec(at, yw)
    ct = transpose(c)
    zero = [[0.0] * k for _ in range(k)]
    kkt = [normal[i] + ct[i] for i in range(n)]
    kkt.extend([c[i] + zero[i] for i in range(k)])
    solution = _solve(kkt, rhs + d)
    estimate, multipliers = solution[:n], solution[n:]
    kkt_inverse = _inverse(kkt)
    covariance = [row[:n] for row in kkt_inverse[:n]]
    fitted = matvec(a, estimate)
    residuals = [y[i] - fitted[i] for i in range(m)]
    return estimate, covariance, residuals, multipliers

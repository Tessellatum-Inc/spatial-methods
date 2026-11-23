"""Small dependency-free covariance and generalized least-squares utilities.

The GLS solver requires a symmetric positive-definite observation covariance
matrix and a full-column-rank design matrix. Covariance validation accepts
positive-semidefinite matrices, including singular ones; the GLS solver does
not silently regularize or invert singular covariance matrices.
"""
from __future__ import annotations

import math


def _matrix(a, name="matrix"):
    if not a or not isinstance(a, (list, tuple)):
        raise ValueError(f"{name} must be a non-empty matrix")
    width = len(a[0])
    if width == 0 or any(len(row) != width for row in a):
        raise ValueError(f"{name} must be rectangular and non-empty")
    out = []
    for row in a:
        values = [float(v) for v in row]
        if not all(math.isfinite(v) for v in values):
            raise ValueError(f"{name} must contain only finite values")
        out.append(values)
    return out


def transpose(a):
    a = _matrix(a)
    return [list(col) for col in zip(*a)]


def matmul(a, b):
    a, b = _matrix(a, "left matrix"), _matrix(b, "right matrix")
    if len(a[0]) != len(b):
        raise ValueError("matrix dimensions do not conform for multiplication")
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def matvec(a, x):
    a = _matrix(a)
    if len(a[0]) != len(x):
        raise ValueError("matrix and vector dimensions do not conform")
    return [sum(v * float(w) for v, w in zip(row, x)) for row in a]


def _square(a, name):
    a = _matrix(a, name)
    if len(a) != len(a[0]):
        raise ValueError(f"{name} must be square")
    return a


def validate_covariance(q, *, atol=1e-12):
    """Validate symmetry and positive semidefiniteness.

    Uses Jacobi rotations to estimate eigenvalues of a real symmetric matrix.
    Tolerance is absolute and should be chosen consistently with matrix units
    and scale. Returns diagnostics; does not require positive definiteness.
    """
    q = _square(q, "covariance")
    n = len(q)
    scale = max(1.0, max(abs(v) for row in q for v in row))
    tol = atol * scale
    for i in range(n):
        for j in range(i):
            if abs(q[i][j] - q[j][i]) > tol:
                raise ValueError("covariance matrix must be symmetric")
    a = [[0.5 * (q[i][j] + q[j][i]) for j in range(n)] for i in range(n)]
    # Jacobi eigenvalue iteration for a real symmetric matrix.
    for _ in range(max(1, 50 * n * n)):
        p, r, largest = 0, 0, 0.0
        for i in range(n):
            for j in range(i + 1, n):
                if abs(a[i][j]) > largest:
                    p, r, largest = i, j, abs(a[i][j])
        if largest <= tol:
            break
        app, arr, apr = a[p][p], a[r][r], a[p][r]
        angle = 0.5 * math.atan2(2.0 * apr, arr - app)
        c, s = math.cos(angle), math.sin(angle)
        for k in range(n):
            if k not in (p, r):
                akp, akr = a[k][p], a[k][r]
                a[k][p] = a[p][k] = c * akp - s * akr
                a[k][r] = a[r][k] = s * akp + c * akr
        a[p][p] = c*c*app - 2*s*c*apr + s*s*arr
        a[r][r] = s*s*app + 2*s*c*apr + c*c*arr
        a[p][r] = a[r][p] = 0.0
    eigenvalues = [a[i][i] for i in range(n)]
    if min(eigenvalues) < -tol:
        raise ValueError(
            f"covariance matrix is not positive semidefinite "
            f"(minimum eigenvalue {min(eigenvalues):.6g})"
        )
    return {"dimension": n, "minimum_eigenvalue": min(eigenvalues),
            "tolerance": tol, "positive_semidefinite": True}


def session_common_covariance(standard_uncertainties, session_ids, tau):
    """Return D + tau^2 Z Z^T in squared units.

    standard_uncertainties and tau must use the same units. Distinct sessions
    have independent common effects in this model.
    """
    sigmas = [float(v) for v in standard_uncertainties]
    if not sigmas or len(sigmas) != len(session_ids):
        raise ValueError("uncertainties and session IDs must have equal non-zero length")
    if any(not math.isfinite(v) or v < 0 for v in sigmas):
        raise ValueError("standard uncertainties must be finite and non-negative")
    tau = float(tau)
    if not math.isfinite(tau) or tau < 0:
        raise ValueError("tau must be finite and non-negative")
    q = []
    for i, si in enumerate(sigmas):
        row = []
        for j, sj in enumerate(sigmas):
            value = (tau * tau if session_ids[i] == session_ids[j] else 0.0)
            if i == j:
                value += si * si
            row.append(value)
        q.append(row)
    validate_covariance(q)
    return q


def diagonal_covariance(q):
    q = _square(q, "covariance")
    return [[q[i][j] if i == j else 0.0 for j in range(len(q))]
            for i in range(len(q))]


def cholesky(q, *, tolerance=1e-14):
    """Lower-triangular Cholesky factor; requires positive definiteness."""
    q = _square(q, "matrix")
    validate_covariance(q)
    n = len(q)
    scale = max(1.0, max(abs(v) for row in q for v in row))
    l = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1):
            value = q[i][j] - sum(l[i][k] * l[j][k] for k in range(j))
            if i == j:
                if value <= tolerance * scale:
                    raise ValueError(
                        "matrix must be positive definite for Cholesky GLS; "
                        "singular or near-singular covariance requires a "
                        "specialized constrained/generalized-inverse method"
                    )
                l[i][j] = math.sqrt(value)
            else:
                l[i][j] = value / l[j][j]
    return l


def solve_lower(l, b):
    l = _square(l, "lower factor")
    if len(b) != len(l):
        raise ValueError("right-hand side length does not match factor")
    x = []
    for i in range(len(l)):
        if abs(l[i][i]) == 0:
            raise ValueError("singular triangular factor")
        x.append((float(b[i]) - sum(l[i][j] * x[j] for j in range(i))) / l[i][i])
    return x


def solve_upper_from_lower(l, b):
    l = _square(l, "lower factor")
    if len(b) != len(l):
        raise ValueError("right-hand side length does not match factor")
    x = [0.0] * len(l)
    for i in range(len(l) - 1, -1, -1):
        if abs(l[i][i]) == 0:
            raise ValueError("singular triangular factor")
        x[i] = (float(b[i]) - sum(l[j][i] * x[j] for j in range(i + 1, len(l)))) / l[i][i]
    return x


def cholesky_solve(l, b):
    return solve_upper_from_lower(l, solve_lower(l, b))


def inverse_spd(q):
    """Inverse of an SPD matrix via Cholesky solves (small problems only)."""
    l = cholesky(q)
    n = len(l)
    columns = [cholesky_solve(l, [1.0 if i == j else 0.0 for i in range(n)])
               for j in range(n)]
    return [[columns[j][i] for j in range(n)] for i in range(n)]


def generalized_least_squares(a, y, q):
    """Solve full-rank linear GLS using SPD observation covariance Q.

    Returns estimate, formal covariance, and residual vector. Covariance is
    known/fixed; no variance-factor rescaling or robust estimation is applied.
    """
    a = _matrix(a, "design matrix")
    q = _square(q, "observation covariance")
    y = [float(v) for v in y]
    if len(a) != len(y) or len(q) != len(y):
        raise ValueError("observation, design and covariance dimensions differ")
    if len(a) < len(a[0]):
        raise ValueError("design matrix cannot have full column rank")
    lq = cholesky(q)
    # Whiten by solving L z = vector where Q = L L^T.
    aw = [solve_lower(lq, [a[i][j] for i in range(len(a))])
          for j in range(len(a[0]))]
    aw = transpose(aw)
    yw = solve_lower(lq, y)
    at = transpose(aw)
    normal = matmul(at, aw)
    ln = cholesky(normal)
    rhs = matvec(at, yw)
    estimate = cholesky_solve(ln, rhs)
    # Covariance of estimate = (A_w^T A_w)^-1.
    columns = [cholesky_solve(ln, [1.0 if i == j else 0.0
                                  for i in range(len(ln))])
               for j in range(len(ln))]
    parameter_covariance = [[columns[j][i] for j in range(len(columns))]
                            for i in range(len(columns))]
    residuals = [y[i] - matvec(a, estimate)[i] for i in range(len(y))]
    return estimate, parameter_covariance, residuals

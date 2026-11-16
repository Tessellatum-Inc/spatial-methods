"""Stochastic Lanczos quadrature for symmetric positive-definite log determinants."""
from __future__ import annotations
import numpy as np
from scipy import sparse


def stochastic_lanczos_logdet(matrix, *, n_probes=20, lanczos_steps=30,
                              random_state=None, reorthogonalize=True):
    """Estimate log(det(A)) with Rademacher probes and Lanczos quadrature."""
    if sparse.issparse(matrix):
        shape = matrix.shape
        if len(shape) != 2 or shape[0] != shape[1] or shape[0] == 0:
            raise ValueError("matrix must be non-empty and square")
        if not np.all(np.isfinite(matrix.data)):
            raise ValueError("matrix entries must be finite")
        difference = matrix - matrix.T
        if difference.nnz and np.max(np.abs(difference.data)) > 1e-10:
            raise ValueError("matrix must be symmetric")
        matvec = lambda vector: np.asarray(matrix @ vector, dtype=float).reshape(-1)
        dimension = int(shape[0])
    else:
        values = np.asarray(matrix, dtype=float)
        if values.ndim != 2 or values.shape[0] != values.shape[1] or values.shape[0] == 0:
            raise ValueError("matrix must be non-empty and square")
        if not np.all(np.isfinite(values)):
            raise ValueError("matrix entries must be finite")
        if not np.allclose(values, values.T, atol=1e-10, rtol=1e-10):
            raise ValueError("matrix must be symmetric")
        matvec = lambda vector: values @ vector
        dimension = int(values.shape[0])
    if isinstance(n_probes, (bool, np.bool_)) or not isinstance(n_probes, (int, np.integer)) or n_probes < 1:
        raise ValueError("n_probes must be a positive integer")
    if isinstance(lanczos_steps, (bool, np.bool_)) or not isinstance(lanczos_steps, (int, np.integer)) or lanczos_steps < 1:
        raise ValueError("lanczos_steps must be a positive integer")
    if not isinstance(reorthogonalize, (bool, np.bool_)):
        raise ValueError("reorthogonalize must be boolean")

    steps = min(int(lanczos_steps), dimension)
    rng = np.random.default_rng(random_state)
    estimates = np.empty(int(n_probes), dtype=float)
    used_steps = np.empty(int(n_probes), dtype=int)
    for probe in range(int(n_probes)):
        z = rng.choice(np.array([-1.0, 1.0]), size=dimension)
        norm_z = float(np.linalg.norm(z))
        q = z / norm_z
        q_previous = np.zeros(dimension, dtype=float)
        beta_previous = 0.0
        basis, diagonal, off_diagonal = [], [], []
        for _ in range(steps):
            basis.append(q.copy())
            product = matvec(q)
            residual = product - beta_previous * q_previous
            alpha = float(q @ residual)
            residual = residual - alpha * q
            if reorthogonalize:
                for _pass in range(2):
                    for vector in basis:
                        residual -= vector * float(vector @ residual)
            beta = float(np.linalg.norm(residual))
            diagonal.append(alpha)
            scale = max(1.0, abs(alpha), float(np.linalg.norm(product)))
            if beta <= np.finfo(float).eps * scale:
                break
            off_diagonal.append(beta)
            q_previous, q = q, residual / beta
            beta_previous = beta
        k = len(diagonal)
        tridiagonal = np.diag(diagonal)
        if k > 1:
            off = np.asarray(off_diagonal[:k-1], dtype=float)
            tridiagonal += np.diag(off, 1) + np.diag(off, -1)
        eigenvalues, eigenvectors = np.linalg.eigh(tridiagonal)
        if np.any(eigenvalues <= 0):
            raise ValueError("matrix must be positive definite")
        estimates[probe] = norm_z**2 * float(
            np.sum(eigenvectors[0]**2 * np.log(eigenvalues)))
        used_steps[probe] = k
    standard_error = (float(np.std(estimates, ddof=1) / np.sqrt(len(estimates)))
                      if len(estimates) > 1 else 0.0)
    return {"estimate": float(np.mean(estimates)),
            "standard_error": standard_error,
            "probe_estimates": estimates,
            "lanczos_steps_used": used_steps}


def chebyshev_logdet(matrix, *, spectral_bounds, degree=100, n_probes=20,
                     random_state=None, quadrature_order=None):
    """Estimate log(det(A)) with Chebyshev polynomial trace approximation.

    The caller supplies conservative positive spectral bounds (lower, upper).
    Chebyshev coefficients approximate log(lambda) on that interval; Rademacher
    probes estimate the trace. Dense NumPy and SciPy sparse matrices are
    supported. Bounds are not inferred because doing so exactly can defeat
    the purpose of a large-matrix approximation.
    """
    if sparse.issparse(matrix):
        shape = matrix.shape
        if len(shape) != 2 or shape[0] != shape[1] or shape[0] == 0:
            raise ValueError("matrix must be non-empty and square")
        if not np.all(np.isfinite(matrix.data)):
            raise ValueError("matrix entries must be finite")
        difference = matrix - matrix.T
        if difference.nnz and np.max(np.abs(difference.data)) > 1e-10:
            raise ValueError("matrix must be symmetric")
        matvec = lambda vector: np.asarray(matrix @ vector, dtype=float).reshape(-1)
        dimension = int(shape[0])
    else:
        values = np.asarray(matrix, dtype=float)
        if values.ndim != 2 or values.shape[0] != values.shape[1] or values.shape[0] == 0:
            raise ValueError("matrix must be non-empty and square")
        if not np.all(np.isfinite(values)):
            raise ValueError("matrix entries must be finite")
        if not np.allclose(values, values.T, atol=1e-10, rtol=1e-10):
            raise ValueError("matrix must be symmetric")
        matvec = lambda vector: values @ vector
        dimension = int(values.shape[0])
    try:
        lower, upper = map(float, spectral_bounds)
    except (TypeError, ValueError):
        raise ValueError("spectral_bounds must contain two finite positive bounds") from None
    if not np.isfinite(lower) or not np.isfinite(upper) or lower <= 0 or upper <= lower:
        raise ValueError("spectral_bounds must satisfy 0 < lower < upper")
    if isinstance(degree, (bool, np.bool_)) or not isinstance(degree, (int, np.integer)) or degree < 1:
        raise ValueError("degree must be a positive integer")
    if isinstance(n_probes, (bool, np.bool_)) or not isinstance(n_probes, (int, np.integer)) or n_probes < 1:
        raise ValueError("n_probes must be a positive integer")
    if quadrature_order is None:
        quadrature_order = max(256, 2 * (int(degree) + 1))
    if isinstance(quadrature_order, (bool, np.bool_)) or not isinstance(quadrature_order, (int, np.integer)) or quadrature_order < degree + 1:
        raise ValueError("quadrature_order must be an integer at least degree + 1")

    nodes = np.arange(int(quadrature_order), dtype=float)
    angles = np.pi * (nodes + 0.5) / int(quadrature_order)
    scaled_nodes = np.cos(angles)
    eigenvalue_nodes = 0.5 * (upper + lower) + 0.5 * (upper - lower) * scaled_nodes
    function_values = np.log(eigenvalue_nodes)
    coefficients = np.array([
        (2.0 / int(quadrature_order)) *
        np.sum(function_values * np.cos(k * angles))
        for k in range(int(degree) + 1)
    ])
    midpoint, half_width = 0.5 * (upper + lower), 0.5 * (upper - lower)

    def scaled_matvec(vector):
        return (2.0 * matvec(vector) - 2.0 * midpoint * vector) / (2.0 * half_width)

    rng = np.random.default_rng(random_state)
    estimates = np.empty(int(n_probes), dtype=float)
    for probe in range(int(n_probes)):
        z = rng.choice(np.array([-1.0, 1.0]), size=dimension)
        previous = z.copy()
        approximation = 0.5 * coefficients[0] * previous
        current = scaled_matvec(z)
        approximation += coefficients[1] * current
        for k in range(2, int(degree) + 1):
            following = 2.0 * scaled_matvec(current) - previous
            approximation += coefficients[k] * following
            previous, current = current, following
        estimates[probe] = float(z @ approximation)
    standard_error = (float(np.std(estimates, ddof=1) / np.sqrt(len(estimates)))
                      if len(estimates) > 1 else 0.0)
    return {"estimate": float(np.mean(estimates)),
            "standard_error": standard_error,
            "probe_estimates": estimates,
            "coefficients": coefficients,
            "spectral_bounds": (lower, upper)}

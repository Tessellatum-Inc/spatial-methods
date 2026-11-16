"""Conjugate-gradient and matrix-free Kronecker linear algebra kernels."""
from __future__ import annotations
import numpy as np
from scipy import sparse


def _matrix_operator(matrix):
    if sparse.issparse(matrix):
        shape = matrix.shape
        if len(shape) != 2 or shape[0] != shape[1] or shape[0] == 0:
            raise ValueError("matrix must be non-empty and square")
        if not np.all(np.isfinite(matrix.data)):
            raise ValueError("matrix entries must be finite")
        difference = matrix - matrix.T
        if difference.nnz and np.max(np.abs(difference.data)) > 1e-10:
            raise ValueError("matrix must be symmetric")
        return int(shape[0]), lambda vector: np.asarray(matrix @ vector).reshape(-1), np.asarray(matrix.diagonal(), dtype=float)
    values = np.asarray(matrix, dtype=float)
    if values.ndim != 2 or values.shape[0] != values.shape[1] or values.shape[0] == 0:
        raise ValueError("matrix must be non-empty and square")
    if not np.all(np.isfinite(values)):
        raise ValueError("matrix entries must be finite")
    if not np.allclose(values, values.T, atol=1e-10, rtol=1e-10):
        raise ValueError("matrix must be symmetric")
    return int(values.shape[0]), lambda vector: values @ vector, np.diag(values).copy()


def conjugate_gradient(matrix, right_hand_side, *, initial=None,
                       tolerance=1e-10, max_iterations=None,
                       preconditioner=None):
    """Solve A x = b for symmetric positive-definite A with CG.

    Optional Jacobi preconditioning uses the positive diagonal of A.
    Convergence is measured against tolerance * max(norm(b), 1).
    """
    dimension, matvec, diagonal = _matrix_operator(matrix)
    b = np.asarray(right_hand_side, dtype=float)
    if b.shape != (dimension,) or not np.all(np.isfinite(b)):
        raise ValueError("right_hand_side must be a finite vector matching matrix size")
    if initial is None:
        x = np.zeros(dimension, dtype=float)
    else:
        x = np.asarray(initial, dtype=float).copy()
        if x.shape != (dimension,) or not np.all(np.isfinite(x)):
            raise ValueError("initial must be a finite vector matching matrix size")
    try:
        tol = float(tolerance)
    except (TypeError, ValueError):
        raise ValueError("tolerance must be finite and positive") from None
    if not np.isfinite(tol) or tol <= 0:
        raise ValueError("tolerance must be finite and positive")
    if max_iterations is None:
        max_iterations = max(1, 10 * dimension)
    if isinstance(max_iterations, (bool, np.bool_)) or not isinstance(max_iterations, (int, np.integer)) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    if preconditioner not in (None, "jacobi"):
        raise ValueError("preconditioner must be None or 'jacobi'")
    if preconditioner == "jacobi":
        if np.any(diagonal <= 0):
            raise ValueError("Jacobi preconditioner requires a positive matrix diagonal")
        apply_preconditioner = lambda residual: residual / diagonal
    else:
        apply_preconditioner = lambda residual: residual.copy()

    residual = b - matvec(x)
    b_norm = float(np.linalg.norm(b))
    scale = max(b_norm, 1.0)
    residual_norm = float(np.linalg.norm(residual))
    if residual_norm <= tol * scale:
        return {"solution": x, "converged": True, "iterations": 0,
                "residual_norm": residual_norm,
                "relative_residual": residual_norm / scale}
    z = apply_preconditioner(residual)
    direction = z.copy()
    rz = float(residual @ z)
    if not np.isfinite(rz) or rz <= 0:
        raise ValueError("matrix/preconditioner is not positive definite")
    converged = False
    iterations = 0
    for iterations in range(1, int(max_iterations) + 1):
        product = matvec(direction)
        denominator = float(direction @ product)
        if not np.isfinite(denominator) or denominator <= 0:
            raise ValueError("matrix is not positive definite")
        alpha = rz / denominator
        x += alpha * direction
        residual -= alpha * product
        residual_norm = float(np.linalg.norm(residual))
        if residual_norm <= tol * scale:
            converged = True
            break
        z = apply_preconditioner(residual)
        rz_new = float(residual @ z)
        if not np.isfinite(rz_new) or rz_new <= 0:
            raise ValueError("matrix/preconditioner is not positive definite")
        direction = z + (rz_new / rz) * direction
        rz = rz_new
    return {"solution": x, "converged": converged, "iterations": iterations,
            "residual_norm": residual_norm,
            "relative_residual": residual_norm / scale}


def kronecker_matvec(factors, vector):
    """Apply a Kronecker product without materialising the full matrix.

    Factors are 2D matrices A_i. The input vector length is the product of
    their column counts; output length is the product of row counts.
    """
    matrices = [np.asarray(factor, dtype=float) for factor in factors]
    if not matrices:
        raise ValueError("factors must contain at least one matrix")
    for factor in matrices:
        if factor.ndim != 2 or min(factor.shape) < 1 or not np.all(np.isfinite(factor)):
            raise ValueError("each factor must be a finite non-empty 2D matrix")
    input_shape = tuple(factor.shape[1] for factor in matrices)
    values = np.asarray(vector, dtype=float)
    if values.shape != (int(np.prod(input_shape)),) or not np.all(np.isfinite(values)):
        raise ValueError("vector length must equal the product of factor column counts")
    result = values.reshape(input_shape)
    for axis, factor in enumerate(matrices):
        moved = np.moveaxis(result, axis, 0)
        transformed = np.tensordot(factor, moved, axes=(1, 0))
        result = np.moveaxis(transformed, 0, axis)
    return result.reshape(-1)

import numpy as np
import pytest
from scipy import sparse
from linear_solvers import conjugate_gradient, kronecker_matvec


def test_conjugate_gradient_matches_dense_direct_solve():
    matrix = np.array([[4., 1., 0.], [1., 3., 1.], [0., 1., 2.]])
    rhs = np.array([1., 2., -1.])
    result = conjugate_gradient(matrix, rhs, tolerance=1e-12)
    np.testing.assert_allclose(result["solution"], np.linalg.solve(matrix, rhs), atol=1e-11)
    assert result["converged"]
    assert result["residual_norm"] < 1e-11


def test_preconditioned_cg_supports_sparse_spd_matrix():
    matrix = sparse.diags([2., 4., 8., 16.], format="csr")
    rhs = np.array([1., 2., 3., 4.])
    result = conjugate_gradient(matrix, rhs, preconditioner="jacobi", tolerance=1e-12)
    np.testing.assert_allclose(result["solution"], rhs / matrix.diagonal(), atol=1e-12)
    assert result["converged"]


def test_cg_initial_guess_and_zero_rhs():
    matrix = np.array([[2., 0.], [0., 3.]])
    result = conjugate_gradient(matrix, [0., 0.], initial=[1., 1.])
    np.testing.assert_allclose(result["solution"], [0., 0.])
    assert result["converged"]
    assert result["iterations"] >= 1


def test_kronecker_matvec_matches_explicit_product_for_rectangular_factors():
    a = np.array([[1., 2.], [3., 4.], [5., 6.]])
    b = np.array([[2., 0., 1.], [1., 3., 2.]])
    vector = np.arange(6., dtype=float) + 1
    result = kronecker_matvec([a, b], vector)
    expected = np.kron(a, b) @ vector
    np.testing.assert_allclose(result, expected, atol=1e-12)


def test_kronecker_matvec_supports_three_factors():
    factors = [np.array([[1., 2.], [0., 1.]]),
               np.array([[2., 0.], [1., 1.]]),
               np.array([[1., -1.], [2., 1.]])]
    vector = np.arange(8., dtype=float)
    np.testing.assert_allclose(kronecker_matvec(factors, vector),
                               np.kron(np.kron(*factors[:2]), factors[2]) @ vector)


def test_linear_solvers_reject_invalid_matrices_and_controls():
    with pytest.raises(ValueError, match="symmetric"):
        conjugate_gradient([[1., 2.], [0., 1.]], [1., 1.])
    with pytest.raises(ValueError, match="positive definite"):
        conjugate_gradient([[1., 0.], [0., -1.]], [1., 1.])
    with pytest.raises(ValueError, match="preconditioner"):
        conjugate_gradient(np.eye(2), [1., 1.], preconditioner="bad")
    with pytest.raises(ValueError, match="vector length"):
        kronecker_matvec([np.eye(2)], [1., 2., 3.])

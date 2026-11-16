import numpy as np
import pytest
from scipy import sparse
from logdet import stochastic_lanczos_logdet


def test_diagonal_spd_logdet_matches_exact_result():
    diagonal = np.array([.5, 1., 2., 4., 7.])
    result = stochastic_lanczos_logdet(np.diag(diagonal), n_probes=5,
                                       lanczos_steps=5, random_state=4)
    assert result["estimate"] == pytest.approx(np.log(diagonal).sum(), abs=1e-11)
    assert result["standard_error"] < 1e-10
    assert np.all(result["lanczos_steps_used"] <= 5)


def test_dense_non_diagonal_spd_matches_exact_probe_quadratic_forms():
    rng = np.random.default_rng(8)
    matrix = rng.normal(size=(6, 6))
    matrix = matrix.T @ matrix + np.eye(6) * .5
    result = stochastic_lanczos_logdet(matrix, n_probes=3,
                                       lanczos_steps=6, random_state=12)
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    log_matrix = (eigenvectors * np.log(eigenvalues)) @ eigenvectors.T
    probes = np.random.default_rng(12).choice([-1., 1.], size=(3, 6))
    oracle = np.sum((probes @ log_matrix) * probes, axis=1)
    # Full Krylov depth resolves each quadratic form; the finite-probe
    # average remains a stochastic trace estimate, not exact log(det(A)).
    np.testing.assert_allclose(result["probe_estimates"], oracle, atol=1e-9)
    assert result["estimate"] == pytest.approx(oracle.mean(), abs=1e-9)


def test_sparse_diagonal_matrix_matches_exact_logdet():
    diagonal = np.array([1.2, 2.4, 3.6, 5.8])
    result = stochastic_lanczos_logdet(sparse.diags(diagonal), n_probes=4,
                                       lanczos_steps=4, random_state=2)
    assert result["estimate"] == pytest.approx(np.log(diagonal).sum(), abs=1e-10)


def test_probe_estimates_are_reproducible_and_error_is_nonnegative():
    matrix = np.diag(np.linspace(1., 5., 12)) + .01
    a = stochastic_lanczos_logdet(matrix, n_probes=7, lanczos_steps=4, random_state=123)
    b = stochastic_lanczos_logdet(matrix, n_probes=7, lanczos_steps=4, random_state=123)
    np.testing.assert_array_equal(a["probe_estimates"], b["probe_estimates"])
    assert a["standard_error"] >= 0


@pytest.mark.parametrize("bad", [
    np.array([[1., 2.], [0., 1.]]),
    np.array([[1., 0.], [0., -1.]]),
    np.ones((2, 3)),
    np.array([[1., np.nan], [np.nan, 1.]])
])
def test_invalid_matrices_are_rejected(bad):
    with pytest.raises(ValueError):
        stochastic_lanczos_logdet(bad, n_probes=2, lanczos_steps=2)


def test_invalid_controls_are_rejected():
    with pytest.raises(ValueError, match="n_probes"):
        stochastic_lanczos_logdet(np.eye(3), n_probes=0)
    with pytest.raises(ValueError, match="lanczos_steps"):
        stochastic_lanczos_logdet(np.eye(3), lanczos_steps=0)


from logdet import chebyshev_logdet


def test_chebyshev_logdet_diagonal_matches_exact_logdet():
    diagonal = np.array([.5, 1., 2., 4., 7.])
    result = chebyshev_logdet(np.diag(diagonal), spectral_bounds=(.5, 7.),
        degree=100, n_probes=4, random_state=4, quadrature_order=256)
    assert result["estimate"] == pytest.approx(np.log(diagonal).sum(), abs=1e-10)


def test_chebyshev_logdet_dense_probe_values_match_eigendecomposition_oracle():
    rng = np.random.default_rng(44)
    matrix = rng.normal(size=(5, 5))
    matrix = matrix.T @ matrix + np.eye(5)
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    log_matrix = (eigenvectors * np.log(eigenvalues)) @ eigenvectors.T
    bounds = (float(eigenvalues[0]), float(eigenvalues[-1]))
    result = chebyshev_logdet(matrix, spectral_bounds=bounds, degree=100,
        n_probes=3, random_state=17, quadrature_order=256)
    probes = np.random.default_rng(17).choice([-1., 1.], size=(3, 5))
    oracle = np.sum((probes @ log_matrix) * probes, axis=1)
    np.testing.assert_allclose(result["probe_estimates"], oracle, atol=1e-9)


def test_chebyshev_logdet_supports_sparse_diagonal_matrices():
    diagonal = np.array([.7, 1.5, 2.2, 4.8])
    result = chebyshev_logdet(sparse.diags(diagonal),
        spectral_bounds=(.7, 4.8), degree=100, n_probes=4,
        random_state=9, quadrature_order=256)
    assert result["estimate"] == pytest.approx(np.log(diagonal).sum(), abs=1e-10)


def test_chebyshev_logdet_rejects_invalid_bounds_and_controls():
    with pytest.raises(ValueError, match="spectral_bounds"):
        chebyshev_logdet(np.eye(3), spectral_bounds=(0., 1.))
    with pytest.raises(ValueError, match="quadrature_order"):
        chebyshev_logdet(np.eye(3), spectral_bounds=(.5, 2.), degree=10,
                         quadrature_order=5)

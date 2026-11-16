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


def test_dense_non_diagonal_spd_matches_slogdet_at_full_krylov_depth():
    rng = np.random.default_rng(8)
    matrix = rng.normal(size=(6, 6))
    matrix = matrix.T @ matrix + np.eye(6) * .5
    sign, expected = np.linalg.slogdet(matrix)
    result = stochastic_lanczos_logdet(matrix, n_probes=3,
                                       lanczos_steps=6, random_state=12)
    assert sign == 1
    assert result["estimate"] == pytest.approx(expected, abs=1e-9)


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

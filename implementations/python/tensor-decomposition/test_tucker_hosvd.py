import numpy as np
import pytest
from tucker_hosvd import tucker_hosvd, tucker_reconstruct

def test_full_multilinear_rank_reconstructs_tensor():
    x = np.random.default_rng(4).normal(size=(3, 4, 2))
    fit = tucker_hosvd(x, x.shape)
    np.testing.assert_allclose(fit["reconstruction"], x, atol=1e-10)
    assert fit["relative_error"] < 1e-10

def test_exact_low_multilinear_rank_tensor():
    rng = np.random.default_rng(12)
    factors = [rng.normal(size=(5, 2)), rng.normal(size=(4, 2)), rng.normal(size=(3, 2))]
    core = rng.normal(size=(2, 2, 2))
    x = tucker_reconstruct(core, factors)
    fit = tucker_hosvd(x, (2, 2, 2))
    assert fit["relative_error"] < 1e-10

def test_factor_columns_are_orthonormal():
    fit = tucker_hosvd(np.arange(60, dtype=float).reshape(3, 4, 5), (2, 3, 2))
    for factor in fit["factors"]:
        np.testing.assert_allclose(factor.T @ factor, np.eye(factor.shape[1]), atol=1e-10)

def test_zero_tensor_has_zero_error():
    fit = tucker_hosvd(np.zeros((2, 3, 4)), (1, 2, 3))
    assert fit["relative_error"] == 0.0
    np.testing.assert_allclose(fit["reconstruction"], 0.0)

@pytest.mark.parametrize("x,ranks", [
    (np.ones(3), (1,)), (np.ones((2, 2)), (1,)),
    (np.ones((2, 2)), (0, 1)), (np.ones((2, 2)), (3, 1)), (np.ones((3, 4)), (3, 4)),
    (np.full((2, 2), np.inf), (1, 1)), (np.ones((2, 2)), (True, 1)),
])
def test_invalid_inputs(x, ranks):
    with pytest.raises(ValueError):
        tucker_hosvd(x, ranks)

def test_reconstruction_rejects_incompatible_factors():
    with pytest.raises(ValueError):
        tucker_reconstruct(np.ones((2, 2)), [np.ones((3, 1)), np.ones((4, 2))])

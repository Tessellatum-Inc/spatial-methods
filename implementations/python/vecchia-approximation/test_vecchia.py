import numpy as np
import pytest
from vecchia import squared_exponential_covariance, vecchia_loglikelihood


def exact_loglik(y, covariance):
    sign, logdet = np.linalg.slogdet(covariance)
    assert sign > 0
    return -.5 * (len(y)*np.log(2*np.pi) + logdet + y @ np.linalg.solve(covariance, y))


def test_all_predecessors_reproduce_exact_gaussian_likelihood():
    x = np.linspace(0, 3, 12)[:, None]
    y = np.sin(x[:, 0]) + .1*np.cos(2*x[:, 0])
    K = squared_exponential_covariance(x, variance=1.3, length_scale=.8, nugget=.05)
    exact = exact_loglik(y, K)
    result = vecchia_loglikelihood(y, x, variance=1.3, length_scale=.8,
                                   nugget=.05, n_neighbors=len(y)-1, jitter=1e-12)
    assert result["loglikelihood"] == pytest.approx(exact, abs=1e-8)


def test_exact_likelihood_is_invariant_to_order():
    rng = np.random.default_rng(4)
    x = rng.uniform(size=(10, 2))
    y = rng.normal(size=10)
    order = rng.permutation(10)
    a = vecchia_loglikelihood(y, x, n_neighbors=9, order=np.arange(10))
    b = vecchia_loglikelihood(y, x, n_neighbors=9, order=order)
    assert a["loglikelihood"] == pytest.approx(b["loglikelihood"], abs=1e-8)


def test_sparse_neighbour_approximation_returns_finite_conditionals():
    x = np.linspace(0, 5, 30)[:, None]
    y = np.sin(x[:, 0])
    result = vecchia_loglikelihood(y, x, n_neighbors=4)
    assert np.isfinite(result["loglikelihood"])
    assert np.all(result["conditional_variances"] > 0)
    assert result["conditional_means"].shape == y.shape


@pytest.mark.parametrize("kwargs", [
    {"n_neighbors": 0}, {"variance": 0}, {"length_scale": -1},
    {"nugget": -1}, {"jitter": -1}, {"order": [0, 0, 1]},
])
def test_invalid_parameters_raise(kwargs):
    with pytest.raises(ValueError):
        vecchia_loglikelihood([0., 1., 2.], [[0.], [1.], [2.]], **kwargs)

import numpy as np
import pytest

from gaussian_inverse import solve_gaussian_linear_inverse


def test_scalar_conjugate_posterior_matches_closed_form():
    result = solve_gaussian_linear_inverse(
        [[1.0]], [2.0], [0.0], [[4.0]], [[1.0]]
    )
    assert result["posterior_mean"] == pytest.approx([1.6])
    assert result["posterior_covariance"] == pytest.approx([[0.8]])
    assert result["posterior_std"] == pytest.approx([np.sqrt(0.8)])


def test_multivariate_posterior_is_symmetric_positive_semidefinite():
    result = solve_gaussian_linear_inverse(
        [[1, 0], [0, 1], [1, 1]],
        [1, -1, 0.2],
        [0, 0],
        [[2, 0.3], [0.3, 1]],
        np.eye(3) * 0.2,
    )
    covariance = result["posterior_covariance"]
    assert np.allclose(covariance, covariance.T)
    assert np.linalg.eigvalsh(covariance).min() >= -1e-10
    assert np.isfinite(result["log_marginal_likelihood"])


def test_prior_mean_is_returned_when_observations_are_uninformative():
    result = solve_gaussian_linear_inverse(
        [[0.0]], [8.0], [3.0], [[2.0]], [[1.0]]
    )
    assert result["posterior_mean"] == pytest.approx([3.0])
    assert result["posterior_covariance"] == pytest.approx([[2.0]])


def test_correlated_observation_noise_supported():
    result = solve_gaussian_linear_inverse(
        [[1, 0], [0, 1]], [1, 2], [0, 0], np.eye(2),
        [[1, 0.2], [0.2, 1]],
    )
    assert result["posterior_mean"].shape == (2,)
    assert result["marginal_observation_covariance"][0, 1] == pytest.approx(0.2)


@pytest.mark.parametrize("design,observations,mean,prior,noise", [
    ([[1, 0]], [1], [0, 0], [[1, 2], [2, 1]], [[1]]),
    ([[1]], [1], [0], [[1]], [[0]]),
    ([[1, 0], [0, 1]], [1, 2], [0, 0], [[1, 0], [0, 1]], [[1, 2], [2, 1]]),
])
def test_non_positive_definite_covariance_rejected(design, observations, mean, prior, noise):
    with pytest.raises(ValueError):
        solve_gaussian_linear_inverse(design, observations, mean, prior, noise)


def test_dimension_and_nonfinite_inputs_rejected():
    with pytest.raises(ValueError):
        solve_gaussian_linear_inverse([[1, 2]], [1], [0], [[1]], [[1]])
    with pytest.raises(ValueError):
        solve_gaussian_linear_inverse([[float("nan")]], [1], [0], [[1]], [[1]])

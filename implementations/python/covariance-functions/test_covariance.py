import numpy as np
import pytest

from covariance import (
    covariance_from_distance,
    covariance_matrix,
    covariance_matrix_diagnostics,
    semivariogram_from_distance,
)


@pytest.mark.parametrize("model", ["exponential", "gaussian", "matern32", "spherical", "wendland_c2"])
def test_covariance_matrix_is_symmetric_with_correct_diagonal(model):
    points = np.array([[0, 0], [0.4, 0.2], [1.2, -0.1], [2.0, 0.8]])
    matrix = covariance_matrix(points, model=model, variance=2.5, range_scale=1.7)
    np.testing.assert_allclose(matrix, matrix.T, atol=1e-12)
    np.testing.assert_allclose(np.diag(matrix), 2.5)


@pytest.mark.parametrize("model", ["exponential", "gaussian", "matern32", "spherical", "wendland_c2"])
def test_covariance_matrices_are_positive_semidefinite_on_small_euclidean_fixture(model):
    points = np.array([[0, 0], [0.4, 0.2], [1.2, -0.1], [2.0, 0.8], [0.2, 1.4]])
    matrix = covariance_matrix(points, model=model, range_scale=0.8)
    result = covariance_matrix_diagnostics(matrix, tolerance=1e-9)
    assert result["symmetric"]
    assert result["positive_semidefinite_within_tolerance"]


def test_semivariogram_is_zero_at_origin_and_increases_for_exponential():
    gamma = semivariogram_from_distance([0, 0.5, 1, 2], model="exponential")
    assert gamma[0] == pytest.approx(0)
    assert np.all(np.diff(gamma) > 0)


def test_compact_support_models_are_zero_at_and_beyond_the_range():
    for model in ("spherical", "wendland_c2"):
        values = covariance_from_distance([1.0, 1.5, 4.0], model=model, range_scale=1.0)
        np.testing.assert_allclose(values, 0.0, atol=0.0)


def test_duplicate_locations_produce_a_valid_singular_covariance_matrix():
    matrix = covariance_matrix([[0, 0], [0, 0], [1, 0]], model="gaussian")
    result = covariance_matrix_diagnostics(matrix)
    assert result["positive_semidefinite_within_tolerance"]
    assert np.linalg.matrix_rank(matrix) < len(matrix)


@pytest.mark.parametrize("bad", [[-1], [float("nan")], [float("inf")]])
def test_invalid_distances_are_rejected(bad):
    with pytest.raises(ValueError):
        covariance_from_distance(bad)


def test_invalid_locations_and_parameters_are_rejected():
    with pytest.raises(ValueError):
        covariance_matrix([[0, float("nan")]])
    with pytest.raises(ValueError):
        covariance_from_distance([1.0], variance=0)
    with pytest.raises(ValueError):
        covariance_from_distance([1.0], range_scale=-1)


def test_compact_support_models_reject_dimensions_above_three():
    with pytest.raises(ValueError):
        covariance_matrix(np.zeros((4, 4)), model="wendland_c2")



def test_random_fourier_features_approximate_gaussian_covariance():
    from covariance import _rff_features
    points=np.array([[0.0,0.0],[0.5,0.2],[1.0,-0.3]])
    rng=np.random.default_rng(23)
    count=30000
    frequencies=rng.normal(0,np.sqrt(2)/1.7,size=(2,count))
    phases=rng.uniform(0,2*np.pi,size=count)
    features=_rff_features(points,frequencies,phases,2.5)
    approximate=features@features.T
    exact=covariance_matrix(points,model="gaussian",variance=2.5,range_scale=1.7)
    np.testing.assert_allclose(approximate,exact,atol=0.035,rtol=0.035)


def test_random_fourier_gp_is_reproducible_and_returns_latent_variance():
    from covariance import fit_random_fourier_gp,predict_random_fourier_gp
    points=np.array([[0,0],[1,0],[0,1],[1,1]],dtype=float)
    values=np.array([1,2,3,4],dtype=float)
    a=fit_random_fourier_gp(points,values,range_scale=1.5,signal_variance=2,
                            noise_variance=0.05,feature_count=128,seed=19)
    b=fit_random_fourier_gp(points,values,range_scale=1.5,signal_variance=2,
                            noise_variance=0.05,feature_count=128,seed=19)
    np.testing.assert_array_equal(a["frequencies"],b["frequencies"])
    np.testing.assert_array_equal(a["weight_mean"],b["weight_mean"])
    result=predict_random_fourier_gp(a,[(0.5,0.5),(2,2)])
    assert result["mean"].shape==(2,)
    assert result["variance"].shape==(2,)
    assert np.isfinite(result["mean"]).all()
    assert np.all(result["variance"]>=0)


def test_random_fourier_gp_large_noise_returns_prior_mean_and_variance():
    from covariance import fit_random_fourier_gp,predict_random_fourier_gp
    model=fit_random_fourier_gp([(0,0)],[100],mean=3,noise_variance=1e12,
                                signal_variance=2,feature_count=512,seed=8)
    result=predict_random_fourier_gp(model,[(0.2,0.4),(3,4)])
    np.testing.assert_allclose(result["mean"],[3,3],atol=0.02)
    np.testing.assert_allclose(result["variance"],[2,2],atol=0.08)


def test_random_fourier_gp_rejects_invalid_training_and_prediction_inputs():
    from covariance import fit_random_fourier_gp,predict_random_fourier_gp
    with pytest.raises(ValueError):
        fit_random_fourier_gp([[0,0]],[1,2])
    with pytest.raises(ValueError):
        fit_random_fourier_gp([[0,0]],[1],noise_variance=0)
    with pytest.raises(ValueError):
        fit_random_fourier_gp([[0,0]],[1],feature_count=0)
    model=fit_random_fourier_gp([[0,0]],[1],seed=1)
    with pytest.raises(ValueError):
        predict_random_fourier_gp(model,[[0,0,0]])

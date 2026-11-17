import numpy as np
import pytest
from spatiotemporal_gp import predict_spatiotemporal_gp, separable_exponential_covariance

def test_covariance_is_product_of_spatial_and_temporal_terms():
    value = separable_exponential_covariance([[0, 0]], [0], [[3, 4]], [2],
        variance=4, spatial_scale=5, temporal_scale=2)[0, 0]
    assert value == pytest.approx(4 * np.exp(-1) * np.exp(-1))

def test_covariance_matrix_is_symmetric_psd_on_irregular_design():
    matrix = separable_exponential_covariance(
        [[0, 0], [1, 0], [0, 2], [2, 1]], [0, .5, 2, 3],
        variance=2.5, spatial_scale=1.7, temporal_scale=2.2)
    np.testing.assert_allclose(matrix, matrix.T, atol=1e-13)
    assert np.linalg.eigvalsh(matrix).min() > -1e-10

def test_cross_covariance_shape_and_zero_variance():
    result = separable_exponential_covariance([[0, 0], [1, 1]], [0, 1],
        [[2, 2]], [2], variance=0)
    assert result.shape == (2, 1)
    np.testing.assert_array_equal(result, np.zeros((2, 1)))

def test_single_observation_posterior_matches_scalar_oracle():
    pred = predict_spatiotemporal_gp([[0]], [0], [2], [[0], [1]], [0, 0],
        variance=4, spatial_scale=1, temporal_scale=1, noise_variance=0, jitter=0)
    expected_mean = np.array([2, 2*np.exp(-1)])
    expected_cov = np.array([[0, 0], [0, 4*(1-np.exp(-2))]])
    np.testing.assert_allclose(pred.mean, expected_mean, atol=1e-12)
    np.testing.assert_allclose(pred.covariance, expected_cov, atol=1e-12)
    np.testing.assert_allclose(pred.variance, np.diag(expected_cov), atol=1e-12)

def test_noise_and_observed_predictive_variance_are_distinct():
    args = dict(train_coordinates=[[0]], train_times=[0], train_values=[2],
        prediction_coordinates=[[0]], prediction_times=[0], variance=4,
        spatial_scale=1, temporal_scale=1, jitter=0)
    latent = predict_spatiotemporal_gp(**args, noise_variance=0)
    noisy = predict_spatiotemporal_gp(**args, noise_variance=1)
    observed = predict_spatiotemporal_gp(**args, noise_variance=1,
        include_observation_noise=True)
    assert latent.mean[0] == pytest.approx(2)
    assert noisy.mean[0] == pytest.approx(1.6)
    assert noisy.variance[0] == pytest.approx(.8)
    assert observed.variance[0] == pytest.approx(1.8)

def test_prediction_covariance_is_symmetric_psd():
    pred = predict_spatiotemporal_gp([[0,0],[1,0],[0,1]], [0,1,2], [1,0,2],
        [[.2,.2],[1.5,.5],[2,2]], [.5,1.5,3], variance=1.5,
        spatial_scale=2, temporal_scale=3, noise_variance=.05)
    np.testing.assert_allclose(pred.covariance, pred.covariance.T, atol=1e-12)
    assert np.linalg.eigvalsh(pred.covariance).min() > -1e-9
    assert np.all(pred.variance >= 0)

@pytest.mark.parametrize("kwargs", [
    {"variance":-1}, {"spatial_scale":0}, {"temporal_scale":-1}])
def test_invalid_covariance_parameters(kwargs):
    with pytest.raises(ValueError):
        separable_exponential_covariance([[0]], [0], **kwargs)

@pytest.mark.parametrize("coords,times", [
    ([[0],[1]], [0]), ([[np.nan]], [0]), ([[0]], [np.inf])])
def test_invalid_covariance_inputs(coords, times):
    with pytest.raises(ValueError):
        separable_exponential_covariance(coords, times)

def test_mismatched_dimensions_and_missing_cross_times_rejected():
    with pytest.raises(ValueError):
        separable_exponential_covariance([[0]], [0], [[0,1]], [0])
    with pytest.raises(ValueError):
        separable_exponential_covariance([[0]], [0], [[1]])

def test_invalid_regression_inputs_rejected():
    common = ([[0]], [0], [1], [[1]], [1])
    with pytest.raises(ValueError):
        predict_spatiotemporal_gp(*common, noise_variance=-1)
    with pytest.raises(ValueError):
        predict_spatiotemporal_gp(*common, jitter=-1)
    with pytest.raises(ValueError):
        predict_spatiotemporal_gp([[0]], [0], [np.nan], [[1]], [1])
    with pytest.raises(ValueError):
        predict_spatiotemporal_gp([[0]], [0], [1,2], [[1]], [1])

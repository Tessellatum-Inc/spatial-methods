import numpy as np
import pytest
from linear_spatial_assimilation import (
    periodic_advection_diffusion_operator, periodic_point_observation_operator,
    run_linear_spatial_assimilation,
)


def test_periodic_transition_preserves_constants_and_mass():
    F = periodic_advection_diffusion_operator(12, 2.0, 0.5, 1.0, 0.2)
    np.testing.assert_allclose(F @ np.ones(12), np.ones(12))
    np.testing.assert_allclose(np.ones(12) @ F, np.ones(12))
    assert np.all(F >= 0)


def test_negative_velocity_uses_right_upwind_neighbour():
    F = periodic_advection_diffusion_operator(8, 1.0, 0.25, -1.0, 0.0)
    assert F[2, 3] > 0 and F[2, 1] == 0


def test_stability_bound_is_enforced():
    with pytest.raises(ValueError, match="stability"):
        periodic_advection_diffusion_operator(8, 1.0, 1.0, 1.0, 0.1)


def test_periodic_sensor_interpolation_wraps():
    H = periodic_point_observation_operator(4, 1.0, np.array([0.5, 3.5, 4.0]))
    np.testing.assert_allclose(H[0], [0.5,0.5,0,0])
    np.testing.assert_allclose(H[1], [0.5,0,0,0.5])
    np.testing.assert_allclose(H[2], [1,0,0,0])
    np.testing.assert_allclose(H @ np.ones(4), np.ones(3))


def test_sequential_assimilation_and_free_forecast():
    n=10
    F=periodic_advection_diffusion_operator(n,1.0,0.2,0.5,0.05)
    H=periodic_point_observation_operator(n,1.0,np.array([1.5,5.5,8.0]))
    R=np.eye(3)*0.04
    result=run_linear_spatial_assimilation(
        np.zeros(n),np.eye(n),F,np.eye(n)*0.005,
        [(np.array([1.0,-0.5,0.25]),H,R),None,
         (np.array([1.0,-0.5,0.25]),H,R)],forecast_steps=2)
    assert result["forecast_means"].shape==(3,n)
    assert result["analysis_means"].shape==(3,n)
    assert result["free_forecast_means"].shape==(2,n)
    assert np.trace(result["analysis_covariances"][0]) < np.trace(result["forecast_covariances"][0])
    np.testing.assert_allclose(result["analysis_covariances"],result["analysis_covariances"].transpose(0,2,1),atol=1e-10)
    assert np.linalg.eigvalsh(result["analysis_covariances"][-1]).min()>-1e-10
    assert result["innovations"][1].size==0


def test_invalid_covariance_and_observation_dimensions_are_rejected():
    F=np.eye(3)
    with pytest.raises(ValueError,match="positive semidefinite"):
        run_linear_spatial_assimilation(np.zeros(3),np.diag([1,1,-1]),F,np.eye(3),[])
    with pytest.raises(ValueError,match="dimensions"):
        run_linear_spatial_assimilation(np.zeros(3),np.eye(3),F,np.eye(3),
                                        [(np.ones(2),np.ones((2,2)),np.eye(2))])
    with pytest.raises(ValueError,match="positive definite"):
        run_linear_spatial_assimilation(np.zeros(3),np.eye(3),F,np.eye(3),
                                        [(np.ones(1),np.ones((1,3)),np.zeros((1,1)))])

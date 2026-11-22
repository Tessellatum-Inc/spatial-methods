import numpy as np
import pytest
from linear_spatial_assimilation import (
    periodic_advection_diffusion_operator, periodic_point_observation_operator,
    periodic_nonuniform_advection_diffusion_operator,
    periodic_nonuniform_point_observation_operator,
    nonperiodic_nonuniform_advection_diffusion_operator,
    nonperiodic_nonuniform_advection_diffusion_step,
    run_linear_spatial_assimilation, verify_spatial_forecasts,
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


def test_nonuniform_variable_coefficient_model_conserves_mass_and_preserves_constants_for_divergence_free_flow():
    widths=np.array([0.5,1.0,1.5,0.75,1.25])
    variable_velocity=np.array([0.4,0.2,-0.1,0.3,0.0])
    diffusivity=np.array([0.02,0.04,0.03,0.01,0.05])
    variable_F=periodic_nonuniform_advection_diffusion_operator(
        widths,0.1,variable_velocity,diffusivity)
    np.testing.assert_allclose(widths@variable_F,widths,atol=1e-12)
    assert np.min(variable_F)>=0

    # A constant concentration is stationary when the 1-D periodic
    # velocity field is divergence-free (constant face velocity).
    constant_velocity=np.full(5,0.2)
    constant_F=periodic_nonuniform_advection_diffusion_operator(
        widths,0.1,constant_velocity,diffusivity)
    np.testing.assert_allclose(constant_F@np.ones(5),np.ones(5),atol=1e-12)
    np.testing.assert_allclose(widths@constant_F,widths,atol=1e-12)
    assert np.min(constant_F)>=0


def test_nonuniform_model_rejects_unstable_step_and_bad_face_fields():
    with pytest.raises(ValueError,match="stability"):
        periodic_nonuniform_advection_diffusion_operator(np.ones(4),2.0,np.ones(4),np.zeros(4))
    with pytest.raises(ValueError,match="one value per face"):
        periodic_nonuniform_advection_diffusion_operator(np.ones(4),0.1,np.ones(3),np.zeros(4))



def test_nonperiodic_zero_total_flux_operator_conserves_mass():
    widths=np.array([0.4,0.8,1.2,0.6])
    velocity=np.array([0.3,-0.1,0.2])
    diffusivity=np.array([0.02,0.04,0.01])
    F=nonperiodic_nonuniform_advection_diffusion_operator(widths,0.1,velocity,diffusivity)
    np.testing.assert_allclose(widths@F,widths,atol=1e-12)
    assert np.min(F)>=0
    state=np.array([1.0,0.4,1.7,0.2])
    assert np.dot(widths,F@state)==pytest.approx(np.dot(widths,state))


def test_nonperiodic_no_flux_diffusion_preserves_constant_state():
    widths=np.array([0.5,1.0,0.75,1.25])
    F=nonperiodic_nonuniform_advection_diffusion_operator(
        widths,0.1,np.zeros(3),np.array([0.1,0.2,0.05]))
    np.testing.assert_allclose(F@np.ones(4),np.ones(4),atol=1e-12)
    np.testing.assert_allclose(widths@F,widths,atol=1e-12)


def test_nonperiodic_operator_rejects_bad_faces_and_unstable_step():
    with pytest.raises(ValueError,match="n-1"):
        nonperiodic_nonuniform_advection_diffusion_operator(
            np.ones(4),0.1,np.ones(4),np.zeros(3))
    with pytest.raises(ValueError,match="positivity"):
        nonperiodic_nonuniform_advection_diffusion_operator(
            np.ones(4),2.0,np.ones(3),np.zeros(3))


def test_nonuniform_sensor_interpolation_is_periodic_and_affine_exact():
    widths=np.array([0.5,1.0,1.5,0.75,1.25])
    centres=np.cumsum(widths)-0.5*widths
    positions=np.array([0.1,0.8,2.2,4.8,5.1])
    H=periodic_nonuniform_point_observation_operator(widths,positions)
    np.testing.assert_allclose(H@np.ones(5),np.ones(5))
    np.testing.assert_allclose(H[1]@centres,0.8,atol=1e-12)
    np.testing.assert_allclose(H[2]@centres,2.2,atol=1e-12)
    np.testing.assert_allclose(H[4],H[0],atol=1e-12)


def test_heldout_forecast_verification_reports_leadwise_errors_without_updates():
    forecasts=np.array([[1.0,2.0,3.0],[2.0,2.0,4.0],[3.0,1.0,5.0]])
    H=np.array([[0.5,0.5,0.0],[0.0,0.0,1.0]])
    scores=verify_spatial_forecasts(
        forecasts,[(np.array([1.0,2.0]),H),None,
                   (np.array([2.0,4.0]),np.eye(3)[:2])])
    assert scores[0]["count"]==2
    assert scores[0]["rmse"]==pytest.approx(np.sqrt(0.625))
    assert np.isnan(scores[1]["rmse"])
    assert scores[2]["count"]==2
    with pytest.raises(ValueError,match="dimensions"):
        verify_spatial_forecasts(forecasts,[(np.ones(2),np.ones((2,2))),None,None])

def test_uniform_upwind_advection_converges_to_translated_fourier_mode():
    length=2*np.pi
    velocity=0.7
    final_time=0.5
    errors=[]
    for n in (40,80,160):
        dx=length/n
        centres=(np.arange(n)+0.5)*dx
        dt=0.4*dx/velocity
        steps=int(round(final_time/dt))
        dt=final_time/steps
        transition=periodic_advection_diffusion_operator(n,dx,dt,velocity,0.0)
        state=np.sin(centres)
        for _ in range(steps):
            state=transition@state
        exact=np.sin(centres-velocity*final_time)
        errors.append(float(np.mean(np.abs(state-exact))))
    assert errors[0]>errors[1]>errors[2]
    assert 1.7<errors[0]/errors[1]<2.4
    assert 1.7<errors[1]/errors[2]<2.4


def test_uniform_central_diffusion_converges_to_fourier_decay():
    length=2*np.pi
    diffusivity=0.3
    final_time=0.2
    errors=[]
    for n in (20,40,80):
        dx=length/n
        centres=(np.arange(n)+0.5)*dx
        dt=0.2*dx**2/diffusivity
        steps=int(round(final_time/dt))
        dt=final_time/steps
        transition=periodic_advection_diffusion_operator(
            n,dx,dt,0.0,diffusivity)
        state=np.sin(2*centres)
        for _ in range(steps):
            state=transition@state
        exact=np.exp(-4*diffusivity*final_time)*np.sin(2*centres)
        errors.append(float(np.mean(np.abs(state-exact))))
    assert errors[0]>errors[1]>errors[2]
    assert errors[0]/errors[1]>3.5
    assert errors[1]/errors[2]>3.5


def test_forced_nonperiodic_step_zero_forcing_matches_homogeneous_operator():
    widths=np.array([0.5,0.8,1.1,0.6])
    state=np.array([1.0,0.4,0.8,1.2])
    args=(widths,0.05,np.array([0.1,-0.05,0.2]),np.array([0.02,0.03,0.01]))
    F=nonperiodic_nonuniform_advection_diffusion_operator(*args)
    result=nonperiodic_nonuniform_advection_diffusion_step(
        *args,state,source_rates=np.zeros(4),boundary_fluxes=(0.0,0.0))
    np.testing.assert_allclose(result["concentrations"],F@state)
    assert result["mass_budget_residual"]==pytest.approx(0.0,abs=1e-12)


def test_forced_nonperiodic_step_accounts_for_sources_and_oriented_boundary_fluxes():
    widths=np.array([1.0,2.0,1.5])
    state=np.array([2.0,1.0,3.0])
    dt=0.1
    sources=np.array([0.5,-0.1,0.2])
    # Positive left flux enters; positive right flux leaves.
    boundaries=np.array([0.4,0.15])
    result=nonperiodic_nonuniform_advection_diffusion_step(
        widths,dt,np.zeros(2),np.zeros(2),state,
        source_rates=sources,boundary_fluxes=boundaries)
    expected=dt*(widths@sources+boundaries[0]-boundaries[1])
    assert result["expected_mass_change"]==pytest.approx(expected)
    assert result["final_mass"]-result["initial_mass"]==pytest.approx(expected)
    assert result["source_mass_change"]==pytest.approx(dt*(widths@sources))
    assert result["boundary_mass_change"]==pytest.approx(dt*(boundaries[0]-boundaries[1]))
    assert abs(result["mass_budget_residual"])<1e-12


def test_forced_nonperiodic_step_rejects_negative_state_without_clipping():
    with pytest.raises(ValueError,match="negative concentrations"):
        nonperiodic_nonuniform_advection_diffusion_step(
            np.ones(3),0.5,np.zeros(2),np.zeros(2),np.array([0.1,1.0,1.0]),
            source_rates=np.array([-1.0,0.0,0.0]))
    with pytest.raises(ValueError,match="negative concentrations"):
        nonperiodic_nonuniform_advection_diffusion_step(
            np.ones(3),0.5,np.zeros(2),np.zeros(2),np.array([0.1,1.0,1.0]),
            boundary_fluxes=(-1.0,0.0))


def test_forced_nonperiodic_step_validates_source_and_boundary_inputs():
    common=(np.ones(3),0.1,np.zeros(2),np.zeros(2),np.ones(3))
    with pytest.raises(ValueError,match="one rate per cell"):
        nonperiodic_nonuniform_advection_diffusion_step(*common,source_rates=np.zeros(2))
    with pytest.raises(ValueError,match="left, right"):
        nonperiodic_nonuniform_advection_diffusion_step(*common,boundary_fluxes=(0.0,))
    with pytest.raises(ValueError,match="finite"):
        nonperiodic_nonuniform_advection_diffusion_step(*common,source_rates=[0.0,np.nan,0.0])

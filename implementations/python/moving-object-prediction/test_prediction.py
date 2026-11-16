import numpy as np
import pytest
from prediction import (dead_reckoning_update_decision,
                        position_confidence_ellipse,
                        predict_constant_velocity)


def test_constant_velocity_state_and_covariance_match_matrix_equations():
    state = np.array([10., 20., 2., -1.])
    covariance = np.diag([1., 2., .25, .5])
    dt = 3.
    result = predict_constant_velocity(state, covariance, time_step=dt)
    transition = np.array([[1., 0., dt, 0.], [0., 1., 0., dt],
                           [0., 0., 1., 0.], [0., 0., 0., 1.]])
    np.testing.assert_allclose(result["state"], [16., 17., 2., -1.])
    np.testing.assert_allclose(result["covariance"],
                               transition @ covariance @ transition.T)


def test_white_acceleration_process_noise_matches_closed_form():
    sigma, dt = .4, 2.
    result = predict_constant_velocity([0., 0., 0., 0.], np.zeros((4, 4)),
        time_step=dt, acceleration_noise_std=sigma)
    expected = sigma**2 * np.array([
        [dt**4/4, 0., dt**3/2, 0.],
        [0., dt**4/4, 0., dt**3/2],
        [dt**3/2, 0., dt**2, 0.],
        [0., dt**3/2, 0., dt**2]
    ])
    np.testing.assert_allclose(result["process_noise"], expected)


def test_confidence_ellipse_axes_and_orientation_for_diagonal_covariance():
    covariance = np.diag([4., 1., .2, .2])
    result = position_confidence_ellipse([3., 5., 0., 0.], covariance,
                                         confidence_level=.95)
    quantile = -2*np.log(.05)
    assert result["center"].tolist() == [3., 5.]
    assert result["major_radius"] == pytest.approx(np.sqrt(4*quantile))
    assert result["minor_radius"] == pytest.approx(np.sqrt(quantile))
    assert result["orientation_rad"] == pytest.approx(0.)


def test_dead_reckoning_triggers_each_threshold_and_no_trigger():
    state = np.array([12., 0., 1., 0.])
    covariance = np.diag([.01, .01, .01, .01])
    common = dict(predicted_state=state, predicted_covariance=covariance,
                  reported_position=[0., 0.], elapsed_since_update=1.,
                  distance_threshold=5., uncertainty_threshold=10.,
                  max_interval=20.)
    distance = dead_reckoning_update_decision(**common)
    assert distance["request_update"] and distance["triggers"]["distance"]
    time = dead_reckoning_update_decision(**{**common, "reported_position":[12.,0.],
        "elapsed_since_update":20.})
    assert time["request_update"] and time["triggers"]["time"]
    uncertainty = dead_reckoning_update_decision(**{**common,
        "reported_position":[12.,0.],
        "predicted_covariance":np.diag([100., 1., .1, .1])})
    assert uncertainty["request_update"] and uncertainty["triggers"]["uncertainty"]
    quiet = dead_reckoning_update_decision(**{**common,
        "reported_position":[12.,0.], "distance_threshold":20.})
    assert not quiet["request_update"]


def test_prediction_rejects_invalid_state_covariance_and_controls():
    with pytest.raises(ValueError, match="state"):
        predict_constant_velocity([1., 2.], np.eye(4), time_step=1.)
    with pytest.raises(ValueError, match="positive semidefinite"):
        predict_constant_velocity([0., 0., 0., 0.],
                                  np.diag([1., 1., 1., -1.]), time_step=1.)
    with pytest.raises(ValueError, match="time_step"):
        predict_constant_velocity([0., 0., 0., 0.], np.eye(4), time_step=0.)
    with pytest.raises(ValueError, match="confidence_level"):
        position_confidence_ellipse([0., 0., 0., 0.], np.eye(4),
                                    confidence_level=1.0)

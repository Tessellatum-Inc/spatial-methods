import pytest

from multiping_covariance import (
    assemble_stochastic_clock_multiping_jacobian,
    propagate_stochastic_clock_multiping_covariance,
)


def test_stochastic_clock_columns_are_ping_local_but_correlate_outputs():
    local = [[[0.0], [0.0], [0.0]], [[0.0], [0.0], [0.0]]]
    shared = [[[0.0], [0.0], [0.0]], [[0.0], [0.0], [0.0]]]
    sensitivities = [[2.0, 0.0, 0.0], [3.0, 0.0, 0.0]]
    jacobian = assemble_stochastic_clock_multiping_jacobian(local, shared, sensitivities)
    assert jacobian[0] == [0.0, 0.0, 0.0, 2.0, 0.0]
    assert jacobian[3] == [0.0, 0.0, 0.0, 0.0, 3.0]

    covariance = [[0.0] * 5 for _ in range(5)]
    covariance[3][3] = 0.25
    covariance[4][4] = 1.0
    covariance[3][4] = covariance[4][3] = 0.2
    output = propagate_stochastic_clock_multiping_covariance(
        local, shared, sensitivities, covariance)["covariance"]
    assert output[0][0] == pytest.approx(1.0)
    assert output[3][3] == pytest.approx(9.0)
    assert output[0][3] == pytest.approx(1.2)


def test_stochastic_clock_full_joint_covariance_retains_navigation_clock_cross_terms():
    local = [[[1.0], [0.0], [0.0]], [[1.0], [0.0], [0.0]]]
    shared = [[[0.0], [0.0], [0.0]], [[0.0], [0.0], [0.0]]]
    sensitivity = [[1.0, 0.0, 0.0], [1.0, 0.0, 0.0]]
    covariance = [[0.0] * 5 for _ in range(5)]
    covariance[0][0] = covariance[1][1] = 1.0
    covariance[3][3] = covariance[4][4] = 0.25
    covariance[0][4] = covariance[4][0] = 0.1
    covariance[1][3] = covariance[3][1] = 0.1
    covariance[3][4] = covariance[4][3] = 0.2
    result = propagate_stochastic_clock_multiping_covariance(
        local, shared, sensitivity, covariance)["covariance"]
    assert result[0][3] == pytest.approx(0.4)

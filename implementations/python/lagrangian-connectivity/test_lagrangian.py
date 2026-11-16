import numpy as np
import pytest
from lagrangian import advect_particles_rk4, connectivity_matrix


def test_rk4_constant_velocity_has_exact_linear_trajectory():
    x = np.linspace(-5., 10., 16)
    y = np.linspace(-5., 5., 11)
    u = np.full((len(y), len(x)), 2.0)
    v = np.full_like(u, -1.0)
    starts = np.array([[0., 0.], [1., 1.]])
    result = advect_particles_rk4(x, y, u, v, starts,
                                  time_step=.5, n_steps=4)
    expected = starts + np.array([4., -2.])
    np.testing.assert_allclose(result["trajectory"][-1], expected, atol=1e-12)
    assert result["active"].all()


def test_rk4_linear_rotation_field_tracks_analytic_solution():
    x = np.linspace(-3., 3., 61)
    y = np.linspace(-3., 3., 61)
    xx, yy = np.meshgrid(x, y)
    omega = .2
    result = advect_particles_rk4(x, y, -omega*yy, omega*xx,
                                  [[1., 0.]], time_step=.05, n_steps=20)
    angle = omega * .05 * 20
    expected = np.array([[np.cos(angle), np.sin(angle)]])
    np.testing.assert_allclose(result["trajectory"][-1], expected, atol=2e-5)


def test_particles_outside_grid_become_inactive_and_nan():
    x = np.linspace(0., 2., 5)
    y = np.linspace(0., 2., 5)
    u = np.ones((5, 5))
    v = np.zeros((5, 5))
    result = advect_particles_rk4(x, y, u, v, [[1.5, 1.0]],
                                  time_step=.5, n_steps=3)
    assert not result["active"][0]
    assert np.isnan(result["trajectory"][2:, 0]).all()


def test_connectivity_counts_and_probabilities_match_direct_oracle():
    result = connectivity_matrix(
        np.array([0, 0, 0, 1, 1, 1]),
        np.array([1, 2, -1, 0, 0, 2]),
        n_sources=3, n_destinations=3,
        weights=np.array([2., 1., 1., 1., 3., 2.]))
    expected = np.array([[0., 2., 1.], [4., 0., 2.], [0., 0., 0.]])
    np.testing.assert_allclose(result["counts"], expected)
    np.testing.assert_allclose(result["probabilities"][0], [0., .5, .25])
    np.testing.assert_allclose(result["probabilities"][1], [2/3, 0., 1/3])
    np.testing.assert_allclose(result["unassigned_fraction"], [.25, 0., 0.])


def test_connectivity_rejects_invalid_region_ids_and_weights():
    with pytest.raises(ValueError, match="outside"):
        connectivity_matrix([0, 2], [0, 1], n_sources=2, n_destinations=2)
    with pytest.raises(ValueError, match="weights"):
        connectivity_matrix([0], [0], n_sources=1, n_destinations=1, weights=[-1.])


def test_advection_validates_grid_field_and_time_controls():
    with pytest.raises(ValueError, match="strictly increasing"):
        advect_particles_rk4([0., 1., 1.], [0., 1.], np.ones((2, 3)),
                             np.ones((2, 3)), [[0., 0.]], time_step=1., n_steps=1)
    with pytest.raises(ValueError, match="velocity arrays"):
        advect_particles_rk4([0., 1.], [0., 1.], np.ones((3, 2)),
                             np.ones((3, 2)), [[0., 0.]], time_step=1., n_steps=1)
    with pytest.raises(ValueError, match="n_steps"):
        advect_particles_rk4([0., 1.], [0., 1.], np.ones((2, 2)),
                             np.ones((2, 2)), [[0., 0.]], time_step=1., n_steps=0)

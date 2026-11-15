import numpy as np
import pytest
from particle_filter import bootstrap_particle_filter
from particle_smoother import ffbsi_particle_smoother


def test_ffbsi_reconstructs_supported_deterministic_transition_paths():
    particles = np.array([[[0.], [10.]], [[0.], [10.]], [[0.], [10.]]])
    weights = np.full((3, 2), 0.5)
    result = ffbsi_particle_smoother(
        {"particles": particles, "weights": weights},
        lambda previous, following: 0.0 if previous[0] == following[0] else -np.inf,
        n_trajectories=100,
        rng=np.random.default_rng(4),
    )
    np.testing.assert_array_equal(result["trajectories"][:, 0, 0],
                                  result["trajectories"][:, 1, 0])
    np.testing.assert_array_equal(result["trajectories"][:, 1, 0],
                                  result["trajectories"][:, 2, 0])
    assert result["trajectories"].shape == (100, 3, 1)
    assert result["indices"].shape == (100, 3)
    assert result["means"].shape == (3, 1)
    assert result["covariances"].shape == (3, 1, 1)


def test_ffbsi_backward_weights_include_filtering_weights():
    particles = np.array([[[0.], [1.]], [[5.], [6.]]])
    weights = np.array([[0.9, 0.1], [1.0, 0.0]])
    result = ffbsi_particle_smoother(
        {"particles": particles, "weights": weights},
        lambda previous, following: 0.0,
        n_trajectories=4000,
        rng=np.random.default_rng(12),
    )
    frequency = np.mean(result["indices"][:, 0] == 0)
    assert frequency == pytest.approx(0.9, abs=0.025)


def test_ffbsi_runs_with_bootstrap_filter_history():
    rng = np.random.default_rng(5)
    initial = rng.normal(0.0, 1.0, size=(500, 1))
    observations = [0.3, 0.5, 0.2, 0.1]
    sigma = 0.2
    transition = lambda x, gen: 0.8 * x + gen.normal(0.0, sigma, size=x.shape)
    loglike = lambda x, z: -0.5 * ((z - x[0]) / 0.3) ** 2
    filtered = bootstrap_particle_filter(observations, initial, transition, loglike,
                                         rng=np.random.default_rng(7))
    log_transition = lambda x, xp: -0.5 * ((xp[0] - 0.8*x[0]) / sigma) ** 2
    smoothed = ffbsi_particle_smoother(filtered, log_transition, 25,
                                       rng=np.random.default_rng(8))
    assert smoothed["trajectories"].shape == (25, 4, 1)
    assert np.isfinite(smoothed["means"]).all()
    assert np.isfinite(smoothed["covariances"]).all()


@pytest.mark.parametrize("count", [0, -1, True, 1.5])
def test_ffbsi_rejects_invalid_trajectory_count(count):
    with pytest.raises(ValueError):
        ffbsi_particle_smoother({"particles": np.ones((1, 2, 1)),
                                 "weights": np.ones((1, 2))},
                                lambda x, xp: 0.0, count)


def test_ffbsi_rejects_invalid_histories_and_transition_density():
    good = {"particles": np.ones((2, 2, 1)), "weights": np.ones((2, 2))}
    with pytest.raises(ValueError):
        ffbsi_particle_smoother({"particles": np.ones((2, 2, 1)),
                                 "weights": np.ones((1, 2))},
                                lambda x, xp: 0.0)
    with pytest.raises(ValueError):
        ffbsi_particle_smoother({"particles": np.ones((2, 2, 1)),
                                 "weights": np.zeros((2, 2))},
                                lambda x, xp: 0.0)
    with pytest.raises(ValueError):
        ffbsi_particle_smoother(good, lambda x, xp: np.nan)
    with pytest.raises(ValueError, match="backward transition"):
        ffbsi_particle_smoother(good, lambda x, xp: -np.inf)

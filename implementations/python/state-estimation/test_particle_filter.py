import numpy as np
import pytest
from particle_filter import effective_sample_size, systematic_resample, bootstrap_particle_filter

def test_effective_sample_size_uniform_and_concentrated_weights():
    assert effective_sample_size(np.ones(10)) == pytest.approx(10.0)
    assert effective_sample_size(np.array([1.0, 0.0, 0.0])) == pytest.approx(1.0)

def test_systematic_resampling_returns_valid_ancestors():
    idx = systematic_resample(np.array([0.1, 0.2, 0.7]), np.random.default_rng(2))
    assert idx.shape == (3,)
    assert np.all((0 <= idx) & (idx < 3))

def test_bootstrap_filter_reproducible_and_normalised():
    rng = np.random.default_rng(9)
    initial = rng.normal(0.0, 1.0, size=(3000, 1))
    observations = [0.8, 1.0, 0.9]
    transition = lambda p, gen: p + gen.normal(0.0, 0.15, size=p.shape)
    loglike = lambda p, z: -0.5 * ((z - p[0]) / 0.2) ** 2
    a = bootstrap_particle_filter(observations, initial, transition, loglike, rng=np.random.default_rng(42))
    b = bootstrap_particle_filter(observations, initial, transition, loglike, rng=np.random.default_rng(42))
    np.testing.assert_allclose(a["means"], b["means"])
    assert a["means"].shape == (3, 1)
    assert a["covariances"].shape == (3, 1, 1)
    for weights in a["weights"]:
        assert weights.sum() == pytest.approx(1.0)
        assert np.all(weights >= 0)

def test_filter_resamples_when_posterior_collapses():
    initial = np.linspace(-3, 3, 200).reshape(-1, 1)
    result = bootstrap_particle_filter([2.8], initial, lambda p, rng: p,
        lambda p, z: -0.5 * ((z - p[0]) / 0.03) ** 2,
        resample_threshold=0.9, rng=np.random.default_rng(3))
    assert result["resampled"][0]
    assert result["effective_sample_sizes"][0] < 0.9 * 200

def test_filter_rejects_all_zero_likelihood():
    initial = np.arange(10, dtype=float).reshape(-1, 1)
    with pytest.raises(ValueError, match="zero likelihood"):
        bootstrap_particle_filter([0], initial, lambda p, rng: p, lambda p, z: -np.inf)

def test_filter_rejects_invalid_transition_shape():
    initial = np.zeros((10, 2))
    with pytest.raises(ValueError):
        bootstrap_particle_filter([0], initial, lambda p, rng: np.array([1.0]), lambda p, z: 0.0)

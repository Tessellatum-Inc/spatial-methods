"""Bootstrap particle filter with systematic resampling."""
from __future__ import annotations
import numpy as np

def effective_sample_size(weights):
    w = np.asarray(weights, dtype=float)
    if w.ndim != 1 or w.size == 0 or not np.all(np.isfinite(w)) or np.any(w < 0):
        raise ValueError("weights must be a nonempty finite nonnegative vector")
    total = w.sum()
    if total <= 0:
        raise ValueError("weights must have positive sum")
    w = w / total
    return float(1.0 / np.sum(w * w))

def systematic_resample(weights, rng=None):
    """Return N ancestor indices using one random offset and a regular grid."""
    w = np.asarray(weights, dtype=float)
    if w.ndim != 1 or w.size == 0 or not np.all(np.isfinite(w)) or np.any(w < 0) or w.sum() <= 0:
        raise ValueError("weights must be a nonempty finite nonnegative vector with positive sum")
    w = w / w.sum()
    rng = np.random.default_rng() if rng is None else rng
    n = w.size
    positions = (rng.random() + np.arange(n)) / n
    cumulative = np.cumsum(w)
    cumulative[-1] = 1.0
    return np.searchsorted(cumulative, positions, side="right")

def _normalise_log_weights(log_weights):
    lw = np.asarray(log_weights, dtype=float)
    if lw.ndim != 1 or not np.all(np.isfinite(lw) | np.isneginf(lw)):
        raise ValueError("log weights must be finite or negative infinity")
    peak = np.max(lw)
    if not np.isfinite(peak):
        raise ValueError("all particles have zero likelihood")
    shifted = np.exp(lw - peak)
    total = shifted.sum()
    if not np.isfinite(total) or total <= 0:
        raise ValueError("particle weights could not be normalised")
    return shifted / total

def bootstrap_particle_filter(observations, initial_particles, transition,
                              log_likelihood, resample_threshold=0.5, rng=None,
                              initial_weights=None):
    """Run a bootstrap/SIR particle filter.

    transition(particle, rng) samples from the state transition density.
    log_likelihood(particle, observation) returns log p(observation|particle).
    The reported moments are weighted posterior moments before resampling.
    """
    zs = list(observations)
    if not zs:
        raise ValueError("observations must be nonempty")
    particles = np.asarray(initial_particles, dtype=float)
    if particles.ndim != 2 or particles.shape[0] < 2 or particles.shape[1] < 1 or not np.all(np.isfinite(particles)):
        raise ValueError("initial_particles must be a finite N-by-state matrix with N >= 2")
    n_particles, n_state = particles.shape
    if not np.isfinite(resample_threshold) or not 0 < resample_threshold <= 1:
        raise ValueError("resample_threshold must be in (0, 1]")
    rng = np.random.default_rng() if rng is None else rng
    if initial_weights is None:
        weights = np.full(n_particles, 1.0 / n_particles)
    else:
        weights = np.asarray(initial_weights, dtype=float)
        if weights.shape != (n_particles,) or not np.all(np.isfinite(weights)) or np.any(weights < 0) or weights.sum() <= 0:
            raise ValueError("initial_weights must be finite, nonnegative, and match particle count")
        weights = weights / weights.sum()
    means, covariances, ess_history, particle_history, weight_history, resampled_history = [], [], [], [], [], []
    for observation in zs:
        propagated = np.asarray([transition(p.copy(), rng) for p in particles], dtype=float)
        if propagated.shape != (n_particles, n_state) or not np.all(np.isfinite(propagated)):
            raise ValueError("transition must return one finite state vector per particle")
        log_likelihoods = np.asarray([log_likelihood(p, observation) for p in propagated], dtype=float)
        if log_likelihoods.shape != (n_particles,):
            raise ValueError("log_likelihood must return one scalar per particle")
        with np.errstate(divide="ignore"):
            log_prior = np.log(weights)
        posterior_weights = _normalise_log_weights(log_prior + log_likelihoods)
        mean = posterior_weights @ propagated
        centered = propagated - mean
        covariance = (centered.T * posterior_weights) @ centered
        ess = effective_sample_size(posterior_weights)
        do_resample = ess < resample_threshold * n_particles
        means.append(mean)
        covariances.append(covariance)
        ess_history.append(ess)
        if do_resample:
            ancestors = systematic_resample(posterior_weights, rng)
            particles = propagated[ancestors].copy()
            weights = np.full(n_particles, 1.0 / n_particles)
        else:
            particles = propagated
            weights = posterior_weights
        particle_history.append(particles.copy())
        weight_history.append(weights.copy())
        resampled_history.append(do_resample)
    return {"means": np.asarray(means), "covariances": np.asarray(covariances),
            "effective_sample_sizes": np.asarray(ess_history),
            "particles": particle_history, "weights": weight_history,
            "resampled": np.asarray(resampled_history, dtype=bool)}

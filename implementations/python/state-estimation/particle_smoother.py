"""Forward-filtering backward-simulation particle smoother (FFBSi)."""
from __future__ import annotations
import numpy as np

def ffbsi_particle_smoother(filter_result, transition_log_density,
                            n_trajectories=100, rng=None):
    """Sample joint state trajectories from a stored bootstrap-filter result.

    filter_result must contain:
      - particles: T arrays of shape (N, state_dimension), representing
        filtering particles after any resampling at each time;
      - weights: T arrays of N nonnegative filtering weights.

    transition_log_density(previous_state, next_state) must return
    log p(next_state | previous_state) for the same transition model used
    by the forward filter. The smoother is offline and uses the full history.
    """
    if isinstance(n_trajectories, (bool, np.bool_)) or not isinstance(
        n_trajectories, (int, np.integer)
    ) or n_trajectories < 1:
        raise ValueError("n_trajectories must be a positive integer")
    if not callable(transition_log_density):
        raise ValueError("transition_log_density must be callable")
    if not isinstance(filter_result, dict) or "particles" not in filter_result or "weights" not in filter_result:
        raise ValueError("filter_result must contain particles and weights histories")

    particles = np.asarray(filter_result["particles"], dtype=float)
    weights = np.asarray(filter_result["weights"], dtype=float)
    if particles.ndim != 3 or particles.shape[0] < 1 or particles.shape[1] < 2 or particles.shape[2] < 1:
        raise ValueError("particle history must have shape (T, N, state_dimension)")
    n_steps, n_particles, n_state = particles.shape
    if not np.all(np.isfinite(particles)):
        raise ValueError("particle history must be finite")
    if weights.shape != (n_steps, n_particles) or not np.all(np.isfinite(weights)) or np.any(weights < 0):
        raise ValueError("weight history must be finite, nonnegative and match particle history")
    totals = weights.sum(axis=1)
    if np.any(totals <= 0):
        raise ValueError("each filtering weight vector must have positive sum")
    weights = weights / totals[:, None]

    rng = np.random.default_rng() if rng is None else rng
    n_trajectories = int(n_trajectories)
    indices = np.empty((n_trajectories, n_steps), dtype=int)
    trajectories = np.empty((n_trajectories, n_steps, n_state), dtype=float)

    for m in range(n_trajectories):
        index = int(rng.choice(n_particles, p=weights[-1]))
        indices[m, -1] = index
        trajectories[m, -1] = particles[-1, index]
        for t in range(n_steps - 2, -1, -1):
            next_state = trajectories[m, t + 1]
            transition_logs = np.asarray([
                transition_log_density(particles[t, i].copy(), next_state.copy())
                for i in range(n_particles)
            ], dtype=float)
            if transition_logs.shape != (n_particles,) or not np.all(
                np.isfinite(transition_logs) | np.isneginf(transition_logs)
            ):
                raise ValueError("transition_log_density must return finite values or negative infinity")
            with np.errstate(divide="ignore"):
                log_filter_weights = np.log(weights[t])
            log_backward_weights = log_filter_weights + transition_logs
            peak = np.max(log_backward_weights)
            if not np.isfinite(peak):
                raise ValueError("all backward transition probabilities are zero")
            backward_weights = np.exp(log_backward_weights - peak)
            backward_weights /= backward_weights.sum()
            index = int(rng.choice(n_particles, p=backward_weights))
            indices[m, t] = index
            trajectories[m, t] = particles[t, index]

    means = np.mean(trajectories, axis=0)
    centred = trajectories - means[None, :, :]
    covariances = np.einsum("mti,mtj->tij", centred, centred) / n_trajectories
    return {
        "trajectories": trajectories,
        "indices": indices,
        "means": means,
        "covariances": covariances,
    }

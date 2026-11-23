"""Empirical quantile mapping and delta-change downscaling baselines."""
import numpy as np


def _finite_array(values, name):
    arr = np.asarray(values, dtype=float)
    if arr.ndim != 1 or arr.size < 1 or not np.isfinite(arr).all():
        raise ValueError(f"{name} must be a finite non-empty 1D sequence")
    return arr


def empirical_quantile_mapping(simulated, model_calibration, observed_calibration, *, n_quantiles=101):
    """Map simulated values through model-calibration to observed quantiles.

    Linear interpolation is used between quantile knots and constant tails
    outside the calibration range. Assumes a stationary calibration bias.
    """
    sim = _finite_array(simulated, "simulated")
    model = _finite_array(model_calibration, "model_calibration")
    observed = _finite_array(observed_calibration, "observed_calibration")
    if isinstance(n_quantiles, bool) or not isinstance(n_quantiles, int) or n_quantiles < 2:
        raise ValueError("n_quantiles must be an integer of at least two")
    probs = np.linspace(0.0, 1.0, n_quantiles)
    model_q, observed_q = np.quantile(model, probs), np.quantile(observed, probs)
    unique_model, inverse = np.unique(model_q, return_inverse=True)
    mapped = np.array([np.mean(observed_q[inverse == i]) for i in range(len(unique_model))])
    corrected = (np.full(sim.shape, mapped[0], dtype=float) if len(unique_model) == 1
                 else np.interp(sim, unique_model, mapped, left=mapped[0], right=mapped[-1]))
    return corrected.tolist()


def delta_change(observed_historical, model_historical, model_future, *, mode="additive"):
    """Apply modelled change to observed historical mean; preserve future shape."""
    obs = _finite_array(observed_historical, "observed_historical")
    hist = _finite_array(model_historical, "model_historical")
    future = np.asarray(model_future, dtype=float)
    if future.size < 1 or not np.isfinite(future).all():
        raise ValueError("model_future must contain finite values")
    if mode not in {"additive", "multiplicative"}:
        raise ValueError("mode must be additive or multiplicative")
    obs_mean, hist_mean = float(np.mean(obs)), float(np.mean(hist))
    if mode == "additive":
        corrected = obs_mean + future - hist_mean
    else:
        if hist_mean == 0:
            raise ValueError("multiplicative delta change requires non-zero model historical mean")
        corrected = obs_mean * (future / hist_mean)
    return corrected.tolist()

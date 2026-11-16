"""Bayesian online change-point detection with known variance and unknown mean."""
from __future__ import annotations
from math import exp, isfinite, log, pi
from typing import Iterable


def bocpd_normal_mean(values: Iterable[float], *, observation_variance: float,
                      prior_mean: float = 0.0, prior_kappa: float = 1.0,
                      hazard: float = 0.01, max_run_length: int | None = None
                      ) -> tuple[list[float], list[int]]:
    """Return per-observation change-point probability and MAP run length.

    Model: conditionally Gaussian observations with known fixed variance and
    unknown segment mean; each segment mean has a Normal prior represented by
    (prior_mean, prior_kappa). Constant hazard is assumed. This is a bounded
    teaching BOCPD model, not the full unknown-variance Student-t formulation.
    """
    x = [float(v) for v in values]
    if not x or any(not isfinite(v) for v in x):
        raise ValueError("values must be non-empty and finite")
    if not isfinite(observation_variance) or observation_variance <= 0:
        raise ValueError("observation_variance must be positive and finite")
    if not isfinite(prior_mean) or not isfinite(prior_kappa) or prior_kappa <= 0:
        raise ValueError("prior_mean must be finite and prior_kappa positive")
    if not isfinite(hazard) or not 0 < hazard < 1:
        raise ValueError("hazard must be strictly between zero and one")
    if max_run_length is not None and (
        not isinstance(max_run_length, int) or isinstance(max_run_length, bool)
        or max_run_length < 1
    ):
        raise ValueError("max_run_length must be a positive integer or None")

    # Run-length posterior and the Normal prior parameters for each run.
    probs = [1.0]
    means = [prior_mean]
    kappas = [prior_kappa]
    cp_probs, map_lengths = [], []
    log_norm_const = -0.5 * log(2.0 * pi * observation_variance)

    for value in x:
        predictive = []
        for mean, kappa in zip(means, kappas):
            variance = observation_variance * (1.0 + 1.0 / kappa)
            z = value - mean
            predictive.append(log_norm_const - 0.5 * log(1.0 + 1.0 / kappa)
                              - 0.5 * z * z / variance)

        # Prior predictive for a fresh segment (run length zero).
        fresh_variance = observation_variance * (1.0 + 1.0 / prior_kappa)
        fresh_z = value - prior_mean
        fresh_log_pred = (log_norm_const - 0.5 * log(1.0 + 1.0 / prior_kappa)
                          - 0.5 * fresh_z * fresh_z / fresh_variance)
        log_growth = [(log(p) if p > 0 else float('-inf')) + log(1.0 - hazard) + lp
                      for p, lp in zip(probs, predictive)]
        log_cp = log(hazard) + fresh_log_pred
        log_weights = [log_cp] + log_growth
        peak = max(log_weights)
        weights = [exp(w - peak) for w in log_weights]
        total = sum(weights)
        next_probs = [w / total for w in weights]

        # Fresh run state plus one updated state for every previous run length.
        next_means = [(prior_kappa * prior_mean + value) / (prior_kappa + 1.0)]
        next_kappas = [prior_kappa + 1.0]
        for mean, kappa in zip(means, kappas):
            next_means.append((kappa * mean + value) / (kappa + 1.0))
            next_kappas.append(kappa + 1.0)

        if max_run_length is not None:
            next_probs = next_probs[:max_run_length + 1]
            next_means = next_means[:max_run_length + 1]
            next_kappas = next_kappas[:max_run_length + 1]
            renorm = sum(next_probs)
            next_probs = [p / renorm for p in next_probs]

        probs, means, kappas = next_probs, next_means, next_kappas
        cp_probs.append(probs[0])
        map_lengths.append(max(range(len(probs)), key=lambda i: (probs[i], -i)))
    return cp_probs, map_lengths

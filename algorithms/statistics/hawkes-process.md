# Exponential Hawkes self-exciting point process

A temporal Hawkes process models event intensity as a baseline plus excitation from previous events:

\[
\lambda(t)=\mu+\sum_{t_i<t}\alpha e^{-\beta(t-t_i)}.
\]

Here (mu>0) is the baseline rate, (alpha\ge0) is excitation and (eta>\alpha) gives a stationary subcritical process with branching ratio (alpha/\beta<1). The implementation uses Ogata thinning to simulate events and computes the conditional log-likelihood over a finite observation window, including the integrated intensity compensator.

## Limits

This is a univariate temporal model. It does not implement spatial Hawkes processes, log-Gaussian Cox processes, ETAS earthquake models, marked or multivariate excitation, covariates, time-varying baselines or hazard forecasting. A stationary subcritical model is not a substitute for domain-specific calibration and validation.

## Verification

Tests cover seeded reproducibility, event ordering and observation-window bounds, the Poisson special case at zero excitation, excitation of close event pairs and long-run simulated mean-rate behaviour.

See the [implementation package](../../implementations/python/hawkes-process/README.md).

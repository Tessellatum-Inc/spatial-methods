# Exponential Hawkes process

Install and test with python -m pip install -r requirements.txt && python -m pytest -q.

The package simulates a univariate temporal Hawkes process with constant baseline intensity and exponential triggering kernel using Ogata thinning. It also evaluates the conditional point-process log-likelihood for ordered event times over a finite observation window.

The stationary process is restricted to positive baseline intensity, non-negative excitation and decay greater than excitation (branching ratio below one). The model has no spatial coordinates, marks, covariates, time-varying baseline, multivariate interactions, LGCP random field or ETAS-specific earthquake productivity/magnitude law. Simulation is intended for methodological examples, not calibrated hazard forecasts.

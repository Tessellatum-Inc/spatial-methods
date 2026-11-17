# Uncertainty propagation and sensitivity

Dependency-free baselines for coordinate positional RMSE, Monte Carlo
propagation under independent uniform inputs, and first-order/total-order
Sobol sensitivity indices using Saltelli pick-freeze estimators.

Run `python -m pip install -r requirements.txt && python -m pytest -q`.

The Monte Carlo and Sobol routines require a deterministic scalar model and
independent uniform input bounds. Sobol estimates are finite-sample estimates
and may be noisy or slightly outside [0,1]. This package does not implement
arbitrary input distributions, correlated inputs, second-order indices,
polynomial chaos, uncertainty distributions for coordinates, or survey-design
variance estimators.

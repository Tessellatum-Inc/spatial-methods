# Positional accuracy, Monte Carlo propagation and Sobol sensitivity

For reference coordinates x_i and estimated coordinates xhat_i, coordinate
errors are e_i=xhat_i-x_i. The implementation reports per-axis bias,
per-axis RMSE and pooled coordinate RMSE
\[
RMSE=\sqrt{\frac{1}{nd}\sum_{i=1}^{n}\sum_{j=1}^{d}e_{ij}^{2}}.
\]

Monte Carlo propagation draws independent uniform inputs from explicit
bounds, evaluates a deterministic scalar model and summarizes its output with
sample mean, variance, standard deviation and empirical quantiles. The input
distribution is part of the model: uniform sampling must not be used as a
substitute for known measurement-error distributions.

For independent inputs, Saltelli pick-freeze estimators use two base samples
A and B and hybrid samples AB_j. The first-order index estimates the main
effect of input j; the total-order index includes all interactions involving
that input. The reference implementation returns S1 and ST but not second-order
indices or confidence intervals. Estimates are stochastic and require
convergence checks.

These are teaching baselines, not a full uncertainty budget. Correlated inputs,
non-uniform distributions, polynomial chaos, geostatistical covariance,
spatially varying error and design-based survey variance remain outside scope.
See the tested [Python package](../../implementations/python/uncertainty-propagation/README.md).

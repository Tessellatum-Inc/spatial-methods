# Uncertainty intervals for spatial impacts

**Status:** implemented parametric Monte Carlo propagation; deterministic zero-covariance, stochastic interval and validation tests added. Full repository tests and CI are not yet confirmed.

## Why uncertainty must be propagated

For SAR/SDM models, marginal effects are not simply the regression coefficients. For covariate \(r\),

\[
S_r=(I-\rho W)^{-1}(\beta_r I+\gamma_r W).
\]

The average direct effect is \(\operatorname{tr}(S_r)/n\), the average total effect is the mean row sum, and the average indirect effect is total minus direct. Since all three are nonlinear functions of the estimated parameters, uncertainty in \(\rho\), \(\beta\), and \(\gamma\) must be propagated jointly.

## Parametric simulation

The implementation accepts a point estimate and a joint covariance matrix. The parameter ordering is explicit:

- SAR: \([\rho,\beta_1,\ldots,\beta_k]\)
- SDM: \([\rho,\beta_1,\ldots,\beta_k,\gamma_1,\ldots,\gamma_k]\)

It draws multivariate-normal parameter vectors, recalculates the exact dense impact matrix for every covariate, and summarises the empirical distribution of direct, indirect and total effects. It reports the point-estimate impact, Monte Carlo standard deviation and equal-tail percentile interval at the requested confidence level.

Draws are rejected when \(I-\rho W\) is singular or exceeds a configurable condition-number threshold. The routine reports accepted and rejected draws and fails if the accepted fraction falls below the requested minimum.

## Important assumptions and limitations

This routine propagates a covariance matrix; it does not estimate one. The covariance must be a defensible joint covariance from the fitted model and must use the documented parameter ordering. A multivariate-normal approximation may be poor near parameter boundaries or under weak identification. Rejection of ill-conditioned draws can truncate the simulated distribution and should be reported, not hidden. Percentile intervals are not automatically likelihood-based confidence intervals.

The method accepts asymmetric as well as symmetric weights, including common row-standardised matrices. It uses dense matrix solves and is intended for small teaching examples. It does not support Bayesian posterior draws directly (although a user could summarise supplied draws in a separate extension), bootstrap resampling, robust covariance estimation or sparse large-scale computation.

## Runnable implementation and tests

- [Impact implementation](../../implementations/python/spatial-econometrics/impacts.py)
- [Tests](../../implementations/python/spatial-econometrics/test_spatial_econometrics.py)
- [Package overview](../../implementations/python/spatial-econometrics/README.md)
- [Spatial econometrics lab](../../notebooks/spatial-econometrics-lab.ipynb)


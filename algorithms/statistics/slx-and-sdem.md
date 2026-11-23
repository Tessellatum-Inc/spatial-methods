# SLX and SDEM spatial regression

## Purpose

SLX and SDEM models represent spatial dependence through neighbouring covariates and, in SDEM, spatially correlated disturbances. They are distinct from SAR/SDM models because neither specifies a spatially lagged dependent variable.

## Models

The SLX specification is

\[
y = X\beta + WX\gamma + \varepsilon,
\]

where \(W\) is a supplied spatial-weights matrix. It is estimated by ordinary least squares on the expanded design \([X,WX]\).

The spatial Durbin error model (SDEM) adds a spatial-error process:

\[
y = X\beta + WX\gamma + u, \qquad
u = \lambda Wu + \varepsilon.
\]

The reference implementation estimates this by concentrated Gaussian maximum likelihood, treating \([X,WX]\) as the exogenous design in the SEM likelihood. The determinant term is therefore \(\log|I-\lambda W|\), with no SAR lag determinant.

## Implementation

- Code: [SLX/SDEM estimators](../../implementations/python/spatial-econometrics/slx_sdem.py)
- Tests: [spatial econometrics test suite](../../implementations/python/spatial-econometrics/test_spatial_econometrics.py)
- SLX returns OLS coefficients, fitted values, residuals, residual variance and effective rank.
- SDEM returns the spatial-error parameter, coefficients, likelihood, fitted values, residuals, conservative parameter bounds and likelihood evaluation count.
- Columns of \(WX\) that are exactly linearly dependent on the included design are dropped in stable order and their reported spatial coefficients are zero. This handles the redundant spatial lag of a constant under row-standardised weights.

## Assumptions and limits

The supplied weights matrix is used as-is; construction, scaling, islands and alignment remain the analyst's responsibility. The estimators require finite inputs, non-negative weights, a zero diagonal, nonzero weights and a full-rank base design. The SDEM routine inherits the dense SEM estimator's conservative norm-bounded search and Gaussian likelihood assumptions.

These are small-sample teaching implementations, not production spatial-econometric software. They do not provide standard errors, robust covariance estimates, specification tests, instrument diagnostics or automatic model selection. OLS SLX inference also requires the usual exogeneity and error assumptions; spatially dependent errors are precisely why SDEM may be appropriate instead.

## Interpretation

- \(\beta\) describes the association with the observation's own covariates, conditional on the model.
- \(\gamma\) describes association with spatially lagged covariates.
- \(\lambda\) measures spatial dependence in the disturbance process; it is not a response spillover parameter.
- In contrast, SAR and SDM models include \(Wy\) and induce feedback through the dependent variable.

## References

- LeSage, J. and Pace, R. K. (2009). *Introduction to Spatial Econometrics*. CRC Press.
- Elhorst, J. P. (2014). *Spatial Econometrics: From Cross-Sectional Data to Spatial Panels*. Springer.

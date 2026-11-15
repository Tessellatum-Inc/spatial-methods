# Spatial econometrics teaching implementations

This package contains small, dense-matrix reference implementations:

1. **Classic and Bera–Yoon robust spatial LM diagnostics** for lag and error dependence.
2. **SAR/SDM direct, indirect and total impact decomposition**, plus Monte Carlo uncertainty propagation from a supplied joint parameter covariance.
3. **Spatial lag 2SLS** using exogenous covariates and spatial lags as instruments for endogenous Wy.
4. **Spatial Durbin 2SLS** with higher-order spatial lags as excluded instruments.
5. **SLX OLS and SDEM concentrated Gaussian ML** for spatially lagged covariates, with and without spatially correlated errors.
6. **Gaussian proper-CAR regression ML** with an eigenvalue-derived positive-definite parameter interval.
7. **Constrained ICAR Gaussian field simulation** with one sum-to-zero constraint per connected graph component.
8. **Concentrated Gaussian maximum likelihood** for SAR, SEM and SDM, plus joint two-parameter SARAR/SAC likelihood estimation.
9. **Spatial HAC covariance for OLS** using a compact-support positive-definite Wendland kernel.
10. **Two-step heteroskedasticity-robust spatial-lag GMM** with 2SLS initial weighting, an updated moment covariance, robust standard errors and an overidentification statistic.\n11. **Kelejian–Prucha spatial-error generalized moments and feasible GLS** using the three innovation moment conditions.

## Run

~~~bash
python -m pip install numpy pytest
python -m pytest -q
~~~

## Scope and limits

- The LM diagnostics calculate classic and Bera–Yoon robust score statistics from an OLS baseline. They do not implement finite-sample corrections, joint tests or model selection. Robust scores are unavailable when their adjustment denominator is not identified.
- All routines use the supplied weights exactly as given. Neighbour construction, row standardisation, islands, alignment and substantive interpretation are modelling decisions for the analyst.
- SLX fits OLS to [X, WX]. SDEM applies the concentrated SEM likelihood to the independent columns of [X, WX]. Neither includes Wy. Redundant WX columns (notably a row-standardised intercept) are dropped and reported with zero spatial-covariate coefficients.
- The spatial lag 2SLS and SDM 2SLS estimators use spatial lags as excluded instruments for Wy; exogeneity and relevance are assumptions, not automatically tested. They do not report standard errors or weak-instrument diagnostics.
- Spatial-lag GMM uses [X, WX, ..., W^qX] as instruments, starts with the 2SLS weighting matrix, then updates it using a heteroskedasticity-robust estimate of the instrument-moment covariance. It reports a robust sandwich covariance and J statistic, but no weak-instrument diagnostics or J-test p-value. It does not accommodate spatially autocorrelated structural errors.\n- Spatial-error GMM implements the homoskedastic-innovation Kelejian–Prucha (1999) three-moment estimator for lambda, followed by feasible GLS. It is not the heteroskedastic extension of Kelejian and Prucha (2010), and its reported GLS covariance relies on the iid innovation variance model.
- The SAR/SEM/SDM ML estimators use conservative norm-bounded parameter intervals and dense log-determinants. SDM drops spatially lagged covariate columns linearly dependent on the included design. SARAR/SAC profiles both spatial parameters over a conservative rectangle using a coarse grid and alternating one-dimensional refinements.
- The impact matrix is \(S_r=(I-\rho W)^{-1}(\beta_r I+\gamma_r W)\). Direct impact is the mean diagonal, total impact is the mean row sum, and indirect impact is total minus direct. Impact uncertainty propagates a supplied joint covariance for [rho, beta..., gamma...] through Monte Carlo; it does not estimate that covariance.
- Proper CAR uses a symmetric non-negative adjacency matrix, no isolated nodes, and the precision τ(D - αA). It is a proper Gaussian CAR regression, not ICAR, BYM/BYM2 or Leroux CAR.
- ICAR simulation uses the singular graph-Laplacian precision τ(D - A), detects connected components, and samples on the component-wise sum-to-zero subspace. It is a field simulator, not a fitted Bayesian regression model.
- Spatial HAC estimates OLS coefficient covariance from distance-weighted residual cross-products using projected planar coordinates and a declared bandwidth. It does not correct endogeneity or spatially lagged outcomes.
- Dense matrices are intended for small teaching cases. These implementations do not provide a complete production inference workflow; use sparse numerical methods and maintained spatial-econometric software for larger or consequential analyses.

Follow the [implementation walkthrough](implementation-walkthrough.md) to trace formulas, validation and tests.

Canonical explanations: [Kelejian–Prucha spatial-error GMM](../../../algorithms/statistics/kelejian-prucha-spatial-error-gmm.md); [spatial LM diagnostics](../../../algorithms/statistics/spatial-lm-diagnostics.md); [spatial impacts](../../../algorithms/statistics/spatial-impacts.md); [impact uncertainty](../../../algorithms/statistics/spatial-impact-uncertainty.md); [spatial lag 2SLS](../../../algorithms/statistics/spatial-lag-2sls.md); [spatial lag GMM](../../../algorithms/statistics/spatial-lag-gmm.md); [concentrated SAR/SEM maximum likelihood](../../../algorithms/statistics/spatial-maximum-likelihood.md); [spatial Durbin 2SLS](../../../algorithms/statistics/spatial-durbin-2sls.md); [spatial Durbin maximum likelihood](../../../algorithms/statistics/spatial-durbin-mle.md); [SARAR/SAC maximum likelihood](../../../algorithms/statistics/spatial-sarar-mle.md); [SLX/SDEM](../../../algorithms/statistics/slx-and-sdem.md); [Gaussian proper CAR](../../../algorithms/statistics/proper-car-gaussian-regression.md); [constrained ICAR Gaussian fields](../../../algorithms/statistics/icar-gaussian-fields.md); [spatial HAC covariance](../../../algorithms/statistics/spatial-hac-covariance.md).

# Spatial econometrics teaching implementations

This package contains small, dense-matrix reference implementations:

1. **Classic and Bera–Yoon robust spatial LM diagnostics** for lag and error dependence.
2. **SAR/SDM direct, indirect and total impact decomposition**, plus Monte Carlo uncertainty propagation from a supplied joint parameter covariance.
3. **Spatial lag 2SLS** using exogenous covariates and spatial lags as instruments for endogenous Wy.
4. **Spatial Durbin 2SLS** with higher-order spatial lags as excluded instruments.
5. **SLX OLS and SDEM concentrated Gaussian ML** for spatially lagged covariates, with and without spatially correlated errors.
6. **Concentrated Gaussian maximum likelihood** for SAR, SEM and SDM, plus joint two-parameter SARAR/SAC likelihood estimation.

## Run

~~~bash
python -m pip install numpy pytest
python -m pytest -q
~~~

## Scope and limits

- The LM diagnostics calculate classic and Bera–Yoon robust score statistics from an OLS baseline. They do not implement finite-sample corrections, joint tests or model selection. Robust scores are unavailable when their adjustment denominator is not identified.
- All routines use the supplied weights exactly as given. Neighbour construction, row standardisation, islands, alignment and substantive interpretation are modelling decisions for the analyst.
- SLX fits OLS to [X, WX]. SDEM applies the concentrated SEM likelihood to the independent columns of [X, WX]. Neither includes Wy. Redundant WX columns (notably a row-standardised intercept) are dropped and reported with zero spatial-covariate coefficients.
- The SDM 2SLS estimator uses higher-order spatial lags as excluded instruments for Wy; exogeneity and relevance are assumptions, not automatically tested. It does not report standard errors or weak-instrument diagnostics.
- The SAR/SEM/SDM ML estimators use conservative norm-bounded parameter intervals and dense log-determinants. SDM drops spatially lagged covariate columns linearly dependent on the included design. SARAR/SAC profiles both spatial parameters over a conservative rectangle using a coarse grid and alternating one-dimensional refinements.
- The impact matrix is \(S_r=(I-\rho W)^{-1}(\beta_r I+\gamma_r W)\). Direct impact is the mean diagonal, total impact is the mean row sum, and indirect impact is total minus direct. Impact uncertainty propagates a supplied joint covariance for [rho, beta..., gamma...] through Monte Carlo; it does not estimate that covariance.
- Dense matrices are intended for small teaching cases. These implementations do not provide a complete production inference workflow; use sparse numerical methods and maintained spatial-econometric software for larger or consequential analyses.

Follow the [implementation walkthrough](implementation-walkthrough.md) to trace formulas, validation and tests.

Canonical explanations: [spatial LM diagnostics](../../../algorithms/statistics/spatial-lm-diagnostics.md), [spatial impacts](../../../algorithms/statistics/spatial-impacts.md), [spatial impact uncertainty](../../../algorithms/statistics/spatial-impact-uncertainty.md), [spatial lag 2SLS](../../../algorithms/statistics/spatial-lag-2sls.md), [concentrated SAR/SEM maximum likelihood](../../../algorithms/statistics/spatial-maximum-likelihood.md), [spatial Durbin 2SLS](../../../algorithms/statistics/spatial-durbin-2sls.md), [spatial Durbin maximum likelihood](../../../algorithms/statistics/spatial-durbin-mle.md), [SARAR/SAC maximum likelihood](../../../algorithms/statistics/spatial-sarar-mle.md), and [SLX/SDEM](../../../algorithms/statistics/slx-and-sdem.md).

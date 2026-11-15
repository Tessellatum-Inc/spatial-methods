# Spatial econometrics teaching implementations

This package contains several small dense-matrix spatial-econometrics components:

1. **Classic and Bera-Yoon robust OLS-based spatial LM diagnostics** for spatial lag and spatial error dependence.
2. **Average impact decomposition** for spatial lag (SAR/SLM) and spatial Durbin (SDM) specifications, with parametric Monte Carlo uncertainty intervals.
3. **Spatial lag 2SLS** using exogenous covariates and their spatial lags as instruments for the endogenous spatially lagged response.
4. **Spatial Durbin 2SLS** with spatially lagged covariates included and higher-order spatial lags used as excluded instruments.
5. **Concentrated Gaussian maximum likelihood** for SAR, SEM and SDM, plus joint two-parameter SARAR/SAC likelihood estimation.

## Run

~~~bash
python -m pip install numpy pytest
python -m pytest -q
~~~

## Scope and limits

- The LM diagnostics calculate classic and Bera-Yoon robust LM-lag/LM-error score statistics from an OLS baseline. They do not implement finite-sample corrections, model selection, or SAR/SEM estimation. Robust scores are reported as unavailable when their adjustment denominator is not identified.
- The LM reference uses the supplied weights exactly as given. Neighbour construction, row standardisation, islands and alignment are modelling decisions that must be resolved before calling it.
- The SLX estimator fits OLS to [X, WX]; the SDEM estimator applies the concentrated SEM likelihood to the independent columns of [X, WX]. Neither includes Wy. Redundant WX columns (notably a row-standardised intercept) are dropped and reported with zero spatial-covariate coefficients.\n- The impact function calculates exact dense-matrix derivatives for a fitted SAR/SDM coefficient set. Its uncertainty companion propagates a supplied joint covariance for [rho, beta..., gamma...] through parametric Monte Carlo draws; it does not estimate that covariance or correct a misspecified sampling model.
- The SDM 2SLS estimator uses higher-order spatial lags as excluded instruments for Wy; exogeneity and relevance are assumptions, not automatically tested. It does not report standard errors or weak-instrument diagnostics.
- The SAR/SEM/SDM ML estimators use a conservative norm-bounded parameter interval and dense log-determinants. SDM drops spatially lagged covariate columns that are linearly dependent on the included design (such as a row-standardised intercept). SARAR/SAC profiles both spatial parameters over a conservative rectangle using a coarse grid and alternating one-dimensional refinements. These estimators do not calculate standard errors or cover the full admissible parameter space.
- The impact matrix is (S_r=(I-\rho W)^{-1}(\beta_r I+\gamma_r W)). Direct impact is the mean diagonal, total impact is the mean row sum, and indirect impact is total minus direct.
- Dense matrices are for small teaching cases. Use sparse numerical methods and a maintained package for real-world estimation.

Follow the [implementation walkthrough](implementation-walkthrough.md) to trace the formulas, validation and tests.

Canonical explanations: [spatial LM diagnostics](../../../algorithms/statistics/spatial-lm-diagnostics.md), [spatial impacts](../../../algorithms/statistics/spatial-impacts.md) and [spatial impact uncertainty](../../../algorithms/statistics/spatial-impact-uncertainty.md), [spatial lag 2SLS](../../../algorithms/statistics/spatial-lag-2sls.md) and [concentrated SAR/SEM maximum likelihood](../../../algorithms/statistics/spatial-maximum-likelihood.md), and [spatial Durbin 2SLS](../../../algorithms/statistics/spatial-durbin-2sls.md) and [spatial Durbin maximum likelihood](../../../algorithms/statistics/spatial-durbin-mle.md), and [SARAR/SAC maximum likelihood](../../../algorithms/statistics/spatial-sarar-mle.md), and [SLX/SDEM](../../../algorithms/statistics/slx-and-sdem.md).

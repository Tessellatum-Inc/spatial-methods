# Spatial econometrics teaching implementations

This package contains several small dense-matrix spatial-econometrics components:

1. **Classic and Bera-Yoon robust OLS-based spatial LM diagnostics** for spatial lag and spatial error dependence.
2. **Average impact decomposition** for spatial lag (SAR/SLM) and spatial Durbin (SDM) specifications.
3. **Spatial lag 2SLS** using exogenous covariates and their spatial lags as instruments for the endogenous spatially lagged response.
4. **Concentrated Gaussian maximum likelihood** for SAR and SEM, with a bounded one-dimensional profile search.

## Run

~~~bash
python -m pip install numpy pytest
python -m pytest -q
~~~

## Scope and limits

- The LM diagnostics calculate classic and Bera-Yoon robust LM-lag/LM-error score statistics from an OLS baseline. They do not implement finite-sample corrections, model selection, or SAR/SEM estimation. Robust scores are reported as unavailable when their adjustment denominator is not identified.
- The LM reference uses the supplied weights exactly as given. Neighbour construction, row standardisation, islands and alignment are modelling decisions that must be resolved before calling it.
- The impact function calculates exact dense-matrix derivatives for a fitted SAR/SDM coefficient set. It does not estimate model coefficients or their covariance.
- The SAR/SEM ML estimators use a conservative norm-bounded parameter interval and dense log-determinants. They do not calculate standard errors or cover the full admissible parameter space.
- The impact matrix is (S_r=(I-\rho W)^{-1}(\beta_r I+\gamma_r W)). Direct impact is the mean diagonal, total impact is the mean row sum, and indirect impact is total minus direct.
- Dense matrices are for small teaching cases. Use sparse numerical methods and a maintained package for real-world estimation.

Follow the [implementation walkthrough](implementation-walkthrough.md) to trace the formulas, validation and tests.

Canonical explanations: [spatial LM diagnostics](../../../algorithms/statistics/spatial-lm-diagnostics.md), [spatial impacts](../../../algorithms/statistics/spatial-impacts.md), [spatial lag 2SLS](../../../algorithms/statistics/spatial-lag-2sls.md) and [concentrated SAR/SEM maximum likelihood](../../../algorithms/statistics/spatial-maximum-likelihood.md).

# Spatial econometrics teaching implementations

This package contains two small dense-matrix building blocks:

1. **Classic OLS-based spatial LM diagnostics** for spatial lag and spatial error dependence.
2. **Average impact decomposition** for spatial lag (SAR/SLM) and spatial Durbin (SDM) specifications.
3. **Spatial lag 2SLS** using exogenous covariates and their spatial lags as instruments for the endogenous spatially lagged response.

## Run

~~~bash
python -m pip install numpy pytest
python -m pytest -q
~~~

## Scope and limits

- The LM diagnostics calculate classic LM-lag and LM-error score statistics from an OLS baseline. They do not implement robust LM variants, finite-sample corrections, model selection, or SAR/SEM estimation.
- The LM reference uses the supplied weights exactly as given. Neighbour construction, row standardisation, islands and alignment are modelling decisions that must be resolved before calling it.
- The impact function calculates exact dense-matrix derivatives for a fitted SAR/SDM coefficient set. It does not estimate model coefficients or their covariance.
- The impact matrix is (S_r=(I-\rho W)^{-1}(\beta_r I+\gamma_r W)). Direct impact is the mean diagonal, total impact is the mean row sum, and indirect impact is total minus direct.
- Dense matrices are for small teaching cases. Use sparse numerical methods and a maintained package for real-world estimation.

Follow the [implementation walkthrough](implementation-walkthrough.md) to trace the formulas, validation and tests.\n\nCanonical explanations: [spatial LM diagnostics](../../../algorithms/statistics/spatial-lm-diagnostics.md), [spatial impacts](../../../algorithms/statistics/spatial-impacts.md) and [spatial lag 2SLS](../../../algorithms/statistics/spatial-lag-2sls.md).

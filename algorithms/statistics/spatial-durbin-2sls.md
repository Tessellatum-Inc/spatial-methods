# Spatial Durbin model by two-stage least squares

**Status:** dense-matrix teaching implementation with deterministic synthetic-recovery and input-validation tests.

## Model

The spatial Durbin model (SDM) is

\[
y=\rho Wy+X\beta+WX\gamma+\varepsilon.
\]

It includes a spatial lag of the outcome and spatial lags of explanatory variables. The coefficients \(\beta\) and \(\gamma\) are not themselves the average direct and indirect effects; feedback through \((I-\rho W)^{-1}\) matters. Use the impact decomposition separately.

## Why instrumental variables are needed

The spatially lagged outcome \(Wy\) is endogenous. The conditional expectation expansion

\[
E[Wy\mid X]=W(I-\rho W)^{-1}X\beta
=WX\beta+\rho W^2X\beta+\rho^2W^3X\beta+\cdots
\]

motivates spatial lags of exogenous covariates as instruments. In the SDM, \(WX\) is already an included regressor, so this implementation uses higher-order spatial lags \(W^2X,W^3X,\ldots\) as excluded instruments for \(Wy\). The instrument matrix also contains all included exogenous regressors \(X\) and the non-redundant columns of \(WX\).

Let \(Z=[Wy,X,WX]\) denote the structural regressor matrix after removing redundant columns, and \(H=[X,WX,W^2X,\ldots,W^qX]\) the instrument matrix after removing linear dependencies. The 2SLS estimator is

\[
\hat\theta=(Z'P_HZ)^{-1}Z'P_Hy,\qquad
P_H=H(H'H)^{-1}H'.
\]

The implementation uses least-squares projections rather than explicitly forming \((H'H)^{-1}\), which is numerically preferable.

## Implementation contract

- 'spatial_durbin_2sls(y, x, weights, instrument_orders=2)' estimates \(\rho,\beta,\gamma\).
- The supplied 'X' must include any desired intercept; the function does not add one.
- Redundant columns of 'WX' and higher spatial lags are removed in stable order. This is important for a row-standardised weights matrix, where \(W\mathbf{1}=\mathbf{1}\).
- 'instrument_orders' must be at least 2 because first-order spatial lags are included in the SDM specification.
- The function rejects non-finite inputs, negative weights, nonzero diagonal weights, rank-deficient 'X', and underidentified projected regressors.
- It reports fitted values, residuals, instrument count and structural regressor count.

The estimator assumes 'X' and its spatial lags are exogenous, and that the excluded higher-order lags are valid and relevant instruments. It does not prove those assumptions, calculate standard errors, diagnose weak instruments, provide overidentification tests, or implement heteroskedasticity/spatial-HAC robust GMM. Dense matrices restrict it to small teaching examples.

## Verification

The tests generate SDM data from known \(\rho,\beta,\gamma\), estimate the model using higher-order spatial instruments, and check approximate recovery, the zero spatial lag of the intercept under row standardisation, output dimensions and finite residuals. Validation tests cover invalid instrument orders, non-finite inputs and collinear regressors. These tests are not a substitute for comparison against a maintained spatial regression package on benchmark datasets.

## Runnable code

- [Implementation](../../implementations/python/spatial-econometrics/spatial_durbin_2sls.py)
- [Tests](../../implementations/python/spatial-econometrics/test_spatial_econometrics.py)
- [Spatial econometrics lab](../../notebooks/spatial-econometrics-lab.ipynb)

## References

- Anselin, L. (1988), *Spatial Econometrics: Methods and Models*, Kluwer Academic Publishers.
- PySAL, [Instrumental Variables Estimation — Spatial Lag Model](https://pysal.org/spreg/notebooks/14_IV_estimation_spatial_lag.html). Explains the use of \(WX,W^2X,\ldots\) as instruments for endogenous \(Wy\).
- PySAL, [GM_Lag API](https://pysal.org/spreg/generated/spreg.GM_Lag.html). Documents spatial two-stage least squares and 'slx_lags', which turns the specification into a Spatial Durbin model.
- LeSage, J. and Pace, R. K. (2009), *Introduction to Spatial Econometrics*, CRC Press.

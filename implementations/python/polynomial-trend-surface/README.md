# Polynomial trend-surface regression

A NumPy implementation of global planar polynomial trend surfaces. It fits
total-degree polynomial bases from degree 0 (constant) through degree 3
(cubic) using least squares, with optional positive observation weights.

Coordinates are centered and scaled before basis construction. The fitted
model exposes coefficients, polynomial term powers, fitted values, residuals,
RMSE and R-squared. Rank-deficient designs are rejected rather than silently
returning an unidentified surface.

Install and test:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Limits

A trend surface models broad global variation; it is not a local interpolator
and does not represent residual spatial autocorrelation. Polynomial degree
and coordinate units matter, and extrapolation outside the sample domain can
be unstable. This baseline does not choose degree by cross-validation,
estimate spatial covariance, provide kriging variance, fit splines, or model
barriers, anisotropy or network distances. Use a projected coordinate system.

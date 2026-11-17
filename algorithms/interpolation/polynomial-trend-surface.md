# Polynomial trend-surface analysis

A polynomial trend surface models broad spatial variation as a global
polynomial in planar coordinates. For total degree d,

```
z(x,y) = sum_{i+j <= d} beta[i,j] x^i y^j + error
```

The implementation supports d = 0, 1, 2 and 3 and estimates coefficients
using ordinary least squares or weighted least squares with positive
observation weights. Coordinates are centered and scaled before constructing
the design matrix. The fitted model reports coefficients, fitted values,
residuals, RMSE and R-squared.

The method is a deterministic global trend estimator, not a local
interpolator. It does not model spatially correlated residuals, estimate a
variogram, produce kriging uncertainty, select polynomial degree
automatically or guarantee stable extrapolation. A rank-deficient design is
rejected.

## Validation

Tests reproduce known constant, linear and quadratic surfaces, including
off-sample prediction; check weighted fitting; verify invariance under
translation and uniform coordinate scaling; and reject unidentifiable
geometries and malformed inputs.

## References

- Cressie, N. (1993). *Statistics for Spatial Data*, revised edition. Wiley.
- Wackernagel, H. (2003). *Multivariate Geostatistics: An Introduction with
  Applications*. 3rd ed. Springer.

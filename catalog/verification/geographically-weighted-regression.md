# Verification — geographically weighted regression

**Status:** Partial implementation of the source-listed local modelling family.

## Implemented and tested

- Fixed and adaptive bandwidth GWR.
- Bisquare and Gaussian spatial kernels.
- Optional nonnegative observation weights.
- Local coefficient, fitted-value and residual outputs.
- Effective local sample size and weighted-design condition diagnostics.
- Rejection of invalid shapes, nonfinite inputs, invalid bandwidths, unsupported kernels and local rank deficiency.

## Independent checks

The test suite uses a synthetic planar grid and an exactly specified global linear surface. Since local weighted least squares must recover the same coefficients for an exactly linear response with a full-rank design, the expected coefficients and fitted values provide a direct oracle. Additional tests cover compact-kernel support, diagnostics, optional observation weights and malformed inputs.

Run from this package directory: python -m pytest -q.

## Not covered

MGWR, GTWR, bandwidth cross-validation, local inference and multiple-testing correction, geographically weighted PCA/summary statistics, general spatially varying-coefficient models, GeoDetector, geographic coordinates and large-data spatial indexing.

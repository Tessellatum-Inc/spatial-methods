# Spatial outlier diagnostics

NumPy-only, small-data reference implementations for exploratory spatial anomaly analysis.

## Methods

- `z_scores`: column-wise population standardisation; constant columns map to zero.
- `spatial_scatter_data`: returns centred observations and their row-standardised spatial lag for a supplied non-negative weights matrix with zero diagonal. This produces data for a Moran-style scatterplot; it does not calculate Moran's I or a p-value.
- `variogram_cloud`: all unique pair distances and half-squared value differences. It is an empirical cloud, not a fitted variogram or formal outlier test.
- `local_outlier_factor`: brute-force Euclidean k-nearest-neighbour LOF. Supply projected coordinates for spatial proximity or other numeric features for feature-space LOF. Complexity is O(n²) memory/time.
- `geographically_weighted_scores`: Gaussian distance-weighted local mean and standardised residual for each point, excluding self. The radius is in the coordinate units.

## Assumptions and limits

Coordinates must be finite, planar/projected values in meaningful linear units. No CRS handling, robust scaling, edge correction, multiple-testing control, automatic bandwidth selection, statistical calibration, isolation forest, or geographically weighted regression is included. Local scores are descriptive and should not be interpreted as calibrated significance tests. Ties in LOF neighbour ordering are deterministic by input index.

## Run

```bash
python -m pytest -q
```

Tests use independent expected values for standardisation, row-standardised spatial lags and pair semivariances, plus synthetic anomaly checks and invalid-input cases.

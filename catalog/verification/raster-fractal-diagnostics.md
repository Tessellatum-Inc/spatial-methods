# Verification dossier: raster fractal diagnostics

## Implemented
- Thresholded binary-support box counting with explicit scales and partial edge boxes.
- Gliding-box binary lacunarity with integral-image window sums, configurable stride and explicit undefined output for empty support.
- Isotropic horizontal/vertical pooled variogram scaling and Hurst slope estimate.

## Independent tests
Tests cover a filled square with exact dimension two, empty support, non-divisible edge dimensions, unit lacunarity for constant full occupancy, undefined empty-support lacunarity, a deterministic linear ramp with H=1, invalid scales, non-finite input and dimensionality.

## Not covered
Multifractal spectra, scale-space theory, MAUP experiments, directional Hurst estimation, multi-origin box-counting, uncertainty intervals and threshold selection. The broad source row remains Partial.

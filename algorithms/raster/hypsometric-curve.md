# Hypsometric curve and integral

## Purpose

A hypsometric curve summarizes how elevation is distributed over a basin or other terrain region. It relates relative elevation to the fraction of region area lying at or above that elevation. The hypsometric integral is a compact summary of the normalized elevation distribution.

## Definitions

For minimum elevation \(z_{\min}\) and maximum elevation \(z_{\max}\), relative elevation is

\[
h_i = \frac{z_i-z_{\min}}{z_{\max}-z_{\min}}.
\]

For a threshold \(h\), the empirical area fraction above it is

\[
A(h)=\frac{\#\{i:h_i\ge h\}}{N},
\]

where \(N\) is the number of selected valid cells. The implementation reports the unique observed relative-elevation thresholds in descending order and the corresponding fraction of cells at or above each threshold.

The hypsometric integral is

\[
HI=\frac{1}{N}\sum_{i=1}^{N}h_i.
\]

For equal-area cells, this mean normalized elevation is the discrete distribution summary associated with the curve.

## Implementation contract

The function hypsometric_curve(elevation, valid_mask=None) returns relative elevation thresholds, area fractions above each threshold, the hypsometric integral, valid-cell count and observed elevation range. Non-finite values are excluded. An optional Boolean mask selects the region. At least two valid cells and positive terrain relief are required. A flat region has no defined relative-elevation normalization and is rejected.

## Assumptions and limitations

The implementation treats every raster cell as equal area. Use a regular projected grid or precompute an area-weighted method for geographic grids and variable-area cells. Basin boundaries and NoData masks determine the sample. The integral is descriptive; it does not independently infer landscape age, tectonic uplift, erosion history or geomorphic stage. Different basin boundaries, DEM resolutions and elevation preprocessing can change the curve.

## Verification

Tests cover exact empirical thresholds and area fractions, valid-mask/NoData selection, invariance to positive vertical affine transformations, invalid masks, insufficient data and zero relief.

# Spatial-block bootstrap for matched raster contrasts

## Purpose

Use spatial blocks, rather than individual raster pixels, as the resampling unit when estimating uncertainty in spatially structured raster comparisons. This reduces the severe pseudo-replication that results from treating neighbouring pixels as independent observations.

This is a reusable method pattern, not a guarantee that blocks are independent or that a bootstrap interval has nominal coverage.

## Estimand

For each scene, compare a target class with a reference class on a common valid support. Where confounding covariates are available, define strata (for example, slope bands and scene-specific radiometric-factor quantiles). Within each spatial block:

1. Retain only strata containing both target and reference observations.
2. Calculate the target-minus-reference difference in the selected metric within each shared stratum.
3. Average the shared-stratum differences equally within the block.
4. Average eligible block contrasts equally to obtain the scene estimate.

Equal weighting at both levels makes the estimand explicit. It is not equivalent to a pooled pixel-weighted difference. Alternative weighting schemes are possible but must be declared before analysis.

## Spatial units and sensitivity

- Assign pixels to a fixed-origin grid in a suitable projected metric CRS.
- Record CRS, grid origin, block dimensions, raster grid, and alignment/resampling rules.
- Evaluate multiple block sizes. The Nairobi R130 study uses 500 m, 1 km and 2 km.
- Check residual spatial autocorrelation and the sensitivity of estimates to block size. A larger block is not automatically independent of its neighbours.

## Bootstrap

Within each scene, resample eligible block contrasts with replacement and calculate the equal-block mean for each replicate. Report the point estimate, percentile interval, eligible block count, replicate count, seed and suppression rule.

The Nairobi R130 implementation uses 2,000 replicates and suppresses intervals with fewer than 20 eligible blocks. Twenty is an exploratory minimum, not a universal adequacy threshold. Repeated random seeds across scene records are used for reproducibility; the per-scene intervals are not a pooled joint confidence interval.

## Residual dependence diagnostics

Where eligible block contrasts occupy a regular grid, calculate a descriptive rook-neighbour Moran's I using only immediately adjacent north/south/east/west eligible blocks. Report the number of eligible blocks and neighbour pairs alongside the statistic. Suppress the statistic below the pre-specified minimum block count or when there are no neighbour pairs or no variation.

This is a diagnostic, not a formal independence test: no p-value is implied, and a low or negative value does not prove independence. Rook adjacency captures only one neighbourhood definition and one spatial scale. Consider variograms, alternative distance bands and sensitivity to block size where the study warrants them. A bootstrap interval should be interpreted cautiously when material positive local autocorrelation remains among block contrasts.

## Multi-scene inference

Do not treat date × burst × polarization records as independent when they share acquisition dates, orbital geometry, processing inputs or spatial footprints. A cross-scene interval requires an explicitly defined target population and a resampling design that respects the crossed or nested dependence structure (for example, date-level and spatial cluster structure). Until justified, report per-scene intervals and descriptive distributions across scenes only.

## Required diagnostics

- Eligible blocks and class sample counts per block.
- Number of matched strata per block.
- Estimate and interval by scene.
- Block-size and covariate-threshold sensitivity.
- Spatial autocorrelation diagnostics and map-based inspection.
- Support loss and interval suppression.
- Explicit statement of whether the target is pixel-weighted, stratum-weighted, block-weighted or scene-weighted.

## Interpretation

Intervals describe variability under the specified block-resampling scheme. They do not establish causal effects, absolute sensor calibration, universal processor equivalence or ground-truth land-cover attribution. Model-derived class labels and uncalibrated confidence scores must be treated as uncertain covariates, not truth.

## Implementations

- [Nairobi R130 implementation](../explorations/radar/spatial_block_uncertainty_nairobi_r130.py)
- [Bootstrap primitives](../explorations/radar/spatial_block_bootstrap.py)
- [Nairobi protocol and current limits](../explorations/radar/NAIROBI_R130_SPATIAL_BLOCK_UNCERTAINTY_PROTOCOL.md)
- [Automated workflow](../.github/workflows/spatial-block-uncertainty-nairobi-r130.yml)

An empirical block-contrast semivariogram can complement Moran's I by summarizing half the mean squared difference between block contrasts over distance-lag bins. Use block-centroid distances and report pair counts for every lag. Treat it as descriptive: sparse bins, irregular eligible-block geometry, anisotropy and nonstationarity can make the curve unstable. Do not infer a dependence range from a single noisy rise or plateau; inspect maps and test sensitivity to lag width and direction.

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

## Contiguous spatial-cluster sensitivity

A complementary sensitivity analysis can aggregate adjacent base blocks into fixed-origin square superblocks, then resample those superblocks with replacement. For each replicate, calculate the ratio of the sampled sum of base-block contrasts to the sampled number of base blocks. This preserves the equal-base-block point estimand even when edge superblocks contain fewer eligible blocks.

The cluster width must be reported in base-block units and converted to ground distance for interpretation. Report eligible base blocks and eligible superblocks separately, along with interval suppression. A cluster-width sensitivity does not prove independence: neighbouring superblocks can remain spatially dependent, and large clusters can leave too few independent resampling units. Do not describe the resulting percentile interval as calibrated without coverage validation or a defensible dependence design. Compare widths and support loss rather than choosing the interval that best supports a preferred conclusion.

The Nairobi R130 experiment tests 2- and 3-base-block supercells with 2,000 replicates. Its minimum eligible-supercell rule is a computational reporting threshold, not a universal statistical guarantee. These results are intended to diagnose how much the independent-base-block interval depends on local grouping.

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

An empirical block-contrast semivariogram complements Moran's I by summarizing half the mean squared difference between block contrasts over distance-lag bins. Use block-centroid distances, express lags in block-width units (also state the corresponding ground-distance scale), and report pair counts for every lag. Retain sparse bins with an explicit status; do not silently treat them as reliable. Treat the curve as descriptive: irregular eligible-block geometry, anisotropy, nonstationarity and support loss can make it unstable. Do not infer a dependence range from a single noisy rise or plateau; inspect maps and test sensitivity to lag width and direction. In the Nairobi R130 implementation, finite-lag pairs are enumerated through local grid-neighbour lookups; the unbounded far-lag bin is calculated analytically from total pairwise semivariance minus near-lag contributions.


## Grid-origin sensitivity

A fixed-origin grid introduces arbitrary boundaries: a small translation can regroup pixels, alter matched-block eligibility and change the block-level estimand. Where conclusions may depend on this choice, repeat block assignment under pre-specified translations (for example, half a block width along each axis and diagonally). Recompute block support, the equal-block estimate and spatial diagnostics for each origin. Keep the unshifted origin as a declared reference and report all offsets in ground-distance units. This is a sensitivity analysis, not a method for selecting the most favourable origin. Stable point estimates do not establish independence; changed estimates indicate that block aggregation and boundary placement materially affect the result.


## Superblock lattice-phase sensitivity

A fixed-origin non-overlapping superblock lattice has an additional arbitrary choice beyond cluster width: its row and column phase relative to the base-block grid. Where this choice could affect uncertainty, enumerate every distinct phase for the chosen square width (for width $k$, there are $k^2$ phases). For each phase:

1. Reassign eligible base blocks to square superblocks using the phase offsets.
2. Record eligible base-block and superblock counts separately.
3. If the superblock count meets the pre-specified minimum, resample superblocks with replacement.
4. Preserve equal weighting of base blocks using the ratio of sampled contrast sum to sampled base-block count, including partial edge superblocks.
5. Record phase offsets, replicate count, seed, interval bounds and suppression status.

The phase enumeration is a sensitivity diagnostic, not a way to choose a favourable lattice. Report the fraction of phase intervals available, the distribution of interval widths, and paired comparisons with the zero-offset reference. The point estimate should remain invariant across phases when the ratio estimator preserves the same equal-base-block estimand; a change indicates a weighting or implementation problem that needs investigation.

In the Nairobi R130 experiment, 2×2 and 3×3 superblocks were evaluated across all phases. The point estimate was invariant, but interval availability was 58.1% and 49.0%, respectively. Median interval-width ratios against the zero-offset phase were near one, while individual ratios showed appreciable variation. These findings reinforce that one fixed lattice phase does not capture the full uncertainty-design sensitivity. See [the phase-aware results](../explorations/radar/nairobi-r130-spatial-cluster-phase-sensitivity-results.md).

This remains exploratory. Enumerating lattice phases does not make superblocks independent, and the minimum cluster count is not a coverage guarantee. A dependence-aware alternative (such as a properly specified moving-block or distance-constrained design) still requires estimand, edge, support and coverage validation before it can be called calibrated.


## Experimental overlapping moving-window bootstrap

An alternative to a non-overlapping superblock lattice is to enumerate overlapping square windows of width $k$ base blocks and sample windows with replacement. A boundary-safe candidate set can be constructed by allowing window origins to extend $k-1$ cells beyond the observed grid. Every eligible base block then belongs to exactly $k^2$ candidate windows, even when the eligible-block mask has holes. This gives equal first-order inclusion probability across eligible blocks and avoids clipping-induced edge under-representation.

For each replicate, sample approximately one window per $k^2$ candidate windows (rounded up). Let $M$ be the number of non-empty candidate windows, $N$ the number of eligible base blocks, and $d=\lceil M/k^2\rceil$ the number of sampled windows. Sum the sampled window contrasts and multiply by $M/(N d k^2)$. Do not divide by the random number of block occurrences. For $N$ eligible blocks and $M$ non-empty candidate windows, each block belongs to exactly $k^2$ windows, so the sum of all candidate-window sums is $k^2\sum_i y_i$. The expected sum of one uniformly sampled window is therefore $k^2\sum_i y_i/M$. With $d=\lceil M/k^2\rceil$ sampled windows, the replicate statistic must be
\[
\hat\mu^* = \frac{M}{N d k^2}\sum_{j=1}^{d} W_j,
\]
not merely $\sum_j W_j/(d k^2)$. The missing factor $M/N$ makes the latter expectation equal to $\sum_i y_i/M$, rather than the equal-block mean $\sum_i y_i/N$. The current implementation applies $M/N$ and tests this identity using a non-zero-mean irregular mask. This normalization fixes the replicate centre; it does not establish interval coverage.
Since every eligible block belongs to exactly $k^2$ candidate windows, the $M/N$ factor is required to convert the average sampled window sum to the equal-block mean, including under irregular masks with variable window sizes. A random occurrence-count denominator can introduce finite-sample weighting bias and must not be used. The windows overlap, so nearby blocks can co-occur in multiple sampled windows. This is intended to carry local spatial dependence into the resampling distribution; it does not guarantee nominal coverage.

The initial implementation is in [spatial_moving_block_bootstrap.py](../explorations/radar/spatial_moving_block_bootstrap.py), with membership and reproducibility tests in [test_spatial_moving_block_bootstrap.py](../explorations/radar/test_spatial_moving_block_bootstrap.py). A first stationary Gaussian AR(1) simulation showed coverage improving as window width increased, but remaining below 0.95 under moderate and strong spatial dependence. See [initial coverage simulation](../explorations/radar/moving-spatial-block-bootstrap-initial-simulation.md) and its reproducible script. This is a warning against treating the method as calibrated.

Before empirical use, extend the simulation to irregular masks, anisotropy, nonstationarity, heavy tails and the matched-strata/block-contrast estimand. Predeclare dependence scales and candidate widths; do not tune the width to the observed Nairobi results. The implementation also suppresses intervals when fewer than 20 eligible base blocks remain, independently of the candidate-window count; a large number of overlapping windows generated from a tiny sample is not treated as adequate support. The method remains experimental until a defensible coverage envelope is demonstrated.


## Experimental spatial HAC alternative

A second candidate estimates uncertainty for the equal-block mean using a spatial heteroskedasticity-and-autocorrelation-consistent (HAC) long-run variance estimator. For eligible block contrasts $y_i$ at grid coordinates $(r_i,c_i)$, let $u_i=y_i-\bar y$ and use the separable product-Bartlett kernel
\[
K_{ij}=\left(1-\frac{|r_i-r_j|}{h_r}\right)_+\left(1-\frac{|c_i-c_j|}{h_c}\right)_+.
\]
The estimated variance of the equal-block mean is
\[
\widehat{\mathrm{Var}}(\bar y)=\frac{1}{N^2}\sum_i\sum_j K_{ij}u_i u_j.
\]
The product of one-dimensional Bartlett kernels is positive semidefinite on the integer lattice; restricting it to an irregular eligible-block subset preserves that property. The implementation reports a normal-approximation interval and accepts separate row and column bandwidths. Bandwidths are sensitivity parameters, not automatically selected or known dependence ranges.

The implementation is [spatial_hac.py](../explorations/radar/spatial_hac.py), with unit tests in [test_spatial_hac.py](../explorations/radar/test_spatial_hac.py) and a reproducible stationary Gaussian coverage experiment in [simulate_spatial_hac.py](../explorations/radar/simulate_spatial_hac.py). The first experiment found empirical coverage of 0.907 at best under weak dependence, 0.813 under moderate dependence and 0.713 under strong dependence; see [spatial HAC results](../explorations/radar/spatial-hac-coverage-results.md). It is not calibrated for inferential use. Results are exploratory until coverage is evaluated across dependence strengths, anisotropy, irregular masks, nonstationarity and the matched-strata/block-contrast estimand. A positive-semidefinite covariance kernel does not guarantee a well-calibrated finite-sample interval. Do not choose bandwidths by selecting the most favourable empirical result.

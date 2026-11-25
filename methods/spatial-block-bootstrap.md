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


## Experimental spatial subsampling alternative

A third candidate uses overlapping fixed-size rectangular subsamples. For each $b\\times b$ subwindow, form $T_b=\\sqrt{b^2}(\\bar y_b-\\bar y_N)$. The empirical distribution of these statistics approximates the full-grid statistic $\\sqrt{N}(\\bar y_N-\\mu)$, so invert its quantiles using $\\sqrt{N}$, not $b$. The first implementation supports complete rectangular grids only and explicitly refuses irregular masks; variable-size subsampling needs a separately justified scaling rule.

See [spatial_subsampling.py](../explorations/radar/spatial_subsampling.py), [tests](../explorations/radar/test_spatial_subsampling.py), [simulation](../explorations/radar/simulate_spatial_subsampling.py) and [coverage results](../explorations/radar/spatial-subsampling-coverage-results.md). The first corrected experiment under-covered at all tested dependence levels (best empirical coverage 0.880, 0.793 and 0.680 for correlations 0.3, 0.6 and 0.8). This remains a comparator, not a calibrated interval.


## Paired comparison of uncertainty candidates

The first paired comparison passes identical stationary Gaussian field realizations to the moving-window percentile bootstrap, product-Bartlett spatial HAC and fixed-size spatial subsampling. All three candidates under-cover, and their Monte Carlo Wilson intervals overlap. See [paired comparison results](../explorations/radar/paired-spatial-uncertainty-comparison-results.md) and the reproducible [comparison script](../explorations/radar/compare_spatial_uncertainty_methods.py). This does not support selecting a winner. The next useful discriminator is directional/anisotropic dependence and then irregular masks, nonstationarity and the actual matched-block estimand.


## Directional dependence diagnostic

The first anisotropic experiment uses separable Gaussian fields with row/column correlations $(0.8,0.3)$ and $(0.3,0.8)$. HAC coverage improves when the longer bandwidth is aligned with the axis of stronger dependence (12 × 4 versus 4 × 12 in the first orientation, and vice versa in the second). This supports retaining separate directional bandwidths as a sensitivity dimension, but the best observed coverage remains below 0.95. See [directional dependence results](../explorations/radar/spatial-uncertainty-anisotropy-results.md) and the reproducible [simulation](../explorations/radar/simulate_spatial_uncertainty_anisotropy.py). Do not interpret the best observed pair as an automatic selector or calibration result.


## Irregular-mask coverage diagnostic

A first mask experiment tests random 20% holes, a single clustered hole, edge truncation with additional holes, and multiple clustered holes. The moving-window and product-Bartlett HAC estimators execute on all these sparse grids, but both continue to under-cover under strong spatial dependence. The fixed-size subsampling implementation explicitly reports irregular masks as unsupported. See [irregular-mask results](../explorations/radar/spatial-uncertainty-irregular-mask-results.md) and [simulation source](../explorations/radar/simulate_spatial_uncertainty_irregular_masks.py). These masks are independent of field values; informative missingness and nonstationarity remain untested.



## Nonstationarity and informative-missingness stress test

A follow-on simulation evaluates whether the mean-interval candidates remain defensible when the field departs from the stationary, independently masked Gaussian designs used above. The finite full-grid mean is the target; all methods receive only eligible cells. Scenarios include a smooth spatial mean gradient, spatially varying variance, an abrupt two-region mean boundary, and a correlated field whose upper tail is selectively removed by a value-dependent eligibility rule. The last scenario deliberately makes missingness informative: the observed-cell mean is not generally the full-grid mean, and the interval methods do not apply a missingness correction.

The experiment uses common realizations across supported methods and records coverage, Wilson Monte Carlo intervals, interval width, estimate bias and eligible-cell counts. Spatial subsampling is expected to refuse the irregular informative-missingness mask under its current complete-grid contract. This is a stress test, not a tuning exercise or a calibration claim. Even good performance in these stylized scenarios would not establish validity for matched-strata block contrasts, informative masks in real imagery, or spatially varying dependence. See [simulation source](../explorations/radar/simulate_spatial_uncertainty_nonstationarity.py) and the [validation workflow](../.github/workflows/spatial-uncertainty-nonstationarity-validation.yml).



## Matched-strata equal-block estimand simulation

The next simulation layer no longer treats block contrasts as directly observed values. Each synthetic block contains multiple shared strata; target and reference observations have unequal sample sizes; target-minus-reference contrasts are estimated within strata; stratum contrasts are averaged equally within block; and eligible blocks are averaged equally in the final estimate. The target for coverage is the finite-population mean of latent equal-stratum block contrasts among blocks with baseline common support.

A second condition removes high-contrast blocks after defining that target population, deliberately introducing informative eligibility. The methods receive only selected blocks, but coverage is assessed against the pre-selection target. Neither candidate applies a missingness correction, so this condition tests selection bias as well as interval behaviour. See [matched-strata equal-block contrast results](../explorations/radar/matched-strata-equal-block-contrast-results.md), [simulation source](../explorations/radar/simulate_matched_strata_equal_block_contrast.py) and [validation workflow](../.github/workflows/matched-strata-equal-block-contrast-validation.yml).

This remains a synthetic design. It is closer to the study estimand than a raw spatial-mean simulation, but it is not a model of Nairobi R130. The current version includes independent Student-t pixel noise with a row-varying scale and spatially varying matched-support quantity; these are stress dimensions, not estimated properties of the Nairobi data. Class-label misclassification and crossed date/burst/polarization dependence remain unmodelled. Do not treat a favourable simulation result as a coverage guarantee or use it to tune the already-reported Nairobi results.

## Synthetic tree/built class-label error sensitivity

A separate sensitivity experiment examines the effect of confusing latent tree and built labels when estimating the trees-minus-built mean absolute residual error contrast. It keeps the equal-stratum-then-equal-block weighting explicit, varies symmetric, asymmetric and spatially varying class-conditional flip rates, and records the shift between the latent-label target and noisy-label estimate together with retained common-support blocks.

This is not a Dynamic World accuracy assessment: confusion rates are assumed, not estimated, and no correction or confidence interval is evaluated. The common-support rule can itself change the retained block population, so support counts must be read with the contrast shifts. See [experiment protocol and results](../explorations/radar/tree-built-label-error-sensitivity.md), [simulation source](../explorations/radar/simulate_tree_built_label_error.py) and [validation workflow](../.github/workflows/tree-built-label-error-validation.yml). Do not interpret its synthetic shifts as Nairobi-specific bias estimates.

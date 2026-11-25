# Nairobi R130 phase-aware superblock bootstrap sensitivity results

**Workflow:** [run 45655099542](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45655099542) — successful  
**Commit:** `9cbe93a514c8152e062acfec0ad89748d1062aee`  
**Artifact:** [nairobi-r130-spatial-block-uncertainty](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45655099542/artifacts/15043905643)  
**Study window:** 2026-10-06 to 2026-11-23  
**Coverage:** 30 date × burst × polarization records; nine block-size/confidence configurations per record; 13 lattice phases per configuration (four for 2×2 superblocks and nine for 3×3 superblocks), totalling 3,510 phase results.

## Question

The earlier contiguous-superblock sensitivity used one fixed superblock lattice origin. That leaves an arbitrary choice: which base blocks are grouped together. This experiment enumerates every distinct row/column phase of the non-overlapping square superblock lattice for widths of two and three base blocks. Every phase resamples eligible superblocks with replacement (2,000 replicates) and suppresses percentile intervals when fewer than 20 eligible superblocks remain.

The underlying scene/configuration point estimate remains the equal-weight mean of eligible base-block contrasts. The bootstrap replicate uses the ratio of sampled contrast sum to sampled base-block count, so partial edge superblocks do not receive the same weight as full superblocks merely because they are one resampling unit.

## Integrity checks

- 30 records × 9 configurations = 270 scene/configuration combinations.
- Every combination contains four 2×2 phases and nine 3×3 phases.
- All 3,510 expected phase entries are present.
- All reported intervals use 2,000 replicates; entries below the 20-superblock threshold are explicitly marked `insufficient_clusters` with zero replicates and null bounds.
- The workflow's block-method test step and complete raster analysis both passed.
- The phase-aware point estimate is invariant across all phases within each scene/configuration, as expected from the preserved equal-base-block estimand.

## Overall results

| Superblock width | Phase results | Intervals reported | Suppressed | Availability | Median eligible superblocks | Median 95% interval width (dB) |
|---:|---:|---:|---:|---:|---:|---:|
| 2×2 base blocks | 1,080 | 628 | 452 | 58.1% | 29 | 0.02682 |
| 3×3 base blocks | 2,430 | 1,190 | 1,240 | 49.0% | 19 | 0.02814 |

The 3×3 design loses more interval availability: 1,240 of 2,430 phases fall below the 20-superblock rule. Only 116 of 270 scene/configuration combinations have intervals available in all nine 3×3 phases; 154 have at least one suppressed phase. For 2×2, 152 of 270 combinations have all four intervals available and 118 have at least one suppressed phase.

Across all valid phase intervals, the median width is 0.02682 dB for 2×2 and 0.02814 dB for 3×3. These pooled medians summarize the collection of scene/configuration/phase intervals; they are not cross-scene inferential summaries.

## Sensitivity by Dynamic World confidence

| Superblock width | DW confidence | Intervals reported | Total phases | Availability | Median interval width (dB) | Median eligible superblocks |
|---:|---:|---:|---:|---:|---:|---:|
| 2×2 | 0.0 | 264 | 360 | 73.3% | 0.01880 | 46 |
| 2×2 | 0.5 | 208 | 360 | 57.8% | 0.02700 | 33 |
| 2×2 | 0.7 | 156 | 360 | 43.3% | 0.05790 | 15 |
| 3×3 | 0.0 | 512 | 810 | 63.2% | 0.01946 | 26 |
| 3×3 | 0.5 | 428 | 810 | 52.8% | 0.02905 | 21 |
| 3×3 | 0.7 | 250 | 810 | 30.9% | 0.05902 | 10 |

Higher Dynamic World confidence thresholds sharply reduce eligible-superblock support and interval availability. The 0.7 threshold is especially fragile under 3×3 grouping: only 250 of 810 phase intervals are reported, and median support is 10 superblocks (below the reporting threshold, hence many phases are suppressed).

## Does lattice phase materially change interval width?

For each scene/configuration, compare every non-zero phase with its zero-offset phase, using only pairs where both intervals exist.

| Width | Paired non-zero-phase comparisons | Median phase/reference interval-width ratio | Minimum–maximum ratio |
|---:|---:|---:|---:|
| 2×2 | 462 | 0.990 | 0.659–1.327 |
| 3×3 | 1,008 | 0.999 | 0.604–1.779 |

The median ratios are close to one, so there is no broad systematic widening or narrowing from changing phase. That does **not** mean phase is irrelevant: individual scene/configuration intervals vary, with 3×3 width ratios ranging from about 0.60 to 1.78 relative to the zero-offset reference. Across each scene/configuration's available phases, the median within-combination range of interval widths is 0.00266 dB for 2×2 and 0.00475 dB for 3×3; the largest ranges are 0.01696 and 0.03715 dB, respectively.

The point estimate itself is exactly invariant across phases in all 270 combinations for each width. Phase sensitivity here is therefore about the uncertainty construction and support, not movement of the estimand.

## Consistency with the earlier fixed-origin cluster run

The zero-offset phase was compared with the earlier fixed-origin superblock interval for the same scene/configuration. For combinations where both intervals were available:

| Width | Paired intervals | Median maximum absolute bound difference (dB) | Maximum bound difference (dB) | Median phase/legacy interval-width ratio |
|---:|---:|---:|---:|---:|
| 2×2 | 160 | 0.000581 | 0.004307 | 1.004 |
| 3×3 | 130 | 0.000635 | 0.005398 | 0.999 |

The small differences are consistent with the two implementations using different deterministic random seeds; they are not evidence of a methodological discrepancy. This is a reproducibility cross-check, not an exact bitwise equality test.

## Interpretation and decision

1. **The point estimand is preserved.** Every phase returns the same scene/configuration estimate because the resampling ratio preserves equal weighting of the eligible base blocks.
2. **The uncertainty interval depends on the arbitrary superblock lattice.** Typical widths are similar across phases, but individual widths can differ materially, particularly for 3×3 clusters.
3. **Support loss is substantial.** Even 2×2 intervals are unavailable in 41.9% of phase outputs; 3×3 intervals are unavailable in 51.0%. Higher confidence thresholds worsen this.
4. **A single fixed phase is not enough.** Reporting only the zero-offset interval hides phase-dependent support and uncertainty. Where this sensitivity matters, report phase availability and interval-width distributions, not only one chosen lattice.
5. **Do not select the phase that gives the narrowest interval or preferred conclusion.** Enumerating phases is a diagnostic of arbitrary grouping, not an optimization procedure.

This does not establish independent superblocks or nominal 95% coverage. Superblocks may remain spatially dependent across their boundaries, and the minimum-20 rule is only an exploratory reporting threshold. The Nairobi scene records also have crossed/repeated date, burst and polarization structure; none of these phase-level results is a pooled cross-scene confidence interval. The experiment does not justify a causal interpretation or a land-cover effect claim.

## Recommended next method work

The fixed-lattice sensitivity has now been quantified. The next methodological step should compare it with a dependence-aware resampling design that does not rely on one non-overlapping lattice phase—for example, a carefully specified moving spatial-block or distance-constrained resampling approach. Such a method needs explicit edge handling, target estimand preservation, support diagnostics, and simulation or other coverage checks before being described as calibrated. Do not promote it merely because it produces wider intervals.

## Reproducibility

- [Main spatial-block uncertainty workflow](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45655099542)
- [Earlier fixed-origin contiguous-superblock results](nairobi-r130-spatial-block-uncertainty-results.md)
- [Grid-origin sensitivity results](nairobi-r130-grid-origin-sensitivity-results.md)
- [Study protocol](NAIROBI_R130_SPATIAL_BLOCK_UNCERTAINTY_PROTOCOL.md)
- [Reusable method](../../methods/spatial-block-bootstrap.md)
- [Implementation](spatial_block_uncertainty_nairobi_r130.py)

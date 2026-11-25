# Nairobi R130 spatial-block uncertainty protocol

## Purpose
Estimate uncertainty around descriptive land-cover residual contrasts without treating spatially dependent pixels as independent replicates.

## Primary contrast
For each scene (date × burst × polarization), compare tree-class MAE with built-class MAE only within the existing matched slope-bin and scene-specific ANF-quartile cells. The scene contrast is the mean of within-cell differences, with cell weighting explicitly specified and sensitivity reported.

## Spatial blocking
1. Use the residual raster's native grid and CRS.
2. Construct a fixed-origin grid of square blocks in metres (recommended primary size 1 km; sensitivity sizes 500 m and 2 km).
3. For geographic grids, transform block assignment using a suitable local metric CRS for Nairobi; do not calculate block dimensions in degrees.
4. Assign each pixel to a block; calculate class MAE within matched slope/ANF strata and block.
5. Retain a block contrast only when it has both built and comparison class samples in the same matched strata. Record class and built counts and number of matched strata.
6. Do not pool pixels across blocks to create an artificially large sample. The resampling unit is the spatial block.

## Bootstrap
- Bootstrap matched blocks with replacement within each scene, preserving scene identity.
- Recompute scene-level contrast for each replicate.
- Report percentile 95% intervals, number of eligible blocks, number of bootstrap replicates (target 2,000), and random seed.
- If a scene has too few eligible blocks for a stable bootstrap, mark its interval as unreliable; do not silently combine scenes to inflate sample size.
- Provide a pooled descriptive estimate across scenes separately from any uncertainty interval. A pooled interval requires a clearly stated target weighting and hierarchical resampling of scenes and blocks.

## Remaining block dependence

For each scene/configuration, retain each eligible block's matched contrast and its row/column on the fixed metric grid. Calculate descriptive rook-neighbour Moran's I from immediately adjacent eligible blocks, and report eligible-block count and neighbour-pair count. Also calculate an empirical block-contrast semivariogram over pre-specified centroid-distance bins; report bin edges, pair counts and semivariance, and flag bins below the minimum pair count. Do not attach p-values or interpret either diagnostic as proof of independence. Inspect residual/block-contrast maps and test sensitivity to lag widths and neighbourhood definitions.

## Sensitivity
Run at 500 m, 1 km, and 2 km block sizes. Also repeat Dynamic World confidence thresholds 0, 0.5, and 0.7. Record support loss and whether the sign and magnitude of contrast are stable.

## Required outputs
JSON with schema/version, block size, metric CRS, bootstrap seed and replicate count, per-scene class contrast, estimate, interval, eligible block count, sample support, threshold, and sensitivity summaries. Include a machine-readable diagnostics section and plain-language limitations.

## Interpretation safeguards
- Spatial blocks are not automatically independent; block-size sensitivity and residual spatial autocorrelation remain necessary.
- Bootstrap intervals describe variability over sampled blocks, not processor absolute calibration or causal land-cover effects.
- Dynamic World labels are predictions and confidence is uncalibrated.
- Terrain slope derives from the DSM and includes surface objects.
- The current matched design controls only coarse slope and ANF bins, not all confounding.
- Do not report pixel-level p-values.
- Suppress or flag intervals where eligible block counts are too small (pre-register a minimum, recommended 20 blocks for exploratory interval reporting; this is a rule of thumb, not a guarantee).

## Implementation status
Implemented in `spatial_block_bootstrap.py` and `spatial_block_uncertainty_nairobi_r130.py`, with unit tests and the `spatial-block-uncertainty-nairobi-r130.yml` workflow. The workflow evaluates 500 m, 1 km, and 2 km blocks at Dynamic World confidence thresholds 0, 0.5, and 0.7, with 2,000 within-scene block-bootstrap replicates and a 20-block interval suppression rule. The current implementation reports per-scene intervals only; it does not produce a pooled cross-scene confidence interval. Outputs are retained as compact JSON artifacts rather than committed raster/data files.

## Current inferential boundary
The 30 scene records are not 30 fully independent replicates: dates, bursts, and polarizations have repeated/crossed structure. Therefore, do not treat a simple resampling of the 30 records as a valid hierarchical bootstrap. A cross-scene interval requires a pre-specified target population and a resampling design that respects date/burst dependence; until that design is justified, report per-scene intervals and descriptive cross-scene distributions only.

## Semivariogram rerun (2026-11-25)

The full 30-scene workflow now emits semivariograms for all nine block-size/confidence configurations. The current exploratory curves show distance-related increases in several configurations but no stable common sill or defensible single dependence range. Far-lag support is sparse in some larger-block/high-confidence subsets. See `nairobi-r130-spatial-block-uncertainty-results.md` for the scene-summary table and interpretation. The independent-block percentile bootstrap remains exploratory; these diagnostics do not calibrate its coverage.

## Contiguous superblock sensitivity (2026-11-25)

A second resampling design is being tested alongside the independent-base-block bootstrap. Eligible base blocks are assigned to fixed-origin square superblocks of 2 or 3 base-block widths. Each replicate samples superblocks with replacement and calculates a ratio of sampled contrast sum to sampled base-block count, preserving equal weighting of the original base blocks despite partial superblocks. The output reports eligible superblocks separately from eligible base blocks and suppresses intervals below 20 eligible superblocks.

This is a sensitivity experiment, not a claim that superblocks are independent. Adjacent superblocks may remain dependent; larger superblocks reduce the number of resampling units and may cause substantial support loss. Compare interval widths, interval availability, and point-estimate preservation across widths. Do not call the intervals calibrated or use the 20-superblock threshold as a universal guarantee. The full raster integration completed successfully in workflow run [45633442093](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45633442093); the artifact was inspected and summarized in `nairobi-r130-spatial-block-uncertainty-results.md`. Cluster intervals are generally wider than the individual-block intervals, while larger clusters reduce interval availability. This remains a sensitivity analysis: adjacent superblocks may still be dependent.

## Grid-origin sensitivity (2026-11-25)

Fixed-origin square grids can change which pixels and matched strata contribute to each block when the origin moves. To expose this arbitrary-boundary sensitivity, the Nairobi implementation repeats block assignment at three pre-specified half-cell shifts: (0.5, 0), (0, 0.5), and (0.5, 0.5) times the block width in EPSG:32737. For each shifted grid it recomputes eligible blocks, the equal-block point estimate, and descriptive rook-neighbour Moran's I. These are geometry/estimand sensitivity summaries only; no shifted-origin bootstrap intervals are calculated in this pass. The unshifted grid remains the reference configuration.

Do not interpret a stable point estimate as proof of independent blocks, or a change in Moran's I as a formal test. The shift experiment diagnoses whether conclusions depend on arbitrary grid alignment. Results are only reported after the full raster workflow artifact has been inspected.

### Completed results

The full raster analysis completed successfully in [workflow run 45643535785](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45643535785), with artifact [15036643524](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45643535785/artifacts/15036643524). The inspected output contains 30 date × burst × polarization records, nine configurations per record, and three shifted-origin results per configuration (810 shifted outputs).

Across configurations, median absolute estimate changes range from 0.0030 to 0.0107 dB. Sign reversals occur in every configuration: 2–13 of the 60–84 valid shifted comparisons, with 2–10 of 30 scene records per configuration showing at least one reversal. The largest absolute change is 0.1437 dB (1 km, confidence 0.5). Median eligible-block counts also change with origin. These results demonstrate that grid alignment can affect scene-level estimates and support; the magnitude and direction are scene/configuration dependent.

The full configuration table and interpretation are in [the grid-origin sensitivity results](nairobi-r130-grid-origin-sensitivity-results.md). These remain point-estimate/support/Moran diagnostics only—not shifted-origin bootstrap intervals, not cross-scene inference, and not a test of block independence. The unshifted grid is retained as the reproducible reference, not asserted to be uniquely correct. Do not select an origin based on preferred results.


## Phase-aware superblock sensitivity (2026-11-25)

The fixed-origin contiguous-superblock experiment has been extended to enumerate every row/column phase of the square superblock lattice: four phases for 2×2 base-block superblocks and nine for 3×3. Each phase uses 2,000 superblock bootstrap replicates when at least 20 eligible superblocks are available. The ratio of sampled contrast sum to sampled base-block count preserves the equal-base-block point estimand for partial edge superblocks.

The full raster analysis completed successfully in [workflow run 45655099542](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45655099542), producing artifact [15043905643](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45655099542/artifacts/15043905643). The inspected artifact contains 30 scene records × 9 configurations × 13 phases = 3,510 phase results. The point estimate is invariant across phases in all scene/configuration combinations, as expected. However, interval availability is 58.1% for 2×2 phases (628/1,080) and 49.0% for 3×3 phases (1,190/2,430). Median interval-width ratios relative to the zero-offset phase are close to one (0.990 and 0.999), but individual ratios range from 0.659–1.327 for 2×2 and 0.604–1.779 for 3×3. Support and interval width therefore depend on the arbitrary grouping phase even when the point estimand is preserved.

See [phase-aware superblock sensitivity results](nairobi-r130-spatial-cluster-phase-sensitivity-results.md) for full summaries and confidence-threshold breakdowns. These are descriptive within-scene sensitivity results, not calibrated intervals or cross-scene inference. The 20-superblock threshold is an exploratory reporting rule, not a guarantee of adequacy; adjacent superblocks may remain dependent. Do not select a lattice phase based on interval width or preferred conclusions.

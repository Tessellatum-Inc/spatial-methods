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

## Status
Protocol specification only. Implementation and validation against the Nairobi study remain pending.

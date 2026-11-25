# Nairobi R130 grid-origin sensitivity results

**Workflow:** [run 45643535785](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45643535785) — successful  
**Commit:** `f188587340001afe42b9cfb3b65962718cb50764`  
**Artifact:** [nairobi-r130-spatial-block-uncertainty](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45643535785/artifacts/15036643524)  
**Study window:** 2026-10-06 to 2026-11-23  
**Coverage:** 30 date × burst × polarization records; nine block-size/confidence configurations per record; three shifted origins per configuration (810 shifted-origin outputs).

## Design

The unshifted grid is the reference. For each 500 m, 1,000 m and 2,000 m block size, membership was recomputed at three half-block translations in EPSG:32737: (0.5, 0), (0, 0.5), and (0.5, 0.5). Each shifted configuration reports eligible blocks, equal-block trees-minus-built MAE contrast, and descriptive rook-neighbour Moran's I. Confidence thresholds are 0, 0.5 and 0.7.

The shifted-origin estimates are point estimates only. No bootstrap intervals were calculated for shifted grids. Comparisons below are made within the same scene and configuration; scene records are not pooled as independent replicates.

## Summary by configuration

The comparison count is the number of non-null baseline-to-shifted estimate pairs across all three shifts. Sign reversals count individual valid shifted comparisons where the estimate changes sign relative to the unshifted estimate. “Scenes with any reversal” counts scene records with at least one of the three shifts reversing sign.

| Block | DW confidence | Baseline estimates | Valid shifted comparisons | Sign reversals | Scenes with any reversal | Median absolute change (dB) | 90th percentile absolute change (dB) | Maximum absolute change (dB) | Median base eligible blocks | Median shifted eligible blocks |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 500 m | 0.0 | 28/30 | 84 | 10 | 6/30 | 0.0030 | 0.0097 | 0.0532 | 231 | 227 |
| 500 m | 0.5 | 26/30 | 78 | 8 | 5/30 | 0.0058 | 0.0154 | 0.0605 | 99 | 95 |
| 500 m | 0.7 | 20/30 | 60 | 7 | 4/30 | 0.0107 | 0.0282 | 0.0514 | 33 | 32 |
| 1,000 m | 0.0 | 28/30 | 84 | 7 | 4/30 | 0.0031 | 0.0108 | 0.0381 | 112 | 111 |
| 1,000 m | 0.5 | 26/30 | 78 | 9 | 7/30 | 0.0076 | 0.0583 | 0.1437 | 62 | 60 |
| 1,000 m | 0.7 | 20/30 | 60 | 2 | 2/30 | 0.0075 | 0.0139 | 0.0223 | 35 | 32 |
| 2,000 m | 0.0 | 28/30 | 84 | 13 | 6/30 | 0.0030 | 0.0118 | 0.0224 | 49 | 53 |
| 2,000 m | 0.5 | 28/30 | 80 | 12 | 10/30 | 0.0073 | 0.0308 | 0.1103 | 35 | 37 |
| 2,000 m | 0.7 | 20/30 | 60 | 4 | 4/30 | 0.0077 | 0.0243 | 0.0319 | 20 | 24 |

Across the full design there are 810 shifted outputs. The table's valid comparison counts are lower where the unshifted or shifted estimate is unavailable; nulls are not treated as zero.

## Interpretation

1. **Grid origin can change the sign of a scene-level contrast.** Sign reversals occur in every block-size/confidence configuration. They are not dominant in every configuration, but they are too frequent to treat the origin as an irrelevant technical choice.
2. **Typical changes are modest, but tails matter.** Median absolute changes range from 0.0030 to 0.0107 dB. The largest observed change is 0.1437 dB at 1 km and confidence 0.5; the 90th percentile in that configuration is 0.0583 dB.
3. **The sensitivity is scene-specific.** Between 2 and 10 of the 30 scene records per configuration have at least one shifted origin that reverses sign. A cross-scene average could conceal these cases.
4. **Eligibility changes too.** Median eligible-block support changes with origin, although the direction is not uniform. A shift can change which pixels and matched strata contribute, not merely relabel an otherwise identical set of blocks.
5. **Higher confidence thresholds thin support.** The number of baseline point estimates falls from 28/30 at confidence 0.0 to 20/30 at 0.7 for 500 m and 1 km. The 2 km, 0.5 configuration has one missing shifted comparison despite 28 baseline estimates.
6. **Moran's I is often unavailable on shifted grids.** The statistic is reported only where the implementation has sufficient eligible blocks and adjacency. It remains descriptive and does not test independence.

## Methodological decision

Treat the unshifted grid as a reproducible reference, not as a uniquely correct partition. Report origin sensitivity alongside block-size, confidence-threshold, and resampling-unit sensitivity whenever scene-level estimates are interpreted. Do not choose the origin that yields the preferred sign, magnitude, Moran's I, or interval. The current experiment does not provide shifted-origin confidence intervals, nor does it establish a dependence-aware resampling scheme.

The combined evidence—grid-origin sign reversals, positive rook-neighbour autocorrelation, semivariogram structure without a stable common range, and wider contiguous-superblock intervals—means the current bootstrap remains exploratory. A subsequent method should investigate spatial moving-block or distance-constrained resampling, while explicitly testing origin and neighbourhood sensitivity. It must not assume that any chosen block or superblock automatically supplies independent units.

## Reproducibility

- [Main spatial-block uncertainty results](nairobi-r130-spatial-block-uncertainty-results.md)
- [Study protocol](NAIROBI_R130_SPATIAL_BLOCK_UNCERTAINTY_PROTOCOL.md)
- [Reusable method](../../methods/spatial-block-bootstrap.md)
- [Implementation](spatial_block_uncertainty_nairobi_r130.py)
- [Workflow](../../.github/workflows/spatial-block-uncertainty-nairobi-r130.yml)

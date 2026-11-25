# Nairobi R130 spatial-block uncertainty results

**Analysis run:** [GitHub Actions run 45627570253](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45627570253)  
**Artifact:** [spatial-block-uncertainty JSON artifact](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45627570253/artifacts/15030370525)  
**Workflow conclusion:** success  
**Study window:** 2026-10-06 to 2026-11-23  
**Records:** 30 date × burst × polarization records  
**Resampling:** 2,000 within-scene block-bootstrap replicates; seed 20261125; minimum 20 eligible blocks for an interval.

## Estimand and sign

The contrast is trees-class MAE minus built-class MAE, in dB, calculated within shared slope/ANF strata and then equally weighted across eligible strata within blocks and across eligible blocks within each scene. Positive values indicate larger processor-comparison MAE in tree-labelled pixels than in built-labelled pixels under this matched estimand. The contrast is descriptive and not a causal land-cover effect.

## Cross-scene descriptive summary

Each row summarizes up to 30 scene records. The median and mean are descriptive summaries of available per-scene point estimates, not pooled pixel estimates or a cross-scene confidence interval. “CI above zero” counts per-scene percentile intervals whose lower endpoint is positive; “crosses zero” includes intervals spanning zero; “below zero” means the upper endpoint is negative. Suppressed intervals are not counted.

| Block | DW confidence | Point estimates | Median (dB) | Mean (dB) | Positive estimates | Available intervals | Above zero | Crosses zero | Below zero | Suppressed |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 500 m | 0.0 | 28/30 | +0.00670 | +0.01026 | 22/28 | 26 | 16 | 9 | 1 | 4 |
| 500 m | 0.5 | 26/30 | +0.01107 | +0.01605 | 19/26 | 20 | 15 | 5 | 0 | 10 |
| 500 m | 0.7 | 20/30 | +0.01368 | +0.01781 | 16/20 | 18 | 7 | 11 | 0 | 12 |
| 1,000 m | 0.0 | 28/30 | +0.00692 | +0.00895 | 21/28 | 26 | 15 | 10 | 1 | 4 |
| 1,000 m | 0.5 | 26/30 | +0.01195 | -0.00083 | 20/26 | 20 | 13 | 7 | 0 | 10 |
| 1,000 m | 0.7 | 20/30 | +0.02571 | +0.03496 | 17/20 | 18 | 9 | 9 | 0 | 12 |
| 2,000 m | 0.0 | 28/30 | +0.00778 | +0.01033 | 22/28 | 20 | 11 | 9 | 0 | 10 |
| 2,000 m | 0.5 | 28/30 | +0.01410 | +0.01369 | 20/28 | 20 | 16 | 4 | 0 | 10 |
| 2,000 m | 0.7 | 20/30 | +0.01518 | +0.02384 | 18/20 | 16 | 8 | 8 | 0 | 14 |

## Interpretation

1. Point estimates are predominantly positive across block sizes and confidence thresholds. The median per-scene contrast ranges from about +0.0067 to +0.0257 dB.
2. Evidence is not uniformly decisive: many per-scene intervals cross zero, and a few are suppressed because fewer than 20 blocks are eligible. At the 0.7 confidence threshold, only 16–18 of 30 scene intervals are available.
3. The 1 km / 0.5 threshold mean is slightly negative despite a positive median and 20/26 positive estimates. This illustrates why the median and distribution should be reported alongside the mean; a small number of large negative estimates influence the mean.
4. Increasing the Dynamic World confidence threshold reduces support. These thresholds select a changing subset of locations and should not be interpreted as a controlled improvement in label accuracy.
5. Block-size sensitivity is material: the number of eligible blocks and interval availability change across 500 m, 1 km and 2 km. No single block size should be selected solely because it produces more intervals excluding zero.

## Limitations

- These are within-scene block-bootstrap intervals, not a joint interval across dates, bursts or polarizations.
- The 30 records share dates, acquisition geometry, geography and processing inputs; they are not independent replicates.
- The 20-block rule is a pragmatic suppression threshold, not a universal guarantee of adequate bootstrap coverage.
- Dynamic World classes and confidence are model-derived covariates, not ground truth or calibrated probabilities.
- Matching is limited to observed shared slope/ANF strata; it does not eliminate all confounding or spatial dependence.
- The contrast concerns relative processor-comparison MAE, not absolute Sentinel-1 calibration, processor interchangeability, or causal effects of land cover.

## Conclusion

The compact rerun completed successfully and reproduced the expected 30 × 9 scene/configuration result structure. The study provides evidence of a generally positive trees-minus-built MAE contrast under the specified matched, block-weighted estimand, but interval overlap, support loss and dependence between scenes limit broader inference. Treat the finding as a study-specific diagnostic requiring independent regional and temporal replication.

## Reproducibility

See the [general spatial-block bootstrap method](../../methods/spatial-block-bootstrap.md), [study protocol](NAIROBI_R130_SPATIAL_BLOCK_UNCERTAINTY_PROTOCOL.md), [implementation](spatial_block_uncertainty_nairobi_r130.py), and [workflow](../../.github/workflows/spatial-block-uncertainty-nairobi-r130.yml).

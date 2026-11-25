# Nairobi R130 spatial-block uncertainty results

**Latest analysis run:** [GitHub Actions run 45629615106](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45629615106)  
**Artifact:** [spatial-block-uncertainty JSON artifact](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45629615106/artifacts/15030018638)  
**Workflow conclusion:** success  
**Study window:** 2026-10-06 to 2026-11-23  
**Records:** 30 date × burst × polarization records  
**Resampling:** 2,000 within-scene block-bootstrap replicates; seed 20261125; minimum 20 eligible blocks for an interval.  
**Spatial dependence diagnostic:** descriptive rook-neighbour Moran's I on the eligible block-level matched contrasts.

## Estimand and sign

The contrast is trees-class MAE minus built-class MAE, in dB, calculated within shared slope/ANF strata and then equally weighted across eligible strata within blocks and across eligible blocks within each scene. Positive values indicate larger processor-comparison MAE in tree-labelled pixels than in built-labelled pixels under this matched estimand. The contrast is descriptive and not a causal land-cover effect.

## Cross-scene descriptive summary

Each row summarizes up to 30 scene records. Median and mean are descriptive summaries of available per-scene point estimates, not pooled pixel estimates or a cross-scene confidence interval. “CI above zero” counts per-scene percentile intervals whose lower endpoint is positive; “crosses zero” includes intervals spanning zero; “below zero” means the upper endpoint is negative. Suppressed intervals are not counted.

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

## Remaining spatial dependence

Moran's I was computed on each scene/configuration's eligible block contrasts, using a binary rook-neighbour graph (north/south/east/west adjacency on the fixed-origin metric block grid). The statistic is descriptive; no permutation distribution or p-value is calculated. Only scene/configurations meeting the 20-block minimum are included below.

| Block | DW confidence | Moran records | Median Moran's I | Mean Moran's I | Positive I |
|---:|---:|---:|---:|---:|---:|
| 500 m | 0.0 | 26 | 0.085 | 0.108 | 23/26 |
| 500 m | 0.5 | 20 | 0.161 | 0.167 | 18/20 |
| 500 m | 0.7 | 18 | 0.063 | 0.082 | 16/18 |
| 1,000 m | 0.0 | 26 | 0.100 | 0.109 | 20/26 |
| 1,000 m | 0.5 | 20 | 0.201 | 0.157 | 14/20 |
| 1,000 m | 0.7 | 18 | 0.161 | 0.180 | 13/18 |
| 2,000 m | 0.0 | 20 | 0.147 | 0.203 | 19/20 |
| 2,000 m | 0.5 | 20 | 0.181 | 0.193 | 19/20 |
| 2,000 m | 0.7 | 16 | 0.221 | 0.231 | 14/16 |

Positive neighbour autocorrelation occurs in most computed scene/configurations. This is evidence that block-level contrasts are not spatially structureless under the chosen rook-neighbour definition. It does **not** establish statistical significance, identify the correct dependence range, or prove that all bootstrap intervals are invalid. It does mean the independent-block resampling assumption is not adequately justified by the block-size choice alone. In particular, percentile intervals may be too narrow where positive dependence remains.

The diagnostic is intentionally conservative in interpretation: no p-value is reported, and rook adjacency is only one neighbourhood definition. A more complete assessment should examine residual/block-contrast maps, empirical variograms or correlograms, alternative distance bands, and larger spatial resampling units. Sensitivity to block size is not a substitute for estimating the dependence range.

## Interpretation

1. Point estimates are predominantly positive across block sizes and confidence thresholds. The median per-scene contrast ranges from about +0.0067 to +0.0257 dB.
2. Evidence is not uniformly decisive: many per-scene intervals cross zero, and some are suppressed because fewer than 20 blocks are eligible.
3. Increasing the Dynamic World confidence threshold reduces support. These thresholds select a changing subset of locations and should not be interpreted as a controlled improvement in label accuracy.
4. The dependence diagnostic finds positive rook-neighbour Moran's I in most scene/configurations. This weakens the case for treating eligible blocks as independent resampling units and requires more spatial-dependence analysis before interpreting the percentile intervals as calibrated uncertainty.
5. Block-size sensitivity is material: eligible block counts, interval availability and Moran's I all change across 500 m, 1 km and 2 km. No single block size should be selected solely because it produces more intervals excluding zero or a lower Moran's I.

## Limitations

- These are within-scene block-bootstrap intervals, not a joint interval across dates, bursts or polarizations.
- The 30 records share dates, acquisition geometry, geography and processing inputs; they are not independent replicates.
- Rook-neighbour Moran's I is a descriptive local diagnostic with no p-value; it does not establish independence or the full spatial dependence range.
- The 20-block rule is a pragmatic suppression threshold, not a universal guarantee of adequate bootstrap coverage.
- Dynamic World classes and confidence are model-derived covariates, not ground truth or calibrated probabilities.
- Matching is limited to observed shared slope/ANF strata; it does not eliminate all confounding or spatial dependence.
- The contrast concerns relative processor-comparison MAE, not absolute Sentinel-1 calibration, processor interchangeability, or causal effects of land cover.

## Conclusion

The latest compact rerun completed successfully and produced 30 scene records with nine block-size/confidence configurations each. It confirms a generally positive trees-minus-built MAE point contrast under the specified matched, block-weighted estimand. However, the new diagnostic shows positive local autocorrelation among block contrasts in most computed scene/configurations. The current block bootstrap should therefore remain exploratory: its resampling units are spatially separated by a chosen grid size, but they are not demonstrably independent. We should not promote the percentile intervals as calibrated uncertainty until the dependence range and a suitable spatial resampling design have been examined.

## Reproducibility

See the [general spatial-block bootstrap method](../../methods/spatial-block-bootstrap.md), [study protocol](NAIROBI_R130_SPATIAL_BLOCK_UNCERTAINTY_PROTOCOL.md), [implementation](spatial_block_uncertainty_nairobi_r130.py), and [workflow](../../.github/workflows/spatial-block-uncertainty-nairobi-r130.yml).

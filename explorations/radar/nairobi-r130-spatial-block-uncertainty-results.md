# Nairobi R130 spatial-block uncertainty results

**Latest analysis run:** [GitHub Actions run 45632101713](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45632101713)  
**Artifact:** [spatial-block-uncertainty JSON artifact](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45632101713/artifacts/15031388245)  
**Workflow conclusion:** success  
**Study window:** 2026-10-06 to 2026-11-23  
**Records:** 30 date × burst × polarization records  
**Resampling:** 2,000 within-scene block-bootstrap replicates; seed 20261125; minimum 20 eligible blocks for an interval.  
**Spatial dependence diagnostics:** descriptive rook-neighbour Moran's I and empirical block-contrast semivariograms on eligible block-level matched contrasts.

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

## Empirical block-contrast semivariograms

The successful rerun (workflow run 45632101713; artifact 15031388245) adds empirical semivariograms for all 30 scene records and nine block-size/confidence configurations. The semivariance is 0.5 × mean((z_i − z_j)^2) for block-level matched contrasts, in dB². Distances are between block-grid centroids and are expressed in block-width units. Each table cell gives the median semivariance across scenes with at least 10 pairs in that lag bin; the parenthetical value is the number of scenes contributing. These are descriptive medians, not pooled estimates.

| Block | DW confidence | 0–1.5 | 1.5–2.5 | 2.5–4.5 | 4.5–8.5 | 8.5–16.5 | 16.5+ |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 500 m | 0.0 | 0.00408 (26) | 0.00468 (26) | 0.00514 (26) | 0.00534 (26) | 0.00487 (26) | 0.00442 (26) |
| 500 m | 0.5 | 0.00666 (20) | 0.00708 (20) | 0.00729 (20) | 0.00714 (20) | 0.00729 (20) | 0.00833 (20) |
| 500 m | 0.7 | 0.01154 (20) | 0.01596 (18) | 0.01341 (20) | 0.01288 (20) | 0.01491 (18) | 0.01508 (20) |
| 1,000 m | 0.0 | 0.00186 (26) | 0.00186 (26) | 0.00219 (26) | 0.00244 (26) | 0.00255 (26) | 0.00298 (26) |
| 1,000 m | 0.5 | 0.00369 (20) | 0.00433 (20) | 0.00435 (20) | 0.00403 (20) | 0.00492 (20) | 0.00535 (20) |
| 1,000 m | 0.7 | 0.01113 (20) | 0.01351 (20) | 0.01137 (20) | 0.01244 (18) | 0.01400 (20) | 0.01744 (20) |
| 2,000 m | 0.0 | 0.00110 (26) | 0.00123 (26) | 0.00156 (26) | 0.00179 (26) | 0.00197 (20) | 0.00168 (18) |
| 2,000 m | 0.5 | 0.00244 (20) | 0.00293 (20) | 0.00321 (20) | 0.00319 (20) | 0.00338 (20) | 0.00303 (12) |
| 2,000 m | 0.7 | 0.00288 (18) | 0.00311 (18) | 0.00320 (18) | 0.00371 (18) | 0.00609 (16) | — (0) |

Interpretation:

1. Several configurations show increasing semivariance with distance beyond the first-neighbour bin. The clearest examples are 1 km at confidence 0.0 and 2 km at confidence 0.0/0.5. This is consistent with spatial structure extending beyond immediate rook neighbours.
2. The curves do not share a stable, clear sill or plateau. Some rise and then flatten or decline; higher-confidence subsets have sparse and uneven support. There is no defensible single dependence range to read off these curves.
3. The distance bins are in block widths, so the same lag represents different ground distances at 500 m, 1 km and 2 km. The changing support and geometry also mean these curves should not be compared as if they came from one fixed sampling design.
4. The final 16.5+ bin is particularly sparse for 2 km at confidence 0.5 and unavailable at confidence 0.7. Do not interpret its medians as stable long-range behaviour.
5. Semivariogram medians are not a formal test of dependence and do not calibrate bootstrap coverage. Together with positive rook-neighbour Moran's I, they strengthen the case for caution but do not prove a specific range or quantify interval undercoverage.

The semivariogram implementation was optimized to enumerate only finite-lag grid neighbours; the unbounded final bin is computed from the total pairwise semivariance minus the enumerated near-lag contribution. This avoids quadratic enumeration of all distant pairs. The full raster workflow and all method tests passed on commit de5f100.

## Interpretation

1. Point estimates are predominantly positive across block sizes and confidence thresholds. The median per-scene contrast ranges from about +0.0067 to +0.0257 dB.
2. Evidence is not uniformly decisive: many per-scene intervals cross zero, and some are suppressed because fewer than 20 blocks are eligible.
3. Increasing the Dynamic World confidence threshold reduces support. These thresholds select a changing subset of locations and should not be interpreted as a controlled improvement in label accuracy.
4. Positive rook-neighbour Moran's I remains common, and semivariograms show distance-related structure beyond the nearest-neighbour bin in several configurations. No stable common dependence range or sill is established; the bootstrap intervals remain exploratory.
5. Block-size sensitivity is material: eligible block counts, interval availability and Moran's I all change across 500 m, 1 km and 2 km. No single block size should be selected solely because it produces more intervals excluding zero or a lower Moran's I.

## Limitations

- These are within-scene block-bootstrap intervals, not a joint interval across dates, bursts or polarizations.
- The 30 records share dates, acquisition geometry, geography and processing inputs; they are not independent replicates.
- Rook-neighbour Moran's I and empirical semivariograms are descriptive diagnostics with no p-values; neither establishes independence, a unique dependence range or bootstrap coverage.
- The 20-block rule is a pragmatic suppression threshold, not a universal guarantee of adequate bootstrap coverage.
- Dynamic World classes and confidence are model-derived covariates, not ground truth or calibrated probabilities.
- Matching is limited to observed shared slope/ANF strata; it does not eliminate all confounding or spatial dependence.
- The contrast concerns relative processor-comparison MAE, not absolute Sentinel-1 calibration, processor interchangeability, or causal effects of land cover.

## Conclusion

The latest rerun completed successfully and produced 30 scene records with nine block-size/confidence configurations each. It confirms a generally positive trees-minus-built MAE point contrast under the specified matched, block-weighted estimand. Moran's I indicates common positive local autocorrelation, while the semivariograms show distance-related increases in several configurations but no stable common sill or defensible dependence range. The current block bootstrap therefore remains exploratory: the chosen grid blocks are not demonstrably independent, and the percentile intervals must not be presented as calibrated uncertainty. The next method step is to test spatially constrained resampling designs against these observed dependence patterns, not to select a block size by whichever gives the narrowest interval.

## Reproducibility

See the [general spatial-block bootstrap method](../../methods/spatial-block-bootstrap.md), [study protocol](NAIROBI_R130_SPATIAL_BLOCK_UNCERTAINTY_PROTOCOL.md), [implementation](spatial_block_uncertainty_nairobi_r130.py), and [workflow](../../.github/workflows/spatial-block-uncertainty-nairobi-r130.yml).

# Sentinel-1 independent-orbit validation experiment

## Purpose

The first Nairobi comparison used Sentinel-1 descending relative orbit 79 (R079). Its leave-one-acquisition-out test only transferred between dates from the same study area, orbit, provider and processing configuration. This experiment seeks a genuinely different viewing geometry without pretending that a partial-footprint acquisition covers the entire Nairobi rectangle.

This is an independent-orbit diagnostic, not an independent-site validation and not a calibration exercise.

## Catalogue discovery

A Sentinel Hub Catalog API search was run for Sentinel-1 IW GRD over the Nairobi search rectangle `[36.65, -1.45, 37.05, -1.15]`, from 2026-10-01 through 2026-11-23. The screen retrieved 13 catalogue features and grouped them by orbit direction and relative orbit.

| Track | Catalogue acquisitions | AOI intersection fraction | Full-AOI items |
|---|---:|---:|---:|
| Ascending R057 | 5 | 0.7464–0.7475 | 0 |
| Ascending R130 | 4 | 0.8422–0.8436 | 0 |
| Descending R079 baseline | 4 | 1.0000 | 4 |

The ascending R130 acquisitions are dated 6 Oct, 18 Oct, 30 Oct and 11 Nov 2026, with 12-day repeat cadence. R130 is selected for the first alternate-orbit experiment because it offers the largest repeated footprint among the independent tracks. R057 remains a secondary candidate.

The catalogue screen intentionally rejected both ascending tracks as full-AOI candidates. Their partial footprints are not silently promoted to full coverage.

Machine-readable discovery evidence: GitHub Actions run [45163484983](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45163484983), artifact `sentinel1-nairobi-orbit-diversity-screen`.

## Partial-coverage experiment design

The R130 experiment uses the same requested Nairobi bbox and output dimensions as the R079 baseline. It:

1. Selects repeated ascending R130 acquisitions whose catalogue footprint intersects at least 80% of the requested rectangle.
2. Requests ellipsoid gamma0 and terrain-corrected gamma0 separately for each acquisition.
3. Preserves provider `dataMask` values and compares only pixels valid in both branches.
4. Reports each date's paired-valid fraction and the intersection of valid pixels across all dates.
5. Runs the same scattering-area relation and residual diagnostics on the R130 acquisitions.

No missing pixels are filled, extrapolated, or treated as observations. A common requested grid does not establish sub-pixel co-registration. The R130 subset may be spatially selective; conclusions must be scoped to its actual common-valid footprint.

Processing workflow: [Sentinel-1 Nairobi alternate-orbit RTC experiment](https://github.com/Tessellatum-Inc/spatial-methods/blob/main/.github/workflows/sentinel1-alternate-orbit.yml).

## Interpretation boundaries

- A result on R130 would test transfer across relative orbit at one Nairobi site. It would not establish transfer to another site, DEM, provider or sensor.
- The local-incidence-angle and scattering-area distributions differ by orbit. The R130 analysis must be interpreted within its own geometry, not pooled blindly with R079.
- A successful area-factor fit on R130 would still be an empirical relationship, not proof of radiometric equivalence or a validated correction.
- Independent stable reference targets and geodetic/radiometric validation remain outstanding.
- Keep `analysis_ready: false`. Do not normalize the temporal stack or use this relationship for change detection.

## Current status

Catalogue discovery succeeded and selected R130 for the partial-coverage experiment. The first processing workflow run using the initial catalogue filter failed with HTTP 400; the filter was simplified to the documented IW constraint and orbit selection is now performed locally from returned metadata. The corrected processing run is [45163757264](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45163757264); its completion and QA artifact must be checked before scientific conclusions are drawn.


## R130 processing results (2026-11-23)

The corrected partial-coverage processing workflow completed successfully in [run 45163757264](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45163757264). A duplicate rerun on the subsequent workflow-only commit also completed successfully in [run 45163774292](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45163774292).

- Four of four R130 acquisitions processed; zero failures.
- Per-scene paired ellipsoid/RTC valid fractions: 0.84220, 0.84189, 0.84301 and 0.84247.
- The report's all-date common valid fraction is 0.84189 of the requested grid (2,648,363 pixels).
- RTC shadow-mask fraction was zero in each acquisition.
- The paired comparison completed for VV and VH, with status `paired_diagnostic_only`.

Mean per-scene area-factor relation diagnostics across the four dates:

| Polarization | OLS slope | Mean R² | Mean median residual offset (dB) | Mean centered P95 absolute residual (dB) |
|---|---:|---:|---:|---:|
| VV | 0.99421 | 0.97837 | -0.01016 | 0.13907 |
| VH | 0.99428 | 0.97847 | -0.00975 | 0.13918 |

Leave-one-acquisition-out temporal screening on R130 showed a small further benefit from angle terms:

| Polarization | Metric | Area only | Area + angle + interaction | Reduction |
|---|---|---:|---:|---:|
| VV | RMSE (dB) | 0.08421 | 0.08287 | 1.60% |
| VV | MAE (dB) | 0.07263 | 0.07129 | 1.85% |
| VV | P95 absolute error (dB) | 0.13935 | 0.13734 | 1.44% |
| VH | RMSE (dB) | 0.08412 | 0.08279 | 1.59% |
| VH | MAE (dB) | 0.07254 | 0.07121 | 1.84% |
| VH | P95 absolute error (dB) | 0.13944 | 0.13737 | 1.48% |

## Cross-orbit interpretation

The R130 results support the usefulness of scattering area as a strong empirical explanatory variable beyond the original R079 sequence. However, the relationship is not coefficient-invariant:

- R079 had an approximate median residual offset of +0.282 dB and mean OLS slope near 0.983.
- R130 has mean median residual offset near -0.010 dB and mean OLS slope near 0.994.

The approximately 0.29 dB offset difference is material. It means a correction calibrated on R079 cannot simply be transferred to R130 with the same intercept. The R130 result is also confounded by orbit direction and platform: R079 was descending Sentinel-1C, while R130 was ascending Sentinel-1D. This is independent acquisition geometry, but not a controlled isolation of relative-orbit effects.

The correct conclusion is therefore narrower: the area-factor relationship remains strong across these two acquisition configurations, while its fitted offset and slope vary. Do not pool the two tracks or apply one universal correction. A next experiment should separate platform from orbit direction where possible, and add independent stable reference targets/geodetic control.

The R130 QA artifact is attached to workflow run [45163757264](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45163757264), artifact `sentinel1-nairobi-alternate-orbit-qa`. The raster artifact is retained separately for 14 days.

The status remains `analysis_ready: false`; no normalization or change detection is authorized by these diagnostics.

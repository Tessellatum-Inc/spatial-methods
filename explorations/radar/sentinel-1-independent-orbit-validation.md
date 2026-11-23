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


## Same-platform ascending R057/R130 comparison (2025 acquisitions)

To remove the Sentinel-1C versus Sentinel-1D platform difference in the 2026 R079/R130 comparison, a second paired experiment selected four ascending Sentinel-1A acquisitions on each of R057 and R130 in January–February 2025. Both tracks were processed with the same ellipsoid and RTC code, DEM, oversampling, requested grid and time window. The comparison was then recomputed on the exact intersection of all eight ellipsoid and RTC data masks.

The common mask contains **1,848,662 pixels (58.77% of the requested grid)**. Mean per-scene diagnostics on that same footprint:

| Track | Median local angle | OLS slope | R² (VV / VH) | Area-factor residual | Local-angle proxy term | Proxy-adjusted median residual | Direct RTC − ellipsoid median / MAE / P95 abs |
|---|---:|---:|---:|---:|---:|---:|---:|
| Ascending R130, Sentinel-1A | 45.95° | 0.992 | 0.986 / 0.986 | -0.053 dB | -0.144 dB | +0.073 dB | +0.021 / 0.301 / 1.035 dB |
| Ascending R057, Sentinel-1A | 32.56° | 0.982 | 0.976 / 0.976 | +2.053 dB | +1.948 dB | +0.078 dB | +0.014 / 0.337 / 1.157 dB |

The offset difference persists on identical pixels and is consistent across all four dates and both polarizations. The per-track residual/local-incidence-angle correlations are weak (about -0.05 for R130 and -0.08 for R057). However, the two tracks' central 80% local-incidence-angle ranges barely overlap: approximately 43.3–49.0° for R130 and 29.9–35.6° for R057. Orbit identity and incidence-angle regime therefore remain confounded. These results cannot isolate an orbit effect or an incidence-angle effect.

The unusually large and stable +2.05 dB R057 offset is a diagnostic flag, not a correction coefficient. Before physical interpretation, verify the provider's scattering-area definition and whether any track-dependent processing convention or product metadata explains the difference. Do not transfer an intercept, pool the tracks, or normalize the imagery.

Reproducibility:
- The paired R057/R130 processing artifacts came from successful [workflow run 45165312108](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45165312108).
- The identical-footprint calculation and per-scene angle diagnostics completed successfully in [workflow run 45168656320](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45168656320).
- The test suite for the shared-footprint comparator passed in [Python examples run 45168656390](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45168656390).

## Angle-proxy diagnostic and next validation step

The common-mask comparator was extended to report the direct RTC-minus-ellipsoid difference and a local-angle proxy term, `-10 log10(tan(localIncidenceAngle))`. This proxy makes the two tracks' median residuals look similar:

| Track | Median area-factor residual | Median local-angle proxy term | Median proxy-adjusted residual | Median direct RTC − ellipsoid |
|---|---:|---:|---:|---:|
| Sentinel-1A ascending R057 | +2.053 dB | +1.948 dB | +0.078 dB | +0.014 dB |
| Sentinel-1A ascending R130 | −0.053 dB | −0.144 dB | +0.073 dB | +0.021 dB |

This is a useful consistency clue, not a validated physical correction. The available RTC `localIncidenceAngle` is measured relative to the **local terrain normal**. The reference-area equation requires ellipsoid incidence angle θE. Substituting the local terrain angle pixel-by-pixel is not justified: mean absolute residual worsens on R130 (about 0.064 to 0.295 dB) and remains large on R057 (about 2.054 to 0.323 dB); P95 absolute proxy-adjusted residuals remain around 1.0–1.1 dB. Direct RTC-minus-ellipsoid differences have mean absolute magnitudes around 0.30–0.34 dB and P95 absolute magnitudes around 1.03–1.16 dB.

A wider Sentinel-1A catalogue screen across both orbit directions, 2025-01-01 through 2026-11-23, with at least four scenes and at least 50% Nairobi AOI overlap found only the already tested ascending R057 and R130 tracks. It found no additional intermediate-angle candidate under those filters ([run 45169939031](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45169939031)). This does not rule out tracks outside the date, platform, direction or overlap filters.

The next discriminating step is therefore to obtain the **ellipsoid incidence angle** independently rather than process more tracks or substitute the terrain angle. The Sentinel-1 product specification defines `incidenceAngle` in each `geolocationGridPoint` record alongside source image line/pixel and geodetic coordinates. The catalogue asset inventory identified the exact source GRD products and S3 prefixes for the eight R057/R130 acquisitions ([inventory run 45169844808](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45169844808)). The catalogue exposes only a `data` COG asset; the annotation XML objects must be listed through the separate CDSE S3 workflow.

That prepared workflow requires CDSE S3 access credentials, separate from the existing Sentinel Hub OAuth credentials. The user must generate an S3 access key and secret in CDSE and add them to GitHub Actions secrets as `CDSE_S3_ACCESS_KEY` and `CDSE_S3_SECRET_KEY`. Do not paste the secrets into chat or commit them. Once configured, list only the small annotation XML and manifest objects, extract/interpolate `incidenceAngle` to the shared output grid, validate interpolation against the source geolocation points, and evaluate the complete reference-area equation on common valid pixels.

No stable radiometric reference or independent geodetic control has been established. Keep `analysis_ready: false`; do not normalize the time series or use the results for change detection.


## Source GRD incidence-angle extraction and pixel-level reference-area test (2026-11-23)

The CDSE S3 credentials were configured as repository secrets. The annotation inventory completed successfully: eight original Sentinel-1A GRD products were inspected and 64 annotation/calibration/RFI XML objects were located (eight per product). The VV product annotation XML was then extracted for each acquisition. Each source geolocation grid contains 210 complete tie points arranged as 10 azimuth lines by 21 range pixels.

The source product `incidenceAngle` values were linearly interpolated in geographic coordinates onto the fixed 2048 × 1536 Nairobi grid. No extrapolation was used. Five-fold interleaved tie-point holdout diagnostics were:

| Track | Tie-point CV MAE | CV RMSE | CV P95 absolute error | Interpolated AOI coverage |
|---|---:|---:|---:|---:|
| R057 | 0.00844° | 0.01277° | 0.02529° | 77.3% |
| R130 | 0.00737° | 0.00943° | 0.01922° | 94.7% |

Uncovered output pixels remain NoData. Intersecting all eight angle rasters with the eight ellipsoid/RTC data masks leaves a common footprint of **1,848,662 pixels (58.77% of the requested grid)**.

### Full reference-area equation

The source GRD geolocation-grid incidence angle, rather than the RTC terrain-relative `localIncidenceAngle`, was used as the ellipsoid reference angle `θE`. The tested relation is:

\[
\Delta_{dB}
=10\log_{10}\left(\frac{\gamma^0_{RTC}}{\gamma^0_E}\right)
=-10\log_{10}(\widehat A_\gamma)-10\log_{10}(\tan\theta_E).
\]

This follows the reference-area definitions described in the Sentinel Hub RTC documentation and the RTC method literature cited above. The Sentinel-1 product specification defines `incidenceAngle` in each `geolocationGridPoint` alongside the source image line/pixel and geodetic coordinates ([ESA Sentinel-1 Product Specification](https://sentiwiki.copernicus.eu/__attachments/1673968/S1-RS-MDA-52-7441%20-%20Sentinel-1%20Product%20Specification%202025%20-%203.16.1.pdf?inst-v=ece54fea-0304-4b72-9f89-45b672ef46c2)).

Mean metrics across four acquisitions and both polarizations on the identical eight-scene common footprint:

| Track | Median θE | Area-only residual MAE | Median ellipsoid reference-area term | Adjusted residual median | Adjusted residual MAE | Adjusted residual P95 abs |
|---|---:|---:|---:|---:|---:|---:|
| Sentinel-1A ascending R057 | 31.925° | 2.054 dB | +2.055 dB | −0.00176 dB | 0.00174 dB | 0.00309 dB |
| Sentinel-1A ascending R130 | 45.375° | 0.0639 dB | −0.05695 dB | +0.00420 dB | 0.00436 dB | 0.00578 dB |

The pixel-level residual after including the ellipsoid reference-area term is extremely small and consistent across all four dates and both VV/VH polarizations. On R057, the area-only residual MAE falls from about 2.054 dB to 0.00174 dB; on R130 it falls from about 0.0639 dB to 0.00436 dB. The adjusted median and error quantiles are similarly stable across all eight date/polarization combinations.

This is strong empirical support for the complete reference-area relation **within these Sentinel Hub processing branches and this Nairobi study area**. It also explains why the area-only residual differed between R057 and R130: their median source ellipsoid incidence angles differ by about 13.45°. The earlier local-angle-only proxy is superseded for this equation; the terrain-relative local angle is not a substitute for θE.

### Scope and remaining validation

- The common valid footprint is only 58.77% of the requested AOI; the result applies to this shared subset, not the whole requested grid.
- Five-fold tie-point validation is internal to each source annotation grid. It is not independent geodetic control.
- Both tracks use the same Sentinel-1A platform, Nairobi site, provider, processing configuration and reference-area convention. This is not independent-site or cross-provider validation.
- The source angle interpolation is sparse-grid interpolation; the reported tie-point errors do not establish absolute geolocation accuracy.
- Stable radiometric reference targets and independent geometric control remain unestablished.

Reproducibility:
- Annotation inventory: [workflow run 45198522746](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45198522746).
- Eight source geolocation grids: [workflow run 45199797385](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45199797385).
- Interpolation and full common-footprint equation test: [workflow run 45201769040](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45201769040).
- Targeted parser/interpolation/comparator tests: [Python examples run 45201796311](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45201796311).

The result does **not** authorize operational normalization, change detection or setting `analysis_ready: true`. The equation is now strongly supported as a description of this provider's RTC/ellipsoid relationship; independent reference-target and cross-site validation are still required before generalization.

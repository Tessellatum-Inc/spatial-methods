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

# Surat R009: ellipsoid-to-terrain gamma-zero relation

## Question

For the same Sentinel-1 GRD acquisition, can the difference between Sentinel Hub's
`GAMMA0_TERRAIN` and `GAMMA0_ELLIPSOID` outputs be explained by the normalized
scattering-area factor and the ellipsoid incidence angle?

This is a focused method-validation case study, not a general radiometric
correction recipe.

## Derivation

For ellipsoid-normalized gamma nought, the standard backscatter convention is

`gamma0_ellipsoid = beta0 * tan(theta_E)`

where `theta_E` is incidence angle relative to the reference ellipsoid.

For terrain-normalized gamma nought, the terrain-normalization factor can be
written as

`gamma0_terrain = beta0 / A_gamma_normalized`

where `A_gamma_normalized` is the terrain illuminated/scattering area normalized
to the beta-zero reference area. Sentinel Hub exposes this quantity as
`scatteringArea` for its terrain-correction branch.

Taking the ratio cancels the common beta-zero term:

`gamma0_terrain / gamma0_ellipsoid = 1 / (scatteringArea * tan(theta_E))`

and therefore

`delta_dB = -10 log10(scatteringArea) - 10 log10(tan(theta_E))`

with `delta_dB = RTC_gamma0_dB - ellipsoid_gamma0_dB`.

The derivation follows the gamma-zero reference-area convention described by
David Small (2011), the RTC area-normalization description in Digital Earth
Africa's Sentinel-1 specification, and Sentinel Hub's definition of
`scatteringArea` as the normalized area used to convert beta-zero to terrain
gamma-zero. The provider documentation describes the processing products and
bands, but does not publish every internal implementation detail; the
equation is therefore tested empirically against the returned products rather
than assumed to be exact.

References:

- Small, D. (2011), [Flattening Gamma: Radiometric Terrain Correction for SAR Imagery](https://doi.org/10.1109/TGRS.2011.2120616).
- [Digital Earth Africa: Sentinel-1 Normalised Radar Backscatter](https://docs.digitalearthafrica.org/en/latest/data_specs/Sentinel-1_specs.html).
- [Copernicus Data Space / Sentinel Hub: Sentinel-1 GRD](https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Data/S1GRD.html).

## Data and method

- Site: CEOS Surat Basin, Queensland, Australia.
- Platform/orbit: Sentinel-1A, ascending relative orbit 9.
- Acquisitions: 2025-12-19, 2025-12-31, 2026-01-12, 2026-01-24.
- Processing branches: `GAMMA0_ELLIPSOID` and `GAMMA0_TERRAIN`.
- RTC DEM: Copernicus DEM 30 m; radiometric terrain oversampling 2.
- Output grid: 2500 x 2200, EPSG:4326, same CRS and affine transform for all
  ellipsoid, RTC, and interpolated-angle rasters.
- Ellipsoid incidence angle: source GRD annotation geolocation-grid
  `incidenceAngle` tie points, linearly interpolated without extrapolation.
- The four angle grids each cover 100% of the requested output grid.
- Five-fold spatially interleaved tie-point validation predicted 179 of 210
  held-out points (85.2%); pooled per-scene RMSE was approximately 0.00598°.
- Distributed-target analysis excludes 15-pixel-radius neighborhoods around
  the three surveyed corner reflectors and excludes pixels flagged by the
  RTC `shadowMask`. Only common valid pixels are compared.
- Sampling interval: every fourth pixel in row and column, after common-mask
  construction.

## Observed result

The paired-processing artifact and the angle-interpolation artifact were
analysed together. Exact grid equality was confirmed for all four scenes.

Across the four-scene common-valid footprint, after reflector-neighborhood
exclusion, 4,835,462 of 5,500,000 pixels remained (87.92%).

| Polarization | Samples | Mean residual bias | Residual standard deviation | P95 absolute residual |
|---|---:|---:|---:|---:|
| VV | 1,215,014 | +0.00770 dB | 0.00035 dB | 0.00824 dB |
| VH | 1,147,292 | +0.00771 dB | 0.00035 dB | 0.00824 dB |

The full predicted term explains the spatial variation extremely closely.
Regressing observed RTC-minus-ellipsoid difference against the predicted
two-term value gives a slope of approximately 0.99998 and R² of approximately
0.999997 for both polarizations. The remaining discrepancy is a small,
consistent positive offset of about 0.0077 dB. The area term alone leaves
substantially larger residuals (about 0.045–0.046 dB MAE per scene).

## Interpretation and limits

**Result: the proposed relationship is strongly supported for these four
Sentinel Hub outputs over this Surat R009 footprint.** The small residual is
not zero and should remain visible in reports; it must not be silently removed
by fitting an intercept.

This is not independent processor validation: both backscatter branches come
from the same provider and source acquisitions. The equation is closely tied
to the processing definitions, so the result is best interpreted as a
cross-check of the provider's paired outputs and the source-angle interpolation,
not as independent proof of absolute radiometric accuracy.

Other limitations:

- Annotation tie-point cross-validation is internal to the source product,
  not independent geodetic control.
- The source-angle interpolation is in geographic coordinates; its reported
  cross-validation error does not capture every systematic angle convention
  difference.
- The four scenes share platform, orbit direction, relative orbit, provider,
  and processing configuration.
- The 10 m output spacing is a requested grid spacing, not native Sentinel-1
  resolution.
- The result does not validate absolute corner-reflector RCS, terrain-model
  accuracy, or performance in steep terrain, layover, or shadow.
- No correction, normalization, or change-detection product is generated.

The next validation step is a processor-independent comparison over a second
site or with an independently generated RTC product, preserving the same
equation, input/output contracts, masks, and diagnostics.

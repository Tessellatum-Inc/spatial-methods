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



### OPERA asset retrieval and metadata QA (2026-11-24)

The ASF catalogue candidates were downloaded after Earthdata application/EULA
authorization. The final GitHub Actions run
[45336118084](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45336118084)
completed successfully and produced the short-lived artifact
`surat-r009-opera-rtc-science-assets` (54 files; approximately 235 MB; 7-day
retention). The manifest records the source URLs, expected and actual byte
counts, and SHA-256 for every file. A local verification of all 54 files found
no missing files, size mismatches, or checksum mismatches.

The final asset set contains 8 RTC HDF5 products, 8 RTC XML sidecars, 16 VV/VH
GeoTIFFs, 8 dynamic RTC masks, and 14 static assets (2 XML sidecars and 12
GeoTIFFs). The latter includes both the ellipsoid-referenced
`incidence_angle.tif` and terrain-normal-referenced
`local_incidence_angle.tif` for each burst. These angle conventions must not
be interchanged.

HDF5 provenance confirms that the four acquisition dates use these original
Sentinel-1A SLC granules:

| Date | Source SLC granule start (UTC) |
|---|---|
| 2025-12-19 | 08:41:11 |
| 2025-12-31 | 08:41:09 |
| 2026-01-12 | 08:41:08 |
| 2026-01-24 | 08:41:07 |

Both adjacent burst products for a date reference the same source SLC granule.
The HDF5 processing metadata records beta-zero input normalization, gamma-zero
output normalization, linear backscatter intensity, and radiometric terrain
correction enabled. The delivered GeoTIFFs are float32, 30 m, UTM zone 55S
(`EPSG:32755`); the two burst grids have different origins and dimensions,
so they must be mosaicked or explicitly aligned before pixelwise comparison.

Using the two burst masks reprojected by nearest neighbour to a 30 m grid over
the rectangular AOI, the union of valid mask-class-0 pixels covers:

| Acquisition | Valid AOI grid cells | Valid fraction |
|---|---:|---:|
| 2025-12-19 | 569,818 / 634,678 | 89.78% |
| 2025-12-31 | 572,028 / 634,678 | 90.13% |
| 2026-01-12 | 571,254 / 634,678 | 90.01% |
| 2026-01-24 | 575,624 / 634,678 | 90.70% |

These are raster-mask coverage estimates on the stated 30 m comparison grid,
not catalogue-footprint percentages. The remaining AOI cells must remain
excluded from paired statistics; do not fill them or infer values.

The static ellipsoid incidence-angle rasters span approximately 40.48–46.01
degrees across the two bursts. This is a useful sanity check, not a substitute
for pixel-level alignment and convention checks. The static gamma0-to-beta0
area-normalization factor is also present.

**Status at the metadata-QA stage:** independent source identity, download
integrity, product normalization metadata, grid CRS/resolution, and required
static angle/ANF availability were verified. The cross-processor comparison
was subsequently completed; its results are recorded below.

## Independent processor validation: OPERA RTC-S1 (metadata verified; comparison pending)

### Catalogue discovery

ASF's OPERA RTC-S1 catalogue was queried for the four Sentinel-1A R009 source
acquisitions. Eight matching RTC-S1 burst products were found: two adjacent
IW3 bursts for each date. The burst identifiers are
`T009_019159_IW3` and `T009_019160_IW3`; all products contain VV and VH.

| Expected source acquisition (UTC) | OPERA burst start times (UTC) | Difference from expected |
|---|---|---:|
| 2025-12-19 08:41:12 | 08:41:23, 08:41:25 | +11 s, +13 s |
| 2025-12-31 08:41:11 | 08:41:21, 08:41:24 | +10 s, +13 s |
| 2026-01-12 08:41:10 | 08:41:20, 08:41:23 | +10 s, +13 s |
| 2026-01-24 08:41:08 | 08:41:19, 08:41:22 | +11 s, +14 s |

The product group metadata identifies the same Sentinel-1A relative orbit and
the expected source orbit sequence. Catalogue-footprint intersections with
the Surat study rectangle are:

| Acquisition date | AOI footprint coverage |
|---|---:|
| 2025-12-19 | 97.43% |
| 2025-12-31 | 97.60% |
| 2026-01-12 | 97.54% |
| 2026-01-24 | 97.89% |

The four-date common footprint covers 97.43% of the rectangle and contains all
three corner-reflector coordinates. These percentages are computed from
catalogue polygons in geographic coordinates; they are discovery-level
coverage estimates, not valid-pixel coverage from the delivered rasters.

Two matching RTC-STATIC products were also found for the same burst IDs. They
provide the gamma0-to-beta0 area-normalization factor, local incidence angle,
number of looks and layover/shadow masks. The OPERA product specification
defines beta-zero reconstruction as RTC gamma-zero multiplied by the
gamma0-to-beta0 ANF.

### Why this is an independent check

OPERA RTC-S1 is a 30 m, burst-based product generated from Sentinel-1 SLC
inputs with the JPL/ISCE3 RTC chain and Copernicus GLO-30 DEM. The existing
Sentinel Hub case uses GRD inputs and its own RTC processing chain. The
acquisitions are time- and orbit-matched, but the input product level,
multilooking, grid spacing and processor differ. Therefore this is a
cross-processor comparison, not a claim that native pixels should be
identical.

Product documentation:

- [ASF OPERA RTC-S1 Product Guide](https://hyp3-docs.asf.alaska.edu/guides/opera_rtc_product_guide/)
- [JPL OPERA RTC-S1 Product Specification](https://d2pn8kiwq2w21t.cloudfront.net/documents/ProductSpec_RTC-S1.pdf)
- [JPL OPERA RTC-S1 Static Layers Specification](https://d2pn8kiwq2w21t.cloudfront.net/documents/ProductSpec_RTC-S1-STATIC.pdf)

### Planned comparison

1. Download the eight RTC burst products and the two static-layer products.
2. Verify the source orbit, burst ID, acquisition time, product version,
   CRS, affine transform, pixel spacing, nodata and raster dimensions.
3. Mosaic adjacent bursts only after proving their grids and overlap behaviour.
4. Decode each acquisition's dynamic RTC mask. For the strict comparison,
   retain mask class 0 (valid and unaffected by layover or shadow); exclude
   classes 1, 2, 3 and 255. The static mask is not substituted for the
   acquisition-specific RTC mask.
5. Aggregate Sentinel Hub values to the OPERA 30 m grid in linear power,
   using valid-area weighting. Do not average dB values or use nearest-neighbour
   resampling for backscatter.
6. Compare OPERA RTC gamma-zero with Sentinel Hub terrain gamma-zero over the
   common valid footprint, separately by polarization and acquisition.
7. Reconstruct beta-zero using the OPERA gamma0-to-beta0 ANF, then reconstruct
   an ellipsoid-referenced gamma-zero using the ellipsoid incidence-angle
   term. Compare this result with Sentinel Hub ellipsoid gamma-zero while
   retaining the residual bias and spatial diagnostics.
8. Exclude reflector neighbourhoods using metric buffers, not a fixed number
   of pixels, and report sample count, valid fraction, bias, MAE, RMSE,
   quantiles and spatial residual structure.

The OPERA static incidence-angle layer is specified as ellipsoid-referenced.
The current automated asset selection includes the ANF and local-incidence
layers; the independent incidence-angle asset link still needs to be resolved
before that layer can be used. The source GRD angle interpolation is retained
as the interim angle input, and this limitation will be explicit in the QA.

### Data access status

The ASF catalogue and asset metadata are accessible, but anonymous requests
to both the Cumulus and ASF Data Pool asset endpoints returned HTTP 401.
The downloader now supports an Earthdata Login bearer token supplied as the
GitHub Actions secret `EARTHDATA_TOKEN`. The token is not stored in the
repository or printed in workflow logs. NASA documents user tokens as valid
for 60 days; renew the secret when the token expires.

**Status:** catalogue discovery and asset selection are complete; raster
download and cross-processor numerical validation are blocked until the
repository secret is configured.

### Cross-processor comparison result (2026-11-24)

The comparison was executed successfully by GitHub Actions run
[45338888272](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45338888272).
The machine-readable report is preserved in the
[surat-r009-opera-sentinelhub-cross-processor-report artifact](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45338888272/artifacts/14895676556)
(30-day retention).

The workflow processed all eight OPERA burst rasters (two adjacent bursts for
each of four dates). Sentinel Hub ellipsoid and terrain backscatter were
masked and area-averaged in **linear power** onto each native OPERA burst grid;
dB conversion happened only after aggregation. It used OPERA dynamic RTC
mask class 0 and static mask class 0, the common Sentinel Hub data masks, the
Sentinel Hub RTC shadow mask, and 450 m circular exclusions around the three
surveyed reflector locations.

The primary diagnostic is the difference between the processors' terrain-
minus-ellipsoid gamma-zero changes:

`residual = (SH gamma0_terrain - SH gamma0_ellipsoid)
          - (OPERA gamma0_terrain - reconstructed OPERA gamma0_ellipsoid)`

All terms are in dB after linear-power aggregation to the common OPERA grid.
The OPERA ellipsoid gamma-zero is reconstructed from the RTC gamma-zero,
gamma0-to-beta0 ANF, and ellipsoid incidence angle as derived above.

| Polarization | Burst-pixel samples | Mean residual bias | MAE | RMSE |
|---|---:|---:|---:|---:|
| VV | 2,391,980 | -0.05373 dB | 0.06059 dB | 0.07165 dB |
| VH | 2,391,932 | -0.05352 dB | 0.06142 dB | 0.07373 dB |

The bias is the mean of the per-burst mean residuals weighted by each burst's
valid sample count; MAE and RMSE are likewise count-weighted summaries of the
eight per-burst statistics. They are descriptive summaries, not a single
pooled-pixel statistic. Per-date and per-burst metrics, direct reconstructed
ellipsoid/terrain backscatter comparisons, and regression diagnostics are
retained in the JSON artifact.

**Interpretation:** the cross-processor terrain-minus-ellipsoid difference is
closely aligned, with a small systematic offset of roughly -0.054 dB and
count-weighted MAE around 0.061 dB for both polarizations. This is encouraging
independent-processor evidence for the geometric relationship. It is not
evidence that OPERA and Sentinel Hub absolute backscatter values are
interchangeable: the processors use different source product levels,
processing chains, grids and effective spatial resolutions.

Important limitations remain:

- OPERA is SLC-derived, burst-based, 30 m and processed with JPL/ISCE3; the
  Sentinel Hub branch uses GRD and a separate processing chain.
- Sentinel Hub's 10 m requested grid is averaged to OPERA's 30 m grid. The
  aggregation changes the statistics relative to a direct native-resolution
  comparison, and the two products' effective resolution is not identical.
- The residual includes processor differences, acquisition-time differences
  of several seconds, area-averaging effects, mask differences and any
  differences in the providers' noise/calibration conventions.
- The weighted aggregate is not a pooled-pixel residual distribution. Use the
  per-burst JSON records for spatial heterogeneity and scene-specific
  interpretation.
- This does not validate absolute radiometric calibration, corner-reflector
  RCS, DEM accuracy, or performance in steep terrain, layover or shadow.

**Conclusion:** the equation has passed a first independent-provider,
four-date/two-polarization cross-check over this Surat footprint, with a
small but non-zero systematic residual. Treat it as supported within this
case-study scope, not universally validated. The next useful stress test is a
different relative orbit or terrain regime, followed by independent point-
target or distributed-target calibration evidence.


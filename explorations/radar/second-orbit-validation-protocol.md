# Second independent Sentinel-1 radiometric validation: design and admission criteria

## Purpose

The Surat Basin R009 study has completed a four-date, two-polarization comparison between Sentinel Hub Sentinel-1 GRD processing and NASA/JPL OPERA RTC-S1. The next experiment must add independent acquisition geometry or terrain conditions. It must not simply increase the number of R009 dates and describe that as independent validation.

This document defines the next experiment before any new raster processing. It is a protocol and candidate-screening decision, not a report of a completed second validation.

## Candidate direction

The repository already contains an alternate-orbit Sentinel Hub experiment for Nairobi County:

- workflow: `.github/workflows/sentinel1-alternate-orbit.yml`
- processor: `process_sentinel1_alternate_orbit.py`
- current default: ascending relative orbit 130
- current screening window: 2026-10-01 through 2026-11-23 UTC
- minimum catalogue footprint intersection: 0.80
- outputs are explicitly partial-coverage diagnostics, not an analysis-ready full-AOI stack.

This is a useful candidate source of alternate-geometry Sentinel Hub acquisitions. It is **not yet an OPERA cross-processor validation**: OPERA RTC-S1 and matching RTC-STATIC layers must first be discovered for the same source acquisitions and actual overlap.

## Scientific question

Does the documented terrain-to-ellipsoid gamma-zero relationship remain internally consistent when evaluated on an independent Sentinel-1 relative orbit and a different study area?

For OPERA RTC-S1:

[
\beta^0 = \gamma^0_{RTC} \times ANF_{\gamma^0\rightarrow\beta^0}
]

[
\widehat{\gamma^0_E} =
\gamma^0_{RTC} \times ANF_{\gamma^0\rightarrow\beta^0}
\times \tan(\theta_E)
]

Compare the OPERA terrain-minus-reconstructed-ellipsoid delta against the equivalent Sentinel Hub GRD terrain-minus-ellipsoid delta. Aggregate linear power onto a declared common grid before converting to dB.

The estimand remains the *cross-processor difference between terrain-to-ellipsoid deltas*, not equality of absolute backscatter.

## Admission gates

A candidate acquisition may enter processing only when all of the following are demonstrated in machine-readable provenance:

1. **Independent geometry:** Sentinel-1 relative orbit differs from R009; record orbit direction, relative orbit, platform, absolute orbit and acquisition time where available.
2. **Source identity:** OPERA HDF5 metadata and Sentinel Hub catalogue metadata identify the same Sentinel-1 source acquisition. A timestamp proximity match alone is insufficient.
3. **Polarization:** VV and VH are both available in both processor branches for the acquisition.
4. **Static-layer identity:** the RTC-STATIC ANF and ellipsoid incidence-angle assets match the OPERA burst IDs exactly.
5. **Spatial overlap:** report catalogue footprint intersection and raster-valid overlap separately. Catalogue coverage is never substituted for raster data-mask coverage.
6. **Geometry:** compare each burst on its native OPERA grid; do not silently mosaic adjacent bursts with different origins or dimensions.
7. **Mask semantics:** document OPERA dynamic and static mask classes and Sentinel Hub data/shadow masks. Preserve valid-data masks through resampling.
8. **Aggregation:** average masked linear power, not dB values, onto the comparison grid. Report resampling method and valid-support threshold.
9. **Reflector/target handling:** if known calibration targets occur in the AOI, inventory them and predefine exclusions. If none are known, state that this is not an absolute calibration experiment.
10. **Sample adequacy:** require at least two source dates and a declared minimum number of valid common pixels per burst/date/polarization; publish failed candidates rather than silently dropping them.

## Design safeguards

- Keep the alternate-orbit experiment separate from the R009 time series. Different look directions and incidence geometries must not be pooled as one temporal stack.
- Use a common spatial subset supported by all selected dates only when reporting multi-date aggregates; also retain per-date/per-burst metrics.
- Report per-scene and per-burst bias, median, MAE, RMSE, 5th/95th percentiles, 95th absolute residual, sample counts and regression diagnostics.
- Keep raw raster data in short-lived Actions artifacts or durable object storage; commit only code, tests, metadata manifests, checksums and compact reports.
- A successful workflow means the computation ran. It does not by itself mean the scientific relationship passed validation.

## Decision rules

- **Proceed:** all admission gates pass for at least two dates, both polarizations and a useful common raster support.
- **Revise candidate:** OPERA products exist but the Sentinel Hub match, static layers, or spatial overlap are inadequate; search another orbit/date window without relaxing source-identity requirements.
- **Stop and document:** no defensible match exists. Do not manufacture a comparison by matching only on date or by using a different Sentinel-1 acquisition.

## Candidate discovery results (2026-11-24)

The ASF and Sentinel Hub catalogue workflows found a consistent R130 candidate set:

| UTC acquisition date | OPERA RTC burst products | Sentinel Hub GRD candidate | Difference to nearest OPERA burst start | Sentinel Hub absolute orbit |
|---|---:|---|---:|---:|
| 2026-10-06 | 3 | `S1D_IW_GRDH_1SDV_20261006T155531_20261006T155556_004896_009371_B797_COG.SAFE` | 11 s | 4896 |
| 2026-10-18 | 3 | `S1D_IW_GRDH_1SDV_20261018T155531_20261018T155556_005071_009986_8434_COG.SAFE` | 11 s | 5071 |
| 2026-10-30 | 3 | `S1D_IW_GRDH_1SDV_20261030T155531_20261030T155556_005246_009F7F_498E_COG.SAFE` | 10 s | 5246 |
| 2026-11-11 | 3 | `S1D_IW_GRDH_1SDV_20261111T155531_20261111T155556_005421_00A58B_0CEC_COG.SAFE` | 10 s | 5421 |
| 2026-11-23 | 3 | `S1D_IW_GRDH_1SDV_20261123T155530_20261123T155555_005596_00AB9A_AA88_COG.SAFE` | 11 s | 5596 |

All five Sentinel Hub candidates are Sentinel-1D, R130 ascending, IW, VV/VH. The OPERA RTC catalogue identifies the same dates and platform, with three IW3 bursts per date. The nearest burst-start differences are only 10–11 seconds. This is a strong catalogue-level pairing signal.

**Still unverified:** the original Sentinel-1 SLC product identifiers recorded in each OPERA HDF5 metadata file have not yet been reconciled with the corresponding Sentinel Hub GRD product identifiers. The OPERA RTC-STATIC layers must also be downloaded and matched to all three bursts. Do not proceed to pixel comparison until these checks pass.

Evidence workflows:
- [OPERA RTC/RTC-STATIC discovery](../../.github/workflows/discover-opera-nairobi-r130.yml)
- [Cross-provider catalogue matching](../../.github/workflows/match-opera-nairobi-r130-sentinelhub.yml)
- [OPERA asset download](../../.github/workflows/download-opera-nairobi-r130-assets.yml)

## Current status

`CATALOGUE_CANDIDATES_MATCHED_5_OF_5; HDF5_SOURCE_IDENTITY_PENDING; RTC_STATIC_AND_RASTER_DOWNLOAD_PENDING`

No second-orbit pixel comparison or scientific validation result is claimed. The Nairobi R130 work remains a candidate cross-provider study until the source-scene identity and raster QA gates pass.

## Source documentation

- [ASF OPERA RTC-S1 product guide](https://hyp3-docs.asf.alaska.edu/guides/opera_rtc_product_guide/)
- [ASF Search API documentation](https://docs.asf.alaska.edu/api/keywords/)
- [NASA/JPL OPERA RTC product overview](https://www.jpl.nasa.gov/go/opera/products/rtc-product/)
- [Sentinel Hub Catalog API](https://docs.sentinel-hub.com/api/latest/api/catalog/)
- [Sentinel Hub Sentinel-1 GRD collection and processing notes](https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Data/S1GRD.html)

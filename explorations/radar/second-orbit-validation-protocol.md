# Second independent Sentinel-1 radiometric validation: design and admission criteria

## Purpose

The Surat Basin R009 study has completed a four-date, two-polarization comparison between Sentinel Hub Sentinel-1 GRD processing and NASA/JPL OPERA RTC-S1. The next experiment must add independent acquisition geometry or terrain conditions. It must not simply increase the number of R009 dates and describe that as independent validation.

This document records the admission protocol, source crosswalk, raster QA, and first cross-processor results for the second independent-orbit case study. The comparison is complete at the first-pass level; residual spatial diagnostics remain outstanding.

## Candidate direction

The repository already contains an alternate-orbit Sentinel Hub experiment for Nairobi County:

- workflow: `.github/workflows/sentinel1-alternate-orbit.yml`
- processor: `process_sentinel1_alternate_orbit.py`
- current default: ascending relative orbit 130
- current screening window: 2026-10-01 through 2026-11-23 UTC
- minimum catalogue footprint intersection: 0.80
- outputs are explicitly partial-coverage diagnostics, not an analysis-ready full-AOI stack.

This candidate set was subsequently matched to OPERA RTC-S1 and RTC-STATIC products, reconciled to the same source datatakes, processed in both Sentinel Hub gamma0 conventions, and compared on native OPERA burst grids. The admission and result records below supersede the initial candidate-only status.

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

**Metadata/raster audit (2026-11-24):** all 96 selected OPERA assets downloaded successfully (15 RTC HDF5 files, 45 dynamic GeoTIFFs, and 18 static GeoTIFFs). The 15 HDF5 files each report the expected Sentinel-1D platform, R130 track, burst ID, source acquisition start time, and absolute orbit number. The five absolute orbit numbers are 4896, 5071, 5246, 5421, and 5596, exactly matching the Sentinel Hub candidate catalogue. For each of the three bursts, all 21 associated dynamic/static rasters have one identical CRS, shape, and affine transform. These checks pass within each burst; adjacent bursts are not forced onto one grid.

The source SLC identifiers were subsequently extracted from the documented `l1SlcGranules` field and cross-checked against the Sentinel Hub GRD product identifiers. See the verified source-datatake crosswalk below.

Evidence workflows:
- [OPERA RTC/RTC-STATIC discovery](../../.github/workflows/discover-opera-nairobi-r130.yml)
- [Cross-provider catalogue matching](../../.github/workflows/match-opera-nairobi-r130-sentinelhub.yml)
- [OPERA asset download](../../.github/workflows/download-opera-nairobi-r130-assets.yml)

## Source datatake identity and raster-grid QA (2026-11-24)

The OPERA HDF5 field `/metadata/processingInformation/inputs/l1SlcGranules` identifies the SLC source granule used for each burst. These identifiers were reconciled against the Sentinel Hub GRD catalogue item names. A two-second start-time tolerance is used because the SLC and GRD product start timestamps differ by one second on two dates; platform, absolute orbit, datatake identifier, and IW mode must still agree.

| UTC date | Absolute orbit | OPERA SLC datatake ID | Sentinel Hub GRD datatake ID | Start-time difference | OPERA bursts linked |
|---|---:|---|---|---:|---:|
| 2026-10-06 | 4896 | `009371` | `009371` | 0 s | 3/3 |
| 2026-10-18 | 5071 | `009986` | `009986` | 0 s | 3/3 |
| 2026-10-30 | 5246 | `009F7F` | `009F7F` | 1 s | 3/3 |
| 2026-11-11 | 5421 | `00A58B` | `00A58B` | 1 s | 3/3 |
| 2026-11-23 | 5596 | `00AB9A` | `00AB9A` | 0 s | 3/3 |

<badge>5/5 datatakes verified</badge>

All 15 OPERA burst HDF5 records link to the same corresponding Sentinel-1D GRD datatake as their date's Sentinel Hub catalogue item. This establishes acquisition-level source correspondence across the two processing chains. It does **not** mean that the SLC and GRD products are identical or that their pixels should match.

The raster audit also confirms 45 dynamic RTC rasters and 18 static rasters. Each burst has 21 associated rasters (15 dynamic across five dates plus six static layers), and all 21 have identical CRS, dimensions, and affine transform within that burst. Adjacent bursts remain separate grids.

Evidence:
- [OPERA asset download run](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45345864969)
- [HDF5, grid and source-datatake audit run](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45351556417)
- [Source and raster audit artifact](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45351556417/artifacts/14900656138)

## Sentinel Hub paired-raster processing

A paired processing workflow now requests both `GAMMA0_ELLIPSOID` and `GAMMA0_TERRAIN` for the five source-verified Sentinel-1D R130 GRD scenes. It uses the same Nairobi study rectangle, the same Process API output grid for both branches, linear-power VV/VH values, Copernicus DEM GLO-30, and radiometric terrain oversampling 2. It records catalogue footprint intersection separately from Process API data-mask coverage, plus SHA-256 hashes and per-scene QA summaries. The outputs remain provisional until each OPERA burst is compared against the Sentinel Hub rasters on its native grid.

Workflow: [Process Nairobi R130 paired gamma0 rasters](../../.github/workflows/process-nairobi-r130-sentinelhub-pairs.yml)

## Sentinel Hub paired-raster results (2026-11-24)

All five source-verified Sentinel-1D R130 scenes were processed in both ellipsoid gamma0 and terrain gamma0 modes using the same 2500 x 2200 EPSG:4326 output grid, linear-power VV/VH, Copernicus GLO-30 DEM, and terrain oversampling 2.

| Date | Catalogue footprint intersection with AOI | Common Sentinel Hub valid pixels | Valid fraction |
|---|---:|---:|---:|
| 2026-10-06 | 84.249% | 4,631,316 | 84.206% |
| 2026-10-18 | 84.219% | 4,629,651 | 84.175% |
| 2026-10-30 | 84.356% | 4,637,344 | 84.315% |
| 2026-11-11 | 84.305% | 4,634,377 | 84.261% |
| 2026-11-23 | 84.260% | 4,631,887 | 84.216% |

The close agreement between catalogue footprint intersection and the Process API's common valid fraction is a useful internal consistency check. These counts describe validity shared by the Sentinel Hub ellipsoid and RTC branches only; they are **not** yet the pixel overlap with OPERA.

Evidence:
- [Sentinel Hub paired-processing workflow](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45351938186)
- [Paired raster artifact (534.7 MB)](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45351938186/artifacts/14901395344)

## OPERA-to-Sentinel Hub common pixel-support QA (2026-11-24)

The five paired Sentinel Hub scenes were reprojected to each native OPERA burst grid using area averaging of linear power and valid-support threshold 0.95. OPERA dynamic mask class 0 and static mask class 0 were treated as valid; Sentinel Hub support required valid ellipsoid and RTC data masks and unflagged RTC shadow mask.

All 15 date/burst combinations and all 30 date/burst/polarization combinations passed the minimum 1,000 common-pixel gate. Common VV/VH sample counts were:

| OPERA burst | VV common pixels across five dates | VH common pixels across five dates |
|---|---:|---:|
| T130-279214-IW3 | 85,447–86,700 | 85,445–86,697 |
| T130-279215-IW3 | 827,865–829,538 | 827,854–829,538 |
| T130-279216-IW3 | 574,926–576,584 | 574,924–576,584 |

The large difference in sample counts between bursts reflects their different native grid footprints and valid overlap with the Sentinel Hub output. The comparison retains each burst separately; it does not mosaic adjacent bursts or treat their sample counts as equivalent areas.

Evidence:
- [Paired processing and common-support QA workflow](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45352163781)
- [Paired rasters and common-support QA artifact (534.7 MB)](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45352163781/artifacts/14900862117)

## First R130 cross-processor comparison (2026-11-24)

The comparison workflow completed for all 15 date/burst combinations and both polarizations. It reconstructs OPERA ellipsoid gamma0 as

`gamma0_ellipsoid = gamma0_RTC * ANF_gamma0_to_beta0 * tan(ellipsoid_incidence_angle)`

and compares `Sentinel Hub (terrain - ellipsoid)` against `OPERA (terrain - reconstructed ellipsoid)`. All inputs are linear-power averages on each native OPERA burst grid before dB conversion.

### Pooled pixel-level residuals

| Metric | VV | VH |
|---|---:|---:|
| Pooled pixels | 7,452,890 | 7,452,850 |
| Mean residual bias | +0.0040 dB | +0.0045 dB |
| MAE | 0.0901 dB | 0.0916 dB |
| RMSE | 0.1294 dB | 0.1302 dB |
| 95th-percentile absolute residual | 0.2541 dB | 0.2543 dB |
| Maximum absolute residual | 3.4023 dB | 3.1613 dB |

The pooled mean bias is very close to zero, and the 95th-percentile absolute residual is about 0.25 dB. However, maximum absolute residuals exceed 3 dB, so the near-zero mean must not be mistaken for uniformly small local differences.

### Burst structure

The per-burst MAE/RMSE pattern is consistent across all five dates:

| Burst | VV MAE range | VH MAE range | Approximate RMSE range |
|---|---:|---:|---:|
| T130-279214-IW3 | 0.064–0.065 dB | 0.069–0.072 dB | 0.085–0.094 dB |
| T130-279215-IW3 | 0.083 dB | 0.084–0.086 dB | 0.117–0.120 dB |
| T130-279216-IW3 | 0.104 dB | 0.104–0.105 dB | 0.148–0.150 dB |

This stable burst-dependent pattern deserves investigation. It may reflect spatial differences in scattering regime, terrain, incidence geometry, or residual processor/resampling effects; the current results do not identify which explanation is responsible. The first burst has much lower dispersion than the third, despite similarly small mean biases.

### Interpretation and limits

This is positive evidence that the terrain-to-ellipsoid gamma0 relationship remains closely aligned between OPERA and Sentinel Hub on a second relative orbit, five dates, three IW3 bursts, and two polarizations. It is not evidence that absolute backscatter products are interchangeable. It is also not an absolute calibration experiment: no Nairobi corner-reflector inventory or absolute RCS target was used. The broad AOI includes urban and peri-urban surfaces.

The Surat R009 study had lower pooled MAE/RMSE (about 0.061/0.072 dB for VV and 0.061/0.074 dB for VH). Nairobi R130's pooled errors are larger (about 0.090/0.129 dB for VV and 0.092/0.130 dB for VH), even though its mean bias is closer to zero. The two sites/orbits should remain separate case studies rather than be pooled.

Evidence:
- [Cross-processor comparison workflow](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45353189679)
- [Cross-processor report artifact](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45353189679/artifacts/14901316555)

### Residual spatial diagnostics (2026-11-24)

The next diagnostic workflow completed successfully. It generated 30 single-band float32 GeoTIFFs (five dates × three native OPERA burst grids × VV/VH) and a JSON report. Maps preserve each native OPERA CRS, transform, dimensions, and -9999 nodata; no burst mosaicking or outlier removal was performed. The exact comparison masks and 0.95 Sentinel Hub valid-support threshold from the first-pass comparator were retained. The report includes per-scene metrics, fractions exceeding 0.5/1/2 dB, incidence-angle bins, within-scene ANF quartiles, and coordinates of the ten largest absolute residuals per scene/polarization.

Workflow: [Nairobi R130 residual diagnostics](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45360551227)  
Artifact: [30 residual maps and diagnostic JSON (55.3 MB; 30-day retention)](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45360551227/artifacts/14904975668)

#### Reconfirmed burst effect and residual tails

The residual-map report independently reproduces the first-pass per-burst pattern. Equal-date means of the per-scene metrics are:

| Burst | VV MAE | VH MAE | VV RMSE | VH RMSE |
|---|---:|---:|---:|---:|
| T130-279214-IW3 | 0.0646 dB | 0.0701 dB | 0.0853 dB | 0.0920 dB |
| T130-279215-IW3 | 0.0831 dB | 0.0849 dB | 0.1176 dB | 0.1188 dB |
| T130-279216-IW3 | 0.1041 dB | 0.1044 dB | 0.1496 dB | 0.1494 dB |

Across all common pixels, weighted fractions above 1 dB are approximately 0.0452% (VV) and 0.0432% (VH); above 2 dB they are approximately 0.00086% and 0.00082%, respectively. The maps retain maximum absolute residuals of 3.402 dB (VV) and 3.161 dB (VH). Thus, the tails are rare but real, and the burst-dependent dispersion is systematic across dates and polarizations.

#### Covariate stratification

Incidence-angle values are concentrated almost entirely in the 44–46° bin. The 46–48° bin has much lower MAE in bursts 279215 and 279216, but contains only a small minority of common pixels. This is not enough angular spread to infer a reliable incidence-angle response; the apparent lower error at the high-angle edge may also reflect a different spatial subset.

ANF quartiles show a more repeatable pattern. In every burst and both polarizations, the lowest and highest within-scene ANF quartiles have higher MAE than the middle two quartiles. For example, burst 279216 VV MAE is about 0.116, 0.079, 0.082, and 0.139 dB in Q1–Q4; VH is about 0.116, 0.080, 0.083, and 0.139 dB. The same U-shaped pattern appears in the other bursts. Mean residual bias also tends negative in Q1 and positive in Q4. This is a strong diagnostic association, not evidence that ANF itself causes the error: ANF may covary with terrain slope, aspect, local scattering regime, or resampling geometry. Quartile boundaries are burst-specific and must not be interpreted as common physical thresholds.


#### Terrain slope/aspect stratification (2026-11-24)

A Copernicus GLO-30 Public DEM was acquired from the AWS Open Data COG bucket, using the two 1° tiles intersecting the Nairobi processing rectangle: `S02_00_E036_00` and `S02_00_E037_00`. Both tiles passed GeoTIFF checks. The resulting 2500 × 2200 EPSG:4326 study-grid raster has 100% data-mask coverage, elevation range 0–2267.64 m and median 1642.69 m. Its SHA-256 and tile list are retained in the DEM QA sidecar.

- [DEM acquisition workflow](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45364142134)
- [DEM artifact (92.5 MB; 30-day retention)](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45364142134/artifacts/14906256438)
- [Terrain stratification workflow](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45364890793)
- [Terrain-stratified JSON report](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45364890793/artifacts/14906925618)

Slope and downslope aspect were calculated from the DEM after reprojection to each native OPERA grid. All 30 residual maps passed terrain stratification. The slope relationship is consistent across bursts and polarizations: MAE generally increases with slope. Illustrative pooled-by-date bins:

| Burst | Polarization | 0–1° slope MAE | 5–10° slope MAE | 10–15° slope MAE | 15–30° slope MAE |
|---|---|---:|---:|---:|---:|
| 279214 | VV | 0.0613 | 0.0926 | 0.1262 | 0.1770* |
| 279214 | VH | 0.0659 | 0.0980 | 0.1384 | 0.2136* |
| 279215 | VV | 0.0642 | 0.1089 | 0.1296 | 0.1596 |
| 279215 | VH | 0.0675 | 0.1091 | 0.1297 | 0.1603 |
| 279216 | VV | 0.0762 | 0.1129 | 0.1503 | 0.2143 |
| 279216 | VH | 0.0783 | 0.1126 | 0.1498 | 0.2139 |

*Burst 279214 has only 80 samples in the 15–30° bin, so those values are unstable and should not be generalized.*

Aspect also shows a repeated directional pattern: south- and southwest-facing bins have higher MAE than north-facing bins. For example, burst 279215 VV MAE is 0.0805 dB in the N bin and 0.1167 dB in SW; burst 279216 is 0.1007 dB in N and 0.1461 dB in SW. VH shows the same pattern. Aspect is defined as downslope azimuth clockwise from north, with low-slope pixels excluded from directional bins.

These patterns make terrain geometry a plausible contributor to the burst-dependent residual spread, but they do not establish causality. The DEM is a DSM, not a bare-earth DTM; buildings and vegetation can influence its derivatives. The public AWS COGs are the Copernicus 2021 release with source acquisition dates primarily 2011–2015, and the 30m source is resampled to the OPERA grids. Slope/aspect may also covary with ANF, land cover, local incidence angle, and the spatial distribution of valid pixels. The strong ANF-quartile pattern and slope/aspect pattern must therefore be tested jointly rather than treated as independent effects.

Next: use date-matched Dynamic World land-cover probabilities (not a single hard label), apply confidence thresholds, and evaluate whether the ANF/slope/aspect associations persist within surface classes. Dynamic World is available near-real-time at 10m through Google Earth Engine; that acquisition route still needs credentials and QA before use. No land-cover attribution or residual exclusion is claimed.

#### Spatial interpretation and next work

Residual maps show spatial texture rather than purely isolated single-pixel noise. A preview of burst 279216 shows coherent fine-scale patterns, but this visual inspection alone does not identify whether they arise from land cover, terrain, scene geometry, or processing differences. No land-cover attribution has been made because a date-appropriate independently validated classification has not yet been admitted.

The next gate should therefore test ANF-tail pixels against terrain slope/aspect and a defensible land-cover layer, then inspect high-residual coordinates against source masks and support edges. Keep the three bursts separate. Do not remove outliers or introduce exclusions unless a physical/methodological criterion is justified before re-estimating agreement.

## Current status

`SOURCE_DATATAKE_IDENTITY_VERIFIED_5_OF_5; HDF5_AND_RASTER_GRID_QA_PASSED; COMMON_PIXEL_SUPPORT_QA_PASSED_15_OF_15; R130_CROSS_PROCESSOR_COMPARISON_COMPLETE; RESIDUAL_MAPS_COMPLETE; ANF_AND_TERRAIN_STRATIFICATION_COMPLETE; DATE_MATCHED_LANDCOVER_ATTRIBUTION_PENDING`

The source, raster-grid, common-pixel-support, cross-processor comparison, residual mapping, and first terrain-covariate gates have passed. The terrain-to-ellipsoid relationship remains supported within this case, but residual dispersion is associated with burst, ANF quartiles, slope, and aspect. Date-matched land-cover attribution and a further independent test remain outstanding; no universal validation claim is made.

## Source documentation

- [ASF OPERA RTC-S1 product guide](https://hyp3-docs.asf.alaska.edu/guides/opera_rtc_product_guide/)
- [ASF Search API documentation](https://docs.asf.alaska.edu/api/keywords/)
- [NASA/JPL OPERA RTC product overview](https://www.jpl.nasa.gov/go/opera/products/rtc-product/)
- [Sentinel Hub Catalog API](https://docs.sentinel-hub.com/api/latest/api/catalog/)
- [Sentinel Hub Sentinel-1 GRD collection and processing notes](https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Data/S1GRD.html)
- [Copernicus DEM AWS Open Data registry](https://registry.opendata.aws/copernicus-dem/)
- [Copernicus DEM COG tile naming and specifications](https://copernicus-dem-30m.s3.amazonaws.com/readme.html)
- [Dynamic World Earth Engine data catalogue](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_DYNAMICWORLD_V1)

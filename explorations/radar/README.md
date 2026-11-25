## Independent Sentinel Hub access route

The repository also contains a separate OAuth2 client-credentials route for Sentinel Hub. It does not replace or modify the OData SAFE downloader.

- [Sentinel Hub Sentinel-1 Catalog client](query_sentinelhub_sentinel1.py) requests a short-lived token from the CDSE identity service, then searches the `sentinel-1-grd` collection for IW scenes intersecting the Nairobi study bounding box.
- The client reads `SENTINEL_HUB_CLIENT_ID` and `SENTINEL_HUB_CLIENT_SECRET` from environment variables. It never prints or writes the client secret or access token.
- The manual workflow is [sentinelhub-sentinel1-catalogue.yml](../../.github/workflows/sentinelhub-sentinel1-catalogue.yml). Configure two GitHub Actions repository secrets with those exact names before dispatching it.
- The workflow saves the STAC response and a metadata sidecar as a short-lived Actions artifact. It does not download a SAFE archive or imagery pixels; catalogue discovery is a first authentication and data-availability check, not a processing result.

Run locally from the repository root:

```bash
export SENTINEL_HUB_CLIENT_ID='your-client-id'
export SENTINEL_HUB_CLIENT_SECRET='your-client-secret'
python explorations/radar/query_sentinelhub_sentinel1.py
```

The OAuth client-credentials flow and Catalog API endpoint/collection are documented by [CDSE Sentinel Hub authentication](https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Overview/Authentication.html), [Catalog API](https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Catalog.html), and [Sentinel-1 GRD collection guidance](https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Data/S1GRD.html). Sentinel Hub catalogue results are not equivalent to original SAFE archive downloads; use the OData route when the study requires the original product package and its complete SAFE structure.

## Sentinel-1 Process API raster sample and quality checks

The separate [Process API client](process_sentinelhub_sentinel1.py) requests one Nairobi Sentinel-1 GRD acquisition as a three-band GeoTIFF. It selects the latest catalogue footprint that covers the entire rectangular search window; a newer partial scene is not preferred. Partial-scene selection requires the explicit `--allow-partial-coverage` option.

1. VV gamma-zero ellipsoid backscatter in linear-power units.
2. VH gamma-zero ellipsoid backscatter in linear-power units.
3. `dataMask`, where 1 marks valid pixels and 0 marks pixels outside the returned scene coverage.

The [raster inspector](inspect_sentinelhub_sentinel1.py) checks the band count, binary data mask, finite/non-negative backscatter values within valid pixels, and reports the actual valid-pixel fraction. It also writes a log-stretched VV/VH quicklook and a machine-readable QA JSON report. The quicklook is visualization only; quantitative work must use the original linear-power bands and data mask.

Install the optional processing dependencies with:

```bash
python -m pip install -r explorations/radar/requirements-sentinelhub-processing.txt
```

Run the inspector after acquiring a raster:

```bash
python explorations/radar/inspect_sentinelhub_sentinel1.py data/sentinelhub/nairobi/<raster-file>.tif
```

The first experimental sample (18 November 2026) covered approximately 74.70% of the requested rectangular extent. Catalogue review found a full-coverage acquisition from 14 November 2026. The selection logic now prefers that full-footprint scene. Any downstream analysis must still intersect the raster data mask with a defined study-area boundary and report coverage within that AOI. The requested 2048 × 1536 grid corresponds to approximately 21.7 m pixel spacing at the raster centre; this is the output grid spacing, not a native-resolution guarantee.

### Nairobi County boundary mask

The [county masking script](mask_sentinelhub_sentinel1_nairobi_county.py) fetches exactly one Nairobi County polygon from the WWF-Kenya ArcGIS FeatureServer, validates it, saves the returned GeoJSON, and creates a separate county-cropped GeoTIFF. The service states that its 47-county boundary layer was supplied by Survey of Kenya and shared to WWF-Kenya by the Ministry of Lands - Directorate of Physical Planning; the service credits Ministry of Lands and WWF-Kenya. See the [service description](https://wwfke-giscoe.wwfkenya.org/arcgis/rest/services/Basedata_Kenya/KenyaCountyBoundary/FeatureServer) and [layer schema](https://wwfke-giscoe.wwfkenya.org/arcgis/rest/services/Basedata_Kenya/KenyaCountyBoundary/FeatureServer/0).

This is an exploratory administrative boundary, not a legal survey/cadastral boundary. The exact GeoJSON used is retained beside the output so the run can be reproduced even if the live service changes. The county QA report calculates valid scene coverage only among pixel centres inside the polygon. VV/VH are set to nodata outside the county or where the source dataMask is invalid; the output dataMask is 1 only for valid county pixels. This is a separate derivative: the original rectangular GeoTIFF is preserved unchanged.

Run the mask after acquiring a raster:

```bash
python explorations/radar/mask_sentinelhub_sentinel1_nairobi_county.py data/sentinelhub/nairobi/<raster-file>.tif
```

The manual [Sentinel Hub raster workflow](../../.github/workflows/sentinelhub-sentinel1-process.yml) now uploads the source GeoTIFF, county-masked GeoTIFF, boundary GeoJSON, source metadata, quicklook, and QA reports together. Its artifact retention is 14 days, so download or persist outputs required for longer-term research.


## Surat R009 radiometric relation and independent processor check

The four-scene Sentinel Hub ellipsoid/RTC relationship analysis, equation derivation,
QA metrics, limitations and OPERA RTC-S1 independent-processor plan are documented in
[surat-r009-angle-equation.md](surat-r009-angle-equation.md).

- [Equation QA implementation](qa_surat_r009_angle_equation.py)
- [OPERA RTC/RTC-STATIC catalogue discovery](discover_opera_surat_r009_products.py)
- [OPERA asset downloader](download_opera_surat_r009_assets.py)
- [Catalogue discovery workflow](../../.github/workflows/opera-surat-r009-discovery.yml)
- [Asset download workflow](../../.github/workflows/download-opera-surat-r009-assets.yml)
- [Cross-processor comparison implementation](compare_opera_surat_r009_processors.py)
- [Cross-processor comparison tests](test_compare_opera_surat_r009_processors.py)
- [Cross-processor comparison workflow](../../.github/workflows/compare-opera-surat-r009-processors.yml)

OPERA catalogue discovery is reproducible without credentials. Raster downloads
require an Earthdata Login bearer token in the repository Actions secret
`EARTHDATA_TOKEN`; never commit the token or paste it into source files. The
cross-processor workflow retrieves the two existing raster artifacts by run ID,
reprojects Sentinel Hub linear-power values to each OPERA burst grid, and writes
a JSON report without storing large rasters in Git.

- [OPERA Nairobi R130 catalogue discovery](discover_opera_nairobi_r130_products.py)
- [Discovery tests](test_discover_opera_nairobi_r130_products.py)
- [Discovery workflow](../../.github/workflows/discover-opera-nairobi-r130.yml)

The discovery workflow screens OPERA RTC-S1 burst products for the Nairobi ascending R130 candidate window and uploads a compact catalogue report. It does not download raster data or prove a Sentinel Hub source-scene match; those remain separate admission gates.

- [OPERA/Sentinel Hub candidate matcher](match_opera_nairobi_r130_sentinelhub.py)
- [Candidate matcher tests](test_match_opera_nairobi_r130_sentinelhub.py)
- [Cross-provider catalogue workflow](../../.github/workflows/match-opera-nairobi-r130-sentinelhub.yml)

The matcher screens the OPERA R130 dates against Sentinel Hub STAC items using relative orbit, orbit direction, platform, dual polarization and a five-minute source-time window. Qualified records are still catalogue candidates; original source-scene identity must be verified before any raster comparison.

- [OPERA Nairobi R130 asset downloader](download_opera_nairobi_r130_assets.py)
- [Downloader tests](test_download_opera_nairobi_r130_assets.py)
- [OPERA asset download workflow](../../.github/workflows/download-opera-nairobi-r130-assets.yml)

The download workflow requires the existing `EARTHDATA_TOKEN` Actions secret. It verifies byte counts where ASF supplies them and records SHA-256 checksums; downloaded rasters remain in a 14-day Actions artifact rather than Git.

- [OPERA R130 metadata and raster-grid audit](audit_opera_nairobi_r130_assets.py)
- [Audit tests](test_audit_opera_nairobi_r130_assets.py)
- [Audit workflow](../../.github/workflows/audit-opera-nairobi-r130-assets.yml)

The audit downloads the retained OPERA asset artifact from workflow run `45345864969`, inspects the HDF5 identification/source-data/processing-input metadata, and checks that all dynamic and static rasters for each burst share the same grid. It deliberately checks grid consistency within each burst, not across adjacent bursts.

- [OPERA SLC / Sentinel Hub GRD datatake verifier](verify_opera_nairobi_r130_source_match.py)
- [Datatake verifier tests](test_verify_opera_nairobi_r130_source_match.py)

The verifier crosswalks OPERA's documented `l1SlcGranules` HDF5 input field against Sentinel Hub GRD catalogue item identifiers using platform, IW mode, acquisition start time, absolute orbit and datatake identifier. It distinguishes source-acquisition correspondence from equality of the two processed products.

- [Nairobi R130 paired Sentinel Hub processor](process_nairobi_r130_sentinel1_validation.py)
- [Nairobi R130 processor tests](test_process_nairobi_r130_sentinel1_validation.py)
- [Nairobi R130 paired-processing workflow](../../.github/workflows/process-nairobi-r130-sentinelhub-pairs.yml)

The processor requests five source-verified GRD datatakes in both ellipsoid and terrain gamma0 conventions, retains linear VV/VH, and emits per-scene data-mask and grid QA. It does not claim radiometric validation; comparison to OPERA native burst grids is a separate downstream gate.

- [Nairobi R130 OPERA/Sentinel Hub common-support QA](qa_nairobi_r130_common_support.py)
- [Common-support QA tests](test_qa_nairobi_r130_common_support.py)

This QA resamples Sentinel Hub validity support and linear-power VV/VH onto each native OPERA burst grid, applies documented OPERA dynamic/static mask semantics and a 95% source-support threshold, and reports valid/common sample counts separately for each date, burst, and polarization. It is a precondition for radiometric comparison, not itself a validation result.

- [Nairobi R130 cross-processor comparator](compare_opera_nairobi_r130_processors.py)
- [Comparator tests](test_compare_opera_nairobi_r130_processors.py)
- [Comparison workflow](../../.github/workflows/compare-opera-nairobi-r130-processors.yml)

The comparator reconstructs OPERA ellipsoid gamma0 from terrain gamma0, ANF and ellipsoid incidence angle, then compares the terrain-minus-ellipsoid delta against Sentinel Hub. It area-averages masked linear power onto native OPERA burst grids before dB conversion and reports per-date/per-burst/per-polarization plus pooled-pixel residual metrics. The workflow runs only after paired-raster processing and common-support QA succeed.

**First independent-orbit result:** the Nairobi R130 cross-processor comparison completed for five dates, three IW3 bursts and VV/VH. Pooled residual bias is approximately +0.004 dB in both polarizations; MAE is approximately 0.090 dB (VV) and 0.092 dB (VH). The full per-burst diagnostics, limitations and follow-on residual investigation are recorded in [the second-orbit protocol and results](second-orbit-validation-protocol.md). This is case-bounded evidence, not universal validation.

## Nairobi R130 residual spatial diagnostics

- [Residual diagnostic implementation](diagnose_opera_nairobi_r130_residuals.py)
- [Residual diagnostic tests](test_diagnose_opera_nairobi_r130_residuals.py)
- [Residual maps and stratification workflow](../../.github/workflows/diagnose-opera-nairobi-r130-residuals.yml)

The diagnostic stage has completed and exported 30 float32 GeoTIFF residual maps (five dates × three native OPERA bursts × VV/VH), preserving each source CRS, affine transform and nodata. The JSON report includes per-scene distributions, exceedance fractions above 0.5/1/2 dB, fixed incidence-angle strata, scene-local ANF quartiles and the ten largest absolute residual coordinates per scene/polarization. It applies the same masks and 95% valid-support threshold as the first-pass comparator. [Workflow run](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45360551227) · [30 maps + JSON artifact](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45360551227/artifacts/14904975668).

The residual dispersion increases consistently from burst 279214 to 279216. Across all three bursts, the lowest and highest ANF quartiles have higher MAE than the middle quartiles, while incidence-angle coverage is too concentrated to support a robust angular-response conclusion. This is an association, not causation; terrain/slope/aspect and independently validated land-cover attribution remain to be tested. No outliers are removed. The [second-orbit validation protocol](second-orbit-validation-protocol.md) records the evidence and limitations. This remains case-bounded evidence, not universal validation.

#### Terrain covariate stage

- [Copernicus DEM acquisition](acquire_nairobi_r130_copernicus_dem.py) downloads the public Copernicus GLO-30 COG tiles from the AWS Open Data bucket, then resamples the masked DEM to the study grid. This avoids the Sentinel Hub DEM Process API's account-restricted COPERNICUS_30 access.
- [Terrain residual stratifier](terrain_stratify_nairobi_r130_residuals.py) reprojects the masked DEM to each native OPERA grid and summarizes residuals by slope and downslope aspect.
- [Terrain derivative tests](test_terrain_stratify_nairobi_r130_residuals.py)
- [DEM acquisition workflow](../../.github/workflows/acquire-nairobi-r130-dem.yml)
- [Terrain stratification workflow](../../.github/workflows/terrain-stratify-nairobi-r130-residuals.yml)

The Copernicus DEM is a surface model, not a bare-earth terrain model. The public GLO-30 AWS copy has limited tile coverage and represents the 2021 public release; the output sampling grid does not create new terrain detail. Source: [AWS Open Data registry](https://registry.opendata.aws/copernicus-dem/) and [tile/readme specification](https://copernicus-dem-30m.s3.amazonaws.com/readme.html). The acquisition and stratification workflows are separate so the DEM is retained as a versioned, short-lived artifact and can be reused. MAE rises with slope in all three bursts and both polarizations; south/southwest aspect bins also show higher errors than north-facing bins. These are associations, not causal explanations: the DEM is a DSM, and slope/aspect may covary with ANF and land cover. A support-edge test found higher >1 dB exceedance fractions in the outermost valid pixel, but the 20-pixel (~600 m) edge buffer generally has lower exceedance rates than the deep interior; edge proximity does not explain the broad burst effect. [Edge diagnostic report](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45365267484/artifacts/14905309441).

#### Date-matched land-cover stage (prepared; credentials required)

- [Dynamic World acquisition](acquire_nairobi_r130_dynamic_world.py) builds a 31-day probability composite around each of the five Sentinel-1 dates, retaining the top-class confidence rather than applying a hard confidence mask.
- [Dynamic World acquisition tests](test_acquire_nairobi_r130_dynamic_world.py)
- [Dynamic World acquisition workflow](../../.github/workflows/acquire-nairobi-r130-dynamic-world.yml)
- [Residual-by-class stratifier](stratify_nairobi_r130_dynamic_world.py)
- [Residual-by-class tests](test_stratify_nairobi_r130_dynamic_world.py)
- [Residual-by-class workflow](../../.github/workflows/stratify-nairobi-r130-dynamic-world.yml)

The workflow is manual and not yet run. It requires two GitHub Actions secrets: `GEE_SERVICE_ACCOUNT_JSON` (Earth Engine-enabled service account key JSON) and `GEE_PROJECT_ID` (the registered Google Cloud project). The service account must be authorized to use Earth Engine. Once those are configured, dispatch the acquisition workflow, then dispatch the class/confidence stratification workflow with the acquisition run ID. The analysis keeps all classes and reports confidence thresholds of 0, 0.5, and 0.7; no pixels are excluded from the primary comparison. Dynamic World is a near-real-time 10m Sentinel-2-derived product with nine class probabilities; quality varies with cloud masking and surface type. Dynamic World is the next candidate for date-specific land-cover context; it requires an Earth Engine-backed acquisition route and confidence filtering, so no land-cover attribution is claimed yet.


#### Spatial-block uncertainty analysis (completed)

- [Study protocol](NAIROBI_R130_SPATIAL_BLOCK_UNCERTAINTY_PROTOCOL.md)
- [Verified results report](nairobi-r130-spatial-block-uncertainty-results.md)
- [Reusable bootstrap method](../../methods/spatial-block-bootstrap.md)
- [Raster integration implementation](spatial_block_uncertainty_nairobi_r130.py)
- [Bootstrap primitives and tests](spatial_block_bootstrap.py) · [tests](test_spatial_block_bootstrap.py)
- [Workflow](../../.github/workflows/spatial-block-uncertainty-nairobi-r130.yml) · [successful run](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45627570253) · [JSON artifact](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45627570253/artifacts/15030370525)

The completed run reports 30 date × burst × polarization records, each evaluated at three block sizes and three Dynamic World confidence thresholds. The result is a within-scene block-bootstrap analysis; the report explicitly avoids treating repeated scene records as independent replicates for pooled inference.

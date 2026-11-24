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

## Second independent-orbit validation

The [second-orbit validation protocol](second-orbit-validation-protocol.md) defines the scientific question, candidate source, admission gates and stop/go rules before additional raster processing. The existing Nairobi ascending R130 Sentinel Hub workflow is a candidate acquisition source only; OPERA RTC-S1 source identity, matching static layers and valid raster overlap still need to be established. No second cross-processor validation is claimed yet.

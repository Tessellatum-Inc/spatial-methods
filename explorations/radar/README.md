undefined

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

The manual [Sentinel Hub raster workflow](../../.github/workflows/sentinelhub-sentinel1-process.yml) now uploads the GeoTIFF, source metadata, quicklook, and QA report together. Its artifact retention is 14 days, so download or persist outputs required for longer-term research.

# STAC imagery review CLI

This is a local, point-window workflow for imagery review. It searches Sentinel-2 L2A STAC items for the blind Fiji pilot points and, where assets are accessible, reads a small RGB window around each point. It does not intentionally download full Sentinel-2 scenes.

## Install

From this directory:

```bash
python -m pip install -r requirements-stac-imagery.txt
```

## Start with catalogue discovery only

```bash
python stac_imagery_review.py \
  --input data/fiji-worldcover-legend-adjudication-blind-review.csv \
  --output-dir /tmp/fiji-stac-review \
  --metadata-only
```

This writes candidate item metadata and catalogue errors. The CLI queries each point independently, follows STAC pagination links (up to ten pages per collection), and sorts returned candidates locally by scene-level cloud cover and acquisition time. It does not rely on the optional STAC sort extension.

Review the results before requesting chips. A partial catalogue failure is retained in `stac-search-errors.csv` even if another collection returned items.

## Create temporary chips from accessible assets

```bash
python stac_imagery_review.py \
  --input data/fiji-worldcover-legend-adjudication-blind-review.csv \
  --output-dir /tmp/fiji-stac-review \
  --keep-chips
```

By default, chips are deleted after their provenance rows are written. Use `--keep-chips` only when you want to inspect them locally. PNG chips are not committed to Git.

The script transforms each WGS84 sample coordinate into the raster asset's own CRS before calculating the pixel window. It prefers explicit 10 m RGB assets and refuses to stack bands whose CRS, affine transform or raster dimensions do not match. The visual stretch is independent per band (2nd–98th percentile); it is for interpretation, not radiometric analysis.

## CDSE S3 credentials

CDSE STAC discovery can work independently of S3 image access. To read CDSE `s3://eodata/...` assets, first create S3 credentials in your Copernicus Data Space account and export them in the shell:

```bash
export AWS_ACCESS_KEY_ID="your-CDSE-access-key"
export AWS_SECRET_ACCESS_KEY="your-CDSE-secret-key"
export CDSE_S3_ENDPOINT="eodata.dataspace.copernicus.eu"
```

Do not put credentials in the script, CSV, Git repository, notebook, or screenshots. This script uses GDAL's `/vsis3/` support for CDSE assets. If the installed GDAL/rasterio build cannot access the CDSE endpoint, the chip row will be marked as failed; it will not download the complete product as a fallback.

## Fiji / antimeridian handling

The CLI queries each point independently. This avoids a single Fiji-wide bounding box spanning +180° and −180°. It searches Earth Search and CDSE separately. Earth Search's known antimeridian catalogue omissions mean that an empty Earth Search response is not proof that no Sentinel-2 observation exists; check CDSE results too.

## Output and storage

- `stac-imagery-provenance.csv`: one row per candidate item/chip attempt.
- `stac-search-errors.csv`: collection/API errors by point, including partial failures.
- Provenance uses a fixed column schema, so metadata-only, failed-chip and successful-chip rows can safely coexist in one run.
- PNG chips: temporary, only retained with `--keep-chips`.
- No full scenes are intentionally downloaded or stored.
- Provenance records item IDs, acquisition time, cloud metadata, selected assets, source grid, output dimensions, output bytes and SHA-256.
- Rasterio/GDAL does not expose an exact network-byte count for these reads, so the CLI does not invent one.
- Stale CSV outputs from an earlier run are removed when the current run has no corresponding rows/errors.

## Interpretation cautions

- Search results are candidates, not proof of local image quality. Scene cloud percentage is not point-level cloud screening.
- Duplicate or blank `sample_id` values, including filename collisions after sanitisation, are rejected before retrieval.
- A point that falls outside the selected raster asset bounds is marked as a failed chip rather than producing a misleading all-nodata image.
- A catalogue failure is recorded as `search_failed`, not `no_items`; only a successful empty search is labelled `no_items`.
- The 25 points are a purposive disagreement sample, not a probability sample.
- A 256-pixel 10 m chip covers roughly 2.56 km per side; it is an overview for context, not a substitute for a closer inspection of individual features.
- Use 2021 imagery for the primary review; any other date must be explicitly documented as temporal context.
- Do not redistribute imagery unless the source licence permits it.

## Validation status

The unit tests cover cloud metadata handling, RGB asset selection, STAC pagination/deduplication, and partial collection failures. Passing those tests does not validate live catalogue availability, CDSE credentials, remote COG/S3 reads, or visual suitability. Those require a run in an environment with network access and (for CDSE S3 assets) the user's own credentials.

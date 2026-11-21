# STAC imagery review CLI

This is a local, point-window workflow for imagery review. It searches Sentinel-2 L2A STAC items for the blind Fiji pilot points and, where assets are accessible, reads a small RGB window around each point. It does not download full Sentinel-2 scenes.

## Install

From this directory:

\`\`\`bash
python -m pip install -r requirements-stac-imagery.txt
\`\`\`

## Start with catalogue discovery only

\`\`\`bash
python stac_imagery_review.py \\
  --input data/fiji-worldcover-legend-adjudication-blind-review.csv \\
  --output-dir /tmp/fiji-stac-review \\
  --metadata-only
\`\`\`

This writes item metadata and search errors. Review the results before requesting chips.

## Create temporary chips from accessible assets

\`\`\`bash
python stac_imagery_review.py \\
  --input data/fiji-worldcover-legend-adjudication-blind-review.csv \\
  --output-dir /tmp/fiji-stac-review \\
  --keep-chips
\`\`\`

By default, chips are deleted after their provenance rows are written. Use \`--keep-chips\` only when you want to inspect them locally. The PNG chips are not committed to Git.

## CDSE S3 credentials

CDSE STAC discovery can work independently of S3 image access. To read CDSE \`s3://eodata/...\` assets, first create S3 credentials in your Copernicus Data Space account and export them in the shell:

\`\`\`bash
export AWS_ACCESS_KEY_ID="your-CDSE-access-key"
export AWS_SECRET_ACCESS_KEY="your-CDSE-secret-key"
export CDSE_S3_ENDPOINT="eodata.dataspace.copernicus.eu"
\`\`\`

Do not put credentials in the script, CSV, Git repository, notebook, or screenshots. This script uses GDAL's \`/vsis3/\` support for CDSE assets. If the installed GDAL/rasterio build cannot access the CDSE endpoint, the chip row will be marked as failed; it will not download the complete product as a fallback.

## Fiji / antimeridian handling

The CLI queries each point independently. This avoids a single bounding box spanning +180° and −180°. It searches Earth Search and CDSE separately. Earth Search's known antimeridian catalogue omissions mean that an empty Earth Search response is not proof of no coverage; check CDSE results too.

## Output and storage

- \`stac-imagery-provenance.csv\`: one row per candidate item/chip attempt.
- \`stac-search-errors.csv\`: catalogue/API errors by point.
- PNG chips: temporary, only retained with \`--keep-chips\`.
- No full scenes are intentionally downloaded or stored.
- The script records chip dimensions, output bytes and SHA-256. Rasterio does not expose an exact network-byte count for GDAL range requests, so it does not invent one.

## Interpretation cautions

- Search results are candidates, not proof of local image quality. Scene cloud percentage is not point-level cloud screening.
- The 25 points are a purposive disagreement sample, not a probability sample.
- A 10 m Sentinel-2 chip may not resolve small fields, narrow features or mixed pixels.
- Use only 2021 imagery for the primary review; any other date must be explicitly documented as temporal context.
- Do not redistribute imagery unless the source licence permits it.

# STAC-first imagery review for the Fiji pilot

**Status:** Architecture decision; implementation is gated on live catalogue and asset-access validation  
**Date:** 2026-11-21  
**Scope:** 25-point blind visual-adjudication pilot for the Fiji–WorldCover comparison

## Decision

Use STAC for imagery discovery and retrieve only point-centred review windows. Do not download or retain complete Sentinel-2 scenes as part of the normal review workflow.

The durable project record is:
- the blind point table and reviewer decisions;
- STAC item identifiers and catalogue URLs;
- acquisition time, platform, processing level and cloud metadata;
- the asset/band identifiers used;
- the point-centred review extent, pixel size, processing parameters and output checksum;
- a record of unavailable or unsuitable imagery.

Rendered chips are disposable working files. They should be written to a temporary output directory, excluded from Git, and deleted after review unless a specific chip is independently licensed and deliberately retained as a research artefact.

## Catalogue roles

### 1. Element 84 Earth Search

Endpoint: https://earth-search.aws.element84.com/v1/

Use as the first candidate for public Sentinel-2 COG assets. The catalogue exposes Sentinel-2 L2A collections and COG representations suitable for windowed reads. Its documentation identifies a known limitation: some scenes crossing the antimeridian have been omitted from the catalogue. Fiji's pilot points occur on both sides of ±180°, so an empty Earth Search result must never be interpreted as proof that no Sentinel-2 observation exists.

### 2. Copernicus Data Space STAC

Endpoint: https://stac.dataspace.copernicus.eu/v1/

Use as the coverage/discovery fallback and as the authoritative Copernicus catalogue check. The Sentinel-2 L2A collection is documented and exposes the expected multispectral band metadata, including B02 (blue), B03 (green), B04 (red) and B08 (NIR).

Important access distinction: catalogue discovery and imagery access are separate. CDSE STAC item assets may use `s3://eodata/...` paths. The official CDSE S3 documentation requires a registered CDSE account and generated S3 credentials. Do not assume that an S3 asset href is an unauthenticated HTTPS COG.

## Retrieval strategy

1. Search each pilot point independently, or use spatial batches that are split at the antimeridian. Never create one Fiji-wide bounding box that spans the dateline.
2. Search 2021 acquisitions and retain candidate item metadata before selecting imagery.
3. Prefer observations with low cloud contamination at the point, not merely the lowest scene-wide cloud percentage.
4. Where a public COG is available, use GDAL/rasterio windowed reads with HTTP range requests. Read only the small window around the point; do not copy the complete COG.
5. Where CDSE is the only source, use a properly authenticated on-demand processing path (for example, CDSE Sentinel Hub Process API) or a window-capable S3 reader. Do not silently fall back to downloading complete SAFE products.
6. Produce a small true-colour chip and, where useful, a seasonal/alternative-date chip. Keep the point ID visible but do not expose Fiji or WorldCover labels.
7. Record the actual source item, acquisition date, cloud metadata, asset/bands, output extent, pixel size, stretch, access date and checksum in the review provenance.
8. If no suitable image can be obtained, record the point as unavailable/insufficient imagery. Do not substitute a different year without recording the temporal difference.

## Storage policy

- No complete Sentinel-2 scenes in the repository.
- No persistent imagery cache by default.
- Temporary chips only; configurable output directory and explicit cleanup.
- Keep imagery out of Git and CI artefacts unless a separately licensed, minimal test fixture is required.
- Keep provenance and reviewer annotations in version control.
- Never redistribute Planet NICFI, Google basemap or other third-party imagery/screenshots without checking the applicable licence.

## Fiji-specific safeguards

- Treat +179° and −179° coordinates as nearby geographic locations, not as distant locations in a naïve longitude bounding box.
- Run independent catalogue checks on both sides of the antimeridian.
- Use 2021 imagery where possible because the map comparison and reference labels target 2021.
- Sentinel-2 is 10 m for B02/B03/B04/B08, but small parcels, narrow features and mixed pixels may remain ambiguous.
- Scene-level cloud percentage is a screening field, not a substitute for inspecting local cloud/shadow conditions.
- The 25 points are purposive disagreement cases. Visual review explains selected disagreements; it does not replace or update the design-adjusted accuracy estimates.

## Validation gate before calling the workflow operational

The implementation is not considered operational until it has:
- returned actual 2021 items for test points on both sides of ±180°;
- demonstrated asset access for at least one usable item from each catalogue path being claimed;
- created and visually inspected a point-centred chip without downloading a full scene;
- recorded exact item IDs, dates, asset names, output dimensions and bytes read/downloaded;
- passed tests for empty search results, dateline coordinates, missing assets, inaccessible S3 assets, and temporary-file cleanup.

## References

- Earth Search STAC API and Sentinel-2 collection documentation: https://earth-search.aws.element84.com/v1/api.html
- Copernicus Data Space STAC API documentation: https://documentation.dataspace.copernicus.eu/APIs/STAC.html
- Copernicus Data Space Sentinel-2 L2A collection: https://stac.dataspace.copernicus.eu/v1/collections/sentinel-2-l2a
- Copernicus Data Space S3 access and credential requirements: https://documentation.dataspace.copernicus.eu/APIs/S3.html
- Copernicus Data Space Sentinel Hub API reference: https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/ApiReference.html

## Execution note

The public STAC documentation and Sentinel-2 L2A collection metadata were checked on 2026-11-21. A live Fiji item search and COG/S3 chip retrieval were not completed in the execution environment used for this decision. Therefore this document records an architecture decision and explicit validation gate, not a claim that Fiji imagery retrieval has already succeeded.

# Fiji multispectral pilot — execution specification

**Status:** 25-point live extraction passed; quality-control refinement in progress  
**Date:** 2026-11-21  
**Scope:** five-point technical pilot, then expand only after validation

## Purpose

Add multispectral evidence to the existing 25-point Fiji disagreement review without changing the original reference labels, baseline accuracy estimates, or blind-review decisions. This is an evidence-generation workflow, not a replacement source of ground truth.

## Inputs and point selection

Use the existing repository file:

`data/fiji-worldcover-legend-adjudication-blind-review.csv`

Resolve the path relative to this implementation directory. The first five rows are the pilot points, in the existing order. Read IDs and coordinates directly from the CSV at runtime; do not duplicate coordinates in code or manually transcribe them.

The five-point pilot is a technical feasibility sample only. It is not statistically representative and must not be used to revise the 834-point accuracy estimate.

## Imagery source policy

- Target Sentinel-2 Level-2A surface reflectance acquired in calendar year 2021.
- Search Earth Search and Copernicus Data Space STAC separately for each point. Never use a Fiji-wide bounding box crossing the antimeridian.
- Keep scene metadata and asset access as separate states. A STAC item being discoverable does not prove its assets are readable.
- Prefer public HTTPS COG assets and windowed reads. Do not download full scenes or SAFE products.
- CDSE S3 assets require valid CDSE-generated credentials. Do not ask for credentials in chat or commit them. If they are unavailable, record the asset as inaccessible and continue with eligible public assets.
- Retain acquisition dates, item IDs, collection, platform, processing baseline where exposed, cloud metadata, asset names/hrefs (redact signed query parameters), pixel size, CRS, window bounds, and SHA-256 of every generated output.

## Bands and native resolutions

| Band | Sentinel-2 meaning | Native resolution | Intended use |
|---|---|---:|---|
| B02 | Blue | 10 m | Visible composite, water/soil context |
| B03 | Green | 10 m | Visible composite, water context |
| B04 | Red | 10 m | Visible composite, vegetation indices |
| B08 | Broad NIR | 10 m | NDVI, vegetation structure |
| B05/B06/B07 | Red-edge | 20 m | Vegetation condition / red-edge response |
| B8A | Narrow NIR | 20 m | Red-edge/NIR response |
| B11/B12 | SWIR | 20 m | Moisture, built/exposed surface context |
| SCL | Scene classification | 20 m | Cloud, cirrus, shadow, snow and invalid-pixel screening |

Do not upsample 20 m bands and describe them as 10 m observations. Keep native-resolution statistics distinct. Any resampling for a common display grid must be documented and must not imply additional spatial detail.

## Derived evidence

Calculate only where input bands are valid and denominator stability checks pass:

- NDVI = (B08 - B04) / (B08 + B04)
- NDWI (McFeeters) = (B03 - B08) / (B03 + B08)
- MNDWI = (B03 - B11) / (B03 + B11)
- NDBI = (B11 - B08) / (B11 + B08)
- Optional red-edge index: NDRE = (B8A - B05) / (B8A + B05)

These indices are contextual indicators, not deterministic land-cover labels. NDWI/MNDWI can confuse water with shadows or built materials; NDBI can confuse built surfaces with bare soil; NDVI can vary with season, crop cycle, moisture and canopy condition.

Produce:
1. True-colour B04/B03/B02 composite.
2. False-colour B08/B04/B03 composite.
3. NDVI and valid-pixel mask.
4. Water-oriented NDWI/MNDWI layers where B11 is available.
5. NDBI/SWIR contextual layer where B11/B08 are available.
6. Native 10 m and 20 m point/neighbourhood summaries.
7. A multi-date evidence table rather than selecting one date solely by scene-level cloud percentage.

## Temporal and spatial protocol

- Search the full 2021 calendar year; record all candidate observations.
- Deduplicate cross-catalogue representations of the same platform acquisition (normalized acquisition timestamp and platform) before selecting a bounded number of scenes. When duplicate representations expose different asset URLs, prefer the one with the greatest number of HTTP(S) or known-public sentinel-cogs assets; do not let deduplication discard a publicly readable copy in favour of a credential-gated S3 representation. Record how many catalogue items were collapsed into unique acquisitions.
- Do not select a scene using scene-wide cloud cover alone. Apply SCL screening and inspect point/neighbourhood valid-pixel fractions.
- Use a shared ground footprint across native grids. The extraction reader anchors the footprint on the 20 m grid; the 10 m window is derived from those exact map bounds and must align to twice the pixel dimensions. For example, a 16 × 16 window on the 20 m grid corresponds to 32 × 32 pixels on the 10 m grid (320 m × 320 m). Report bounds, CRS, native pixel size and valid-pixel count.
- Distinguish stable spectral patterns from seasonal/temporal variability. Where evidence changes across dates, flag the point as temporally ambiguous.
- Respect Fiji's antimeridian: search each point separately, and preserve longitude sign exactly.

## Quality gates

The pilot is not operational until:
- all five input rows are read directly from the tracked CSV;
- at least one suitable 2021 observation is retrieved for each pilot point, or a precise unavailability reason is recorded;
- actual multiband raster windows are read successfully (not merely STAC metadata queried);
- SCL masking and nodata handling are tested;
- index calculations are tested against hand-computable synthetic arrays;
- outputs retain native band resolution and CRS metadata;
- all outputs have checksums and machine-readable provenance;
- no original class labels, map labels, or accuracy outcomes are exposed in the blind evidence bundle.

## Interpretation and governance

Multispectral evidence can strengthen or challenge visual interpretation, but cannot by itself establish ground truth. The reference points were visually labelled and are not field-verified. No class decision may be silently changed. A revised label requires a documented review record, reviewer identity, evidence, confidence, alternative class, and explicit versioning. An independent reviewer is preferred; AI-generated interpretation must be labelled as AI-assisted and not independent adjudication.

The 25 disagreement points are purposive. They help diagnose selected disagreements but do not replace or update the design-based 834-point accuracy estimates.

## Storage and cost controls

- No Cloudflare R2 subscription or payment method is required for this phase.
- No paid imagery, Planet NICFI subscription, commercial API, or full-scene download.
- Keep scripts, small manifests, metadata, tests and summary tables in Git.
- Keep raster chips and derived rasters as temporary workflow outputs or CI artifacts only when small and necessary. Do not commit large imagery.
- Use existing GitHub Actions capacity conservatively; no new paid runners or services.

## Current implementation status

The bounded 25-point public Earth Search multispectral run completed successfully on 2026-11-21. It attempted 75 candidate scenes: 61 complete reads and 14 failures caused by an S3 asset bucket requiring AWS credentials. Every one of the 25 points had at least one successful candidate with all four core 10 m bands and the complete requested 11-band set including SCL. Successful records span 22 distinct acquisition timestamps across the sample. The first deduplicated run exposed a representation-selection issue: for some acquisitions it retained a credential-gated S3 record even though another catalogue's duplicate offered public HTTPS assets. Deduplication now scores asset accessibility and keeps the most publicly readable representation for each acquisition. These counts describe retrieval, not cloud-free coverage or independent temporal observations.

The repository now has three distinct layers:

1. `stac_imagery_review.py` discovers 2021 scenes and retrieves RGB chips from public Earth Search COG assets.
2. `multispectral_metrics.py` provides numerical index, SCL-mask and window-summary primitives using co-registered arrays.
3. `multispectral_raster.py` selects Sentinel-2 band assets and reads small windows while preserving native 10 m and 20 m grids.

The multispectral raster reader has synthetic GeoTIFF tests in GitHub Actions. It is deliberately not yet wired into a live multi-date pilot runner. Do not imply that full multispectral retrieval, SCL-screened index generation, multi-date compositing or neighbourhood statistics have been completed.

The existing RGB workflow has completed a live full-pilot retrieval run: 25 blind-review points, 75 candidate/window attempts, 61 successful RGB chip reads, 14 failed candidate reads, and at least one successful chip for every point. This validates RGB retrieval coverage only, not multispectral asset availability or reference-label suitability.

The 25-point extraction artifact is retained in GitHub Actions. Initial inspection shows all successful records contain native 20 m SCL. The first 25-point run used equal pixel counts at both resolutions, creating different ground footprints (320 m at 10 m and 640 m at 20 m). This was identified before interpretation. The reader has now been revised to anchor on the 20 m footprint and derive aligned 10 m windows from the same bounds, without resampling. The follow-up run must validate this change. Quality reporting also exposes unmasked and SCL-valid NDRE summaries, plus native-grid SCL class and valid-pixel fractions. SCL is not projected onto the 10 m NDVI grid; cross-resolution masking is deliberately not implied. No land-cover class assignments, map labels, or accuracy outcomes are generated by this pipeline.

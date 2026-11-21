# Fiji Sentinel-2 multispectral raster extraction

## Purpose

This module adds the raster-I/O layer needed to move the Fiji blind-review pilot beyond RGB imagery. It reads small point-centred windows from Sentinel-2 STAC assets and preserves source provenance. It does not assign land-cover labels, adjudicate reference labels, or alter the original accuracy assessment.

## Implementation

- `multispectral_raster.py` selects Sentinel-2 bands using common Earth Search and Copernicus Data Space STAC asset aliases.
- It reads only a bounded raster window around each supplied WGS84 coordinate.
- It reprojects the point coordinate into each asset CRS before calculating the pixel window.
- Nodata is represented as NaN.
- STAC `raster:bands` scale and offset are applied when supplied; otherwise source values remain in source units.
- Per-band metadata records the selected asset key, source href, CRS, map-unit pixel size, scale/offset, nodata and grid signature.
- Missing bands are explicitly listed.
- Bands within the same nominal native grid group must share CRS, affine transform and raster dimensions.

## Resolution and alignment rules

Sentinel-2 bands are separated into two native-grid groups:

| Native grid | Bands |
|---|---|
| 10 m | B02, B03, B04, B08 |
| 20 m | B05, B06, B07, B8A, B11, B12, SCL |

The module never resamples 20 m data to 10 m. It also refuses to combine bands whose grids do not match within their native group.

The current `window_pixels` parameter is a pixel count per band, not a fixed ground-distance footprint. Therefore a 32 × 32 window at 10 m covers a different ground area from a 32 × 32 window at 20 m. Do not compare those window summaries as if they represented the same spatial footprint. A later orchestration layer should use an explicit ground-distance window policy if cross-resolution neighbourhood comparisons are required.

## Interpretation safeguards

- SCL is returned as a categorical band; it is not treated as reflectance.
- The reader does not silently apply a 20 m SCL mask to 10 m bands.
- The numerical index functions are separate. Indices requiring bands from different native grids must wait for an explicit, documented common-grid strategy.
- Scene-level cloud cover is not a point-level cloud assessment.
- Successful window reads establish technical retrieval, not suitability of a scene for reference interpretation.
- No map labels, class transitions, or accuracy outcomes are included in the extraction output.

## Tests and verification

The GitHub Actions unit-test job runs synthetic GeoTIFF tests for:
- native asset alias preference and public HTTPS preference;
- extraction of 10 m and 20 m windows without resampling;
- scale application where STAC metadata is present;
- nodata conversion;
- rejection of misaligned bands within one native grid;
- explicit reporting of missing assets.

These are local synthetic-raster tests. They do not prove that every requested band is available in every live STAC item. The five-point live multispectral retrieval pilot remains a separate verification step.

## Cost and data handling

- No paid imagery, paid API, object storage, or new infrastructure is required.
- The reader uses small remote raster windows, not whole-scene downloads.
- Do not commit raster chips or large derived imagery to Git.
- Keep imagery outputs as short-lived workflow artifacts only when necessary.

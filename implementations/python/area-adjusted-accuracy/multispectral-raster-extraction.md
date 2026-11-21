# Fiji Sentinel-2 multispectral raster extraction

## Purpose

This module adds the raster-I/O layer needed to move the Fiji blind-review pilot beyond RGB imagery. It reads small point-centred windows from Sentinel-2 STAC assets and preserves source provenance. It does not assign land-cover labels, adjudicate reference labels, or alter the original accuracy assessment.

## Implementation

- `multispectral_raster.py` selects Sentinel-2 bands using common Earth Search and Copernicus Data Space STAC asset aliases.
- It reads only a bounded raster window around each supplied WGS84 coordinate.
- It reprojects the point coordinate into each asset CRS before calculating the pixel window.
- Nodata is represented as NaN.
- STAC `raster:bands` scale and offset are applied when supplied; otherwise source values remain in source units.
- Per-band metadata records the selected asset key, source href, CRS, map-unit pixel size, scale/offset, nodata, grid signature, window shape and exact window bounds.
- Missing bands are explicitly listed.
- Bands within the same nominal native grid group must share CRS, affine transform and raster dimensions.

## Resolution and alignment rules

Sentinel-2 bands are separated into two native-grid groups:

| Native grid | Bands |
|---|---|
| 10 m | B02, B03, B04, B08 |
| 20 m | B05, B06, B07, B8A, B11, B12, SCL |

The module never resamples 20 m data to 10 m. It refuses to combine bands whose grids do not match within their native group.

When both resolutions are requested, the 20 m grid anchors the window bounds. The 10 m window is derived from those exact map bounds and must align to twice the pixel dimensions. For example, a 16 × 16 window at 20 m corresponds to a 32 × 32 window at 10 m, with both covering 320 m × 320 m. Cross-resolution arrays therefore describe the same footprint while retaining their native pixel sizes. If the 10 m grid is not exactly aligned to the 20 m reference bounds, extraction fails rather than silently resampling. If only one grid group is available, the requested pixel count applies to that group.

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
- shared map bounds across 10 m and 20 m windows without resampling;
- rejection of cross-resolution grids whose pixel alignment is not exact;
- explicit reporting of missing assets.

These are local synthetic-raster tests. They do not prove that every requested band is available in every live STAC item. The five-point and 25-point live multispectral retrieval runs are separate from synthetic tests. A successful run confirms asset retrieval and extraction, not visual suitability or ground truth.

## Cost and data handling

- No paid imagery, paid API, object storage, or new infrastructure is required.
- The reader uses small remote raster windows, not whole-scene downloads.
- Do not commit raster chips or large derived imagery to Git.
- Keep imagery outputs as short-lived workflow artifacts only when necessary.

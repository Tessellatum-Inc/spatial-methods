# Fiji Sentinel-2 multispectral visual evidence

**Status:** Implemented; live workflow validation pending  
**Date:** 2026-11-21

## Purpose

Generate reproducible, label-blind visual context from the same Sentinel-2 raster windows used for numerical summaries. The generator creates evidence panels only; it does not classify land cover, rank classes, or expose either map's labels.

## Panels

| Panel | Inputs | Native grid | Interpretation role |
|---|---|---:|---|
| True colour | B04/B03/B02 | 10 m | Visible surface context |
| False colour | B08/B04/B03 | 10 m | Vegetation and surface structure |
| NDVI | B08/B04 | 10 m | Vegetation greenness/context |
| SCL categories | SCL | 20 m | Cloud/shadow/scene-quality context |
| SCL-screened NDRE | B8A/B05 + SCL | 20 m | Red-edge vegetation response |
| SWIR/red-edge | B12/B11/B05 | 20 m | Moisture, exposed surface and vegetation context |

Panels are generated only when required bands are present and their arrays have matching shapes. The implementation does not resample or combine 10 m and 20 m bands. NDRE masking is applied only when the SCL array has the same shape and therefore the same native grid.

## Display treatment

RGB channels are independently stretched using the 2nd and 98th percentiles of the current point-window. Index panels use the 0th and 100th percentiles. These are display stretches, not analytical transformations; original numeric arrays and reported index summaries are unchanged. Because each window has its own stretch, panel brightness is not directly comparable between dates or points. Visual comparisons should use the numeric summaries and provenance alongside the images.

The SCL panel displays category codes as grayscale intensity for compact inspection. It is categorical data, not a continuous measure; consult the SCL class-count and fraction report rather than interpreting brightness as magnitude.

## Provenance

Every image record includes sample ID, STAC item ID, acquisition timestamp, panel name, native grid, source-band names, display stretch, mask description and SHA-256 checksum. The JSON visual manifest indexes the generated PNGs. Source raster metadata remains in the multispectral CSV provenance field, including native grid signatures and window bounds.

## Scientific limitations

- These panels are Sentinel-2 evidence, not field observations or verified ground truth.
- A 320 m neighbourhood is contextual; the point's assigned reference class may represent a smaller or mixed feature.
- A percentile stretch can hide subtle absolute radiometric differences between acquisitions.
- SCL is a scene-classification product and can itself be wrong; it is a quality screen, not ground truth.
- The 20 m SCL mask is applied to NDRE only on its native grid. It is not projected onto 10 m NDVI.
- No MNDWI or NDBI panel is generated because the conventional band definitions cross native 10 m/20 m grids. No unreported resampling is introduced to make them.
- The 25 points are a purposive disagreement sample. Their review cannot revise the original design-based 834-point accuracy estimate.

## Human review

Use the panels as corroborating evidence. Record the visible observation separately from class interpretation, confidence, ambiguity and limitations. Do not infer a class solely from one index. Where a point is mixed, seasonally variable, obscured or not interpretable at the available scale, record ambiguity and request a second review rather than forcing a class. AI-generated interpretation is not independent human validation.

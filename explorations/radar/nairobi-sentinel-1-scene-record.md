# Nairobi Sentinel-1 scene record

**Status:** Study specification prepared; scene selection and processing not yet completed.
**Study area:** Nairobi urban search window, Kenya.
**Coordinate reference:** WGS 84 (EPSG:4326).

## Area of interest

- West: 36.65°E
- South: 1.45°S
- East: 37.05°E
- North: 1.15°S

This rectangular window is for scene discovery only. It is not an official administrative boundary or a final analysis mask. Record the boundary source and version if an area-based analysis is later performed.

## Investigation question

How does C-band Sentinel-1 backscatter vary across dense built-up areas, vegetated/open spaces and water-related surfaces in Nairobi, and which patterns may be explained by surface scattering versus acquisition geometry?

## Candidate scene selection

Select the latest suitable Sentinel-1 IW GRD scene intersecting the AOI, preferably with VV and VH polarisation. If the latest scene does not provide complete coverage or the required channels, select the next suitable candidate and document the reason.

| Field | Record |
|---|---|
| Product identifier | Pending |
| Satellite | Pending |
| Acquisition date/time (UTC) | Pending |
| Product type / mode | Pending |
| Pass direction | Pending |
| Relative orbit | Pending |
| Polarisation | Pending |
| Scene footprint coverage | Pending |
| Processing source / product | Pending |
| Backscatter coefficient | Pending |
| Value scale and units | Pending |
| DEM / terrain correction | Pending |
| Speckle filter | Pending |
| Software and version | Pending |

## Minimum workflow

1. Search the Copernicus Data Space catalogue or ASF Vertex using the AOI and select a suitable scene.
2. Preserve the original product identifier and metadata.
3. Process the GRD data using a documented, product-appropriate workflow, or use an RTC derivative whose metadata and processing choices are available.
4. Inspect VV and VH separately. Record whether values are linear power, amplitude or decibels and identify the backscatter coefficient.
5. Inspect at least three contrasting areas. For each, record observations and competing physical explanations.
6. Compare with a temporally close Sentinel-2 observation or another dated reference, documenting temporal mismatch and limitations.
7. Do not produce a land-cover label, flood claim or accuracy statistic without an appropriate reference dataset and validation design.

## Observation table

| Area / feature | VV observation | VH observation | Plausible explanation(s) | Alternative explanation / uncertainty | Reference evidence |
|---|---|---|---|---|---|
| Dense built-up area | Pending | Pending | Pending | Pending | Pending |
| Vegetated / open area | Pending | Pending | Pending | Pending | Pending |
| Water-related / smooth surface | Pending | Pending | Pending | Pending | Pending |

## Deliverable

A reproducible scene interpretation note with source product, processing provenance, three observations, competing explanations, reference evidence and limitations. A map is optional; defensible interpretation is the required output.

## Evidence and access

- [Copernicus Sentinel-1 collection and coverage](https://dataspace.copernicus.eu/data-collections/copernicus-sentinel-missions/sentinel-1)
- [Copernicus Data Space Sentinel-1 product documentation](https://documentation.dataspace.copernicus.eu/Data/SentinelMissions/Sentinel1.html)
- [Copernicus Data Space catalogue API documentation](https://documentation.dataspace.copernicus.eu/APIs/OData.html)
- [Copernicus Browser product search](https://documentation.dataspace.copernicus.eu/Applications/Browser.html)
- [ASF Vertex](https://search.asf.alaska.edu/)

**No scene-specific result is claimed until a product has been selected, downloaded or accessed, processed, and its metadata archived.**

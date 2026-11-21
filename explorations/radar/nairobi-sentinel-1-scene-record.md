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

## Reproducible catalogue search specification

The first discovery pass is defined as an ASF Search API query over the study window:

- Dataset: `SENTINEL-1`
- Beam mode: `IW`
- Processing level: `GRD_HD` (high-resolution detected GRD)
- Polarisation: `VV+VH`
- Acquisition interval: 1 October 2026 through 21 November 2026 (UTC)
- Spatial predicate: the closed WGS 84 polygon defined by the search-window coordinates above
- Output: GeoJSON; maximum 30 candidate records

[Open the defined ASF catalogue query](https://api.daac.asf.alaska.edu/services/search/param?dataset=SENTINEL-1&beamMode=IW&processingLevel=GRD_HD&polarization=VV%2BVH&start=2026-10-01T00%3A00%3A00Z&end=2026-11-21T23%3A59%3A59Z&intersectsWith=polygon%28%2836.65%20-1.45%2C37.05%20-1.45%2C37.05%20-1.15%2C36.65%20-1.15%2C36.65%20-1.45%29%29&output=geojson&maxResults=30)

**Execution status:** The query has been specified and its parameter meanings checked against the ASF Search API documentation. The executable client in [query_asf_sentinel1.py](query_asf_sentinel1.py) constructs the closed WKT polygon with the required nested parentheses and archives the exact response with a SHA-256 digest. The query parameter names and accepted values are checked against the [official ASF Search API keyword reference](https://docs.asf.alaska.edu/api/keywords/), including the closed WKT `intersectsWith` predicate and GeoJSON output. The live API response could not be retrieved in this review environment. Therefore this is not evidence that the query returned zero or any particular number of scenes, and no candidate product is selected yet.

A second, independent catalogue route is now implemented using the [Copernicus Data Space OData API](https://documentation.dataspace.copernicus.eu/APIs/OData.html). Run it from the repository root:

```bash
python explorations/radar/query_copernicus_sentinel1.py
```

The client filters the Sentinel-1 collection, the documented IW GRD product type, the same closed EPSG:4326 study polygon and an explicit UTC interval. It requests expanded product attributes and archives the exact JSON response with query parameters, retrieval time, response SHA-256 and pagination status under `data/copernicus/nairobi/`. The query does not assume a dual-polarisation result: inspect each product's returned attributes and product name to establish its channels. If an OData `nextLink` is present, the saved first page is incomplete and must not be treated as an exhaustive search. The client does not download products or establish full AOI coverage.

When executing the query, preserve the raw GeoJSON response and query timestamp. Inspect each candidate's full footprint, acquisition time, product identifier, platform, pass direction, relative orbit, polarisation, processing level, and downloadable asset. Confirm full coverage of the intended analysis sub-area rather than relying only on polygon intersection.

If the dual-polarisation query yields no suitable candidate, run and document a second query with `polarization=VV`; do not silently substitute a single-polarisation scene. If the time window must be widened, record the new interval and reason. Select a scene only after comparing candidates and confirming asset access.

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

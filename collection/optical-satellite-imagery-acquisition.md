# Optical satellite imagery acquisition and observation design

**Subject:** SM-COL-004 — Satellite and airborne optical remote sensing  
**Status:** Initial collection-method record; technical review and field/application testing pending  
**Scope:** A measurement-centred method for planning and documenting optical satellite imagery acquisition. Sentinel-2 is used as a worked reference, not as a universal model for all optical sensors.

## 1. Purpose

Optical imagery acquisition is not simply downloading a scene over an area of interest. It is the selection and retrieval of observations whose sensor, spectral response, spatial and temporal sampling, illumination, atmospheric conditions, product processing and provenance are suitable for a defined question.

This record covers the collection side of that chain:

- define the phenomenon and observation requirements;
- select a sensor and product family;
- design spatial and temporal sampling;
- discover candidate acquisitions;
- assess quality and access;
- retrieve and preserve the required assets and metadata;
- record limitations before analysis begins.

Radiometric theory belongs in [Electromagnetic observations and radiometric quantities](../foundations/remote-sensing-physics/electromagnetic-observations-and-radiometric-quantities.md). Algorithms such as NDVI and compositing belong in the Spatial Algorithms pillar. This page does not prescribe one universal processing workflow.

## 2. Begin with the measurand and decision

Write down the target question before searching imagery. Identify:

1. **Phenomenon:** what surface, process or change is of interest?
2. **Measurand or indicator:** what quantity is to be observed or estimated (for example, surface reflectance in a specified band, a spectral index, or a mapped class)?
3. **Spatial support:** what area, feature size or minimum mapping unit matters?
4. **Temporal support:** what date, season, event window or revisit interval is needed?
5. **Spectral requirement:** which wavelength regions or spectral response characteristics are necessary?
6. **Accuracy and uncertainty:** what positional, radiometric, thematic or temporal uncertainty is acceptable?
7. **Decision consequence:** what happens if the observation is missing, ambiguous or wrong?

Do not select a sensor solely because it is familiar or has the smallest advertised pixel size. The observation requirements should drive the platform, product, date range and validation design.

## 3. Choose an observation system

Optical satellite systems differ in spectral bands, swath width, revisit, spatial resolution, radiometric performance, acquisition strategy, processing levels, access conditions and archive history.

A sensor-selection record should compare at least:

| Requirement | Questions |
|---|---|
| Spectral | Does the sensor measure the wavelengths needed? What are the band response functions and bandwidths? |
| Spatial | What is the native ground sampling distance for each band? Is it adequate for the target feature? |
| Temporal | What is the nominal revisit and actual usable observation frequency under cloud and acquisition constraints? |
| Radiometric | What calibration, quantisation, dynamic range and noise characteristics apply? |
| Geometric | What geolocation, orthorectification and registration properties are documented? |
| Environmental | How do cloud, haze, smoke, shadow, snow, sun angle and surface conditions affect usability? |
| Operational | Is the archive accessible, stable, licensed for the intended use and available at the needed latency? |
| Provenance | Can the product version, processing baseline, source identifier and asset checksums be preserved? |

### Sentinel-2 as a reference system

Sentinel-2 MSI provides 13 spectral bands at 10 m, 20 m and 60 m ground sampling distances. The band groups do not all share the same native resolution. Its Level-1C product provides orthorectified top-of-atmosphere reflectance; Level-2A provides bottom-of-atmosphere (surface) reflectance and quality information including scene classification, aerosol optical thickness and water vapour layers. Product specifications and processing baselines matter; always use the current specification corresponding to the downloaded collection.

Do not describe a 20 m or 60 m band resampled to a 10 m grid as a native 10 m observation. Resampling changes the grid representation, not the information content of the original sensor measurement.

## 4. Select product level deliberately

Product levels encode processing history, not a universal quality ranking.

For Sentinel-2, broadly:

- **Level-1B:** radiometrically corrected imagery in sensor geometry, expressed as TOA radiance, with geometric model information.
- **Level-1C:** orthorectified imagery in cartographic geometry, expressed as TOA reflectance.
- **Level-2A:** orthorectified imagery with atmospheric correction to BOA/surface reflectance and additional quality/ancillary layers.

Use Level-2A when surface-reflectance analysis is appropriate and the product's atmospheric correction and quality layers meet the study needs. Use Level-1C when TOA observations or a custom correction chain is required. Do not assume Level-2A removes all atmospheric, topographic, adjacency, BRDF or cloud contamination effects.

The level names and contents are sensor- and product-specific. Landsat, Sentinel-2, commercial constellations and airborne systems do not necessarily use identical level semantics.

## 5. Design spatial and temporal sampling

### Area of interest

Define the area of interest in a documented CRS. Record whether the search geometry is a point, buffered point, polygon, tile or larger region. For small targets, ensure the search and extraction windows are large enough to accommodate geolocation uncertainty and the intended neighbourhood statistics.

A scene footprint intersecting the area does not guarantee full coverage of the target or a complete neighbourhood.

### Date and temporal window

Choose dates from the phenomenon's temporal behaviour:

- crop or vegetation monitoring may require a phenological window;
- flood mapping may require pre-event, event and post-event observations;
- urban change may require dates that distinguish persistent change from construction phases or seasonal effects;
- water-quality applications may require strict atmospheric and sun-glint conditions.

Record the actual acquisition timestamp and time zone convention, not only a calendar date. Avoid combining observations from different seasons without an explicit model of seasonal variation.

### Multi-date design

For time series, record the planned temporal cadence, missing-data strategy and rules for duplicate or overlapping acquisitions. A “best available” composite is a sampling and selection procedure; its selection score and temporal distribution must be documented.

## 6. Discover candidate acquisitions

Use an authoritative mission catalogue or a documented STAC API/catalogue. Search by spatial intersection and time range, then inspect the returned item metadata.

A catalogue result is a discovery record, not proof that the imagery assets are readable or scientifically suitable.

For every candidate, retain where available:

- catalogue and collection identifier;
- item/product identifier and product URI;
- platform, instrument and processing level;
- acquisition timestamp and orbit/relative orbit where relevant;
- footprint and coverage fraction over the area of interest;
- cloud metadata and its spatial scope;
- processing baseline and product generation time;
- band assets, asset media types and native resolutions;
- CRS, grid, scale/offset, units and nodata metadata;
- quality layers and ancillary products;
- licence, provider terms and citation requirements.

When the same acquisition appears in multiple catalogues, deduplicate by the actual acquisition identity and retain the most useful accessible representation. Do not discard an openly readable asset in favour of a duplicate requiring credentials without recording the reason.

## 7. Assess image quality at the target

Scene-wide cloud percentage is a screening signal, not a local quality verdict. A scene with low overall cloud cover may have the area of interest obscured; a scene with higher overall cloud cover may have a clear target region.

Inspect the target footprint and relevant neighbourhood for:

- cloud and cirrus;
- cloud shadow;
- haze and aerosol effects;
- smoke, dust and thin cloud;
- snow or ice where relevant;
- saturation, defective pixels and nodata;
- water glint or specular reflection;
- terrain shadow and illumination variation;
- geolocation and band-to-band registration;
- edge-of-swath or incomplete coverage effects.

Use product quality bands and scene-classification layers according to their documented class definitions and resolution. Do not assume the quality mask is perfect or that every class has the same meaning across sensors and processing baselines.

For Sentinel-2 Level-2A, the Scene Classification Layer (SCL) is typically delivered at 20 m and 60 m product resolutions. If it is used to mask 10 m spectral bands, document the resampling or grid-mapping rule. Do not silently treat a 20 m SCL pixel as four independent 10 m classifications.

## 8. Asset access and retrieval

Separate three states in the acquisition log:

1. **Discovered:** catalogue metadata returned and candidate identified.
2. **Accessible:** the required asset can be retrieved under the available public or authenticated access conditions.
3. **Read and verified:** the retrieved data decode, have expected dimensions/bands/metadata, and pass basic integrity checks.

A successful HTTP response does not by itself prove a raster is complete or scientifically valid.

Prefer windowed reads and cloud-optimised assets where suitable. Avoid downloading full scenes when a small, documented region is sufficient. For authenticated object storage, use provider-issued credentials in a secure execution environment; never commit secrets or paste them into public issue logs.

Record the exact asset URLs or stable identifiers, redacting temporary signed query parameters. Compute checksums for downloaded assets or generated extracts when reproducibility requires byte-level provenance.

## 9. Preserve native measurement support

Bands from one sensor may have different native spatial resolutions. Before combining them:

- inspect each band's CRS, affine transform, pixel size, dimensions and nodata;
- define the analysis grid and justify its resolution;
- choose and document the resampling method for each data type;
- distinguish continuous reflectance from categorical QA classes;
- retain native-grid summaries where resampling could alter interpretation;
- ensure neighbourhood windows represent comparable ground footprints.

Nearest-neighbour resampling is often appropriate for categorical classes; continuous data may require a suitable interpolation method. Neither is universally correct for every application. Resampling can alter values and spatial dependence, so preserve original data and record the operation.

## 10. Acquisition record template

For each selected observation, record:

| Field | Entry |
|---|---|
| Study / application | |
| Observation question / measurand | |
| Area of interest and CRS | |
| Sensor / platform | |
| Instrument / band configuration | |
| Product collection / level / version | |
| Product or item identifier | |
| Acquisition timestamp | |
| Processing baseline / generation time | |
| Footprint coverage | |
| Cloud metadata and its scope | |
| Target-area quality inspection | |
| Bands / QA assets used | |
| Native pixel size per band | |
| CRS / grid / scale / offset / units | |
| Asset access status | |
| Retrieval method and asset identifiers | |
| Checksums / integrity results | |
| Licence and attribution | |
| Known limitations / rejected candidates | |
| Selection rationale | |

Keep rejected candidates or a concise rejection log when the selection could influence a scientific or operational conclusion.

## 11. Quality gates before analysis

An acquisition is ready for downstream analysis only when the relevant gates are satisfied:

- the observation question and required measurand are defined;
- the sensor and product level are suitable for that question;
- the acquisition date and spatial coverage are appropriate;
- required bands and quality layers are present and readable;
- product-specific scaling, offsets, units and nodata are understood;
- native spatial resolutions and grid alignment are documented;
- target-area quality has been assessed, not inferred only from scene metadata;
- provenance, licence and processing baseline are retained;
- limitations and rejected alternatives are recorded.

Passing these gates establishes an auditable input dataset, not a validated analysis result.

## 12. Connection to current repository work

- [Remote-sensing cross-pillar pathway](../learning-paths/remote-sensing-cross-pillar-pathway.md) — maps the optical and SAR branches and their current maturity.
- [Fiji multispectral pilot specification](../implementations/python/area-adjusted-accuracy/fiji-multispectral-pilot-spec.md) — a bounded live-data workflow that applies STAC discovery, public asset checks, native-resolution handling and blind-review boundaries.
- [Electromagnetic observations and radiometric quantities](../foundations/remote-sensing-physics/electromagnetic-observations-and-radiometric-quantities.md) — explains the physical quantities and product semantics underlying optical imagery.
- [Remote sensing index foundations](../learning-paths/remote-sensing-indices.md) — connects suitable reflectance inputs to spectral-index methods.

The Fiji pilot is an application-specific workflow, not evidence that all optical acquisition systems or products have been covered. Its multispectral execution and quality-control gates remain in progress as stated in its specification.

## 13. References

- Copernicus, [Sentinel-2 Products Specification Document, Issue 15.1](https://sentinels.copernicus.eu/documents/d/sentinel/sentinel-2-products-specification-document-15_1) — product structure and Level-2A contents.
- Copernicus Data Space Ecosystem, [Sentinel-2 data collection](https://dataspace.copernicus.eu/data-collections/copernicus-sentinel-missions/sentinel-2) — mission bands, spatial resolutions and product access.
- Copernicus, [Sentinel-2 Collection 1 Level-1C](https://sentinels.copernicus.eu/sentinel-data-access/sentinel-products/sentinel-2-data-products/collection-1-level-1c) — TOA product characteristics and processing-baseline context.
- Copernicus, [Sentinel-2 Collection 1 Level-2A](https://sentinels.copernicus.eu/sentinel-data-access/sentinel-products/sentinel-2-data-products/collection-1-level-2a) — BOA reflectance, scene classification and quality/ancillary layers.
- USGS, [Landsat Surface Reflectance](https://www.usgs.gov/landsat-missions/landsat-surface-reflectance) — a separate mission example of surface-reflectance products and collection-specific processing.

Always consult the current mission and collection documentation for the exact product acquired. Product definitions and processing baselines can change.

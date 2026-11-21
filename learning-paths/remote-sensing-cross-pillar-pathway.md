# Remote sensing: from sensor measurements to spatial evidence

**Status:** Partial cross-pillar pathway; navigation and evidence audit established, integrated remote-sensing recipe not yet available  
**Purpose:** Connect optical and radar remote sensing to the four Spatial Methods pillars without pretending that their sensors, measurements or processing chains are interchangeable.

Remote sensing is not one algorithm family. It is a chain that begins with a physical interaction and a sensor/platform, produces observations with specific measurement properties, and only then supports computational analysis and an application claim.

This pathway is intentionally split into two branches:

- **Optical multispectral remote sensing:** reflected solar radiation, spectral response, radiometric calibration, atmospheric effects, quality masks and spectral analysis.
- **Synthetic aperture radar (SAR):** active microwave transmission, coherent or detected products, polarisation, viewing geometry, scattering, calibration and terrain effects.

They share some downstream raster, statistical and validation methods, but do not share one universal sensor model or preprocessing recipe.

## 1. Start with the question

Choose the route that matches the observation and intended claim.

| Question | Appropriate starting route | Do not assume |
|---|---|---|
| What does a vegetation-sensitive spectral index show? | Optical multispectral / [remote-sensing indices path](remote-sensing-indices.md) | NDVI is a direct measurement of biomass, yield or plant health |
| How do optical bands vary across a landscape? | Sentinel-2 surface-reflectance investigation | Band numbers and spatial resolutions are identical across sensors |
| Why is a radar surface bright or dark? | [Radar exploration](../explorations/radar/README.md) | Brightness uniquely identifies a land-cover class |
| What does a Sentinel-1 backscatter product represent? | [Sentinel-1 backscatter investigation](../explorations/radar/sentinel-1-backscatter-investigation.md) | GRD, SLC and RTC products are interchangeable |
| Can imagery support a land-cover or change claim? | Define a study design, reference source and validation method first | A visually plausible image or index map proves classification accuracy |

## 2. Optical multispectral route

### Theoretical Foundations

An initial shared module, [Electromagnetic observations and radiometric quantities](../foundations/remote-sensing-physics/electromagnetic-observations-and-radiometric-quantities.md), is now published. It establishes core terminology and product interpretation, but technical review and learner testing remain pending. A defensible optical route ultimately needs deeper treatment of:

- electromagnetic spectrum, wavelength and spectral response functions;
- solar irradiance, atmospheric transmission and surface reflectance;
- radiance, reflectance, digital numbers, calibration and product scaling;
- atmospheric and topographic effects, illumination and viewing geometry;
- mixed pixels, spatial resolution, point-spread effects and resampling;
- uncertainty and the distinction between measured, corrected and derived quantities.

Until those foundations are developed and reviewed, use the existing algorithm notes for their bounded mathematical and computational scope; do not treat them as a complete sensor-physics course.

### Spatial Data Collection

An initial [optical satellite imagery acquisition method](../collection/optical-satellite-imagery-acquisition.md) now documents observation design, sensor/product selection, STAC/catalogue discovery, quality screening, asset access, native-resolution handling and provenance. It uses Sentinel-2 as a bounded reference, not a universal sensor template. Technical review and application testing remain pending. The Fiji Sentinel-2 pilot supplies a separate application-specific evidence workflow.

Relevant records:
- [Spatial Data Collection subject map](../collection/README.md)
- [Fiji multispectral pilot specification](../implementations/python/area-adjusted-accuracy/fiji-multispectral-pilot-spec.md)
- [Sentinel-2 blind-review workflow](../implementations/python/area-adjusted-accuracy/sentinel2-review-workflow.md)

Important collection decisions include product level, sensor/platform, acquisition date, cloud and shadow screening, spectral band mapping, native resolution, CRS/grid alignment, asset availability, licensing and provenance. A catalogue item being discoverable does not prove its assets are accessible.

### Spatial Algorithms

The repository already has substantial but uneven optical methods and implementations. Start with:
- [NDVI method](../algorithms/remote-sensing/ndvi.md)
- [Spectral-index family](../algorithms/remote-sensing/spectral-index-family.md)
- [Spectral-index implementation](../implementations/python/spectral-indices/README.md)
- [Cloud and quality-mask methods](../algorithms/remote-sensing/qa-cloud-masks.md)
- [Temporal compositing](../algorithms/remote-sensing/temporal-compositing.md)
- [Change-vector analysis](../algorithms/remote-sensing/change-vector-analysis.md)
- [Remote-sensing source catalogue section](../catalog/sections/05-remote-sensing.md)

The algorithm catalogue is broad, but its own audit marks many topics partial. A tested numerical primitive does not establish that the correct sensor bands, reflectance scale, atmospheric correction, masks, spatial grid or reference design have been selected.

### Spatial Recipes and practical evidence

There is not yet a canonical end-to-end optical remote-sensing recipe that takes a defined question through acquisition, preprocessing, analysis, independent validation and delivery.

The [Fiji multispectral pilot](../implementations/python/area-adjusted-accuracy/fiji-multispectral-pilot-spec.md) is the strongest current live-data example in this branch, but its status must be read narrowly:

- a bounded 25-point public Earth Search retrieval run succeeded for RGB chip access, with at least one successful chip for each point;
- a five-point multispectral technical pilot and quality-control refinement are in progress;
- the workflow has not yet completed an integrated live multi-date SCL-screened index and neighbourhood-statistics run;
- the points are purposive disagreement cases, not a probability sample;
- imagery supplies contextual evidence, not field-verified ground truth, and cannot revise the design-based 834-point accuracy estimate.

Use the pilot to study source discovery, asset accessibility, native-grid handling, temporal evidence and blind-review governance—not as proof of a finished operational classification workflow.

## 3. SAR route: Sentinel-1 as the first bounded case

### Theoretical Foundations

A SAR foundation must cover electromagnetic propagation and scattering, pulse/range concepts, Doppler and platform motion, coherent signal processing, phase, polarisation, speckle, radiometry, incidence geometry and measurement uncertainty. The shared electromagnetic/radiometric introduction is now available, but radar-specific foundations for scattering, radar measurement and signal processing remain incomplete. The Radar exploration is an orientation and investigation resource, not a substitute for those canonical foundations.

### Spatial Data Collection

The [Radar exploration](../explorations/radar/README.md) distinguishes Earth-observation SAR from weather radar, radar systems engineering and other branches. Its [territory map](../explorations/radar/territory-map.md) explains the shared and branch-specific concepts.

The [Nairobi Sentinel-1 scene record](../explorations/radar/nairobi-sentinel-1-scene-record.md) is a study specification only. Scene selection and processing are pending. It correctly requires the product identifier, acquisition time, mode, pass direction, relative orbit, polarisation, coverage, processing source, coefficient, value scale, DEM and filtering history to be recorded before interpretation.

### Spatial Algorithms

Relevant existing records include:
- [Lee speckle filtering](../algorithms/remote-sensing/lee-speckle-filter.md)
- [SAR CFAR detection](../algorithms/remote-sensing/sar-cfar.md)
- [local InSAR coherence](../algorithms/remote-sensing/insar-local-coherence.md)

These are scoped methods, not a complete Sentinel-1 GRD or InSAR processing chain. In particular, detected GRD data do not retain the complex phase required for conventional interferometric processing. Product type must match the intended analysis.

### Spatial Recipes and practical evidence

The [Sentinel-1 backscatter investigation](../explorations/radar/sentinel-1-backscatter-investigation.md) is a guided interpretation protocol. It explains how to inspect a GRD or documented RTC product, record coefficient and scale, consider competing physical explanations, and seek independent contextual evidence.

The [Radar source register](../explorations/radar/source-notes.md) states that no scene-specific Sentinel-1 data have yet been downloaded and processed in this documentation pass. The Nairobi scene record likewise remains pending. Therefore:

- no Nairobi backscatter result is claimed;
- no land-cover classification or flood extent is established;
- no scene-specific accuracy statistic is available;
- the investigation is not yet a validated operational SAR recipe.

## 4. Validation is part of the method

Before making an application claim, define what would count as independent evidence and what uncertainty the evidence can resolve.

Examples:
- An index map can show a spectral contrast; field observations or a suitable independent reference are needed for a vegetation or water claim.
- A radar backscatter pattern can support a physical interpretation; acquisition geometry, surface conditions and dated reference evidence must be considered.
- A classification needs a sampling and reference design, class definitions, uncertainty treatment and accuracy assessment appropriate to the claim.
- A change map needs temporal consistency, stable processing, event context and independent evidence of the change.

Keep separate:
1. software tests on synthetic arrays;
2. successful data discovery or asset reads;
3. successful processing of public observations;
4. visual interpretation and expert review;
5. independent reference validation;
6. operational fitness-for-purpose acceptance.

Evidence at one level does not automatically establish the next.

## 5. Current cross-pillar assessment

| Pillar | Optical multispectral | SAR / Sentinel-1 |
|---|---|---|
| Theoretical Foundations | Initial electromagnetic/radiometric module published; detailed optical radiative transfer, technical review and learner testing remain open | Shared electromagnetic introduction published; radar scattering, measurement and signal-processing foundations remain incomplete |
| Spatial Data Collection | Initial optical satellite acquisition method published; technical review and application testing pending; Fiji pilot documents a bounded Level-2A/STAC workflow | Radar exploration and Nairobi scene specification exist; no completed scene acquisition record |
| Spatial Algorithms | Broad catalogue and multiple tested implementations; sensor-aware preprocessing and validation remain uneven | Lee filter, CFAR and local coherence notes exist; no complete sensor-to-product processing chain |
| Spatial Recipes | No mature integrated optical recipe yet; Fiji pilot is an evidence workflow, not one | Guided backscatter investigation exists; no executed Nairobi recipe or validated application |

This table is a gap map, not a maturity score. It deliberately leaves incomplete cells visible.

## 6. Recommended development sequence

1. **Extend and review the foundation:** technically review the initial electromagnetic/radiometric module, then develop separate optical radiative-transfer and radar scattering/signal-formation modules.
2. **Extend collection records:** technically review and test the optical acquisition method, then document SAR acquisition separately, including product families, geometry, metadata, access, calibration and quality controls.
3. **Audit algorithms against inputs:** connect each algorithm to required sensor/product types, band mapping, units, masks, grid, assumptions, failure modes and validation needs.
4. **Complete one bounded optical execution:** finish the Fiji multispectral quality-control gates, preserve its blind-review boundaries, and report exactly which live processing stages have passed.
5. **Execute the Nairobi SAR study:** select and archive a suitable Sentinel-1 scene, process it reproducibly, record observations and independent contextual evidence, and do not promote it to a recipe until the hand-offs and validation are reviewed.
6. **Create end-to-end recipes only after the chain is understood:** define acceptance criteria before execution and keep application-specific choices out of general-purpose methods.

## 7. Maintenance rule

When the pathway changes, update the evidence status as well as the links. Do not promote a planned foundation, a scene specification, a synthetic test or a successful data download into a claim of a complete method. The purpose of this pathway is to show how the pillars depend on one another—and where the work still is.

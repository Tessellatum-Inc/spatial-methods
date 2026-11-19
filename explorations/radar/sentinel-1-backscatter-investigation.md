# Laboratory: reading a Sentinel-1 SAR scene

> A first practical investigation for the Radar exploration. The purpose is to interpret a real observation carefully, not to produce a validated land-cover or flood map.

## Investigation record

- **Question:** What can the backscatter patterns in one Sentinel-1 scene tell us about the observed landscape—and what can they not tell us?
- **Exploration:** [Radar: a curiosity-led exploration](../README.md)
- **Type:** Guided observation and optional desktop processing
- **Expected effort:** Approximately 60–120 minutes, depending on data access and whether SNAP is used.
- **Status:** Practical guide; no scene-specific result is claimed in this document.

## 1. What you will produce

A short scene interpretation record containing:
- the place and acquisition details;
- the product type and polarisation channels inspected;
- three observed patterns;
- at least two plausible explanations for each pattern where appropriate;
- one uncertainty or limitation;
- a next question that could be tested.

The goal is disciplined interpretation. A polished map is not required.

## 2. The question behind the exercise

A SAR image is not a photograph. A Sentinel-1 measurement depends on the transmitted signal, acquisition geometry, surface properties, processing and product representation.

Ask:

1. What product am I looking at?
2. What quantity is displayed?
3. What acquisition geometry and polarisation apply?
4. Which physical explanations are plausible?
5. What other evidence would help distinguish them?

## 3. Find a scene

Open [ASF Vertex](https://search.asf.alaska.edu/) and choose a small area you recognise.

1. Search a location with a mixture of land-cover types if possible.
2. Filter to Sentinel-1.
3. Select one scene and record its acquisition date, relative orbit or pass information if exposed, mode, product type and available polarisations.
4. Prefer a scene with the product metadata needed for the question. Do not compare two scenes as if they were directly equivalent until acquisition and processing differences have been checked.
5. Note the provider's current access and download requirements.

You can use the [Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu/) as an alternative data-discovery route.

**Record:** location or AOI, scene identifier, acquisition date/time, product type, mode, polarisation, orbit/pass and source URL.

## 4. Inspect before interpreting

Use the browse/preview capability available in the data portal, or open the downloaded product in a suitable tool.

If using [ESA SNAP](https://step.esa.int/main/download/snap-download/), first confirm the current version and product support. Work from a copy of the downloaded data and retain the original.

Inspect:
- image dimensions and bands;
- polarisation channels available;
- displayed units and scaling;
- no-data areas and scene edges;
- obvious geometric distortions, shadows or artefacts;
- whether the image has been calibrated or terrain corrected.

Do not infer physical backscatter values from an arbitrary display stretch or screenshot. Record the actual band and units.

## 5. Optional processing route

The exact workflow depends on the Sentinel-1 product and the question. Use current ESA/ASF documentation for the selected product. A common high-level route for a Sentinel-1 GRD backscatter interpretation is:

1. Read the product metadata and confirm the product type and polarisations.
2. Apply the appropriate radiometric calibration to obtain a defined backscatter quantity (for example, sigma nought), following the product-specific guidance.
3. Apply terrain correction when a map-geocoded result is required, using an appropriate DEM and recording its source.
4. Choose a display scale suitable for the units and purpose.
5. Export the result with metadata and processing notes.

Do not treat this as a universal recipe. Orbit-file handling, border-noise treatment, thermal-noise handling, speckle filtering, terrain flattening, resampling and other steps depend on the product, software version and scientific question. Avoid adding filters simply to make an image look smoother.

## 6. Observe and record

Choose three areas or patterns in the scene. For each, complete:

| Observation | Possible explanation | Alternative explanation | What evidence could distinguish them? |
|---|---|---|---|
| Pattern 1 | | | |
| Pattern 2 | | | |
| Pattern 3 | | | |

Prompts:
- Does smooth open water appear relatively dark in this acquisition?
- Are there bright linear or clustered patterns that could relate to built structures or geometry?
- Do vegetated areas show different responses across available polarisations?
- Could terrain slope, radar shadow, layover, moisture or incidence angle explain the pattern?
- Is the pattern consistent across the scene, or does geometry change the interpretation?

These are prompts, not a lookup table. Do not assign land-cover classes from brightness alone.

## 7. Validate the interpretation

Use at least one independent source appropriate to the location and date, such as:
- optical imagery acquired near the same date;
- a reliable land-cover or water reference dataset;
- terrain/elevation data;
- field observations or a documented event report.

Record the reference source, date, resolution, licence and limitations. A reference layer may itself be inaccurate or temporally mismatched. Explain what it can and cannot validate.

## 8. What this exercise does not establish

This exercise does not:
- produce a validated land-cover classification;
- prove that a dark area is water;
- establish flood extent without event context and independent validation;
- measure ground deformation;
- compare backscatter quantitatively across acquisitions without consistent calibration and acquisition controls;
- establish a universal relationship between a surface type and a backscatter value.

## 9. Investigation record

- **Scene and location:**
- **Acquisition date:**
- **Product / mode:**
- **Polarisation(s):**
- **Displayed quantity and units:**
- **Processing steps and software version:**
- **Three observations:**
- **Competing explanations:**
- **Independent reference used:**
- **What remains uncertain:**
- **Next question:**

## 10. Extensions

Choose one extension only when it answers a question you now have:

- Compare VV and VH within the same acquisition and explain what the difference may indicate.
- Compare two acquisitions after checking orbit, geometry, season, moisture and processing consistency.
- Investigate a documented flood with pre/post-event data and independent reference information.
- Explore speckle and compare the original with a carefully justified filter.
- Move toward InSAR by learning why complex phase and coherence are needed.

## 11. Sources and technical checks

- [ASF Vertex](https://search.asf.alaska.edu/) — scene discovery and product metadata.
- [ASF learning resources](https://asf.alaska.edu/learn/) — SAR concepts and data guidance.
- [ESA SNAP](https://step.esa.int/main/download/snap-download/) — processing environment and current documentation.
- [Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu/) — Sentinel data discovery and access.

Before publishing a result based on a specific scene, record the exact product identifier, processing parameters, software version, DEM and reference data. Recheck current product-specific guidance. This guide intentionally does not prescribe universal parameter values.

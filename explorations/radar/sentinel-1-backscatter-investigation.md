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

## 3. Choose your data route

There are two sensible ways to begin. Choose based on whether your immediate goal is interpretation or learning the processing chain.

### Route A — inspect a prepared RTC product (recommended first)

Use [ASF Vertex](https://search.asf.alaska.edu/) to search Sentinel-1 and look for an available **Radiometrically Terrain Corrected (RTC)** product for your area. ASF's [RTC Product Guide](https://hyp3-docs.asf.alaska.edu/guides/rtc_product_guide/) explains the product, available radiometry, pixel spacing, DEM and optional processing choices.

This route reduces the setup burden. It does not remove the need to understand the processing history.

Record:
- scene identifier and acquisition date/time;
- source Sentinel-1 product and acquisition mode;
- polarisation;
- RTC product identifier and generation options;
- radiometric convention (gamma-nought or sigma-nought);
- scale (power, amplitude or decibel);
- pixel spacing and DEM;
- whether a speckle filter was applied.

**Important:** RTC products are processed derivatives, not raw sensor observations. Read the product metadata and guide before interpreting or comparing values.

### Route B — process a Sentinel-1 GRD product yourself

Search for a Sentinel-1 **GRD** product in ASF Vertex or the [Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu/). For a first backscatter interpretation, GRD is generally the more approachable product family: it is detected and multi-looked. It does not preserve the complex phase required for conventional interferometric processing. The official [Sentinel-1 Product Definition](https://sentiwiki.copernicus.eu/__attachments/1673968/S1-RS-MDA-52-7440-Sentinel-1-Product-Definition-2025-2.8.pdf) describes the distinction between SLC and GRD.

Record the product identifier, acquisition date/time, mode, resolution class, polarisation and orbit/pass metadata. Do not treat a quick-look image or uncalibrated digital number as a quantitative backscatter measurement.

## 4. Inspect before interpreting

Open the RTC GeoTIFF or GRD product in a suitable GIS or image-processing tool. If using [ESA SNAP](https://step.esa.int/main/download/snap-download/), confirm the current version and product support first. The [Sentinel-1 Toolbox feature list](https://step.esa.int/main/toolboxes/sentinel-1-toolbox/s1tbx-features/) documents capabilities including calibration, speckle filtering, orbit handling and Range-Doppler terrain correction.

Inspect:
- product type and processing level;
- image dimensions, bands and polarisation channels;
- whether values are calibrated backscatter, and the coefficient used;
- whether values are linear power or decibels;
- map projection, pixel spacing and no-data areas;
- DEM and terrain-correction information, if applicable;
- visible geometric distortions, shadows, layover or artefacts.

Do not infer physical backscatter values from an arbitrary display stretch or screenshot. Record the actual band, units, scaling and processing history.

## 5. Optional processing route

For a GRD workflow in SNAP, use the current ESA/STEP documentation and product metadata to choose appropriate operators and parameters. A high-level workflow may include:

1. Inspect metadata and confirm the GRD product, mode and polarisation.
2. Apply an appropriate orbit file when required by the processing objective and available orbit quality.
3. Apply product-appropriate noise handling and radiometric calibration.
4. Decide whether radiometric terrain correction / terrain flattening is required for the intended analysis and terrain.
5. Apply geometric terrain correction when a map-geocoded output is needed.
6. Export the output with its metadata, processing graph and parameter record.

This is deliberately not a universal button-by-button recipe. The correct order and operator settings depend on product type, acquisition mode, SNAP version and scientific objective. See the [Copernicus Sentinel-1 GRD processing description](https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Data/S1GRD.html) and the [ASF RTC Product Guide](https://hyp3-docs.asf.alaska.edu/guides/rtc_product_guide/) for documented processing choices.

**Do not automatically despeckle.** ASF notes that speckle filtering can reduce apparent noise but also reduce spatial resolution; whether it helps depends on the application. Compare filtered and unfiltered data when filtering is justified, and record the choice.

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

- [ASF Vertex](https://search.asf.alaska.edu/) — scene discovery and access to available derived products.
- [ASF RTC Product Guide](https://hyp3-docs.asf.alaska.edu/guides/rtc_product_guide/) — product radiometry, DEM, scale, pixel spacing and speckle-filter choices.
- [ASF learning resources](https://asf.alaska.edu/learn/) — SAR concepts and data guidance.
- [ESA Sentinel-1 Toolbox features](https://step.esa.int/main/toolboxes/sentinel-1-toolbox/s1tbx-features/) — documented SNAP processing capabilities.
- [Copernicus Sentinel-1 GRD processing documentation](https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Data/S1GRD.html) — processing stages and backscatter coefficient options for that service.
- [Sentinel-1 Product Definition (2025, revision 2/8)](https://sentiwiki.copernicus.eu/__attachments/1673968/S1-RS-MDA-52-7440-Sentinel-1-Product-Definition-2025-2.8.pdf) — authoritative product definitions, including SLC and GRD.
- [Copernicus Data Space Ecosystem](https://dataspace.copernicus.eu/) — Sentinel data discovery and access.

Before publishing a result based on a specific scene, record the exact product identifier, processing parameters, software version, DEM and reference data. Recheck current product-specific guidance. This guide intentionally does not prescribe universal parameter values.

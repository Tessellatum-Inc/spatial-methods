# Laboratory: reading a Sentinel-1 SAR scene

> A first practical investigation for the Radar exploration. The purpose is to interpret a real observation carefully, not to produce a validated land-cover or flood map.

## Investigation record

- **Question:** What can the backscatter patterns in one Sentinel-1 scene tell us about the observed landscape—and what can they not tell us?
- **Exploration:** [Radar: a curiosity-led exploration](../../README.md)
- **Type:** Guided observation and optional desktop processing
- **Expected effort:** Approximately 60–120 minutes, depending on data access and whether SNAP is used.
- **Status:** Practical guide; no scene-specific result is claimed in this document.

## Study area: Nairobi, Kenya

The first worked case uses the Nairobi urban area as a practical, recognisable study setting.

**Search window (WGS 84):** west 36.65°E, south 1.45°S, east 37.05°E, north 1.15°S.

This is a rectangular scene-discovery window around Nairobi's urban core, **not** an official Nairobi County or metropolitan boundary and not the final analysis mask. Once a scene is selected, use a documented Nairobi boundary or a clearly described sub-area for any area-based statistics. Keep the search window and analysis boundary conceptually separate.

**Initial question:** How does C-band Sentinel-1 backscatter vary across Nairobi's dense built-up areas, vegetated/open spaces and water-related surfaces, and which patterns can be explained by surface scattering versus acquisition geometry?

This is an interpretation exercise, not a claim that SAR alone can reliably classify Nairobi's land cover.

### Scene-selection rule

Use the Copernicus Data Space catalogue or ASF Vertex to identify candidate scenes. Start with the latest available **Sentinel-1 IW GRD** acquisition intersecting the search window, preferably with **VV and VH**. Select one complete scene that covers the intended sub-area. Record the acquisition time, relative orbit, pass direction, product identifier, polarisation, resolution class and footprint. If the newest candidate has incomplete coverage, missing dual polarisation or an unsuitable footprint, move to the next suitable acquisition and record why.

For a first pass, use the original GRD product in a reproducible processing workflow or a documented RTC derivative. Do not mix values from different providers or processing conventions as though they were directly equivalent. The Copernicus Data Space catalogue documents worldwide Sentinel-1 GRD availability; its catalogue APIs support spatial and temporal product searches.

### Comparison context

Where practical, identify a Sentinel-2 optical observation close to the SAR acquisition date and use it only as contextual evidence for visible surface conditions. Record the time difference, cloud cover and any seasonal or land-cover change that limits comparison. Optical imagery is not ground truth. Add a dated reference layer or authoritative local dataset if the interpretation makes a specific land-cover or water claim.

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


---

## 12. Nairobi paired ellipsoid-versus-RTC experiment (2026-11-23)

A four-acquisition Sentinel-1C IW GRD experiment was run over the Nairobi County mask using the same requested output grid for the ellipsoid and terrain-corrected processing branches. The acquisitions were 9 October, 21 October, 2 November and 14 November 2026; all were descending relative orbit 79 with VV/VH. The paired diagnostic compared linear-power outputs on common valid pixels, then expressed differences in dB.

### Question

Does the observed difference follow the inverse scattering-area factor?

`RTC - ellipsoid (dB) = -10 log10(scatteringArea)`

### Result

All four acquisitions completed; each polarization comparison contains approximately 3.145 million common valid pixels. Across the eight VV/VH comparisons:

- Pearson correlation between observed and predicted differences: approximately **0.97618–0.97620**.
- OLS slope: approximately **0.98299–0.98305**, not exactly 1.
- OLS intercept: approximately **+0.276 dB**.
- Median observed-minus-predicted offset: approximately **+0.282 dB**.
- 95th percentile absolute residual before centering: approximately **0.448 dB**.
- 95th percentile absolute residual after subtracting the median offset: approximately **0.176 dB**.

This is a strong and repeatable empirical relationship for this processing setup and study window. It is not proof that the two products are radiometrically equivalent, nor that scattering area alone explains the RTC transformation.

### Does the remaining residual depend on terrain geometry?

The residual was centered by subtracting its scene/polarization median, then summarized by fixed scattering-area and local-incidence-angle bins. The pattern was nearly identical across all dates and both polarizations.

| Stratum | Median centered residual by scattering area (dB) | Median centered residual by local incidence angle (dB) |
|---|---:|---:|
| First bin: area <0.9 / angle <35° | -0.108 | -0.120 |
| Second: 0.9–1.0 / 35–40° | -0.074 | -0.057 |
| Third: 1.0–1.1 / 40–45° | -0.005 | +0.025 |
| Fourth: 1.1–1.2 / 45–50° | +0.058 | -0.079 |
| Fifth: area ≥1.2 / angle ≥50° | -0.063 | -0.114 |

The corresponding 95th percentile absolute centered residuals remain tightly grouped: approximately **0.175–0.180 dB** in every bin. The bin medians therefore reveal a small but repeatable structure in the residual location, while the residual spread is comparatively stable. The two stratifications are separate one-variable summaries; they do not establish independent effects because scattering area and incidence geometry may be related.

### Other QA evidence

- All four acquisitions had complete coverage of the requested 2048 × 1536 grid and all paired comparisons completed.
- Local-incidence-angle surfaces were extremely similar between dates: the 95th percentile absolute difference from the first acquisition ranged from about 0.0017° to 0.0045°. This is geometry-layer consistency, not a geolocation validation.
- Global image-content phase-correlation shifts relative to the first acquisition ranged from about 0.058 to 0.118 pixels. This is a screening diagnostic only; it does not prove sub-pixel co-registration.
- The eroded ESA WorldCover 2021 built-up candidate contained 157,983 pixels (about 11.1% of county-valid pixels), but the 2021 class does not prove those surfaces remained invariant in 2026.
- The JRC Global Surface Water v1.5 95% occurrence candidate had zero pixels after two erosion iterations. It therefore supplied no usable persistent-water core for this study window.

### Interpretation and next experiment

The inverse-area factor is a strong first-order explanation of the observed RTC-minus-ellipsoid difference, but the slope departure, non-zero offset and structured residual medians argue against treating the simple equation as an exact correction. The comparator now includes a pre-specified, low-complexity residual model using scattering area and local incidence angle jointly. It compares area-only OLS against area-plus-angle-plus-interaction OLS on checkerboard spatial blocks with a 32-pixel edge buffer (512-pixel blocks by default), and reports test-set RMSE, MAE and P95 absolute error. This is a within-scene spatial screening split, not independent validation across sites or dates; the incremental held-out improvement must be checked across all four acquisitions and both polarizations before drawing a conclusion.

Do not use the fitted relation to normalize the time series, declare radiometric equivalence, or enable change detection. The current processing and QA reports correctly remain `analysis_ready: false` because independent geometric and radiometric validation is still absent.


### Leave-one-acquisition-out transfer test

A second test trains on three acquisitions and evaluates the fourth, rotating through all four dates independently for VV and VH. To keep memory bounded, the model uses a systematic sample at every fourth row and column (approximately one-sixteenth of eligible pixels). Each fold contains about 589,800 training samples and 196,600 held-out samples.

Across all eight held-out date/polarization folds:

- Area-only mean test RMSE: **0.10457 dB**.
- Area + angle + interaction mean test RMSE: **0.10142 dB** (about **3.01% lower**).
- Mean test MAE: **0.09005 → 0.08654 dB** (about **3.90% lower**).
- Mean P95 absolute error: **0.17675 → 0.17463 dB** (about **1.20% lower**).
- RMSE reduction in individual folds: approximately **2.98–3.05%**.

The small improvement transfers consistently to each held-out date in this four-scene series. This is stronger evidence than a within-scene random pixel split, but it is not independent-site validation: all dates share the same Nairobi study area, descending relative orbit 79, provider, requested grid and processing configuration. The systematic sampling design may also interact with spatial texture. Treat the angle terms as a modest empirical refinement, not a validated physical correction.

The area-only relation remains the simpler baseline. Neither model is applied to the imagery, and the workflow continues to report `analysis_ready: false`. A next-stage validation would need independent stable targets and/or acquisitions from another relative orbit or study area, plus stronger geodetic and radiometric validation.

The machine-readable QA evidence is retained in the GitHub Actions artifact `sentinelhub-sentinel1-nairobi-qa-reports` from run [45160482637](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45160482637). The full temporal stack is a separate artifact from the same run.


### Latest full-data rerun and reference-target screening (2026-11-23, run 45160482637)

The complete processing workflow was rerun on commit `e43566496e1068955a9498887a0187e67fd02812`. The workflow completed successfully. The compact QA artifact contains nine JSON reports; the full temporal-stack artifact was also uploaded.

**Processing completion**
- Four of four Sentinel-1C IW GRD acquisitions were processed through the separate `GAMMA0_TERRAIN` branch; zero scene failures.
- Each RTC output matched the requested 2048 × 1536 ellipsoid-reference grid and contained 3,145,728 valid pixels.
- The RTC shadow-mask fraction was zero for all four outputs. This is the provider's reported mask result, not proof that all terrain-related distortions are absent.
- All four paired ellipsoid/RTC comparisons completed, with zero failed comparisons and full common-valid grid coverage.

**Recomputed temporal transfer screen**

The latest QA report reproduces the leave-one-acquisition-out result. Across the four held-out dates, mean metrics were:

| Polarization | Model | RMSE (dB) | MAE (dB) | P95 absolute error (dB) |
|---|---|---:|---:|---:|
| VV | Area only | 0.10457 | 0.09005 | 0.17675 |
| VV | Area + angle + interaction | 0.10142 | 0.08654 | 0.17463 |
| VH | Area only | 0.10457 | 0.09005 | 0.17675 |
| VH | Area + angle + interaction | 0.10142 | 0.08654 | 0.17463 |

The RMSE reduction was approximately 2.98–3.05% in each fold. This confirms a small, consistent within-study-area transfer improvement, not an independently validated correction. The sample design remains systematic (every fourth row and column), and all four acquisitions share the same Nairobi area, descending relative orbit 79, provider and processing setup.

**Geometry and registration diagnostics**

- The local-incidence-angle surfaces remain highly consistent: the P95 absolute difference from the first acquisition was approximately 0.00169°, 0.00447° and 0.00279° for the three later dates.
- Global phase-correlation shifts were 0.058, 0.118 and 0.105 pixels relative to the first acquisition.
- The tiled phase-correlation screen showed spatial variation in local image-content shifts. These are image-matching diagnostics, not independent tie-point or geodetic registration measurements. Neither the global nor tiled results establish sub-pixel geolocation accuracy.

**Reference-target screen: an important limitation**

The eroded WorldCover 2021 built-up candidate covers 157,983 pixels, but its temporal backscatter statistics are not invariant across these four 2026 acquisitions. Relative to 9 October, the median changed as follows:

| Acquisition | VV median change (dB) | VH median change (dB) |
|---|---:|---:|
| 21 October | -0.032 | -0.049 |
| 2 November | +0.941 | +0.430 |
| 14 November | +0.577 | +0.196 |

This does not prove the land cover itself changed; moisture, surface conditions, acquisition effects and residual processing differences can also contribute. It does show that the class mask cannot be treated as a stable radiometric calibration target without further investigation. The JRC Global Surface Water v1.5 screen produced only 26 candidate pixels at 95% occurrence and zero pixels after two erosion iterations; it provides no usable eroded water core in this study window.

**Decision**

The rerun strengthens confidence that the paired processing and diagnostic calculations are repeatable. It does not solve the independent-validation problem. The area-factor relationship remains a strong empirical description, and angle terms remain a modest refinement, but neither is approved as a correction. Keep `analysis_ready: false`; do not normalize the time series or use this relationship for change detection.

The next experiment should prioritize an independent validation design rather than adding more model complexity: identify an alternative relative orbit and/or a second study area, and seek contemporaneous, defensible stable targets or independent geometric/radiometric reference data. Any candidate target must first pass a temporal stability screen; a land-cover label alone is insufficient.

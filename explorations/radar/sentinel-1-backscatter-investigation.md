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


### Independent-orbit screening update (2026-11-23)

A separate Sentinel Hub catalogue search identified ascending R130 as a repeatable partial-coverage track: four acquisitions at 12-day intervals, each intersecting approximately 84.2–84.4% of the Nairobi rectangle. Ascending R057 had five repeat acquisitions but covered only about 74.6–74.8%. Neither ascending track fully covers the rectangle, so the new experiment preserved data masks and evaluated only actual common-valid pixels.

The R130 RTC/ellipsoid experiment processed all four acquisitions with zero failures. Its all-date common-valid fraction was 84.19% of the requested grid. The mean per-scene area-factor relation had R² around 0.978 for both VV and VH. Leave-one-acquisition-out angle terms reduced RMSE by about 1.6%.

This is meaningful cross-configuration evidence, but the fit coefficients are not invariant: R130's median residual offset was about -0.010 dB, compared with about +0.282 dB in the original descending R079 stack. R130 is ascending Sentinel-1D, while R079 is descending Sentinel-1C, so platform and orbit direction are confounded. Do not transfer the R079 intercept to R130 or pool the tracks as one time series. See [the independent-orbit experiment record](sentinel-1-independent-orbit-validation.md) and [workflow run 45163757264](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45163757264).

The broader conclusion remains: the scattering-area relationship is strong across both tested acquisition configurations, but the fitted offset/slope vary and independent radiometric/geodetic reference validation is still absent. Keep `analysis_ready: false`.


### Same-platform ascending-orbit comparison on an identical footprint (2026-11-23)

To separate platform effects from orbit effects, a paired Sentinel-1A experiment processed four ascending R057 acquisitions and four ascending R130 acquisitions from January–February 2025. Both tracks used the same Nairobi output grid, the same ellipsoid and RTC processing functions, and the same requested temporal window. The comparison was then restricted to the intersection of valid data masks across all eight acquisitions and both processing branches.

The shared footprint contains **1,848,662 pixels (58.77% of the requested grid)**. On this identical footprint, the mean per-scene results were:

| Track | Median local incidence angle | Area-factor OLS slope | R² (VV / VH) | Median residual offset (VV / VH) | Mean absolute residual (VV / VH) |
|---|---:|---:|---:|---:|---:|
| Ascending R130, Sentinel-1A | 45.95° | 0.992 | 0.986 / 0.986 | -0.053 / -0.053 dB | 0.064 / 0.064 dB |
| Ascending R057, Sentinel-1A | 32.56° | 0.982 | 0.976 / 0.976 | +2.053 / +2.053 dB | 2.054 / 2.054 dB |

The residual-offset difference is large and repeatable across all four acquisitions in each track and both polarizations. It persists after restricting the analysis to exactly the same pixels, so it is not explained by different valid map footprints. Within each track, the residual-angle correlation is weak (approximately -0.05 for R130 and -0.08 for R057), while the track-level median local incidence angles differ by about 13.4 degrees.

**Interpretation restraint:** relative orbit and local incidence angle are strongly confounded in this two-track comparison: the R057 and R130 angle distributions barely overlap (approximately 29.9–35.6° versus 43.3–49.0° for the central 80%). The offset difference therefore cannot be assigned to orbit geometry alone, nor can the angle effect be isolated from track identity with these two tracks. The strikingly consistent R057 offset also warrants checking the provider's scattering-area semantics and the exact RTC/ellipsoid pairing before any physical interpretation. Do not treat the +2.05 dB as an orbit correction.

The same-platform comparison is a useful warning against transferring an intercept between tracks. It does not validate a correction, and it does not authorize pooling the acquisitions. The later catalogue screen found no additional repeated Sentinel-1A ascending track with at least four scenes and 70% Nairobi overlap, so the immediate next step is to obtain the ellipsoid incidence angle independently from the source GRD geolocation grid and verify the provider's area-factor convention. A second study area remains a useful later validation path. Until then, keep `analysis_ready: false`; do not normalize or run change detection from these coefficients.

Reproducibility:
- Same-platform processing artifacts: [workflow run 45165312108](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45165312108).
- Common-mask analysis and machine-readable metrics: [workflow run 45168656320](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45168656320).
- Shared-mask analysis code: `compare_sentinel1_same_platform_orbit_pair.py`.

### Radiometric reference-area interpretation correction (2026-11-23)

A review of the provider documentation and the Sentinel Hub-derived Digital Earth Africa RTC method changes the interpretation of the area-only residual. Sentinel Hub describes `scatteringArea` as a normalized area used to convert β⁰ to terrain-corrected γ⁰ ([Sentinel-1 GRD band and processing documentation](https://docs.sentinel-hub.com/api/latest/data/sentinel-1-grd/)). Yuan et al. (2022), describing the Sentinel Hub RTC implementation, state that the normalized illuminated-area factor is used as `γ⁰_RTC = β⁰ / Âγ`; for an ellipsoid reference, the β⁰-to-γ⁰ area ratio is `tan(θE)` ([paper, Remote Sensing 14, 351](https://doi.org/10.3390/rs14020351), especially Section 2.3 and its discussion of the equivalent incidence angle).

Consequently, when comparing terrain-corrected γ⁰ with ellipsoid γ⁰, the area-only identity is incomplete. Under those reference-area definitions:

\[
\Delta_{dB}=10\log_{10}\left(\frac{\gamma^0_{RTC}}{\gamma^0_E}\right)
=-10\log_{10}(\widehat A_\gamma)-10\log_{10}(\tan\theta_E).
\]

The area-only residual is therefore expected to contain the ellipsoid reference-area term `-10 log10(tan(θE))`; it should not automatically be interpreted as a calibration offset or processing error. This explains why the residual offsets differed so strongly between R057 and R130 despite their nearly identical direct RTC-minus-ellipsoid medians.

The common-footprint results support this interpretation at the track-summary level:

| Track | Area-only median residual | Median local-angle proxy term | Median proxy-adjusted residual | Median direct RTC − ellipsoid |
|---|---:|---:|---:|---:|
| Sentinel-1A ascending R057 | +2.053 dB | +1.948 dB | +0.078 dB | +0.014 dB |
| Sentinel-1A ascending R130 | −0.053 dB | −0.144 dB | +0.073 dB | +0.021 dB |

The near-identical proxy-adjusted median residuals (~+0.075 dB) are encouraging. However, the available `localIncidenceAngle` band is the angle relative to the **local terrain normal**, not the ellipsoid incidence angle θE required by the equation. Substituting local angle pixel-by-pixel is not validated: it increases mean absolute residual on R130 (about 0.064 to 0.295 dB) and leaves substantial tails. The current result is a diagnostic consistency check, not an approved per-pixel correction.

Direct RTC-minus-ellipsoid differences also are not identically zero at every pixel: median differences are near +0.01–0.02 dB, but mean absolute differences are about 0.30–0.34 dB and P95 absolute differences about 1.03–1.16 dB. The spatial distribution of these differences still needs investigation.

**Revised scientific question:** obtain or derive the ellipsoid incidence angle θE for each pixel/acquisition, verify the provider's exact `scatteringArea` normalization convention against its processing implementation, and test the complete reference-area equation on flat, low-slope reference areas before extending it to terrain. Keep `analysis_ready: false`; do not normalize or use this as a change-detection correction.

Reproducibility: the direct-difference and local-angle-proxy metrics are in [shared-mask analysis run 45169287651](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45169287651); code is in `compare_sentinel1_same_platform_orbit_pair.py`.

### Independent ellipsoid-angle source and next validation step (2026-11-23)

A catalogue-only search for repeated Sentinel-1A ascending tracks over Nairobi (2025-01-01 through 2026-11-23; at least four scenes and at least 70% AOI overlap) found only the already processed R057 and R130 tracks. It found **zero additional intermediate-angle candidates**. The search is discovery evidence only; it does not establish that no other track exists outside the date, platform, direction or overlap filters. See [catalogue workflow run 45169939031](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45169939031).

The next validation should therefore obtain the **ellipsoid incidence angle** independently rather than substitute the local terrain angle. The ESA Sentinel-1 product specification defines `incidenceAngle` in each `geolocationGridPoint` record alongside its source image line/pixel and geodetic coordinates ([Sentinel-1 Product Specification v3.17.1](https://sentiwiki.copernicus.eu/__attachments/a_5d8a355336074550216faed21c971c0c65afa039c4636b3e29bfd9f93298421a/S1-RS-MDA-52-7441-Sentinel-1Product-Specification-v3.17.1.pdf?cb=33fb0d1e3e6b352759057478ddfd1660)). This is the independent angle field needed by the reference-area equation above.

The Copernicus Data Space catalogue inventory identified the exact source GRD products and their `s3://eodata/...` asset prefixes for the eight processed R057/R130 acquisitions. [Inventory workflow run 45169844808](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45169844808) completed successfully. A separate on-demand workflow, `.github/workflows/sentinel1-grd-annotation-object-inventory.yml`, is prepared to list only the small annotation XML and manifest objects; it does not download full SAFE products or imagery.

**One external prerequisite:** CDSE S3 access uses a separately generated S3 access key and secret key, not the Sentinel Hub OAuth client ID/secret. The official [CDSE S3 documentation](https://documentation.dataspace.copernicus.eu/APIs/S3.html) describes how to generate these credentials and the `https://eodata.dataspace.copernicus.eu/` endpoint. Add them to the repository's GitHub Actions secrets as `CDSE_S3_ACCESS_KEY` and `CDSE_S3_SECRET_KEY`; do not paste them into chat or commit them. The prepared workflow also uses the existing `SENTINEL_HUB_CLIENT_ID` and `SENTINEL_HUB_CLIENT_SECRET` secrets to resolve the catalogue asset links.

Once the annotation XML objects are listed, extract and interpolate `incidenceAngle` to the shared output grid, then evaluate the full reference-area equation against the paired RTC/ellipsoid rasters. Validate interpolation against source geolocation points and restrict analysis to common valid pixels. Do not substitute the terrain `localIncidenceAngle` band as if it were θE. Keep `analysis_ready: false` until this independent geometric test and stable-target validation pass.

Latest reproducible angle-proxy/common-mask run: [workflow run 45169689313](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45169689313).


### Completion: source ellipsoid-angle extraction and full equation test (2026-11-23)

This section supersedes the previous "next validation step" status: the CDSE S3 credentials have now been configured and the source metadata workflow has completed.

Eight original Sentinel-1A GRD products were inspected. The inventory found 64 annotation/calibration/RFI XML objects; the VV product annotation XML was extracted for each of the eight acquisitions. Each geolocation grid contains 210 complete tie points (10 azimuth lines × 21 range pixels). The source `incidenceAngle` field was interpolated in geographic coordinates onto the fixed 2048 × 1536 Nairobi output grid, with no extrapolation.

| Track | Tie-point CV MAE | CV RMSE | CV P95 absolute error | Interpolated AOI coverage |
|---|---:|---:|---:|---:|
| R057 | 0.00844° | 0.01277° | 0.02529° | 77.3% |
| R130 | 0.00737° | 0.00943° | 0.01922° | 94.7% |

The common footprint after intersecting the eight incidence rasters with all eight ellipsoid/RTC data masks is **1,848,662 pixels (58.77% of the requested grid)**. Pixels outside the source tie-point convex hull remain NoData.

The full reference-area relation was then tested on that identical footprint:

\[
\Delta_{dB}
=10\log_{10}\left(\frac{\gamma^0_{RTC}}{\gamma^0_E}\right)
=-10\log_{10}(\widehat A_\gamma)-10\log_{10}(\tan\theta_E).
\]

Here `θE` is the source GRD annotation geolocation-grid `incidenceAngle`, not the RTC `localIncidenceAngle`. The equation follows from the ellipsoid gamma reference-area factor `tan(θE)` and the provider's normalized scattering-area convention described above.

Mean results across four acquisitions and VV/VH on the identical common mask:

| Track | Median θE | Area-only residual MAE | Median `-10 log10(tan θE)` | Adjusted residual median | Adjusted residual MAE | Adjusted residual P95 abs |
|---|---:|---:|---:|---:|---:|---:|
| R057 | 31.925° | 2.054 dB | +2.055 dB | −0.00176 dB | 0.00174 dB | 0.00309 dB |
| R130 | 45.375° | 0.0639 dB | −0.05695 dB | +0.00420 dB | 0.00436 dB | 0.00578 dB |

The result is consistent across all four dates and both polarizations. The area-only residual MAE falls from 2.054 to 0.00174 dB on R057, and from 0.0639 to 0.00436 dB on R130. The residual medians and tails are similarly small. This strongly supports the full reference-area equation as an explanation of the provider's paired RTC/ellipsoid outputs on this study footprint.

The earlier local-angle-only proxy was an incomplete substitute: the terrain-relative angle is not θE. The source ellipsoid angle resolves the track-dependent area-only offsets. Do not treat the earlier local-angle proxy as the equation's correction term.

Reproducibility:
- Source annotation inventory: [run 45198522746](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45198522746).
- Eight source geolocation grids: [run 45199797385](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45199797385).
- Full interpolation and equation test: [run 45201769040](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45201769040).
- Targeted tests: [run 45201796311](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45201796311).

This remains a provider-internal, single-site, same-platform/two-orbit validation. The interpolation cross-validation is internal to the source tie-point grids, not independent geodetic control. The common footprint is 58.77% of the requested AOI. Stable radiometric targets, independent geometric control and a second study area/provider are still needed before generalization. Keep `analysis_ready: false`; do not operationalize normalization or change detection from this result alone.

### Source ellipsoid-incidence validation of the RTC reference-area equation (2026-11-23)

The CDSE GRD annotation workflow retrieved the source `incidenceAngle` geolocation-grid points for all eight R057/R130 acquisitions. Linear interpolation to the shared 2048 × 1536 EPSG:4326 Nairobi grid was performed without extrapolation. Five-fold spatially interleaved holdout of the source tie points gave:

| Track | Grid coverage | Tie-point CV MAE | Tie-point CV P95 absolute error |
|---|---:|---:|---:|
| Ascending R130 | 94.7% | 0.00737° | 0.01922° |
| Ascending R057 | 77.3% | 0.00844° | 0.02529° |

Coverage is the fraction of requested output pixels inside the source tie-point convex hull; uncovered pixels remain NoData. The CV figures measure interpolation agreement at held-out source tie points, not independent geodetic accuracy. The R057 coverage limitation is material and must be preserved in every downstream comparison.

Using the source ellipsoid angle \\(\\theta_E\\), the complete reference-area relation is:

\\[
\\gamma^0_{RTC}=\\frac{\\beta^0}{\\widehat A_\\gamma},
\\qquad
\\gamma^0_E=\\beta^0\\tan(\\theta_E)
\\]

\\[
\\Delta_{dB}=10\\log_{10}\\left(\\frac{\\gamma^0_{RTC}}{\\gamma^0_E}\\right)
=-10\\log_{10}(\\widehat A_\\gamma)-10\\log_{10}(\\tan\\theta_E).
\\]

Thus the residual after removing the scattering-area term must be compared with the **negative** ellipsoid reference-area term, \\(-10\\log_{10}(\\tan\\theta_E)\\). This sign is important; the local terrain incidence angle is not a substitute for \\(\\theta_E\\).

On the 1,848,662-pixel common footprint, the source-angle-adjusted residual was:

| Track | Median adjusted residual (VV / VH) | Mean absolute adjusted residual (VV / VH) | P95 absolute adjusted residual (VV / VH) |
|---|---:|---:|---:|
| Ascending R130 | +0.0042 / +0.0042 dB | 0.00436 / 0.00436 dB | 0.00576 / 0.00577 dB |
| Ascending R057 | −0.0018 / −0.0018 dB | 0.00174 / 0.00174 dB | 0.00309 / 0.00309 dB |

These results are highly consistent with the reference-area equation and explain the apparent +2.05 dB R057 versus −0.053 dB R130 area-only offsets. They are not an independent validation of Sentinel Hub's complete RTC implementation: the RTC and ellipsoid backscatter branches still come from the same provider, and the scattering-area semantics are provider-defined. The source angle is independently read from the original GRD annotation, but its interpolation is internally cross-validated only.

The direct RTC-minus-ellipsoid difference remains more variable (mean absolute difference about 0.30–0.34 dB; P95 absolute difference about 1.03–1.16 dB). The equation explains the systematic reference-area difference; it does not imply the two backscatter rasters are pixelwise identical. Terrain resampling, orthorectification, interpolation, and other processing differences remain.

**Decision:** the full reference-area equation now has strong within-provider, two-track, two-polarization empirical support over the common footprint. It is a scientific explanation of the observed relationship, not an approved general-purpose correction or a validated change-detection normalization. R057 has only 77.3% source-angle grid coverage, and the study still lacks independent-provider processing, corner-reflector calibration, and independent-site validation. Keep `analysis_ready: false`.

Reproducibility: [source-angle extraction, interpolation and paired comparison workflow run 45201769040](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45201769040); code: `extract_sentinel1_grd_incidence_grids.py`, `interpolate_sentinel1_ellipsoid_incidence.py`, and `compare_sentinel1_same_platform_orbit_pair.py`.

### Calibration-LUT cross-check of source ellipsoid incidence angles (2026-11-23)

A second source of incidence-angle information was extracted from each original GRD product's **VV calibration XML**. Each file contains 27 calibration vectors and approximately 17,300 range samples. Using the ESA calibration-LUT relationships,

\\[
\\theta_E=\\arccos\\left(\\left(\\frac{A_\\gamma}{A_\\sigma}\\right)^2\\right)
=\\arcsin\\left(\\left(\\frac{A_\\beta}{A_\\sigma}\\right)^2\\right),
\\]

the two independently derived angle arrays agree internally to a maximum of about **0.00005°** across the eight products. The identities follow the ESA Sentinel-1 radiometric calibration definitions of the beta, sigma and gamma normalization LUTs ([ESA calibration technical note](https://sentinels.copernicus.eu/documents/247904/685163/S1-Radiometric-Calibration-V1.0.pdf)).

The calibration-derived angles were then linearly interpolated in source image line/pixel coordinates to the 210 geolocation-grid tie points in each product's annotation XML. All **210/210** annotation points were inside the calibration LUT interpolation hull for every acquisition.

| Track | Mean signed difference (calibration − annotation) | MAE | RMSE | P95 absolute difference |
|---|---:|---:|---:|---:|
| Ascending R130 | −0.0318° | 0.0553° | 0.0705° | 0.1401° |
| Ascending R057 | +0.0034° | 0.0661° | 0.0961° | 0.1856° |

This is a useful independent *metadata-path* cross-check: the calibration LUT and annotation geolocation grid agree closely, with a small track-specific bias and bounded tails. It does not establish absolute angle accuracy against an external geodetic instrument, but it substantially reduces the risk that the angle used in the reference-area equation was misinterpreted or read from the wrong field.

The calibration LUT is denser than the annotation geolocation grid. A subsequent experiment can test whether using calibration-derived angles mapped through the annotation geolocation grid improves the target-grid angle surface; do not replace the current angle raster until that comparison is validated.

Reproducibility: [calibration-LUT angle validation workflow run 45203702710](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45203702710); code: `probe_sentinel1_grd_calibration_lut.py`.

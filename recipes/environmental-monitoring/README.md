# Environmental monitoring: observations-to-spatiotemporal-estimates recipe

**Recipe ID:** SM-REC-014  
**Connected collection framework:** [Spatial observation and sampling design](../../collection/spatial-observation-and-sampling-design.md)  
**Connected methods:** [Dynamic spatial models and data assimilation](../../foundations/spatial-statistics-and-stochastic-processes/dynamic-spatial-models-filtering-and-data-assimilation.md); [spatiotemporal random fields](../../foundations/spatial-statistics-and-stochastic-processes/spatiotemporal-random-fields-advection-and-dynamic-prediction.md)  
**Status:** Design-stage, technology-neutral workflow. Repository geostatistical and transport/assimilation implementations have synthetic tests; no environmental field campaign, sensor calibration, operational forecast or regulatory acceptance is claimed.  
**Audience:** Environmental scientists, geospatial analysts, monitoring programme designers, water/land managers and teams developing spatial decision-support systems.

> This recipe is a project design and data-quality framework. It is not a substitute for a parameter-specific sampling standard, laboratory method, instrument manual, environmental permit, health-and-safety plan or competent authority's requirements. Select the governing protocol for the actual measurand and jurisdiction before fieldwork.

## 1. Purpose and end product

Design and execute a traceable monitoring workflow that turns repeated environmental observations into spatial estimates and, where justified, time-evolving estimates or forecasts.

Examples of target variables include water temperature, dissolved oxygen, conductivity, turbidity, soil moisture, air temperature, particulate concentration and remotely sensed environmental indicators. These variables do not share one measurement model. The project must define each measurand and its observation procedure separately.

The workflow is:

**decision and measurand → sampling design → instrument and method verification → acquisition → immutable observation archive → quality assessment → spatial estimation → optional dynamic model and assimilation → independent verification → delivery and review**

Possible outputs include:
- quality-controlled observation records with calibration and provenance;
- station, sample, transect, pixel or footprint geometries with explicit support;
- coverage and missingness summaries;
- spatial estimates with uncertainty and extrapolation masks;
- time series and, where justified, forecast products with issue times and lead times;
- quality, uncertainty and model-diagnostic layers;
- reproducible processing configuration, data lineage and review report.

A map is not the only deliverable. Depending on the decision, a validated time series, threshold-event record, trend estimate or sampling recommendation may be more useful than a continuous surface.

## 2. Scope and boundaries

### Included
- Decision framing, measurand and target-domain definition.
- Spatial and temporal sampling design.
- Technology-specific method selection and verification planning.
- Field/sample metadata and immutable raw-data handling.
- Quality flags, calibration records, missingness and traceability.
- Spatial estimation and uncertainty reporting.
- Optional state evolution, data assimilation and forecast verification.
- Independent checks, reporting and data hand-off.

### Not automatically included
- Laboratory accreditation or method validation.
- Instrument manufacture, calibration service or repair.
- Environmental impact assessment or regulatory compliance determination.
- A universal physical model for all environmental variables.
- Automatic sensor fault diagnosis or imputation of missing observations.
- A complete operational forecasting platform, alerting service or public-health warning.
- A claim that a synthetic numerical test validates a real environment.

Define additional specialist work packages where the project requires laboratory chain-of-custody, hazardous fieldwork, regulated sampling, ecological interpretation, hydrodynamic modelling or operational response.

## 3. Gate 0 — Define the decision and measurand

Write a one-page monitoring brief before selecting stations or buying sensors.

| Item | Required definition |
|---|---|
| Decision | What action, assessment or scientific question will the observations support? |
| Target phenomenon | What environmental property or process is being studied? |
| Measurand | Exact quantity, operational definition, units and method |
| Target domain | Geographic extent, depth/height range, population or environmental compartment |
| Spatial support | Point, plot, transect, water-column depth, pixel footprint, catchment or other support |
| Temporal support | Instantaneous reading, exposure interval, sample period, daily summary or event window |
| Estimand | Mean, total, exceedance probability, spatial gradient, trend, field state or forecast |
| Decision threshold | Source and rationale for any threshold; do not invent a universal limit |
| Quality objective | Required bias, precision, uncertainty, completeness, latency and traceability |
| Intended user | Who interprets the result and what they are permitted to conclude? |

Keep the phenomenon, observation and derived estimate distinct. A laboratory concentration from a bottle sample is not the same support as an in-situ probe reading or a satellite retrieval. Similar units do not make them interchangeable.

For multiple variables, create a separate measurand record for each one. Record detection limits, reporting limits, censoring and analytical method where relevant.

**Gate 0 exit:** approved monitoring brief, measurand register, target domain and decision-specific quality objectives.

## 4. Gate 1 — Design the sampling and observation system

Use the [spatial observation and sampling design framework](../../collection/spatial-observation-and-sampling-design.md) to document the sampling frame, selection process and observation support.

### 4.1 Choose the design for the inference

- **Probability sample:** appropriate when estimating a finite-population quantity and inclusion probabilities can be defined.
- **Fixed stations:** useful for temporal continuity and process surveillance, but the station network may not represent the entire target domain.
- **Systematic grid or transects:** useful for gradients and broad spatial coverage; assess random starts and periodic-pattern risks.
- **Stratified design:** ensures representation of pre-defined zones or subpopulations.
- **Adaptive design:** adds observations in response to observed events or uncertainty; preserve the adaptive selection history and use an inference method compatible with the design.
- **Remote-sensing sampling:** represents sensor footprints and acquisition times, not automatically ground truth at a point.
- **Opportunistic observations:** useful for reconnaissance but should not be treated as a probability sample without defensible inclusion assumptions.

Do not mix design-based population inference and model-based prediction without stating which assumptions support each result. Fixed stations can be excellent for temporal change detection and poor for estimating a regional mean if their placement is selective.

### 4.2 Design temporal coverage

Choose frequency from the process timescale and decision latency. Record:
- nominal interval and allowable timing tolerance;
- event-triggered or storm/high-flow sampling rules;
- seasonal coverage and planned duration;
- time standard, timestamp source and clock synchronisation;
- integration or averaging interval;
- expected telemetry delay and data revision policy.

A high-frequency sensor does not guarantee high effective information if readings are strongly autocorrelated, drift or repeatedly sample the same conditions.

### 4.3 Select the technology by measurand

For every sensor, sample method or data product, document:
- what is directly measured and what is derived;
- operating range, resolution, detection limit and known interferences;
- spatial footprint and temporal integration;
- calibration/verification method and schedule;
- environmental operating limits and failure modes;
- reference standards, laboratory method or authoritative product specification;
- expected bias, repeatability and uncertainty components.

**Gate 1 exit:** sampling plan, station/sample frame, observation schedule, technology selection rationale and independent-check design.

## 5. Gate 2 — Establish reference, calibration and field readiness

Prepare a method-specific equipment and reference register.

For each instrument or analytical method, record manufacturer/model or method identifier, serial number where applicable, firmware/software, configuration, units, calibration certificate or reference standard, calibration date, validity interval, operator and maintenance history.

Before deployment:
1. Verify the instrument using the manufacturer and governing method procedure.
2. Record as-found checks before adjustment where the procedure permits.
3. Record as-left checks after calibration or adjustment.
4. Define field blanks, duplicates, reference samples, check standards or co-location observations as appropriate to the method.
5. Document sensor placement, orientation, depth/height, shielding, installation geometry and local conditions.
6. Confirm clock synchronisation, data logger configuration, telemetry and backup.
7. Prepare a field safety and access plan appropriate to the site and hazards.

For laboratory samples, define containers, preservatives, filtration, holding times, temperature control, chain-of-custody, laboratory method and reporting limits. For remote sensing, record product level, sensor, acquisition time, processing baseline, atmospheric/geometric corrections and quality masks. Do not apply a probe calibration concept to a satellite retrieval without a valid cross-calibration model.

**Gate 2 exit:** signed readiness record and method-specific verification evidence. If calibration is expired, the instrument fails its check or the method's conditions are not met, quarantine the affected measurements until disposition is documented.

## 6. Gate 3 — Acquire observations and preserve provenance

Never make the cleaned dataset the only surviving copy. Preserve original files and source records as immutable inputs, with checksums where practical.

A minimum observation record should include:

| Field | Meaning |
|---|---|
| observation_id | Stable unique record identifier |
| measurand_id | Exact variable/method definition |
| observed_at | Timestamp with explicit time standard |
| received_at | Ingestion/receipt time, distinct from observation time |
| location/support | Coordinates plus point/line/area/volume support definition |
| value and unit | Original reported value and unit; do not silently normalise |
| method_id | Instrument, laboratory method or product processing identifier |
| instrument_id | Stable instrument reference where applicable |
| calibration_ref | Calibration/check record reference |
| qc_status | Raw, provisional, accepted, flagged, rejected or superseded |
| uncertainty | Value, type, coverage convention and source, where available |
| provenance | Source file, operator, processing version and transformation history |

Also preserve station deployment intervals, sensor depth/height, maintenance, fouling/cleaning, outages, field notes, weather/hydrological context and reasons for missed samples.

For each ingestion, record the source checksum, schema version, ingestion time, parser version, row counts and rejected-row report. Corrections should create a new version or superseding record; never silently overwrite the original measurement.

**Gate 3 exit:** immutable source archive, parsed observation table, provenance manifest and ingestion exception report.

## 7. Gate 4 — Quality control and observation acceptance

Quality control must be measurand- and method-specific. Define rules before examining whether they produce a preferred spatial pattern.

Possible checks include:
- valid coordinate, timestamp, units and method identifiers;
- instrument range and status flags;
- calibration validity at observation time;
- rate-of-change and physical plausibility screens;
- duplicate, blank, reference and co-location comparisons;
- laboratory holding-time and chain-of-custody checks;
- sensor fouling, drift, biofouling, power loss and telemetry-gap flags;
- remote-sensing cloud, shadow, geometry, retrieval and quality masks;
- spatial/temporal consistency checks used as investigation triggers, not automatic rejection.

A statistical outlier is not automatically a bad observation. Extreme environmental events may be real. Flag for review, retain the original value and record the disposition, reason, reviewer and timestamp.

Maintain separate states for:
- **raw:** received without acceptance decision;
- **accepted:** passes the predeclared method and QC requirements;
- **flagged:** retained but requires qualification or review;
- **rejected:** excluded from a specified analysis with reason recorded;
- **superseded:** replaced by a traceable corrected record.

Report missingness by station, time, variable and cause where known. Do not fill missing values with zero. Any imputation must be labelled as derived and must not be fed back as if it were an independent observation.

**Gate 4 exit:** versioned QC dataset, flag definitions, exception log and acceptance summary.

## 8. Gate 5 — Construct the spatial estimate

First determine whether the data support the requested spatial inference.

### 8.1 Exploratory and design checks
- Map observations, sampling frame, strata, inaccessible regions and gaps.
- Plot distributions and time series by station/method.
- Compare co-located methods and inspect systematic offsets.
- Assess spatial clustering, anisotropy, barriers and nonstationarity.
- Check whether the target locations lie within the spatial support of observations.
- Separate temporal change from spatial gradients where sampling times differ.

### 8.2 Choose a method that matches the question

Possible methods include design-weighted estimation, stratified estimators, deterministic interpolation, kriging or other geostatistical prediction. The method must match the sampling design, covariance assumptions, spatial support and intended estimand.

For a model-based estimate, a common conditional-Gaussian representation is

[
Z(mathbf{s}_0)midmathbf{z}
sim
mathcal{N}!left(
m_0+C_{0y}C_{yy}^{-1}(mathbf{z}-mathbf{m}),
 C_{00}-C_{0y}C_{yy}^{-1}C_{y0}
ight),
]

when the joint model is Gaussian and (C_{yy}) is nonsingular. In computation, solve linear systems or use a justified factorisation rather than explicitly forming the inverse. This is a model-based conditional distribution, not a design-unbiased guarantee.

For each output cell/location, retain the estimate, uncertainty measure, observation support/count, distance or other support diagnostic, and extrapolation/quality flag. Do not publish a smooth surface without showing where it is weakly supported.

### 8.3 Validate spatial estimates independently

Use a validation design that reflects intended use:
- spatial blocks or separated sites for transfer to new locations;
- independent reference samples where available;
- temporal holdouts if the product is intended for future dates;
- stratified reporting across environmental zones and relevant value ranges.

Do not tune a variogram, select covariates, choose a model or set thresholds using the same held-out observations later reported as independent validation. Report sample count, bias, MAE/RMSE or task-appropriate scores, uncertainty calibration and spatial pattern of residuals.

**Gate 5 exit:** spatial estimate with uncertainty/support layers, documented model and parameters, and independent validation report.

## 9. Gate 6 — Add temporal dynamics only when justified

A time series of maps is not automatically a dynamic model. Decide whether the application requires temporal interpolation, change detection, state estimation or a genuine forecast.

A generic state-space model is

[
mathbf{x}_{k}=f_k(mathbf{x}_{k-1},mathbf{u}_k)+mathbf{w}_k,
qquad
mathbf{y}_k=h_k(mathbf{x}_k)+mathbf{v}_k,
]

where (mathbf{x}_k) is the latent environmental state, (mathbf{u}_k) contains known drivers, and (h_k) represents the actual observation process. State and observation errors require explicit assumptions; correlated errors, biases and calibration uncertainty may need additional state variables or covariance structure.

For a scalar transported/diffusing quantity, one possible model class is

[
rac{partial c}{partial t}
+
ablacdot(mathbf{u}c)
=

ablacdot(oldsymbol{kappa}
abla c)
+s,
]

where (mathbf{u}) is a transport velocity, (oldsymbol{kappa}) a diffusion/dispersion tensor and (s) a source/sink term. This is not a universal environmental equation. Select the governing balance law and constitutive terms for the actual variable and medium; specify initial and boundary conditions, forcing, parameter sources and model error.

### 9.1 Assimilation cycle

1. Freeze the information set available at forecast issue time.
2. Propagate the prior state to the observation time using the chosen process model.
3. Apply only observations available by that time, through their correct observation operators and error models.
4. Store forecast and analysis separately, with issue time and observation cutoff.
5. Produce forecasts from the analysis state using declared future-driver assumptions.
6. Score forecasts against later observations that were not used for assimilation, tuning or model selection.

The repository's [2-D spatial data-assimilation implementation](../../implementations/python/spatial-data-assimilation/README.md) demonstrates finite-volume advection-diffusion, point observations and ensemble-transform Kalman analysis on synthetic rectilinear grids. It is a bounded teaching implementation, not a general environmental model. In particular, its point observation operator is not a pixel/area footprint model, its transport solver does not establish the correct physics for a specific environment, and its unconstrained Gaussian ETKF can produce negative concentrations. Do not clip negative analyses and claim the original mass budget remains valid.

For each forecast, record:
- issue time and information cutoff;
- target valid time and lead;
- model/version, parameters, initial state and forcing source;
- observations assimilated and their QC states;
- forecast and analysis outputs separately;
- uncertainty representation and known limitations;
- independent verification data and scores.

**Gate 6 exit:** documented state/observation/process model, reproducible forecast-analysis cycle and leakage-safe verification design. If these cannot be justified, deliver descriptive monitoring and spatial estimates rather than a nominal forecast.

## 10. Gate 7 — Delivery, interpretation and operational review

Deliver only products supported by the evidence. A typical package contains:
- monitoring brief and measurand register;
- sampling and station design, including frame and inclusion information;
- instrument/method, calibration and reference records;
- immutable raw archive and provenance manifest;
- versioned QC observations and exception report;
- spatial estimates, uncertainty, coverage and support layers;
- dynamic model configuration and forecast records, if applicable;
- independent validation report and limitations;
- metadata, reproducible code/configuration and data dictionary;
- review date, responsible owner and maintenance plan.

State what users may and may not conclude. A threshold exceedance at a station does not automatically establish the affected area; a modelled surface is not a direct observation; a forecast is conditional on its initial state, process model and future forcing. Regulatory interpretation and public alerts require the applicable authority, quality system and response protocol.

## 11. Minimum project review checklist

- [ ] Decision, target domain and measurand are explicit.
- [ ] Spatial and temporal support are defined for every observation type.
- [ ] Sampling design and intended inference are compatible.
- [ ] Calibration, reference and field verification procedures are documented.
- [ ] Raw observations and source files are preserved with provenance.
- [ ] QC rules and rejection/flagging decisions are traceable.
- [ ] Missingness, censoring and detection limits are represented honestly.
- [ ] Spatial estimation assumptions and extrapolation limits are reported.
- [ ] Independent validation is separated from fitting and model selection.
- [ ] Dynamic model physics, boundaries, forcing and observation operators are justified before assimilation.
- [ ] Forecast issue times and information cutoffs prevent temporal leakage.
- [ ] Outputs include uncertainty, coverage, lineage and limitations.
- [ ] Operational and regulatory claims are made only by appropriately authorised parties.

## 12. Evidence status and known gaps

This recipe is a reusable design framework, not an executed monitoring campaign. The linked repository components provide synthetic numerical tests for selected spatial-statistical, transport and assimilation methods. They do not verify any particular sensor, laboratory procedure, environmental process model, jurisdictional standard or real-world forecast.

Before claiming an operational environmental-monitoring workflow, a project still needs:
- a selected measurand and governing field/laboratory protocol;
- a real sampling frame and field deployment;
- calibration and independent reference evidence;
- an application-specific observation operator;
- a physically justified process model where forecasting is required;
- independent spatial and chronological forecast validation;
- a documented acceptance decision by the responsible project authority.

## 13. Further reading within this repository

- [Spatial observation and sampling design](../../collection/spatial-observation-and-sampling-design.md)
- [Random fields, covariance and variograms](../../foundations/spatial-statistics-and-stochastic-processes/random-fields-covariance-and-variograms.md)
- [Dynamic spatial models, filtering and data assimilation](../../foundations/spatial-statistics-and-stochastic-processes/dynamic-spatial-models-filtering-and-data-assimilation.md)
- [Spatiotemporal random fields, advection and dynamic prediction](../../foundations/spatial-statistics-and-stochastic-processes/spatiotemporal-random-fields-advection-and-dynamic-prediction.md)
- [Geostatistics catalogue](../../algorithms/geostatistics/README.md)
- [Spatial data-assimilation implementation](../../implementations/python/spatial-data-assimilation/README.md)

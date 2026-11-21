# Spatial observation and sampling design

> **Pillar:** Spatial Data Collection  
> **Connections:** Theoretical Foundations, Spatial Algorithms, Spatial Recipes  
> **Status:** Initial cross-technology method framework; specialist review and application-specific validation pending  
> **Purpose:** Design observations that can support a stated spatial decision, estimate or model without confusing the sample, the measurement and the phenomenon.

## 1. The design question comes before the instrument

A spatial dataset is the result of an observation design. It is not simply a collection of coordinates or sensor files.

Before selecting GNSS, a total station, a satellite, an aircraft, a mobile mapping system, a fixed sensor, a field team or a crowdsourced platform, define:

- **Target phenomenon:** what real-world property, object, event or process is of interest?
- **Target population or domain:** where and when does the question apply?
- **Unit of observation:** what is sampled or measured—point, parcel, pixel, transect, event, person, asset, water sample, time interval or another unit?
- **Measurand:** what quantity is directly observed, in what units and under what operational definition?
- **Estimand or decision:** what quantity, pattern, classification or decision must the observations support?
- **Required support:** at what spatial and temporal scale should the result be interpreted?
- **Quality requirement:** what uncertainty, bias, completeness, timeliness and traceability are acceptable?

An instrument is selected only after these requirements are sufficiently clear. A sensor's nominal accuracy, pixel size, point density or sampling frequency is not by itself evidence that the final dataset is fit for purpose.

## 2. Separate phenomenon, observation and derived data

Keep three layers distinct.

1. **Phenomenon:** the real-world property or process, which may vary continuously in space and time.
2. **Observation:** a physical or human-mediated measurement produced by a sensor, instrument, sampling procedure or report.
3. **Derived data:** a value or geometry inferred through calibration, correction, classification, interpolation, fusion, adjustment or modelling.

For example, a GNSS receiver records signal observations and estimates a position; a camera records image-plane radiance samples and photogrammetry estimates object-space geometry; a satellite instrument records a spatially integrated signal and a retrieval algorithm estimates a geophysical variable. These outputs have different measurement models and error structures.

Record which quantities are directly measured, which are estimated, and which are assigned through interpretation. Do not describe a derived class, interpolated surface or modelled value as if it were directly observed.

## 3. Define the spatial and temporal support

The *support* of a measurement is the spatial and/or temporal domain over which it represents the phenomenon.

Examples include:

- a point coordinate or point-level field observation;
- a line-integrated measurement along a transect or route;
- an areal average over a plot, pixel footprint or administrative unit;
- a three-dimensional volume or voxel;
- a sensor footprint integrated over an exposure or acquisition interval;
- a time-window average, event observation or continuous sensor time series.

Two datasets can use the same variable name and units while representing different supports. A point sample of soil moisture is not automatically equivalent to a satellite pixel estimate or a plot average. Aggregation and disaggregation change the question and can introduce uncertainty.

Record at least:

- spatial support geometry and its definition;
- temporal support, timestamp convention and duration;
- spatial resolution or sampling interval, without equating it to accuracy;
- coordinate reference system, datum/realisation and epoch where relevant;
- treatment of boundaries, mixed supports and missing coverage.

## 4. Construct a defensible sampling frame

The sampling frame is the operational representation from which units can be selected. It may be a list of assets, a polygon partition, a road network, a raster grid, a set of candidate sites, a time-event register or a sensor's observable domain.

Check whether the frame:

- covers the intended target population;
- includes duplicates, obsolete units or invalid geometries;
- omits inaccessible or poorly mapped areas;
- has unequal or unknown probabilities of inclusion;
- changes during the observation period;
- introduces coverage bias through its source or construction.

A perfect sampling algorithm cannot repair a frame that systematically excludes part of the target population. Document the frame's source, date, version, exclusions and known coverage gaps.

## 5. Choose a sampling design

The design should follow the estimand, spatial structure, access constraints and available resources. The following are design families, not interchangeable recipes.

| Design | Useful when | Main cautions |
|---|---|---|
| Simple random | A complete frame exists and each unit can be selected independently with equal probability | May produce spatial gaps or inefficient travel; requires a defensible frame |
| Stratified | Important subgroups or environmental zones need representation | Strata must be defined before selection; allocation affects precision and weights |
| Systematic grid or transect | Regular coverage, gradients or spatial structure are important | Use a random start where appropriate; periodic patterns can interact with the grid |
| Cluster or multistage | Units are naturally grouped or field access is costly | Within-cluster similarity can reduce effective sample size; preserve selection probabilities at every stage |
| Spatially balanced probability | Broad geographic spread is important while retaining probability-based inference | Design and inclusion probabilities must be understood; geographic balance does not remove measurement bias |
| Adaptive | Additional observations are triggered by observed features, rare events or thresholds | Adaptive selection and inference must be documented; naive analysis of the final sample can be biased |
| Purposive or expert-selected | Specific features, extremes, failure cases or mechanisms are the target | Usually does not support design-unbiased population estimates without additional assumptions |
| Convenience or opportunistic | Rapid reconnaissance or exploratory data gathering is the immediate goal | Strong selection bias is likely; label the data as opportunistic and limit inference |

A dense grid is not automatically representative. A large number of convenience observations does not become a probability sample merely because it is large. For model training and validation, distinguish sampling for coverage, sampling for prediction, and independent sampling for evaluation.

### 5.1 Inclusion probabilities and weighted estimation

For probability samples, let (pi_i) be the probability that population unit (i) is included. If the target is a finite-population total, the Horvitz–Thompson estimator is:

\[
\widehat{T}_{HT}=\sum_{i\in s}\frac{y_i}{\pi_i}
\]

where (s) is the realised sample and (y_i) is the observed value for sampled unit (i). This estimator relies on known, positive inclusion probabilities and an appropriate sampling design. Variance estimation must reflect the joint inclusion probabilities and actual design.

For stratified simple random sampling, with (H) strata, population size (N_h), sample size (n_h), and within-stratum sample variance (s_h^2), the estimated variance of the stratified total is:

\[
\widehat{\operatorname{Var}}(\widehat{T}_{st})
=\sum_{h=1}^{H}N_h^2\left(1-\frac{n_h}{N_h}\right)\frac{s_h^2}{n_h}
\]

This expression is for the stated stratified random design; it should not be reused for a different design without deriving the appropriate variance estimator.

### 5.2 Sample size is a design calculation, not a universal constant

For a simple random sample estimating a proportion under an approximate normal confidence interval, an initial large-population calculation is:

\[
n_0=\frac{z_{1-\alpha/2}^{2}\,p(1-p)}{e^2}
\]

where (p) is the anticipated proportion, (e) is the desired absolute margin of error, and (z_{1-\alpha/2}) is the corresponding normal quantile. If (p) is unknown, (p=0.5) gives the largest value under this approximation.

For a finite population of size (N), a common correction is:

\[
n=\frac{n_0}{1+\frac{n_0-1}{N}}
\]

These calculations assume a particular estimator and sampling design. They do not automatically account for clustering, unequal weights, nonresponse, spatial dependence, measurement error or multiple outcomes. A design effect, expected nonresponse and operational constraints may change the required number of observations. State assumptions and show the calculation rather than quoting a universal sample size.

## 6. Account for spatial dependence and uneven observability

Spatial observations are rarely independent by default. Nearby measurements may be similar because of the process itself, shared environment, common instrument conditions or common collection teams.

Design implications include:

- stratify or balance across meaningful environmental or operational zones;
- consider gradients, boundaries, rare features and known transition areas;
- avoid treating many nearby observations as equivalent to the same number of geographically dispersed observations;
- record inaccessible locations and reasons for non-observation;
- distinguish deliberate oversampling of rare classes from population-representative sampling;
- retain enough design information to calculate appropriate weights and uncertainty.

Spatial balance improves geographic spread, but it does not guarantee independence, unbiased measurement or adequate representation of every process. For predictive modelling, spatially separated validation can better test transfer to new locations than a random split of neighbouring observations. The split strategy must match the intended deployment domain.

## 7. Match the acquisition technology to the measurand

The same study may require several observation technologies. Choose them by what they can measure, their support, observability and failure modes—not by novelty.

| Technology family | Typical observations | Design questions |
|---|---|---|
| GNSS and positioning systems | Coordinates, trajectories, timing and signal-derived estimates | Sky visibility, multipath, reference frame, correction source, occupation, antenna setup and independent checks |
| Total stations and terrestrial survey instruments | Angles, distances, directions and derived coordinates | Line of sight, control geometry, centring, instrument checks, atmospheric effects and observation redundancy |
| Levelling systems | Height differences and vertical control | Datum, route design, staff and instrument checks, refraction, closure and benchmark stability |
| Optical satellite and airborne sensors | Reflected/emitted radiance sampled over image footprints | Spectral response, illumination, clouds, view geometry, calibration, revisit and spatial/temporal support |
| Radar and microwave sensors | Returned microwave signal, amplitude/intensity and, for suitable products, phase | Wavelength, polarisation, incidence geometry, coherence, terrain effects, acquisition mode and product level |
| Photogrammetry and structure from motion | Image observations used to infer three-dimensional geometry | Image network geometry, calibration, overlap, control, texture, motion and occlusion |
| LiDAR and laser scanning | Ranges and derived point clouds or surfaces | Scan geometry, trajectory, registration, reflectance, occlusion, point density and control |
| Bathymetric and hydrographic systems | Depth-related acoustic or optical observations | Sound-speed profile, water level, vessel motion, sensor offsets, tide/datum and coverage |
| In-situ environmental sensors | Physical or chemical measurements at a sensor location or footprint | Calibration, drift, response time, placement, exposure, sampling interval and maintenance |
| Field sampling and laboratory analysis | Collected material or field observations | Sampling frame, compositing, contamination, preservation, chain of custody and laboratory method |
| Mobile mapping and robotics | Trajectories, images, ranges and fused observations | Time synchronisation, calibration, trajectory quality, occlusion, motion and reference control |
| Crowdsourced and volunteered data | Human observations, reports, traces and edits | Participation bias, contributor context, positional uncertainty, duplicate reports, verification and licensing |
| Administrative and operational records | Events, assets, service locations and reported attributes | Definition consistency, geocoding, reporting coverage, update cycle, provenance and privacy |

This list is deliberately open. New instruments and platforms can be added without changing the underlying design questions.

## 8. Design calibration, control and quality assurance

Quality assurance must be planned before collection. Select checks that test the relevant parts of the measurement chain.

### Instrument and sensor checks

- calibration status, certificate or documented calibration procedure;
- warm-up, configuration, firmware and software version;
- sensor offsets, boresight, lever arms and timing where applicable;
- repeatability, drift, saturation, detection limits and environmental sensitivity;
- pre-collection and post-collection checks where the instrument or method requires them.

### Reference and control

- authoritative reference source and its uncertainty;
- datum, coordinate epoch, vertical reference and transformations;
- control distribution and stability;
- independent check observations not used to fit or tune the result;
- traceable links between raw observations, control and derived products.

### Field and operational checks

- completeness against the planned sampling frame;
- timestamps, location, operator, equipment and method;
- environmental conditions and deviations;
- repeated or redundant observations;
- missing, rejected or inaccessible units and the reason;
- secure backups and immutable preservation of raw observations.

### Statistical and spatial checks

- residuals and closure tests appropriate to the measurement model;
- outlier investigation without automatic deletion;
- spatial patterns in residuals and missingness;
- uncertainty summaries and error budgets;
- independent validation matched to the intended use;
- checks for leakage between training, tuning and evaluation data.

A quality flag is not a substitute for evidence. Retain the raw values, check results, acceptance rules and reasons for any rejection or correction.

## 9. Preserve provenance and uncertainty

Each observation should be traceable to its origin and interpretation. A minimum record should consider:

| Record element | What to preserve |
|---|---|
| Identity | Stable observation ID and parent campaign/project ID |
| Target | Feature, phenomenon, sampling unit and operational definition |
| Position and support | Geometry, CRS/reference frame, epoch, spatial support and positional uncertainty |
| Time | Observation time, time zone or time standard, duration and clock source where relevant |
| Measurement | Value, unit, measurand, method and direct/derived status |
| Instrument | Sensor/instrument identity, configuration, calibration and firmware/software |
| Context | Operator or responsible process, environment, access and collection conditions |
| Design | Sampling frame/version, selection method, inclusion probability or selection rationale |
| Quality | Flags, checks, residuals, uncertainty and acceptance status |
| Provenance | Raw source, processing lineage, transformations, edits and licence/permissions |

Uncertainty is not one number unless the measurand and error model justify that simplification. Distinguish random variation, systematic effects, reference uncertainty, sampling uncertainty, model uncertainty and unknown bias. Do not combine terms without considering dependence and units.

## 10. From observation design to a reusable dataset

A defensible collection workflow follows a traceable chain:

1. State the decision, estimand or intended use.
2. Define the target population, unit, support and sampling frame.
3. Choose a design and document inclusion or selection rules.
4. Select technologies that can observe the required measurands.
5. Specify reference, calibration, control and independent checks.
6. Pilot the design and revise it where evidence shows a weakness.
7. Collect raw observations and preserve original records.
8. Process and transform with explicit software, parameters and provenance.
9. Assess quality and uncertainty against predeclared criteria.
10. Publish a dataset and data dictionary with limitations and permitted uses.

The result is not just a geometry file. It is an observation dataset, a record of how the observations were selected and produced, and evidence about what can responsibly be inferred from them.

## 11. Common design failures

- **Choosing the sensor first:** produces technically impressive data that may not answer the question.
- **Confusing resolution with accuracy:** pixel size, point spacing and sampling frequency do not establish positional or thematic quality.
- **Using an incomplete frame:** creates coverage bias that processing cannot repair.
- **Ignoring support:** compares point measurements, pixel footprints and areal averages as if they were equivalent.
- **Treating opportunistic data as representative:** confuses volume with probability-based coverage.
- **Using the same observations for fitting and validation:** overstates performance and hides generalisation error.
- **Ignoring inaccessible areas and missingness:** makes the final map appear more complete than the evidence.
- **Discarding raw observations:** prevents independent audit and alternative processing.
- **Recording only final coordinates:** loses the measurement method, reference, uncertainty and provenance needed for reuse.

## 12. Design review checklist

Before authorising a collection campaign, confirm:

- [ ] The target phenomenon, estimand and intended decision are explicit.
- [ ] The target population, spatial/temporal domain and observation unit are defined.
- [ ] Spatial and temporal support are documented.
- [ ] The sampling frame and its coverage limitations are understood.
- [ ] The sampling design and selection probabilities or rationale are recorded.
- [ ] The technology is appropriate to the measurand and environment.
- [ ] Reference, calibration, control and independent checks are planned.
- [ ] Uncertainty, missingness, bias and nonresponse are considered.
- [ ] Raw observations, metadata and provenance will be preserved.
- [ ] Acceptance criteria and stop/rework rules are defined.
- [ ] Permissions, safety, privacy, licensing and professional constraints are addressed.

If a critical item is unknown, record it as unresolved. Do not silently convert an assumption into a collection specification.

## 13. Connections to the other Spatial Methods pillars

- **Theoretical Foundations:** measurement science, sampling theory, probability, spatial statistics, uncertainty, geodesy and sensor physics explain why the design works and where it fails.
- **Spatial Algorithms:** spatial balancing, sample allocation, network-constrained sampling, interpolation, adjustment, classification and validation implement parts of the design.
- **Spatial Recipes:** combine a specific study question, data source, collection plan, processing chain and acceptance checks into a reproducible workflow.
- **Real-world applications:** ecology, infrastructure, transport, public health, agriculture, water, disaster response and urban analysis define the actual measurands and decisions.

The framework is cross-technology by design. Specialised collection methods should extend it with their own physical measurement models, acquisition constraints, calibration procedures and domain-specific quality evidence.

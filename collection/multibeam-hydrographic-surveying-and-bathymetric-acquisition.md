# Multibeam hydrographic surveying and bathymetric acquisition

> **Pillar:** Spatial Data Collection  
> **Subject:** SM-COL-013 — Hydrographic, marine and bathymetric surveying  
> **Scope:** Vessel-based multibeam echo-sounder (MBES) acquisition and processing context, with single-beam comparison; positioning, attitude, sound velocity, water levels, calibration, coverage and quality assessment  
> **Status:** Initial method synthesis; no vessel mobilisation, sonar calibration or field validation is claimed  
> **Related methods:** [GNSS positioning](gnss-positioning-and-navigation-observation.md); [terrestrial surveying](terrestrial-surveying-total-station-and-levelling.md); [airborne LiDAR](airborne-lidar-acquisition-and-strip-adjustment.md); [coastal optical bathymetry algorithm](../algorithms/remote-sensing/stumpf-bathymetry-and-oc4v4.md)

## 1. What hydrographic sounding measures

Hydrographic surveying determines water depth, seabed form and, where required, the position and characteristics of underwater features. Acoustic echo sounders transmit sound into the water and detect energy returned from the seabed or other reflectors. The measured travel time is converted to range using a model of sound speed and acoustic propagation. Position, vessel attitude, transducer geometry and the vertical reference are then used to derive a seabed coordinate or reduced depth.

This method concentrates on vessel-based multibeam echo sounding (MBES). A multibeam system emits a fan of acoustic beams and produces a swath of soundings. Single-beam echo sounding (SBES) measures depth in a narrower footprint along the vessel track. Side-scan sonar is principally an imaging/feature-search sensor rather than a direct substitute for calibrated bathymetric sounding. Interferometric sonar, sub-bottom profilers, airborne bathymetric LiDAR and satellite-derived bathymetry have different measurement models and need separate procedures.

A dense sounding cloud is not automatically a complete seabed search, a correctly reduced depth surface or a safe navigation product. Coverage, feature detection, uncertainty, datum reduction and interpretation are separate quality questions.

## 2. Define the survey purpose and specification

Establish the intended use before selecting the system or line plan. Applications include navigation safety, harbour and port maintenance, dredging and construction, river and reservoir surveys, coastal change, habitat mapping, underwater infrastructure, sediment and geomorphology studies, and offshore engineering.

Specify:
- area of interest, survey purpose and responsible authority/client;
- required bathymetric coverage and feature-search requirements;
- depth range, seabed type, expected relief and smallest feature to detect;
- horizontal and vertical uncertainty requirements;
- horizontal reference frame, realisation and epoch;
- vertical reference surface/datum, separation model and water-level strategy;
- sounder type, frequency, beam configuration and backscatter needs;
- line spacing, overlap, cross-lines and independent reference observations;
- deliverables, grid resolution, uncertainty layers, metadata and acceptance rules.

For safety-of-navigation work, select the applicable survey order and criteria from the current hydrographic authority specification. IHO S-44 is a framework for defining requirements, not a universal substitute for project instructions. A research bathymetry grid, a dredging quantity survey and a charting survey may need different feature detection, coverage and uncertainty criteria.

## 3. Acoustic depth measurement

For a simplified vertical, two-way acoustic path with constant sound speed (c) and measured travel time (Delta t), the range is:

\[
D = \frac{c\,\Delta t}{2}
\]

The factor of two accounts for the outbound and return paths. This expression is only a simplified model. Actual MBES beams travel obliquely through a water column in which sound speed varies with depth, temperature, salinity and pressure. The beam path is refracted; the sounding position and depth therefore depend on ray tracing or the system's validated beamforming/refraction model.

For a layered water column, Snell's law describes refraction:

\[
\frac{\sin\theta_1}{c_1}
=
\frac{\sin\theta_2}{c_2}
=
\cdots
=
\frac{\sin\theta_k}{c_k}
\]

where each \(c_k\) is sound speed in a layer and \(\theta_k\) is the ray angle measured consistently relative to the layer normal. A sound-speed error can produce both depth and horizontal-position errors, especially for outer beams.

### 3.1 Sound-speed observations

Two sound-speed measurements have distinct roles:

- **Sound-speed profile (SVP):** measures sound speed through the water column, commonly derived from conductivity-temperature-depth (CTD) observations or a direct sound velocimeter. It supports refraction correction.
- **Surface sound speed:** supports the conversion from measured beam steering/angle to the actual acoustic direction at the transducer face. It may be measured by a velocimeter or derived from near-surface observations using a documented procedure.

A profile taken at one location and time may not represent the entire survey area. Thermoclines, freshwater inflows, tides, fronts, depth changes and weather can produce spatial or temporal variability. Plan casts across the survey area and repeat them when conditions or data diagnostics indicate that the profile is no longer representative. There is no universally correct fixed cast interval for all environments.

Record instrument identity, calibration/verification, cast time and location, profile depth, processing, interpolation and the profile assigned to each survey line or time interval. Do not silently extrapolate a shallow cast to deeper soundings.

## 4. Georeferencing and vertical reference

A sounding's final coordinate depends on the transducer position, vessel attitude, acoustic range/beam direction, timing, mounting offsets and reference transformation. A simplified rigid-body transformation is:

\[
\mathbf{X}_{b}^{E}
=
\mathbf{r}_{I}^{E}(t)
+
R_{b}^{E}(t)
\left[
\mathbf{l}_{I\rightarrow T}^{b}
+
R_{s}^{b}\,\mathbf{x}^{s}
\right]
\]

where:
- \(\mathbf{X}_{b}^{E}\) is the seabed point in the earth-fixed frame;
- \(\mathbf{r}_{I}^{E}(t)\) is the navigation position of the IMU origin at the sounding epoch;
- \(R_b^E(t)\) is the body-to-earth rotation;
- \(\mathbf{l}_{I\rightarrow T}^{b}\) is the lever arm from IMU origin to transducer reference point;
- \(R_s^b\) is the calibrated sonar-to-body rotation;
- \(\mathbf{x}^{s}\) is the acoustic sounding vector in the sonar frame, derived from range and beam angle.

The exact frame chain depends on system architecture. GNSS antenna-to-IMU offsets, transducer draft, mounting alignment, sign conventions, rotation order and the reference point of the navigation solution must be represented consistently. Heave and attitude may be output by an integrated motion sensor or navigation estimator; avoid applying the same correction twice.

### 4.1 Water level and vertical datum

A depth relative to the transducer is not yet a seabed elevation or a chart-datum-reduced depth. The final vertical reference may be a tidal datum, local project datum, national height datum, geoid-related surface or ellipsoid, depending on the application.

If the transducer elevation \(z_T\) is expressed in a chosen vertical reference with positive-up coordinates, and \(D\) is the corrected vertical depth below the transducer, a simplified seabed elevation is:

\[
z_b = z_T - D
\]

The transducer elevation must itself be derived using the correct vessel draft, dynamic motion, water-level or ellipsoidal-height method. A water-level time series must be tied to the required datum through documented benchmarks and separation relationships. Tide predictions, observed water levels, GNSS-derived water levels and ellipsoidally referenced bathymetry are not interchangeable without an explicit datum and uncertainty model.

Record the vertical datum, benchmark ties, water-level sensor, time series, interpolation, separation model, epoch and uncertainty. Never compare ellipsoidal heights directly with depths or orthometric/chart-datum elevations without the required transformations.

## 5. Vessel motion, offsets and calibration

The complete measurement system may include:
- GNSS receiver and antenna;
- inertial navigation system (INS) or motion reference unit;
- MBES transducer and transmit/receive arrays;
- sound-speed sensor at the transducer;
- SVP/CTD instrument;
- water-level sensor or GNSS vertical reference;
- heading source, timing interface and acquisition computer.

Measure and document the geometry between sensor reference points. Calibrate or verify:
- roll, pitch and heading/azimuth alignment;
- latency between position, attitude and sonar observations;
- transducer/IMU/GNSS lever arms;
- transducer draft and reference point;
- heave response and dynamic motion;
- sonar range, beam-angle and timing behaviour;
- sound-speed sensor performance.

A **patch test** estimates residual angular and timing offsets using designed reciprocal and crossing lines over suitable seabed geometry. Typical tests isolate latency, pitch, roll and heading/yaw effects through different line orientations, directions, speeds and bottom slopes/features. The exact design and analysis depend on sonar and navigation architecture. Record the test area, line geometry, environmental conditions, estimated corrections, residuals, software and acceptance decision. Re-run or review calibration after sensor movement, repair, impact or unexplained systematic mismatch.

Vessel squat and settlement can alter transducer depth with speed and loading. Record the vessel configuration and assess whether dynamic draft corrections are needed. Do not assume a static draft measurement represents the vessel at survey speed.

## 6. Survey planning and acquisition

### 6.1 Coverage and line design

MBES swath width depends on water depth, beam sector, bottom slope, vessel attitude, sound-speed structure and acceptable outer-beam quality. A wider sector increases nominal coverage but can worsen refraction and geometric uncertainty at outer beams. Line spacing should be based on the required coverage and quality at the actual seabed, not a generic percentage of depth.

Plan:
1. Main-line direction, spacing, speed and overlap.
2. Cross-lines/tie-lines to expose systematic differences and test consistency.
3. Turns, acceleration/deceleration and areas of unstable vessel motion.
4. Sound-speed profile stations and surface sound-speed monitoring.
5. Control, water-level and benchmark observations.
6. Feature search and least-depth investigation where required.
7. Safe vessel access, traffic, weather, current, depth and navigation constraints.

Distinguish **bathymetric coverage** (where valid depth soundings exist) from **feature search** (whether the system and survey design can detect features of the required size). A full-looking grid does not prove that all hazards or objects were detected.

### 6.2 Field procedure

**Before mobilisation**
- Confirm project instructions, survey order/acceptance criteria, datums and permits.
- Verify vessel, transducer installation, sensor configuration, calibration records and offsets.
- Confirm GNSS/INS correction source, reference frame and antenna setup.
- Verify sound-speed instruments, SVP procedure, water-level method and time synchronisation.
- Plan patch test, reference lines, cross-lines, line spacing and backup.
- Check acquisition software, storage, naming, backups and data logging.

**At the start of acquisition**
- Record vessel draft, loading, transducer immersion, sensor offsets and configuration.
- Complete navigation initialisation and required patch-test/verification lines.
- Measure surface sound speed and acquire an appropriate water-column profile.
- Confirm timing, position, heading, attitude, heave and sonar data are synchronised.
- Inspect raw beams, outer-beam behaviour, noise, coverage and real-time quality indicators.

**During survey**
- Monitor vessel speed, heading, attitude, GNSS quality, heave, sonar status and data gaps.
- Acquire SVPs at a frequency and distribution appropriate to changing water masses and project requirements.
- Record water-level observations and any interruptions, sensor changes or unusual conditions.
- Inspect overlap, cross-lines, outer-beam artefacts, sound-speed artefacts and data completeness.
- Re-run affected lines when coverage or quality is not recoverable by defensible processing.

**After acquisition**
- Back up raw sonar, navigation, attitude, sound-speed, water-level and event records.
- Check line completeness, time continuity, calibration status, profile coverage and metadata before leaving the area.
- Record unresolved gaps, rejected lines and reasons.

## 7. Processing, uncertainty and quality control

A defensible processing sequence generally includes:
1. Ingest and checksum raw sonar and ancillary records.
2. Verify time systems, latency, sensor configuration and installation offsets.
3. Apply range, beam-angle and sound-speed corrections.
4. Process GNSS/INS position, heading, attitude and heave.
5. Apply lever arms, patch-test parameters and vessel draft/squat corrections.
6. Reduce soundings to the project vertical reference using the documented water-level or ellipsoidal method.
7. Inspect and clean soundings while preserving raw observations and rejection history.
8. Compare main lines, cross-lines and overlapping swaths.
9. Assess uncertainty, coverage, feature detection and independent checks.
10. Generate bathymetric surfaces and uncertainty layers with explicit gridding rules.

Build an uncertainty budget that includes relevant contributions from acoustic range, sound speed and refraction, beam angle, GNSS position, heading, roll/pitch, heave, timing, lever arms, draft, water level/datum, vessel dynamics and processing. Contributions may be correlated; do not blindly combine all terms as independent scalars. Use a covariance-aware propagation model where the required accuracy justifies it.

IHO S-44 expresses depth uncertainty through total vertical uncertainty (TVU) and horizontal uncertainty through total horizontal uncertainty (THU), with requirements at a stated confidence level. For the depth-dependent TVU model:

\[
TVU_{max}(d)=\sqrt{a^2+(b\,d)^2}
\]

where \(d\) is depth and \(a,b\) are parameters specified for the applicable survey order. Use the values and confidence conventions from the current adopted edition and project instructions; do not copy a threshold from another order or jurisdiction.

Quality assessment should report separately:
- absolute horizontal and vertical uncertainty/accuracy;
- cross-line and overlapping-swath consistency;
- coverage and data voids;
- feature search/detection evidence;
- sound-speed and water-level adequacy;
- data cleaning and rejected sounding statistics;
- grid resolution, interpolation and uncertainty;
- independent reference/check observations.

A small cross-line difference does not prove absolute accuracy: all lines may share a common datum or calibration bias. Likewise, low sounding scatter does not prove that the seabed was fully searched or that small features were detected.

## 8. Deliverables and provenance

Retain and deliver, as required by the project:
- raw sonar files and checksums;
- vessel and sensor configuration, serial numbers and firmware;
- installation diagrams, offsets, draft and calibration/patch-test reports;
- GNSS/INS observations, trajectory, heading, attitude and quality indicators;
- sound-speed profiles and surface sound-speed records with time/location;
- water-level records, benchmark ties and vertical datum transformations;
- line plans, tracklines, cross-lines, survey dates and environmental observations;
- processing software/version, parameters, rejected data and processing history;
- sounding data, uncertainty estimates, coverage and feature-search evidence;
- gridded bathymetry, grid resolution, interpolation, uncertainty and metadata;
- control/check observations, their uncertainty and their independent role;
- licence, ownership, use restrictions and delivery formats.

Keep raw observations, corrected soundings, cleaned soundings, reduced depths, gridded bathymetry and derived products distinguishable. A grid is an interpreted representation of observations; preserve source soundings and the method used to create each cell.

## 9. Physical-world applications and limits

Hydrographic acquisition supports navigation, ports, dredging, coastal engineering, river/reservoir management, offshore infrastructure, marine habitat, sediment transport and coastal change. Method selection must follow the target and environment:
- MBES for swath bathymetry and seafloor form;
- SBES for depth profiles or applications where its narrower footprint is sufficient;
- side-scan sonar for acoustic imagery and feature search, normally complemented by a depth-measuring system;
- sub-bottom profiling for shallow subsurface structure rather than only the seabed interface;
- bathymetric LiDAR for suitable shallow/clear-water conditions and airborne coverage;
- satellite-derived bathymetry for suitable optical conditions and calibrated depth retrieval, with independent validation.

Turbidity, bubbles, waves, vessel motion, current, shallow-water access, vegetation, soft sediments, steep slopes, acoustic shadows and changing sound-speed structure can limit results. No single sensor detects every feature in every environment.

## 10. Standards and technical references

- [IHO S-44 — Standards for Hydrographic Surveys, Edition 6.2.0 (October 2024)](https://iho.int/uploads/user/pubs/standards/s-44/S-44_Edition_6.2.0_adopted.pdf). International framework for survey orders, coverage, feature detection, uncertainty and metadata. The IHO publication catalogue currently identifies Edition 6.2.0 as the published edition. A 6.3.0 document dated 2026 is in draft/estimate status and should not be treated as an adopted replacement unless the IHO publication register confirms adoption.
- [NOAA Hydrographic Surveys Specifications and Deliverables (HSSD)](https://nauticalcharts.noaa.gov/publications/standards-and-requirements.html). A detailed national implementation of IHO hydrographic survey requirements; use as a technical reference, not as a Kenyan specification.
- [NOAA hydrographic survey equipment overview](https://nauticalcharts.noaa.gov/learn/hydrographic-survey-equipment.html). Explains multibeam sonar measurement and swath coverage.
- [IHO C-13 — Manual on Hydrography](https://iho.int/en/capacity-building-publications). Technical background on positioning, depth determination, seafloor classification and water levels.
- [Canadian Hydrographic Service survey management guidelines](https://www.chs.gc.ca/data-gestion/guidelines-directrices/index-eng.html). Practical guidance on sound-speed profiles, patch tests and independent comparison.

These references do not replace current national hydrographic instructions, maritime safety requirements, vessel procedures, professional competence or client specifications. Confirm applicable Kenyan authorities, permissions, vertical datum, control and data-ownership requirements before any operational survey. This method is an educational synthesis, not an authorisation to conduct hydrographic work.

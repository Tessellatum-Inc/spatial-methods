# Multibeam bathymetry: observations-to-validated-surface recipe

**Recipe ID:** SM-REC-013  
**Connected collection method:** [SM-COL-013 — Multibeam hydrographic surveying and bathymetric acquisition](../../collection/multibeam-hydrographic-surveying-and-bathymetric-acquisition.md)  
**Status:** Desk-designed workflow; acoustic ray-tracing teaching implementation has synthetic tests; no vessel mobilisation, sonar acquisition, calibration, field validation or operational bathymetric surface is claimed.  
**Audience:** Hydrography learners, spatial data practitioners, coastal and marine researchers, and project teams scoping a multibeam survey.

> This recipe is a technical workflow framework, not a hydrographic survey specification, navigation-safety certification, vessel operating procedure, legal authorisation or guarantee of survey accuracy. Project instructions, the competent national hydrographic authority, applicable law, professional competence and client acceptance criteria take precedence.

## 1. Purpose and end product

Convert multibeam echo-sounder (MBES) observations into a traceable, datum-referenced and quality-assessed bathymetric surface.

The workflow is:

**requirements → reference and control → system verification → acquisition → corrections and ray tracing → sounding review → uncertainty and coverage assessment → gridding → independent validation → delivery**

A bathymetric surface is not simply a raster of depths. It is a derived representation of accepted observations, with a defined horizontal and vertical reference, spatial support, resolution, uncertainty, coverage and provenance.

Potential outputs include:
- georeferenced sounding point cloud or accepted sounding dataset;
- bathymetric grid or surface;
- per-cell sounding density/count and coverage mask;
- per-cell uncertainty or quality layer where supported by the processing method;
- feature and least-depth records where required;
- acquisition, calibration, processing and validation reports;
- metadata, lineage and raw-data archive.

Do not create every output merely because software can export it. Define products from the intended decision and acceptance requirements.

## 2. Scope and workflow boundaries

### Included
- Project requirements and survey-order selection.
- Horizontal and vertical reference decisions.
- Control, water-level and benchmark planning.
- MBES, GNSS/INS, motion, sound-speed and timing system inventory.
- Installation geometry, patch testing and verification.
- Main-line, cross-line, coverage and feature-search design.
- Raw-data preservation and acquisition metadata.
- Sound-speed, navigation, motion, offset and vertical-reference corrections.
- Sounding review, uncertainty, coverage and consistency assessment.
- Surface generation, independent checks and delivery.

### Excluded unless separately designed and authorised
- Vessel operations, navigation plans and maritime safety case.
- Instrument manufacture, sonar beamforming or proprietary vendor processing.
- Legal hydrographic certification or official chart compilation.
- Dredging, engineering design, construction or navigation-safety decisions.
- Automatic feature detection guarantees.
- A full CUBE or other uncertainty-aware surface estimator in the repository.
- A production-quality replacement for established hydrographic processing suites.

The repository's [layered-water-column acoustic ray tracer](../../algorithms/coastal/layered-water-column-acoustic-ray-tracing.md) and its [Python implementation](../../implementations/python/hydrographic-ray-tracing/README.md) are deliberately narrow teaching components. They do not perform the complete corrections described here.

## 3. Gate 0 — Define the requirement before choosing the survey

Prepare a project requirements record.

| Requirement | Must be resolved |
|---|---|
| Purpose | Navigation, dredging, engineering, habitat, research, change monitoring or another use |
| Area | Boundary, buffers, exclusions, water depth range and access |
| Survey classification | Applicable IHO S-44 order or another client/national specification, with rationale |
| Feature detection | Feature types and sizes that must be detected; coverage/search requirements |
| Bathymetric coverage | Required coverage percentage and treatment of gaps/uncertainty |
| Horizontal reference | CRS, datum/reference-frame realisation, coordinate epoch where relevant, units and transformation |
| Vertical reference | Chart/sounding datum, geoid or other vertical reference, benchmark ties and reduction method |
| Uncertainty | Horizontal and vertical uncertainty requirements, confidence convention and acceptance test |
| Resolution | Required grid cell size and minimum support/density |
| Time | Survey epoch, tidal/water-level conditions, repeat interval and change-detection needs |
| Deliverables | Soundings, grids, uncertainty, density, features, metadata, reports and raw archive |
| Constraints | Vessel, permissions, environment, weather, traffic, safety, data ownership and budget |
| Acceptance | Independent checks, reference source, sample design and predeclared pass/fail rules |

Do not infer the survey order from the equipment available. Do not select a grid size from display preference. Do not invent a universal overlap, line spacing, uncertainty tolerance or feature-detection threshold.

**Gate 0 exit:** requirements, governing specification, reference strategy, independent-check design and acceptance criteria are documented. Unresolved critical requirements stop the workflow.

## 4. Gate 1 — Establish horizontal and vertical reference

Record the full reference definition, not only an EPSG code or a label such as “MSL”.

### Horizontal reference
- CRS and authoritative definition;
- geodetic datum/reference-frame realisation;
- coordinate epoch where dynamic reference frames apply;
- coordinate units, axis order and sign conventions;
- transformation operation, grids, area of use and software/version;
- GNSS correction service/reference station and its frame;
- control coordinates, source, epoch and uncertainty.

### Vertical reference
- vertical datum or sounding/chart datum;
- benchmark identifiers, descriptions, coordinates/heights, source and uncertainty;
- observed water-level source, sensor, sampling interval, time standard and quality;
- water-level transfer/interpolation method and spatial applicability;
- ellipsoid-to-vertical-datum separation model and version if ellipsoidally referenced;
- geoid/quasigeoid model, tidal datum epoch and any required separation surfaces;
- sign convention, units and uncertainty.

Depth, ellipsoidal height, orthometric height, water level and chart datum are different quantities. Never subtract or combine them without a defined transformation and compatible epochs, signs and reference surfaces.

**Gate 1 exit:** an approved horizontal/vertical reference decision record and traceable control/water-level source register.

## 5. Gate 2 — Verify the measurement system

Build an installation and equipment register for:
- MBES model, serial number, firmware, frequency, sector and configuration;
- transducer reference point and mounting geometry;
- GNSS antenna(s), reference point, correction source and trajectory output;
- INS/MRU, heading source, timing and synchronisation;
- surface sound-speed sensor and SVP/CTD equipment;
- water-level sensor, tide gauge or ellipsoidally referenced method;
- acquisition/processing software and versions.

Measure and record lever arms between GNSS antenna, IMU and transducer reference points. Record axis conventions, mounting orientation, draft, immersion and any vessel-specific dynamic draft/squat model.

Verify or calibrate the system using the relevant manufacturer, project and hydrographic procedures. A patch test typically uses designed reciprocal/crossing lines and suitable seabed geometry to estimate residual latency, roll, pitch and heading offsets. Record the actual line design, conditions, estimated corrections, residuals, software and acceptance decision. Reassess after sensor movement, repair, impact or unexplained systematic mismatch.

Confirm:
- GNSS/INS initialisation and solution quality;
- heading, roll, pitch and heave availability and time alignment;
- timing/latency and lever-arm conventions;
- transducer draft and vessel configuration;
- sound-speed sensor checks and SVP procedure;
- raw data logging, storage, backup and event annotation.

**Gate 2 exit:** verified installation/configuration record, calibration/patch-test evidence and a documented decision that the system is fit to begin the planned acquisition. Do not treat a manufacturer's nominal specification as end-to-end project validation.

## 6. Gate 3 — Plan and acquire the survey

### 6.1 Design coverage and line geometry

Plan main lines, cross-lines, turns, tie-lines and any dedicated feature-search lines. Swath width depends on depth, sector angle, bottom slope, vessel attitude, sound-speed structure and outer-beam quality. Wider sectors may increase nominal coverage while degrading outer-beam uncertainty or increasing refraction sensitivity.

Design line spacing and overlap for the actual seabed, survey order, coverage and feature-detection requirement. Cross-lines should provide meaningful independent geometry and expose systematic differences; simply repeating a nearby line under the same conditions may not reveal common-mode bias.

Specify where and when to collect:
- sound-speed profiles through the water column;
- surface sound speed at the transducer;
- water-level observations and benchmark ties;
- control/reference observations;
- cross-lines and repeat lines;
- least-depth or feature investigations, where required.

### 6.2 Acquisition records

For every line/event preserve:
- stable line ID, project and survey area;
- UTC timestamp and time system;
- vessel, operator, sensor and configuration identifiers;
- raw sonar file references and checksums;
- GNSS/INS quality, position, heading, attitude and heave;
- sound-speed profile and surface sound-speed record references;
- water-level and vertical-reference record references;
- speed, draft/loading, environmental conditions and unusual events;
- line direction, intended role, actual coverage and gaps;
- rejected/repeated line reasons and operator notes.

Inspect raw beams and coverage during acquisition. Monitor GNSS/INS quality, motion, sound-speed conditions, noise, outer-beam artefacts, data gaps and cross-line consistency. Back up all raw observations and ancillary records before leaving the survey area.

**Gate 3 exit:** acquisition completeness check passed, raw files checksummed and backed up, and all known gaps/deviations recorded.

## 7. Gate 4 — Process observations into corrected soundings

Preserve immutable raw observations. All corrections should be traceable to a source record, configuration, model and software version.

A defensible processing chain usually includes:

1. Ingest raw sonar, navigation, attitude, sound-speed, water-level and event data; verify checksums and time systems.
2. Verify transducer installation, sensor reference points, lever arms, axis conventions and latency.
3. Apply sonar range/beam-angle calibration and appropriate sound-speed corrections.
4. Apply GNSS/INS trajectory, heading, roll, pitch, heave and time synchronisation.
5. Apply patch-test parameters, transducer draft and vessel squat/dynamic-draft corrections where supported.
6. Transform each observation into the project horizontal reference and apply the specified vertical-reference reduction.
7. Retain raw-to-corrected lineage, processing parameters and rejected sounding reasons.
8. Inspect swath overlap, cross-lines, outer-beam behaviour, refraction artefacts and systematic mismatches.

### 7.1 Acoustic ray tracing

For a horizontally stratified water column, Snell's law preserves horizontal slowness:

\[
p=\frac{\sin\theta_i}{c_i},
\qquad
\theta_i=\arcsin(p c_i)
\]

where \(c_i\) is sound speed and \(\theta_i\) is the ray angle from vertical in layer \(i\). In a constant-speed layer:

\[
\Delta x_i=\Delta z_i\tan\theta_i,
\qquad
\Delta t_i=\frac{\Delta z_i}{c_i\cos\theta_i}
\]

This relation explains why a depth-dependent sound-speed profile changes the beam path and horizontal footprint. The repository's implementation traces a two-dimensional forward ray through piecewise-constant layers for a supplied launch angle and half the two-way travel time.

**Do not mistake this component for complete MBES refraction correction.** It does not process raw beamforming, transducer-array geometry, full 3D vessel attitude, horizontal sound-speed gradients, surface sound-speed mismatch, bottom detection, vendor-specific beam angles or uncertainty. Use the acquisition/processing system's validated hydrographic workflow for operational corrections; use this implementation for learning and bounded numerical experiments.

### 7.2 Vertical reduction

Keep the vertical reduction explicit. A simplified sign convention may express seabed elevation relative to a datum as:

\[
H_b=H_T-D_v
\]

where \(H_T\) is the transducer reference-point elevation in the same vertical datum and \(D_v\) is the corrected vertical component from that reference point down to the seabed. This is only a bookkeeping identity: the full computation must correctly transform GNSS antenna height, IMU/transducer lever arms, attitude, heave, draft, acoustic geometry and the vertical reference. If the project instead stores positive-down depths, document the exact origin and sign convention.

Never apply an assumed tide correction to ellipsoidally referenced bathymetry, or mix tide-reduced depths with ellipsoidal heights, without a defined and validated transformation.

**Gate 4 exit:** corrected sounding dataset has complete processing lineage, declared horizontal/vertical references and no unexplained systematic artefacts. Failed or uncertain corrections are flagged, not hidden.

## 8. Gate 5 — Sounding review, uncertainty and quality assessment

Review soundings before gridding. Preserve rejected observations and rejection reasons; do not silently edit or delete data to improve visual appearance.

Assess separately:
- absolute horizontal and vertical positioning uncertainty;
- cross-line and overlapping-swath consistency;
- sound-speed profile adequacy and refraction artefacts;
- coverage, gaps and density;
- feature search/detection evidence;
- water-level/datum adequacy;
- outliers, noise and rejected sounding rates;
- independent check observations and their uncertainty.

Build a total propagated uncertainty (TPU) model from relevant components: acoustic range, sound speed/refraction, beam angle, GNSS position, heading, roll/pitch, heave, timing, lever arms, draft, squat, water level/datum and processing. Some contributions may be correlated. A covariance-aware propagation is preferable where correlations materially affect the result; do not blindly sum standard deviations or assume independence.

For IHO S-44 the depth-dependent maximum allowable TVU is represented by:

\[
TVU_{max}(d)=\sqrt{a^2+(b\,d)^2}
\]

where \(d\) is depth and \(a,b\) are parameters for the selected survey order. The formula is an acceptance envelope, **not an uncertainty estimator**. Use the applicable adopted standard and project instructions for coefficients, confidence conventions, coverage and feature-detection requirements.

Cross-line agreement is a useful relative consistency check but does not prove absolute accuracy: all lines may share a common datum, calibration or trajectory bias. Low scatter also does not prove complete feature search.

**Gate 5 exit:** documented sounding review, uncertainty evidence, cross-line/overlap analysis, coverage report and independent checks satisfy the predeclared requirements—or the area/line is explicitly marked conditional, rejected or requiring reacquisition.

## 9. Gate 6 — Generate the bathymetric surface

Choose the gridding method and cell size from the intended use, survey order, sounding density, footprint, spatial correlation, seabed morphology and uncertainty. The cell size must not imply more spatial detail than the observations support.

Before gridding, record:
- input sounding version and accepted/rejected status;
- horizontal/vertical reference and units;
- grid origin, extent, cell size and alignment;
- interpolation/estimation method and parameters;
- handling of multiple soundings per cell, outliers and data voids;
- minimum support/count or other evidence needed to populate a cell;
- uncertainty propagation or estimation method;
- treatment of edges, steep slopes, features and mixed seabed;
- software/version and processing timestamp.

The existing [multibeam sounding gridding reference implementation](../../implementations/python/coastal-processes/README.md) provides simple per-cell mean/median aggregation and sounding counts. It is a transparent baseline for demonstrating binning. It is **not** a CUBE implementation, not a full uncertainty-aware estimator, and not a substitute for hydrographic surface generation or feature-preserving modelling. Do not use it for operational acceptance without a separately specified and validated method.

Deliver the bathymetric surface with separate coverage/density and uncertainty layers where defensible. Keep source soundings and cell lineage. A cell with no observations is a void, not a zero depth. Do not fill gaps with unconstrained interpolation and then report them as measured coverage.

**Gate 6 exit:** surface method, support, resolution, void policy, uncertainty and lineage are documented; the surface does not overstate observed coverage or detail.

## 10. Gate 7 — Independent validation and acceptance

Use checks that were not used to calibrate, adjust or tune the same data wherever possible. The validation design must be established before processing.

Potential checks include:
- independent reference soundings from a suitable and documented method;
- independently observed control and benchmark ties;
- cross-lines designed to test systematic differences;
- repeat lines acquired under changed geometry or conditions;
- known features or surfaces with appropriate reference uncertainty;
- independent review of processing, datum and feature-search evidence.

For every check, report its source, time, reference frame/datum, uncertainty, method, sample distribution and independence limitations. A check dataset with uncertainty comparable to or larger than the required tolerance may not support the desired acceptance claim.

Compare the measured differences with the correct acceptance statistic and confidence convention. Report bias, spread, spatial pattern and outliers, not only one aggregate RMSE. Distinguish:
- internal consistency;
- relative accuracy;
- absolute accuracy;
- coverage/completeness;
- feature-detection performance;
- fitness for the stated purpose.

If a gate fails, identify the cause, correct the relevant processing/acquisition issue and repeat the affected checks. Do not change acceptance criteria after seeing the result.

**Gate 7 exit:** signed quality/acceptance record with pass, conditional pass or fail for each requirement. Any limitation must travel with the delivered dataset.

## 11. Gate 8 — Package and deliver

The delivery package should include, as required:
- raw sonar, GNSS/INS, attitude, sound-speed and water-level records;
- checksums, immutable archive and data inventory;
- vessel/sensor register, installation diagram, lever arms, draft and calibration/patch-test records;
- control, benchmark and reference-system records;
- accepted corrected soundings and rejected-data log;
- bathymetric grid, uncertainty, density and coverage layers;
- feature records and search evidence where required;
- processing software/version, parameters, logs and lineage;
- independent check data, statistics and acceptance report;
- metadata, licence, ownership, restrictions and delivery formats.

Keep raw, corrected, cleaned, reduced and gridded data distinguishable. A final raster alone is not a reproducible hydrographic deliverable.

## 12. Failure modes and response

| Failure mode | Observable symptom | Required response |
|---|---|---|
| Incorrect sound-speed profile | Refraction artefacts, systematic outer-beam disagreement | Review profile timing/location/depth, surface sound speed and ray-tracing assumptions; reacquire or reprocess |
| Patch-test or latency error | Direction-dependent or line-dependent offsets | Recheck line design, timing and sensor alignment; repeat calibration/affected lines |
| GNSS/INS degradation | Position jumps, attitude gaps, inconsistent swath placement | Flag affected epochs/lines, inspect trajectory and correction status, reacquire if necessary |
| Wrong lever arm or axis convention | Consistent position/depth bias, attitude-dependent displacement | Verify physical measurement, sign and frame conventions; reprocess and independently check |
| Vertical datum mismatch | Uniform or spatially varying depth offset | Stop delivery; verify datum, benchmark ties, time series and separation model |
| Poor coverage or outer-beam quality | Gaps, weak overlap, unstable outer beams | Adjust line spacing/sector/speed and reacquire; do not mask missing coverage |
| Over-cleaning | Loss of genuine seabed features | Review raw data and rejection rules; preserve audit trail and independent review |
| Unsupported gridding | Smoothed features, false detail or filled voids | Revisit method, cell support and void policy; use a validated estimator appropriate to the requirement |
| Common-mode bias | Cross-lines agree but independent checks fail | Investigate shared datum, calibration, trajectory and control sources |

## 13. Physical-world applications

The workflow can support port and harbour surveys, dredging quantities, navigation products, coastal engineering, river/reservoir bathymetry, offshore infrastructure, marine habitat mapping, sediment studies and repeat seabed-change monitoring. Each application has different requirements for coverage, feature detection, vertical reference, uncertainty, spatial resolution and temporal comparability.

The same recipe should not be applied unchanged to shallow vegetated water, turbid estuaries, deep ocean, steep rocky seabed and inland reservoirs. Sensor selection, vessel/platform, acoustic frequency, feature search and reference strategy must be adapted to the physical environment and intended decision.

## 14. Standards and technical references

- [IHO S-44 — Standards for Hydrographic Surveys](https://iho.int/en/standards-and-specifications). The IHO standards page lists Edition 6.2.0 (October 2024) as the published edition. A later 6.3.0 document surfaced as a draft/estimate; verify the publication register before treating it as adopted.
- [NOAA Hydrographic Surveys Specifications and Deliverables](https://nauticalcharts.noaa.gov/publications/standards-and-requirements.html). A detailed national implementation and useful technical exemplar, not a Kenyan specification.
- [NOAA hydrographic surveying overview](https://oceanservice.noaa.gov/navigation/hydro/). Explains multibeam depth measurement and hydrographic purpose.
- [IHO Manual on Hydrography (C-13)](https://iho.int/en/capacity-building-publications). Background on positioning, depth determination, water levels and hydrographic practice.

For Kenya, confirm current national hydrographic authority requirements, maritime permissions, control and vertical reference sources, data ownership and applicable professional obligations before operational work. This repository method is an educational synthesis, not a permit or certification.

## 15. Evidence state and next technical gaps

**Current evidence:** desk-designed recipe; a bounded piecewise-constant acoustic ray tracer with synthetic unit tests; a simple sounding-bin gridding baseline. No actual sonar data have been processed, no patch test has been performed, no vertical datum has been realised and no independent bathymetric validation has been conducted.

**Next technical gaps:**
1. Water-column acoustics and hydrographic vertical-reference foundations.
2. A documented covariance-aware hydrographic TPU model with explicit component inputs and correlation assumptions.
3. A validated sounding-to-grid estimator with support, uncertainty and coverage semantics.
4. A synthetic end-to-end hydrographic fixture that tests lineage, datum bookkeeping, coverage and failure gates without pretending to be field data.
5. A real dataset only after its licence, provenance, reference, processing history and independent checks are established.

Do not close these gaps with a visually plausible raster or unverified public dataset.

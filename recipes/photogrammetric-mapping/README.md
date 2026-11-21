# Photogrammetric mapping: project-to-validated-deliverable recipe

**Recipe ID:** SM-REC-007  
**Connected subjects:** SM-COL-007, SM-COL-004, SM-COL-009, SM-FND-011  
**Status:** Desk-designed workflow; EXIF-only public-dataset baseline executed; field validation and independent specialist review pending  
**Audience:** Intermediate learners, researchers and practitioners planning a bounded photogrammetric mapping project

> This recipe describes a defensible workflow structure, not an approved flight plan, survey specification, safety case, regulatory authorisation or guarantee of accuracy. An EXIF-only baseline has been run on the public HEIG-VD dataset, but this is not a field campaign or accuracy assessment. Project requirements, competent personnel, jurisdictional rules and professional responsibilities take precedence.

> **Implementation note:** The repository has completed an EXIF-only ODM baseline on the public HEIG-VD dataset and structurally inspected its orthophoto, DSM and LAZ. This demonstrates the processing chain on one dataset only; it is not a field campaign, GCP-controlled run or positional-accuracy assessment.

## 1. Purpose and outcome

Turn a defined mapping requirement into an acquired, processed, independently assessed and documented photogrammetric dataset.

The recipe connects the four Spatial Methods pillars:

- **Theoretical Foundations:** perspective geometry, measurement science, uncertainty, camera models and coordinate reference systems.
- **Spatial Data Collection:** camera/platform selection, reconnaissance, control, image acquisition and field records.
- **Spatial Algorithms:** image matching, bundle adjustment, dense reconstruction, surface modelling and orthorectification.
- **Spatial Recipes:** the project decisions, handoffs, quality gates and evidence trail that make the work reproducible.

Typical outputs may include an orthomosaic, point cloud, digital surface model (DSM), digital terrain model (DTM), mesh, extracted features or a combination. Not every project needs every output. Define the product from its intended use, not from what a software package can export.

## 2. Start with a requirements contract

Do not begin by choosing a drone, camera, overlap percentage or software. First record:

| Requirement | Questions to resolve |
|---|---|
| Purpose | What decision, analysis or operation will use the data? |
| Area and coverage | What boundary, buffer, exclusions and completeness are required? |
| Feature and surface | What must be visible or measurable? Ground, canopy, roof, façade, corridor, stockpile or other? |
| Deliverables | Orthomosaic, DSM, DTM, point cloud, mesh, vector features, report or archive? |
| Spatial quality | What horizontal/vertical accuracy, resolution, completeness or feature-detection performance is actually required? |
| Reference | Which horizontal CRS, reference-frame realisation/epoch where relevant, vertical datum, units and height type? |
| Time | Single epoch, repeat monitoring, change detection or time-critical delivery? |
| Radiometry | Are calibrated reflectance, colour consistency or only visual appearance required? |
| Constraints | Access, permissions, airspace, privacy, environment, weather, security, budget and schedule? |
| Acceptance | Which independent observations and measurable criteria will determine acceptance? |

Record unresolved requirements as unresolved. Do not invent tolerances or infer accuracy from GSD. If the client cannot define the intended use or acceptance need, pause and resolve the specification before acquisition.

**Gate 1 — Requirements approved:** scope, deliverables, coordinate/vertical reference, quality criteria, constraints and validation plan are documented.

## 3. Reconnaissance and feasibility

### 3.1 Desk reconnaissance

Review current imagery, terrain information, site boundaries, access routes, known hazards, surface types, vegetation, buildings, power lines, restricted areas and likely occlusions. Identify whether the task is aerial, terrestrial, close-range or multi-platform; do not force an aerial workflow onto a façade or obstructed site.

### 3.2 Site reconnaissance

Where safe and authorised, inspect the site and record:

- actual boundary, access and take-off/landing or camera-station options;
- terrain relief, slope breaks, structures, vegetation and occlusion;
- surfaces likely to be texture-poor, reflective, transparent, repetitive or moving;
- target visibility, placement options and control/check-point access;
- changing shadows, sun direction, wind exposure and likely illumination windows;
- people, traffic, wildlife, sensitive locations and privacy risks;
- emergency arrangements, communications and operational exclusions.

A desk review is not a substitute for an on-site risk assessment where one is required.

### 3.3 Legal, safety and operational review

Identify the current requirements for the actual country, platform, operation, airspace, site and intended data collection. For Kenya, verify current requirements with the relevant authorities and competent local professionals before any UAS activity; do not assume a generic internet checklist or this document establishes permission. Confirm landowner/site consent, insurance, operator competency, privacy/data-protection obligations, environmental restrictions and emergency procedures as applicable.

**Gate 2 — Feasibility approved:** the selected method can observe the target, the site can be accessed lawfully and safely, and constraints have owners and controls. If not, redesign, use another sensor/method or stop.

## 4. Select the sensor and observation geometry

Choose the platform and camera from required coverage, object scale, accuracy, surface, access, environment and available expertise.

Document camera make/model, sensor dimensions, pixel pitch if known, focal length, lens, focus, shutter type, calibration information, image format, geotagging/trajectory source and synchronisation assumptions. Record platform and navigation system details where relevant.

### 4.1 Plan image scale and coverage

For a near-nadir pinhole camera over locally planar ground:

`GSD = H p / f`

where H is height above local ground, p is physical pixel pitch and f is focal length, in consistent units.

For sensor width W and height L:

`F_W ≈ H W / f` and `F_L ≈ H L / f`

For forward and side overlap fractions o_f and o_s, idealised image-centre spacing is:

`d_f ≈ F_L(1 - o_f)` and `d_s ≈ F_W(1 - o_s)`

Use the [flight-design calculation companion](../../implementations/python/photogrammetric-flight-design/README.md) for the bounded GSD, footprint and spacing calculations.

These approximations do not account for terrain relief, variable height above ground, camera tilt, distortion, rolling-shutter effects, aircraft dynamics, turns, boundary margins, wind, regulatory limits or complete coverage geometry. They are not a mission planner.

### 4.2 Design for geometry, not a magic overlap number

Choose forward/side overlap and image spacing appropriate to the sensor, terrain, texture, speed, object and processing method. Consider cross-strips, oblique/convergent images, multiple heights or ground-based views when they address a known weakness such as calibration stability, vertical geometry, façades or occlusion. Additional images cost time and processing; justify them.

No single overlap percentage or GCP count is universally correct. Treat published values as context-dependent starting points, then design for the actual requirements and validation strategy.

### 4.3 Plan control and independent checks

Separate three roles:

- **Tie points:** matched image observations used to connect images and support reconstruction.
- **Ground control points:** surveyed object-space coordinates used to constrain georeferencing/adjustment.
- **Check points:** independent reference observations withheld from adjustment and used to assess the result.

Design control and check-point locations to represent the spatial extent and relevant elevation range. Avoid clustering all control in one area. Ensure points are identifiable in sufficient images, accessible, stable and measured in the required reference system. Record survey method, instrument, observation procedure, uncertainty, units, datum, epoch where relevant and point descriptions.

The number, distribution and quality of points must follow project needs and applicable standards; do not copy a numerical recommendation without checking its scope. If independent checks cannot be collected, state that the output lacks that form of external positional validation.

**Gate 3 — Acquisition design approved:** sensor, geometry, coverage, control/check design, expected data volume, logistics and risk controls are reviewed.

## 5. Prepare the field campaign

Before mobilisation:

1. Freeze the approved project specification and version it.
2. Confirm platform, camera, firmware/software versions and equipment condition.
3. Confirm storage capacity, batteries/power, communications and backup media.
4. Check calibration status, focus, lens cleanliness, time synchronisation and image naming.
5. Prepare flight/camera plan, site maps, control descriptions and field forms.
6. Verify control/check-point coordinates and reference information.
7. Confirm permissions, weather criteria, emergency procedures and team roles.
8. Define stop-work triggers and who can authorise a restart.
9. Prepare a data manifest and file/folder naming convention.
10. Conduct a team briefing and record go/no-go decision.

A plan is not authority to operate. The responsible operator must independently confirm current permissions, conditions and safety controls.

## 6. Acquire imagery and field evidence

Follow the approved plan while adapting to actual conditions through documented decisions.

### During capture

- Monitor actual height above ground, speed, camera attitude and image interval where available.
- Check exposure, focus, blur, image completeness and overlap indicators.
- Watch for changing illumination, wind, moving objects, occlusion and unexpected terrain.
- Confirm that control targets are visible and not displaced or obscured.
- Record interruptions, deviations, equipment changes, weather and operator decisions.
- Record image/flight identifiers associated with control and check observations.

Do not continue blindly when quality indicators fail. Pause, diagnose, re-fly or document a justified limitation.

### Field close-out

Before leaving the site, check coverage and file counts, inspect representative images, confirm control/check observations are complete, verify logs and metadata, and make at least two verified copies where the project data policy requires it. Do not erase or overwrite original media until copies have been verified.

**Gate 4 — Field data accepted for ingest:** raw imagery, logs, control records and metadata are present; gaps and exceptions are documented; backups are verified.

## 7. Ingest, preserve and prepare data

Create an immutable raw-data area and a separate working area. A practical structure is:

```text
project/
  00_admin/          # brief, permissions, risk and decisions
  01_raw/
    imagery/
    trajectory/
    control/
    field_logs/
  02_working/
    image_qc/
    alignment/
    reconstruction/
  03_quality/
    checkpoints/
    reports/
  04_deliverables/
  05_metadata/
  06_archive/
```

Adapt the structure to the organisation's data policy. Never treat this example as a universal archival standard.

At ingest:

- generate file inventory and checksums for transferred files;
- compare source and copied file counts and sizes;
- preserve original filenames and timestamps;
- preserve original image files and navigation/trajectory logs;
- record camera, platform, acquisition date/time and time zone;
- record coordinate reference, vertical reference, units and transformations;
- record control/check files, survey method and uncertainty;
- document missing/corrupt files, exclusions and manual edits;
- capture software, version, settings and processing environment.

Do not silently rewrite original EXIF metadata or coordinate values. Store corrected or interpreted values as derived records with a traceable transformation.

## 8. Process with explicit checkpoints

The following is a conceptual handoff, not software-specific instructions. Different packages use different names, algorithms and parameter conventions.

1. **Image inspection:** reject or flag unusable images using documented criteria; retain a rejection log.
2. **Image alignment:** estimate image correspondences and camera poses; inspect alignment completeness, camera calibration behaviour and tie-point distribution.
3. **Control integration:** import control with correct CRS, units and uncertainty; verify point identification and weighting assumptions.
4. **Bundle adjustment:** refine camera parameters and object geometry; inspect residuals, parameter plausibility, network geometry and stability.
5. **Dense reconstruction:** generate point cloud or depth products only where required; inspect noise, holes, vegetation/surface interpretation and edge effects.
6. **Surface/model generation:** derive DSM, DTM, mesh or other products according to the actual target surface and classification method.
7. **Orthorectification and mosaicking:** use a suitable elevation surface; inspect seamlines, building lean, occlusion, relief displacement and radiometric inconsistencies.
8. **Export:** use documented formats, CRS, units, pixel size, vertical reference and NoData conventions.

Keep processing settings and intermediate reports. Do not optimise solely for a visually attractive output or low control residuals.

## 9. Quality assessment and independent validation

Evaluate quality against the requirements approved at Gate 1.

### 9.1 Internal diagnostics

Review image alignment completeness, tie-point distribution, reprojection residuals, camera calibration plausibility, bundle-adjustment behaviour, point-cloud density/coverage, surface artefacts, mosaic seams and processing warnings. These diagnose the model and workflow; they are not a substitute for independent accuracy checks.

### 9.2 Independent positional checks

Use check points that were not used in control, calibration tuning or model fitting. Confirm their survey quality and reference compatibility. Compare model-derived coordinates with independently observed coordinates using the project's specified statistics and reporting convention.

Report components separately where relevant (for example, east, north and up), sample size, bias, RMSE or other required statistics, outliers and exclusions, spatial distribution, reference uncertainty and the applicable acceptance test. Do not hide systematic bias inside a single aggregate statistic. Do not claim a standard's compliance unless its sampling design, minimum sample, confidence treatment and reporting rules were followed.

Where checkpoints are sparse or unevenly distributed, describe the limitation. A good checkpoint statistic over one small sub-area does not prove uniform quality over the full block.

### 9.3 Product-specific checks

- **Orthomosaic:** gaps, blur, seams, duplicated/missing features, building displacement and radiometric inconsistency.
- **DSM/DTM:** surface definition, vegetation/building inclusion, holes, interpolation, edge artefacts and vertical checks.
- **Point cloud:** density, completeness, noise, outliers, classification and surface representation.
- **Mesh:** holes, texture artefacts, scale, georeferencing and object completeness.
- **Extracted features:** positional checks, attribute completeness, topology and semantic correctness.

**Gate 5 — Quality decision:** accept, conditionally accept, reprocess, reacquire or reject against pre-agreed criteria. Record who made the decision and the evidence used.

## 10. Package and deliver

A defensible handover normally contains:

- agreed data products in specified formats;
- project boundary and coverage footprint;
- coordinate/vertical reference and units;
- metadata and acquisition summary;
- processing method, software/version and material parameters;
- control/check-point descriptions and validation results;
- quality report, limitations and exclusions;
- provenance, file inventory and checksums;
- readme explaining folder structure, intended use and known issues;
- source/licence and access conditions where relevant.

Make clear whether the product is a visual reference, analytical dataset, engineering input or survey deliverable. Do not imply fitness for a use that was not specified and tested.

## 11. Failure handling and decision rules

| Condition | Response |
|---|---|
| Requirements or CRS unresolved | Stop design; resolve before acquisition |
| Access, permission or safety issue | Do not proceed until resolved by responsible parties |
| Insufficient coverage or severe blur | Reacquire affected coverage if feasible; otherwise document exclusion and assess whether scope can be met |
| Weak tie-point geometry or unstable calibration | Diagnose geometry, camera model and scene; redesign/reprocess or reacquire |
| Control/check mismatch or suspect reference | Quarantine affected points; verify survey, datum, units and transformations before adjustment |
| Independent checks fail | Investigate bias, control, calibration, geometry and processing; reprocess or reacquire, then revalidate |
| No independent checks available | State validation limitation; do not make unsupported accuracy claims |
| Surface does not represent target | Correct classification/measurement approach or change deliverable specification |

## 12. Reproducibility and project records

Use the companion [project record and QA checklist](project-record-template.md) to record the project specification, acquisition, processing, quality decision and handover. Preserve a versioned copy for every project. A completed checklist is evidence of recorded decisions, not proof that the work is technically correct.

## 13. Processing implementation

The [OpenDroneMap processing and checkpoint QA companion](../../implementations/python/photogrammetry-odm/README.md) provides a reproducible Docker invocation pattern and a separate checkpoint-statistics utility. It is an implementation companion, not a claim that this recipe has been executed on imagery. Keep the processing image version pinned and record its digest, arguments, environment and output inventory. The checkpoint tool requires independent reference/model coordinate pairs in a common coordinate and vertical reference; it does not transform coordinates or certify standards compliance.

## 14. References and connected material

- Sampath, A., Shrestha, M., While, M. and Scholl, V. M. (2023). *Guidelines for Calibration of Uncrewed Aircraft Systems Imagery*. USGS Open-File Report 2023–1033. [Official report](https://pubs.usgs.gov/publication/ofr20231033/full). UAS-specific guidance on acquisition, calibration, control, tie points and QA; interpret within its stated context.
- [Photogrammetric image acquisition: geometry, control and quality assurance](../../collection/photogrammetry/image-acquisition.md) — acquisition theory and planning.
- [Photogrammetric image-acquisition exercise](../../collection/photogrammetry/image-acquisition-exercise.md) — worked educational exercise.
- [Photogrammetric flight-design calculations](../../implementations/python/photogrammetric-flight-design/README.md) — bounded planning calculations.
- [Measurement principles and field verification](../../foundations/measurement-science/measurement-principles-and-field-verification.md) — measurement quality and independent verification.
- [Survey-to-spatial-dataset workflow](../survey-to-spatial-dataset/README.md) — broader sensor-neutral field-to-dataset workflow. This photogrammetry recipe is a specialised branch, not a replacement.

## 15. Evidence and review status

This recipe is a desk-designed workflow assembled from the cited technical material and the repository's existing measurement and acquisition content. It has not been executed as a field campaign, tested against a real client specification, independently reviewed by a photogrammetry specialist or validated for a particular jurisdiction. The USGS source is authoritative for its stated UAS programme but does not establish Kenyan regulatory requirements or universal operating parameters.

Before operational use, have the project-specific design reviewed by appropriately competent photogrammetry, surveying, aviation/safety and data-governance professionals as applicable.

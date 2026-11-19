# Survey-to-spatial-dataset workflow

**Status:** Design brief and workflow skeleton; no field campaign has been conducted.  
**Recipe pillar:** Spatial Recipes  
**Connected pillars:** Theoretical Foundations, Spatial Data Collection and Spatial Algorithms  
**Related cluster:** [Reference, positioning and measurement](../../catalog/first-curation-cluster-reference-positioning-measurement.md)  
**Source map:** [Surveying and field measurement](../../catalog/surveying-field-measurement-source-map.md)  
**Foundational synthesis:** [Measurement principles and field verification](../../foundations/measurement-science/measurement-principles-and-field-verification.md)

> This is a learning and capability-development workflow, not a cadastral survey specification, construction set-out procedure, legal boundary determination or substitute for qualified professional judgement. A real project must establish its jurisdictional, contractual, safety and professional requirements before work begins.

## 1. Purpose

Demonstrate how a defined real-world spatial information requirement becomes a documented, quality-assessed and reusable spatial dataset.

The workflow deliberately connects the entire chain:

**problem → measurement design → reference → acquisition → processing → independent checks → spatial dataset → delivery**

It is intended to become a practical capstone for Spatial Methods. The first implementation should use a small, bounded, non-cadastral topographic or asset-mapping task, selected only after access, equipment, permissions, intended use and validation options are understood.

The workflow is technology-aware rather than technology-led. GNSS, total stations, levelling, tape/laser measurement, photogrammetry, terrestrial/mobile LiDAR and other sensors are alternatives for different measurands and environments. No single technology is assumed to be suitable for every feature or accuracy requirement.

## 2. Intended outcome

Produce a spatial dataset whose user can understand:

- what features or phenomena were captured and why;
- how their positions and attributes were observed or derived;
- which reference system, coordinate epoch and units apply;
- what instruments, sensors, procedures and processing were used;
- what quality checks were performed and what they establish;
- what uncertainty, limitations and omissions remain;
- whether the dataset is fit for its stated purpose.

The deliverable is not just a map. It is a dataset plus enough evidence and provenance for another competent person to inspect and responsibly reuse it.

## 3. Scope boundaries

### Included in the teaching workflow

- A bounded, permissioned study area.
- A defined feature inventory and data dictionary.
- Selection of a suitable positioning/measurement approach.
- A measurement and acquisition plan.
- Instrument/system checks appropriate to the chosen method.
- Preservation of raw observations and field metadata.
- Coordinate processing and any necessary adjustment.
- Independent checks and documented quality assessment.
- A structured spatial dataset and delivery note.

### Excluded unless separately specified and professionally authorised

- Cadastral boundary definition, subdivision or re-establishment.
- Legal or statutory survey plans and submissions.
- Construction set-out or safety-critical engineering acceptance.
- Utility locating where specialist detection and permissions are required.
- Claims of regulatory compliance or survey accuracy without the applicable specification and evidence.
- Unpermitted access, intrusive work, drone operations or collection of sensitive personal information.

The Kenyan legal and professional context must be checked for the actual activity. The [Surveying and field measurement source map](../../catalog/surveying-field-measurement-source-map.md) identifies the Land Surveyors' Board, Survey Act and Survey Regulations as source routes; their current applicability and exact requirements must be reviewed before a field protocol is approved.

## 4. Workflow

### Stage 0 — Define the problem and acceptance need

Write a short project brief before choosing equipment.

Record:

- decision or activity the dataset will support;
- study boundary and intended scale;
- feature classes and attributes required;
- intended users and delivery format;
- positional, thematic, completeness and temporal quality needs;
- required confidence or acceptance criteria, where specified;
- exclusions, access constraints, privacy concerns and safety risks.

Do not invent a universal positional tolerance. Derive acceptance requirements from the intended use, governing specification and consequences of error. If requirements are unknown, mark them unresolved rather than silently selecting a convenient instrument.

**Output:** approved scope statement, feature list, draft data dictionary and acceptance plan.

### Stage 1 — Establish the spatial reference

Determine the appropriate horizontal and vertical reference information.

Record, where applicable:

- coordinate reference system and authoritative definition;
- datum/reference-frame realisation and coordinate epoch;
- vertical datum or height system;
- geoid/quasigeoid model and version if used;
- transformation operation, grids, area of use and software/version;
- source and uncertainty of control coordinates;
- units, axis order and coordinate conventions.

Do not assume that a CRS label alone fully describes the reference used. For Kenya, consult current authoritative national sources and institutional guidance; do not treat a general GIS CRS selection as a substitute for official national transformation or control information.

**Output:** reference-system decision record and control-source register.

### Stage 2 — Choose the observation and acquisition method

Select the method from the measurand, site conditions, required quality, feature type, access, availability and cost.

| Method family | Potential role | Questions to resolve |
|---|---|---|
| GNSS positioning | Open-sky point positioning and control ties | Sky visibility, correction service, reference frame, multipath, occupation and independent checks |
| Total station | Relative positioning, detail and constrained environments | Line of sight, control geometry, setup/centring, prism/reflectorless mode and field verification |
| Levelling | Height differences and vertical control | Required height quality, route design, staff/instrument checks, refraction and closure |
| Tape or laser distance | Short local dimensions and offsets | Range, surface, alignment, instrument specification and repeatability |
| Photogrammetry | Image-derived geometry and surface/feature products | Image geometry, control/check distribution, camera calibration, texture and occlusion |
| Terrestrial/mobile LiDAR | Dense 3D geometry and asset/scene capture | Registration, trajectory/control, reflectance, occlusion, point density and independent checks |
| Other sensors or sampling systems | Thematic/environmental observations | Measurand, calibration, sampling design, spatial support, temporal behaviour and metadata |

Methods may be combined. A sensor's nominal precision or marketing specification is not proof that the complete project workflow meets its requirement.

**Output:** method-selection rationale, equipment/access list and unresolved assumptions.

### Stage 3 — Design control, sampling and independent checks

Design the geometry and checks before acquisition.

Specify:

- control points or reference observations and their provenance;
- observation geometry and redundancy;
- number and distribution of observations;
- repeat measurements and changed setups where useful;
- independent check points or observations withheld from adjustment;
- expected uncertainty contributors and covariance assumptions;
- field verification procedures and acceptance criteria;
- what happens if checks fail.

Redundancy is not automatically independence. Repeating the same setup may reproduce the same bias. Design checks that can expose relevant failure modes.

**Output:** measurement plan, check design and predeclared acceptance rules.

### Stage 4 — Prepare and verify acquisition systems

For each instrument or sensor, identify:

- make/model, serial or asset identifier and firmware/software;
- configuration, reference settings and relevant correction models;
- calibration certificates or other available traceability records;
- field verification procedure and its scope;
- operator competence and setup procedure;
- environmental and site conditions affecting performance;
- limitations, known faults and maintenance status.

A field repeatability test is not automatically a calibration or proof of end-to-end dataset accuracy. Use the appropriate standard or professional procedure for the specific instrument and project.

**Output:** equipment register and completed pre-use verification record, or an explicit statement that verification remains outstanding.

### Stage 5 — Acquire and preserve observations

Capture raw observations before transformation or adjustment. Do not replace original records with cleaned or edited values.

For each observation or feature, preserve relevant fields such as:

- stable point/feature ID;
- raw measurement or sensor record reference;
- date/time and time zone;
- operator and instrument/sensor identifier;
- setup, antenna/prism/staff height and configuration;
- method, observation mode and relevant settings;
- environmental/site conditions;
- reference/control used;
- field codes, attributes, photographs or supporting records;
- notes, anomalies, rejected observations and reasons.

Use a consistent naming and backup procedure. Record missing, obstructed, inaccessible or unobserved features rather than implying complete coverage.

**Output:** immutable raw-data package, field log and acquisition metadata.

### Stage 6 — Process, transform and estimate

Apply the processing appropriate to the selected method.

Possible operations include:

- unit, instrument and environmental corrections;
- coordinate conversion and reference-frame operations;
- GNSS baseline or position processing;
- traverse, levelling or network adjustment;
- photogrammetric bundle adjustment and reconstruction;
- point-cloud registration and classification;
- geometry construction and feature attribution.

Record software, versions, parameters, input files, processing order and rejected data. Retain intermediate outputs where they are necessary to reproduce the result.

Evaluate the functional and stochastic models. Do not treat small residuals as proof that the reference, observations or model are correct.

**Output:** processed observations, estimated coordinates/geometries, adjustment or processing report and reproducibility record.

### Stage 7 — Independent quality assessment

Compare the result with checks that were not used to fit or tune it, where the project design allows.

Assess relevant dimensions separately:

- positional quality;
- attribute/thematic correctness;
- completeness;
- logical consistency and topology;
- temporal currency;
- metadata and provenance;
- fitness for the intended use.

Report the check sample, reference source and uncertainty, test method, statistics, acceptance criteria, failures and limitations. Distinguish internal precision from external accuracy and independent validation.

If acceptance criteria are not met, investigate the cause, document corrective action and repeat appropriate checks. Do not silently delete inconvenient observations or change thresholds after seeing the results.

**Output:** quality report and explicit pass/fail/conditional-use decision against the stated requirements.

### Stage 8 — Build and deliver the spatial dataset

Create a documented dataset with:

- geometry and feature schema;
- stable identifiers;
- attribute definitions, domains and units;
- CRS and reference metadata;
- acquisition date and temporal meaning;
- source and processing lineage;
- quality/uncertainty information at an appropriate level;
- known omissions, limitations and restrictions;
- software and format versions;
- reuse and data-rights statement.

Select an interoperable format suitable for the intended users and data structure. GeoPackage may be considered for a portable vector delivery, but format selection must follow the project requirements rather than habit.

**Output:** spatial dataset, metadata, quality report, processing record and concise handover note.

## 5. Cross-pillar knowledge map

| Workflow component | Primary pillar | Supporting subjects |
|---|---|---|
| Measurand, reference and uncertainty | Theoretical Foundations | Geodesy, metrology, statistics, adjustment theory |
| Instrument/sensor and field procedure | Spatial Data Collection | Surveying, GNSS, levelling, photogrammetry, LiDAR, sampling |
| Corrections, transformations and estimation | Spatial Algorithms | Coordinate operations, least squares, covariance propagation, quality tests |
| End-to-end delivery | Spatial Recipes | Planning, acquisition, processing, validation, data engineering and provenance |

Relevant subject IDs include SM-FND-008, SM-FND-011, SM-ALG-004, SM-ALG-018, SM-COL-001, SM-COL-002, SM-COL-003, SM-REC-003, SM-REC-008, SM-REC-017, SM-INF-005, SM-INF-009 and SM-INF-011. See the [master subject index](../../catalog/master-subject-index.md) for canonical scope and relationships.

## 6. Evidence and release gates

The capstone must progress through explicit evidence states. Do not describe a planned activity as completed.

| Gate | Evidence required | Permitted claim |
|---|---|---|
| G0 — Desk design | Scope, source review, method rationale, risks, access and validation plan | Designed workflow |
| G1 — Synthetic demonstration | Clearly labelled synthetic observations and reproducible calculations | Demonstrated computational logic under stated assumptions |
| G2 — Public/borrowed data test | Identified dataset, licence, provenance, processing record and independent comparison where possible | Tested on the named dataset within stated limits |
| G3 — Prototype acquisition | Documented equipment, permissions, field procedure, raw data and checks | Prototype field workflow exercised |
| G4 — Physical validation | Suitable independent references, accepted procedures, uncertainty and review | Validated only for the stated site, equipment, method and conditions |

Passing one gate does not imply passing the next. A synthetic adjustment does not establish instrument performance; a public-data test does not establish field acquisition capability; one successful field site does not establish universal performance.

## 7. First implementation plan

The first implementation should proceed in this order:

1. **Choose a bounded application.** Prefer a permissioned, non-cadastral site/asset inventory or topographic feature-mapping task with a clear user and modest consequences.
2. **Confirm feasibility.** Identify site access, permissions, safety, equipment availability, competent supervision, data rights and independent check options.
3. **Set requirements.** Agree feature classes, intended use, scale, acceptance criteria and output schema.
4. **Select one primary acquisition method.** Add a second method only where it answers a clear measurement or validation need.
5. **Build the desk workflow.** Complete the reference, field plan, data dictionary, metadata model and processing plan.
6. **Create a synthetic rehearsal if useful.** Use it to test schema and calculations, not to claim field performance.
7. **Run a small acquisition only after approval.** Preserve raw data and record deviations.
8. **Assess and publish the result.** Include limitations and evidence state.

### Feasibility decisions still open

- Exact site and application.
- Whether the first task is point/asset inventory, topographic detail or another bounded product.
- Available instrument/sensor and access to its manuals and verification records.
- Availability of an authoritative reference/control source.
- Who can supervise or independently check the work.
- Permissions, safety and data/privacy conditions.
- Required quality and delivery specification.
- Budget, transport and practical timing.

These are real dependencies, not details to invent in the document. The capstone remains at G0 until they are resolved.

## 8. Source and standards starting points

Use the [surveying and field measurement source map](../../catalog/surveying-field-measurement-source-map.md) as the annotated register. Important source families include:

- BIPM/JCGM GUM and VIM for measurement uncertainty and terminology.
- Relevant ISO 17123 part for the actual instrument/system and test question.
- RICS GNSS guidance where GNSS land-survey practice is relevant.
- USACE control/topographic surveying and NOAA geodetic levelling manuals as technical exemplars, not Kenyan legal specifications.
- IERS, IGS and national geodetic authorities for reference frames, control and positioning products.
- Kenya's Land Surveyors' Board, Survey Act, Survey Regulations and current government geodetic information for jurisdictional and professional review.

The source map records edition, access and jurisdiction caveats. Before an operational protocol is released, inspect the exact current documents and confirm that each supports the specific claim being made.

## 9. Synthetic rehearsal — first executable validation pipeline

A standard-library Python validator and a small synthetic fixture are available in [synthetic rehearsal](synthetic/README.md). The fixture contains four stop records, six asset records, four observation records and four example quality checks. It validates required fields, identifiers, controlled values, foreign-key relationships, timestamps and declared check records, then writes a JSON QA report and CSV error list.

The fixture uses invented local Cartesian coordinates with **no CRS**. It is deliberately not georeferenced and must not be displayed as Nairobi locations. A passing run demonstrates schema/record validation only; it does not establish positional accuracy, field performance, independent evidence or operational fitness.

The script was executed against the committed fixture: 4 stops, 6 assets, 4 observations, 4 quality-check records; 0 validation errors. A negative test with an unknown asset-to-stop foreign key correctly returned a failure. The committed report preserves the input hashes and limitations.

## 9. Proposed first application

The proposed first application is a small [urban public-transport stop and roadside-asset inventory](pilot-project-definition.md) in Nairobi. It is a design candidate, not a confirmed site or authorised field assignment. The linked project definition sets out the study question, scope boundaries, relational data model, collection principles, validation strategy, deliverables and G0 feasibility gate.

This application is intended to connect measurement science and field acquisition to a useful spatial dataset. It does not imply official stop designation, route validation, cadastral authority, engineering acceptance or accessibility certification.

## 9. Current status and next decision

**Current status: G0 design plus a limited G1 synthetic schema rehearsal.** The workflow architecture and source routes are documented. No site has been selected, no equipment has been inspected, no permissions have been obtained, no field observations have been collected and no physical validation is claimed.

The next decision is to confirm whether the proposed Nairobi stop/asset inventory is feasible, identify a suitable corridor and resolve access, safety, equipment, reference and independent-check requirements. Only then should it be specialised into an executable field protocol.

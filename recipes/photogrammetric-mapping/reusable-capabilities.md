# Photogrammetric mapping — reusable capability register

**Application / recipe:** SM-REC-007  
**Status:** Integration and automation planning  
**Purpose:** Make the reusable contributions of the photogrammetry application visible and prevent its work from becoming a disconnected project-specific toolchain.

This register is an integration map, not a claim that a complete end-to-end photogrammetry platform exists. It distinguishes existing repository components from the handoffs and automation still to be built or verified.

## 1. Why this application is useful to Spatial Methods

Photogrammetric mapping is a strong integration test because a credible deliverable depends on several different kinds of knowledge and work:

- requirements and fitness-for-purpose decisions;
- camera geometry and image acquisition;
- positioning, control and independent reference measurements;
- data discovery, access and preservation;
- image inspection and metadata integrity;
- photogrammetric processing;
- independent quality assessment;
- reproducible packaging and delivery.

It therefore tests whether the four pillars connect in practice, and it exposes opportunities for reusable data, processing and QA automation.

## 2. Existing capabilities in the repository

| Capability | Current canonical location | What it contributes | Current boundary |
|---|---|---|---|
| End-to-end project method | `recipes/photogrammetric-mapping/README.md` | Requirements, feasibility, acquisition, processing, validation and delivery gates | Desk-designed; not field-tested or independently specialist-reviewed |
| Project record and QA checklist | `recipes/photogrammetric-mapping/project-record-template.md` | Reusable project decisions, evidence and sign-off record | Template; does not itself verify compliance |
| Image acquisition principles | `collection/photogrammetry/image-acquisition.md` | Acquisition geometry, camera and field considerations | Method guidance, not a flight authorisation |
| Flight-design calculations | `implementations/python/photogrammetric-flight-design/` | Bounded GSD, footprint and image-spacing calculations with tests | Calculation companion, not a mission planner |
| Rehearsal dataset acquisition | `implementations/python/photogrammetry-odm/acquire_rehearsal_dataset.py` | Retrieves a defined dataset at a resolved immutable repository revision | Specific to the documented public rehearsal dataset |
| Image dataset audit | `implementations/python/photogrammetry-odm/dataset_audit.py` | File inventory, checksums, readability, dimensions and selected EXIF checks | Structural audit; GPS presence is not positional validation |
| Dataset metadata audit | `implementations/python/photogrammetry-odm/dataset_metadata_audit.py` | Checks known GCP, image observation and OPK export structure and consistency | Dataset-specific structural checks; not a survey or CRS validation |
| ODM invocation | `implementations/python/photogrammetry-odm/odm_runner.py` | Validates project layout and constructs a reproducible Docker invocation | Does not choose parameters, install Docker or interpret outputs |
| Independent checkpoint statistics | `implementations/python/photogrammetry-odm/checkpoint_qa.py` | Computes residual summaries from model and independently observed checkpoint coordinates | Does not design the sample, transform coordinates or decide acceptance |

These components are already useful contributions. The opportunity now is to make their interfaces and handoffs coherent.

## 3. Workflow and automation map

| Stage | Human/domain decision | Existing automation | Integration opportunity |
|---|---|---|---|
| Define requirements | Intended use, deliverables, quality and acceptance | Project record template | Machine-readable project manifest with explicit unresolved fields and approval gates |
| Discover data | Dataset suitability, licence, provenance and coverage | Rehearsal dataset source documented | Source record and discovery adapter pattern reusable across public datasets |
| Acquire data | Select immutable source revision and subset | Revision-pinned acquisition helper and hashes | Standard acquisition manifest schema, resumable transfer and integrity verification |
| Inspect data | Decide whether files and metadata are fit for processing | Image and metadata auditors | Unified audit report, explicit severity levels and machine-readable pass/warn/fail results |
| Design acquisition | Select geometry and control/check layout | Flight-design calculation companion; recipe guidance | Connect project requirements to calculation inputs and preserve calculation provenance |
| Process imagery | Select software/version and justified parameters | ODM runner | Preflight validation, pinned engine image, configuration record and captured execution logs |
| Inspect products | Assess completeness, artefacts, CRS, resolution and metadata | Some structural QA is described in recipe | Product inventory and format/metadata checks before positional acceptance |
| Validate accuracy | Define independent check design and acceptance | Checkpoint residual statistics | Predeclared acceptance rules, reference-uncertainty record and report generation |
| Package delivery | Decide what the recipient needs and what limitations must be disclosed | Project record template | Reproducible delivery manifest linking raw data, processing, checks, outputs and reports |

## 4. Reusable capabilities to promote

The following capabilities have value beyond photogrammetry and should be designed as shared patterns where the implementation is genuinely domain-independent.

### A. Immutable data acquisition

A reusable acquisition component should support:

- source identity and canonical URL/repository;
- immutable revision, version or snapshot resolution;
- explicit file/subset selection;
- retry and resumability where supported;
- size and checksum verification;
- retrieval timestamps and tool versions;
- a machine-readable manifest;
- clear separation between raw and working copies.

Photogrammetry provides a concrete test, but the same pattern applies to scientific datasets, imagery archives, reference data and other public research resources.

### B. Dataset integrity and metadata inspection

A shared audit framework should distinguish:

- file existence and readability;
- expected versus observed counts;
- format and schema validity;
- metadata presence and plausibility;
- coordinate/reference declarations;
- duplicate or conflicting records;
- integrity hashes;
- warnings that require human interpretation.

Domain-specific parsers should remain plugins or separate modules. Do not turn one generic auditor into a collection of photogrammetry-specific assumptions.

### C. Processing run provenance

A reusable processing record should capture:

- input manifest and checksums;
- software/container version and image digest;
- parameters and configuration;
- execution environment;
- start/end time and exit status;
- logs and warnings;
- output inventory and checksums;
- links to QA reports.

The orchestrator should call existing domain tools and preserve their outputs; it should not silently reimplement processing logic.

### D. Independent validation

The validation pattern should make the distinction between production data and independent reference data explicit.

It should capture:

- reference source and measurement method;
- sample design and spatial distribution;
- reference uncertainty;
- points or observations used in adjustment versus withheld for checks;
- residual definitions and coordinate conventions;
- predeclared acceptance criteria;
- exclusions and their rationale;
- limitations and reviewer decision.

The statistics may be shared, but the acceptance rule must remain application- and specification-dependent.

### E. Reproducible project packaging

A delivery package should be able to trace each output to:

- project requirements;
- source data;
- acquisition record;
- processing configuration;
- software version;
- QA evidence;
- validation decision;
- known limitations.

This pattern can serve many Spatial Recipes, not only photogrammetry.

## 5. Proposed integration sequence

The immediate objective is not to add more isolated photogrammetry scripts. It is to integrate what already exists.

1. **Inventory and interface review:** inspect the existing scripts, inputs, outputs, tests and provenance fields. Identify overlap and incompatible assumptions.
2. **Project manifest:** define a small versioned manifest that records project identity, requirements, source records, processing configuration, validation plan and output locations. Do not place credentials or sensitive site data in the public repository.
3. **Unified preflight:** combine existing dataset and metadata checks into a report that clearly distinguishes blockers, warnings and informational observations. Preserve the underlying detailed reports.
4. **Processing handoff:** make the manifest and verified input inventory drive a dry-run ODM command; require an explicit user/operator action for actual processing.
5. **Output audit:** inventory expected products, verify readability and metadata, and record omissions without assuming every ODM product must exist.
6. **Independent QA handoff:** connect the separately prepared check-point observations to the checkpoint statistics tool and the project-specific acceptance rules.
7. **Delivery manifest:** package provenance, outputs, processing logs, QA reports, limitations and sign-off information.
8. **Extract shared patterns:** only after the photogrammetry workflow works end to end, promote general acquisition, audit, provenance, orchestration and reporting components to shared infrastructure.

## 6. Boundaries and safeguards

- The current workflow is desk-designed and has not been field-tested or independently specialist-reviewed.
- The documented rehearsal dataset has not yet been acquired and processed end to end in the current project environment.
- Synthetic unit tests do not establish the accuracy of a real photogrammetric product.
- ODM is the processing engine; the repository's runner is orchestration, not an alternative reconstruction engine.
- Ground control and independent check points must remain distinct.
- A checksum establishes file identity/integrity, not scientific validity.
- EXIF GPS presence is not proof of positional accuracy.
- GSD is not positional accuracy.
- Internal bundle-adjustment residuals are not independent external validation.
- A computed RMSE is not, by itself, a standards-compliance decision.
- UAS operations, survey work and safety-critical applications require current jurisdictional and professional review.

## 7. What this application contributes to the wider system

When integrated, photogrammetry should leave Spatial Methods with:

1. stronger acquisition and immutable-data patterns;
2. reusable dataset integrity and metadata audit patterns;
3. a standard processing provenance record;
4. a clear separation between workflow orchestration and domain algorithms;
5. an independent validation pattern with explicit reference uncertainty;
6. a project manifest and delivery package pattern;
7. a worked recipe demonstrating how the four pillars cooperate.

The application-specific outputs remain useful, but these reusable capabilities are the compounding value for Spatial Methods.

## 8. Completion test

The integration is ready for a first end-to-end rehearsal when a competent user can:

- prepare a project record and manifest;
- acquire the documented public dataset reproducibly;
- verify its files and metadata;
- generate a reviewable processing command;
- run a pinned processing engine;
- inventory and inspect outputs;
- assess independently measured checkpoints;
- compare results with predeclared project acceptance rules;
- package provenance and limitations for another person to review.

Passing this rehearsal would establish a reproducible software workflow for the documented dataset. It would not establish field performance, universal accuracy or operational suitability.


## 9. Integration update — manifest and read-only preflight

The first integrated handoff now exists in the implementation:

- `project_manifest.py` validates the versioned project record and reports manifest-level blockers and warnings.
- `dataset_audit.py` inventories image files, records SHA-256 hashes and checks image readability/dimensions when Pillow is available.
- `odm_runner.py` constructs the Docker invocation from the project directory and explicit image/arguments.
- `project_preflight.py` connects those components into one machine-readable report and includes the constructed processing command without executing it.
- `test_project_preflight.py` covers the read-only handoff, missing imagery, expected-count mismatch and non-execution boundary.

This is a meaningful integration milestone, not completion of the full workflow. The preflight does not yet run the HEIG-VD-specific GCP/observation/OPK metadata audit, inspect generated ODM products, execute processing, or evaluate checkpoint acceptance criteria. Those checks remain separate until their inputs and domain boundaries can be connected safely.

### Current status

| Integration component | Status |
|---|---|
| Versioned project manifest | Implemented |
| Manifest validation | Implemented |
| Generic image inventory and integrity audit | Existing component; connected |
| Image readability/dimensions | Connected when Pillow is installed |
| ODM command construction | Existing component; connected as dry-run only |
| Unified machine-readable preflight | Implemented |
| Dataset-specific GCP/observation/OPK audit | Separate, not yet integrated |
| Processing execution and run provenance | Not yet integrated |
| Output product inventory and inspection | Not yet implemented |
| Independent checkpoint acceptance workflow | Statistics exist; project-level handoff not yet integrated |
| Reproducible delivery package | Not yet implemented |

### Next integration milestone

Build a processing-run record that captures the exact input inventory, image digest, ODM arguments, runtime environment, execution timestamps, exit status, logs and output inventory. Keep execution explicitly operator-triggered. Then add output-product inspection as a separate read-only stage. Only after these interfaces are stable should the workflow move toward automated end-to-end execution.


## 10. Integration update — processing-run provenance

A separate processing-run recorder now extends the preflight handoff into a traceable execution event.

- `processing_run.py` hashes supported input images before execution.
- It records the requested container reference and, when explicitly executing, attempts to capture the local image ID, repository digests, OS and architecture.
- It captures the exact command, Python/platform context, start/finish timestamps, exit code and stdout/stderr logs.
- It inventories files under the project after execution, recording relative paths, sizes and SHA-256 hashes.
- Dry-run is the default and does not invoke Docker. Processing requires an explicit `--execute` argument.
- The run-record directory must be outside the project directory to avoid recursively recording its own evidence.

Automated tests cover dry-run behaviour, input hashing, rejection of an in-project run directory, successful mocked execution and failed mocked execution.

### Capability boundary

The recorder documents the wrapper-observable processing event. It is not yet a full execution attestation, deterministic-build guarantee, output semantic validator or accuracy assessment. It does not currently validate raster CRS, resolution, nodata, footprint, vertical reference, point-cloud integrity or orthophoto content.

### Updated integration status

| Integration component | Status |
|---|---|
| Versioned project manifest and validation | Implemented |
| Generic image inventory, hashes and readability | Integrated |
| ODM command construction | Integrated |
| Unified read-only preflight | Implemented |
| Explicit processing-run record | Implemented |
| Input and output file checksums | Implemented |
| Execution logs and exit status | Implemented |
| Container image metadata capture | Best-effort |
| Dataset-specific metadata audit | Separate |
| Output semantic/geospatial inspection | Next |
| Independent checkpoint acceptance workflow | Existing statistics; project-level integration pending |
| Reproducible delivery package | Pending |

### Next integration milestone

Create output inspection adapters that understand the actual geospatial products rather than merely listing files. At minimum, inspect raster readability, dimensions, band count, CRS, affine transform, pixel size, nodata and bounds; inspect point-cloud metadata where supported; and compare observed outputs against declared deliverables. Preserve warnings for missing or unexpected products. Keep semantic QA distinct from geometric accuracy acceptance.


## 11. Integration update — output inspection

The first output-inspection adapter is now available as `output_inspection.py`.

It:
- inventories generated project files with relative paths and sizes;
- checks explicitly declared expected outputs and blocks when they are missing;
- inspects GeoTIFF readability and records dimensions, bands, data types, CRS, transform, bounds, pixel size and nodata when Rasterio is installed;
- reports unavailable raster inspection as a warning rather than silently treating file presence as validation;
- rejects expected paths that escape the project directory.

Tests cover missing declared outputs, absent Rasterio, path traversal and relative inventory.

### Capability boundary

This adapter establishes structural evidence only. It does not verify that a CRS is correct, compare geospatial outputs to independent control, assess orthophoto seamlines or radiometry, or inspect point-cloud/mesh semantics. Those require dedicated adapters and explicit acceptance criteria.

### Updated integration status

| Integration component | Status |
|---|---|
| Project manifest and validation | Implemented |
| Image inventory, hashes and readability | Integrated |
| ODM command construction and dry-run handoff | Integrated |
| Explicit processing-run record, logs and checksums | Implemented |
| Output inventory and expected-file checks | Implemented |
| GeoTIFF structural inspection | Implemented when Rasterio is installed |
| Point-cloud and mesh inspection | Pending |
| Independent checkpoint residual statistics | Implemented |
| Project-level validation evidence and human decision record | Implemented; evidence completeness is explicit |
| Reproducible delivery package | Pending |

### Next integration milestone

Assemble source provenance, processing provenance, output inspection, independent validation and unresolved limitations into a reviewable delivery package. Keep these distinct forms of evidence separate.


## 12. Integration update — independent checkpoint evidence

The project-level evidence adapter is now implemented as `validation_evidence.py`, reusing the existing transparent residual calculations in `checkpoint_qa.py`.

- Requires a separately supplied checkpoint CSV and explicit project context.
- Records project/run identifiers, horizontal CRS, vertical reference, coordinate units, reference uncertainty, sample design and whether checkpoint independence is confirmed.
- Hashes the checkpoint CSV and any linked processing-run/output-inspection JSON records.
- Checks the supplied processing-run identifier against the run record when that identifier is present.
- Reports residual statistics separately from evidence completeness and the human acceptance decision.
- Missing required context or unconfirmed checkpoint independence produces `not_assessable`; no generic threshold is invented.
- Acceptance defaults to `pending`. A non-pending decision requires a named reviewer and written rationale.

Tests cover the pending/assessable distinction, missing reference metadata, non-independent checkpoints, human decision traceability and linked run-record identity.

### Important boundaries

The adapter does not prove checkpoint independence or sample representativeness, transform coordinates, validate CRS compatibility, propagate reference uncertainty, calculate confidence intervals or determine standards compliance. The descriptive radial P95 is not CE95. GCPs, training points and AI-assisted interpretations are not independent checkpoints. A single reviewer decision must not be described as independent multi-reviewer validation.

### Updated integration status

| Integration component | Status |
|---|---|
| Project manifest, image audit and preflight | Implemented |
| Explicit processing-run provenance | Implemented |
| Output inventory and GeoTIFF structural inspection | Implemented when Rasterio is installed |
| Independent checkpoint residual statistics | Implemented |
| Project-level validation evidence and human decision record | Implemented; evidence completeness explicit |
| LAS/LAZ point-cloud structural inspection | Implemented when laspy is installed; streamed count/coordinate/classification/intensity summaries |
| Point-cloud classification correctness, density and positional QA; mesh semantic inspection | Pending |
| Reproducible evidence delivery dossier | Implemented; release authorization remains external |


## 13. Integration update — reproducible evidence delivery dossier

The first delivery-dossier builder is now available as `delivery_dossier.py`.

It assembles five existing evidence records into a ZIP archive:
- project manifest;
- read-only preflight report;
- processing-run provenance;
- output inspection report;
- checkpoint-validation evidence.

The embedded `delivery-dossier.json` records SHA-256 hashes, byte sizes, observed statuses, project/run identity consistency, warnings and limitations. The builder rejects missing or invalid JSON evidence and flags project/run identity conflicts as `inconsistent`.

The dossier status is deliberately not a release decision:
- `inconsistent`: declared project or processing-run identities conflict;
- `review_required`: evidence statuses or human acceptance remain unresolved;
- `assembled`: supplied records are consistent and carry the expected positive statuses.

Even when assembled, `release_authorized` remains false. The archive contains the evidence records, not raw imagery or the complete photogrammetric products; those remain separately preserved and linked by the provenance records.

Tests cover successful assembly, pending acceptance, run-identity mismatch and missing required evidence.

### Current integration status

| Capability | Status |
|---|---|
| Project manifest and integrated preflight | Implemented |
| Input inventory and source hashes | Implemented |
| Acquired snapshot integrity verification | Implemented; verifies declared sizes and SHA-256, detects missing/modified/unmanifested files |
| Explicit ODM processing-run provenance | Implemented; live Docker execution not yet rehearsed |
| Output inventory and GeoTIFF structural inspection | Implemented when Rasterio is installed |
| Independent checkpoint residual statistics | Implemented |
| Project-level validation evidence and human decision record | Implemented |
| Evidence ZIP dossier with checksums and consistency checks | Implemented |
| LAS/LAZ streamed structural inspection | Implemented when laspy and a compatible LAZ backend are installed; point counts, finite coordinates, observed/header extent reconciliation, classification/intensity summaries and bounded sample |
| Point-cloud classification correctness, density and positional QA | Pending |
| Wavefront OBJ syntax and vertex-index inspection | Implemented; topology, self-intersections, texture completeness, normal quality and geometric accuracy remain unverified |
| Real-dataset end-to-end rehearsal | Pending |
| Independent multi-reviewer validation and project-specific release | External human/project process |

### Next integration milestone

Run a controlled rehearsal on a documented, non-sensitive dataset with real outputs and independently surveyed checkpoints. Close remaining structural gaps (point-cloud classification correctness, density/positional QA and mesh inspection where deliverables require them), test the complete handoff from acquired snapshot through dossier, and record every unavailable or unverified capability rather than filling gaps with assumptions.


## 14. Integration update — acquisition and mesh structural safeguards

Two structural gaps have been tightened:

- The acquisition verifier rejects symlinks in any component of a declared file path and reports symlink entries found inside the selected dataset directory. A symlinked source tree cannot quietly pass as an ordinary byte-for-byte snapshot.
- The OBJ inspector validates finite vertex, texture-coordinate and normal records; positive and negative indices for face references; repeated vertex indices; and zero-area polygons using a face-local Newell area-vector tolerance.

These checks improve file-structure evidence only. OBJ manifoldness, self-intersections, texture-file availability, normal correctness, watertightness and geometric accuracy remain unassessed. LAS/LAZ classification correctness, point density and positional accuracy also remain unassessed.

The new unit tests exercise symlinked acquisition paths and directories, malformed OBJ texture references, collinear faces and valid negative OBJ indices. The synthetic pipeline test still does not represent a real photogrammetric processing run.

### Real-data gate

The next evidence milestone remains a controlled acquisition and processing rehearsal on the documented HEIG-VD dataset. The operator run sheet is in `implementations/python/photogrammetry-odm/rehearsal-plan.md`. It defines integrity, metadata, coordinate-reference, control/checkpoint, Docker and delivery stop conditions. Until those steps are completed with actual source files and real outputs, the workflow remains synthetically integrated but not end-to-end rehearsed.


## 15. Integration update — first real-data acquisition and review preparation

The HEIG-VD drone 2019 source was acquired and structurally audited at revision `e0dfeba2b6ed94ea1ae2bf773e742c39fb437b71`.

| Capability | Status |
|---|---|
| Immutable source acquisition and SHA-256 verification | Real run completed; 36/36 selected files verified |
| Image inventory and decoding | Real run completed; 32/32 JPGs readable, 5472 × 3648 px |
| Dataset metadata reconciliation | Real run completed; 31 surveyed-point records, 206 image observations, 30 observed points, 32 OPK rows |
| Known source exception handling | Point 100 duplicate/unobserved record documented; image 0075 without GCP observations reported |
| Control-only ODM GCP preparation | Implemented and run provisionally; 8 controls, 51 image-observation rows, 29 images |
| Role-blind human review preparation | Implemented; 30 point sheets with 640 × 640 crops and blank observation-decision worksheet |
| Real ODM EXIF-only baseline execution | Completed; processing record succeeded with pinned ODM 3.6.2 image digest |
| Structural output inspection | Completed; orthophoto, DSM and LAZ readable; no blockers/warnings |
| GCP-controlled ODM variant | Pending; proposed split remains unreviewed/unlocked |
| Independent checkpoint remeasurement and accuracy assessment | Pending |
| Project-specific acceptance and release | External human/project process |

The proposed split is `proposed_not_locked`; the EXIF-only baseline did not use it. The source Metashape image picks are not independent human remeasurements, and the supplied OPK solution is not independent validation. The baseline products have 0.05 m raster pixels and a structurally readable 1,963,721-point LAZ, but no positional accuracy has been established.

### Next integration milestone

Complete and lock the role-blind observation review, confirm the control/checkpoint partition and vertical reference, then run the approved control-GCP variant. Preserve all checkpoints outside adjustment and tuning. Only after independently established checkpoint evidence exists should the workflow be described as accuracy-assessed.


The role-blind point review packet is preserved separately from the technical audit artifact in [workflow run 44900854170](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44900854170/artifacts/14705374556). It contains 30 point sheets and a blank 206-row observation decision worksheet; no control/checkpoint role mapping is included.


The real EXIF-only baseline processing and structural inspection are complete. See [processing run 44899855412](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44899855412) and [output inspection run 44901305912](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44901305912). The evidence/product artifact is [available here](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44901305912/artifacts/14706410333). The initial inspection lacked pyproj; a separate post-run inspection with pyproj succeeded. Future manual baseline runs install pyproj.

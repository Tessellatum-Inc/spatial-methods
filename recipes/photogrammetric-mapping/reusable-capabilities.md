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

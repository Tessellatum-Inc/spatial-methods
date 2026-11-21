# Reviewer guide — photogrammetry / ODM evidence pipeline

**Scope:** `implementations/python/photogrammetry-odm/`  
**Purpose:** Give a future reviewer a repeatable route through the code, tests, evidence records and known limitations. This guide is an inspection aid, not an approval or certification.

## 1. Start with the claims boundary

This package currently provides a set of tested workflow components and evidence handoffs. It is **not yet a demonstrated end-to-end photogrammetric production workflow**.

The following distinctions are mandatory:

- A passing unit test establishes behaviour against its test fixture, not successful processing of real imagery.
- A dry-run establishes that a command can be constructed; it does not establish that Docker or ODM can execute it.
- A processing exit code of zero does not establish geospatial correctness or positional accuracy.
- A file hash establishes byte identity, not authenticity, scientific validity or fitness for purpose.
- A readable GeoTIFF and populated CRS field do not prove the CRS is correct.
- Checkpoint statistics are only meaningful when reference and model coordinates share compatible horizontal and vertical references, units and axis order.
- An `assessable` evidence record means required context was supplied and independence was declared; the adapter does not independently prove either.
- A dossier marked `assembled` is a consistent evidence bundle, not a release approval. `release_authorized` remains false.
- A sole reviewer's decision is a single-reviewer adjudication, not independent multi-reviewer validation.

## 2. Recommended review order

1. Read [the implementation README](README.md) for prerequisites, commands and component boundaries.
2. Read [the end-to-end rehearsal plan](rehearsal-plan.md) and [dataset inspection record](dataset-inspection.md) before interpreting the HEIG-VD example.
3. Inspect the versioned manifest and context templates. Confirm placeholders are not mistaken for project facts.
4. Verify any acquired source snapshot with `verify_acquisition.py` before image or metadata audits; inspect the file-level results, symlink report and manifest hash, not only the summary status.
5. Review the implementation in this order:
   - `project_manifest.py` — project contract and manifest validation;
   - `verify_acquisition.py` — verify the acquired source snapshot against its immutable file manifest;
   - `dataset_audit.py` — generic image inventory, hashes and optional readability checks;
   - `project_preflight.py` — read-only integration and severity reporting;
   - `odm_runner.py` — command construction and project checks;
   - `processing_run.py` — explicit execution boundary and provenance capture;
   - `output_inspection.py` — read-only output inventory and GeoTIFF structure;
   - `checkpoint_qa.py` — residual definitions and statistics;
   - `validation_evidence.py` — evidence completeness and human decision record;
   - `delivery_dossier.py` — checksummed evidence packaging.
6. Run the package tests from this directory:
   ```bash
   python -m pytest -q
   ```
   Or use the standard-library test runner:
   ```bash
   python -m unittest -v
   ```
7. Review the latest GitHub Actions run for the exact commit being examined. Do not infer green CI from an earlier commit or from selected successful shards.
8. For any proposed real-data claim, require the acquisition manifest, input hashes, exact engine digest, logs, output inspection, independent checkpoint evidence and project-specific acceptance specification.

## 3. Evidence handoff map

| Record | Primary purpose | Reviewer should verify |
|---|---|---|
| Project manifest | Declares intended use, sources, references, processing and deliverables | Version, project identity, unresolved placeholders, CRS and vertical reference, criteria reference |
| Preflight report | Read-only readiness and command handoff | Blockers/warnings, observed image count, supported formats, command, no execution |
| Processing-run record | Captures input identity and processing event | Input hashes, requested image, resolved image metadata if available, command, timestamps, exit status, logs, output inventory |
| Output-inspection report | Records observed files and raster structure | Expected outputs, missing files, readability, CRS/transform/bounds/nodata, unavailable dependencies |
| Validation evidence | Links checkpoints and human decision | CSV hash, reference uncertainty, sample design, independence declaration, criteria reference, reviewer and rationale |
| Delivery dossier | Packages the five evidence records | Archive hashes, identity consistency, status, warnings and explicit non-authorization |

The dossier does not contain raw imagery or complete generated products. Reviewers must verify that those are preserved separately and can be matched to the recorded hashes and paths.

## 4. Required reviewer questions

### Project definition and coordinate references
- Is the intended use explicit and suitable for the product?
- Are horizontal CRS, vertical datum/reference, height type, units and axis order declared separately where necessary?
- Is the acceptance specification project-specific, versioned and available to the reviewer?
- Are placeholders, assumptions and unresolved decisions visible?

### Source data and acquisition
- Does the immutable source revision match the acquisition manifest?
- Do image counts, filenames, dimensions, hashes and metadata reconcile?
- Are licence and attribution obligations preserved?
- Are raw inputs kept separate from mutable working copies?
- Are EXIF positions treated as metadata rather than assumed survey control?

### Processing provenance
- Was execution explicitly requested, rather than inferred from a dry-run?
- Is the container reference pinned, and is a resolved digest recorded where available?
- Do command, arguments, environment, timestamps, exit code and logs agree?
- Are failures and not-started runs preserved as records rather than silently discarded?
- Can outputs be tied to the exact input inventory and run?

### Output inspection
- Are declared expected outputs present?
- Are all reported raster properties plausible for the project specification?
- Is a populated CRS field independently checked against the intended CRS?
- Are LAS/LAZ point counts reconciled, coordinate values finite, and classification/intensity summaries plausible? Are classification correctness, density suitability and positional accuracy evaluated separately?
- Are mesh deliverables inspected where they are in scope?
- Are structural inspection and product/positional acceptance kept distinct?

### Independent validation
- Were checkpoints withheld from control, tuning and training?
- Is the reference source, measurement method, uncertainty and sample design documented?
- Are model and reference coordinates in compatible horizontal and vertical references?
- Are exclusions and extraction methods documented?
- Are criteria predeclared and applied by an identified reviewer?
- Is the reviewer's role accurately described (single-reviewer or independent multi-reviewer)?

### Delivery and release
- Do project and run identifiers agree across all records?
- Do the hashes in the dossier match the actual evidence files?
- Are warnings, unavailable checks and limitations retained?
- Is release authorization made by the responsible project authority outside this packaging tool?

## 5. Status interpretation

- `blocked`: a required structural or declared condition prevents the next handoff.
- `review_required`: the tool has found unresolved warnings, incomplete decisions or conditions requiring human review.
- `ready_for_operator_review`: configured preflight checks found no blocker/warning; this is not an approval to process or deliver.
- `prepared`: processing command and input record prepared; no execution occurred.
- `not_started`: execution was requested but could not start (for example, Docker is unavailable); inspect the recorded error.
- `succeeded` / `failed`: wrapper-observed process outcome only.
- `not_assessable`: required validation context is absent or checkpoint independence is not confirmed.
- `pending`: no human acceptance decision has been recorded.
- `inconsistent`: dossier identity checks found conflicting declarations.
- `assembled`: evidence records were packaged and consistency checks passed; this is not release authorization.

Do not collapse these statuses into a single pass/fail score.

## 6. Known gaps at this stage

- No live Docker/ODM execution has been demonstrated in this repository environment.
- The HEIG-VD rehearsal imagery has not yet been acquired, byte-audited and processed locally.
- LAS/LAZ point records are streamed when `laspy` is installed; declared/observed count reconciliation, finite coordinates, observed/header extent reconciliation (using a tolerance derived from coordinate scales), classification counts, intensity range and a bounded coordinate sample are recorded. Classification correctness, density suitability and positional accuracy remain unassessed.
- Wavefront OBJ vertex, texture-coordinate and normal records are checked for finite values; face vertex/texture/normal indices and repeated-index/zero-area faces are checked. Manifoldness, self-intersections, texture-file availability, normal quality and geometric accuracy remain unassessed.
- Raster inspection is conditional on Rasterio; image readability checks are conditional on Pillow.
- Checkpoint independence, sample representativeness, reference uncertainty and CRS correctness are declarations/evidence for human review, not independently established by these scripts.
- No universal accuracy threshold is encoded. Acceptance must cite the project's own specification.
- The delivery ZIP packages the original acquisition provenance manifest and its verification report alongside project, processing and validation evidence, but not source imagery or complete products. It cross-checks the exact manifest hash, resolved revision, selected dataset path and declared file count.
- A synthetic acquisition-to-dossier integration test now exercises the evidence handoff and verifies that unexecuted processing and unresolved checkpoint evidence remain open. It is not a live ODM rehearsal.
- The workflow has not been independently specialist-reviewed or field-tested.

## 7. How to record a review finding

For each finding, record:

1. file and function or report field;
2. exact commit SHA and test/workflow run;
3. observed behaviour and a minimal reproducible example;
4. expected behaviour and why it matters;
5. severity and affected downstream evidence;
6. proposed correction;
7. whether the correction changes existing evidence or requires a new processing run.

Do not silently edit historical evidence records. Correct the implementation, create a new run/evidence record, and retain the old record as part of the audit trail where appropriate.

## 8. Current milestone and next gate

The current milestone is **synthetic integrated evidence handoff tested; real execution not yet rehearsed**. The next substantive gate is a controlled real-dataset rehearsal on a network-enabled machine with a pinned ODM image, verified source bytes, documented control/checkpoint partition, real outputs and independently surveyed checkpoints. Reviewers should require the complete handoff from manifest through dossier and a documented disposition of every warning before describing the workflow as rehearsed.

Last updated: 2026-11-21.


## 9. Real-data evidence status — HEIG-VD drone 2019

The source dataset has been acquired and structurally audited at immutable revision `e0dfeba2b6ed94ea1ae2bf773e742c39fb437b71`. The saved acquisition manifest verifies 36/36 files. All 32 JPGs decode at 5472 × 3648 pixels and contain GPS metadata. The metadata audit reports 31 surveyed point records, 206 image observations across 30 points, and 32 OPK records.

Known source structure must not be misclassified:
- point 100 has no image observation and duplicates point 206, as the publisher documents;
- image `...0075` has no ground-point observation, but may still contribute tie points;
- the supplied OPK solution used ground points as control and is not independent validation.

A proposed split (8 controls, 19 checkpoints, 3 low-observation points withheld) is stored separately and remains `proposed_not_locked`. The 51-row GCP candidate contains controls only. A role-blind review packet provides per-point crops and a blank observation decision worksheet. The image picks are publisher-provided Metashape measurements, not independent remeasurements.

**Do not call this an end-to-end ODM rehearsal yet.** ODM has not been executed, checkpoint residuals have not been computed, and no validation or release decision exists. The next gate is locked human review, followed by a pinned-container baseline and approved GCP run.

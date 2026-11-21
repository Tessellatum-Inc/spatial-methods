# Reviewer guide — photogrammetry / ODM evidence pipeline

**Scope:** `implementations/python/photogrammetry-odm/`  
**Purpose:** Give a future reviewer a repeatable route through the code, tests, evidence records and known limitations. This guide is an inspection aid, not an approval or certification.

## 1. Start with the claims boundary

This package now includes a real EXIF-only ODM processing baseline and structural output inspection, in addition to tested workflow components and evidence handoffs. It is **not yet a demonstrated end-to-end accuracy-validated production workflow**.

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
   - `prepare_odm_gcp.py` — source-bound control-only ODM GCP export;
   - `visual_review.py` and `lock_visual_review.py` — role-blind observation review material and decision lock;
   - `independent-checkpoint-measurement-protocol.md` and its CSV template — independent image-coordinate measurement after the split is locked;
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

- A live Docker/ODM execution has been demonstrated on the HEIG-VD imagery in CI using the pinned ODM 3.6.2 image. This was an EXIF-only baseline without GCPs; it is not a controlled-GCP experiment.
- The HEIG-VD rehearsal imagery has been acquired and byte-audited; the EXIF-only outputs have been structurally inspected. The GCP-controlled variant and independent checkpoint validation remain pending.
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

The HEIG-VD reference-system gate is documented in [coordinate-reference-handling.md](coordinate-reference-handling.md). The source has LV95 horizontal coordinates and LN02 heights; a two-dimensional EPSG:2056 header is not evidence that ODM output encodes LN02 vertical semantics.


The current milestone is **real EXIF-only baseline processed and structurally inspected; GCP-controlled and independent validation stages pending**. Reviewers should require the locked role-blind observation review; post-lock unblinding and approval of the control/checkpoint partition; independent checkpoint image remeasurement from original unannotated images; explicit horizontal/vertical reference handling; control-only GCP processing; and compatible reference coordinates plus validation evidence before describing the workflow as accuracy-assessed.

Last updated: 2026-11-21.


## 9. Real-data evidence status — HEIG-VD drone 2019

The source dataset has been acquired and structurally audited at immutable revision `e0dfeba2b6ed94ea1ae2bf773e742c39fb437b71`. The saved acquisition manifest verifies 36/36 files. All 32 JPGs decode at 5472 × 3648 pixels and contain GPS metadata. The metadata audit reports 31 surveyed point records, 206 image observations across 30 points, and 32 OPK records.

Known source structure must not be misclassified:
- point 100 has no image observation and duplicates point 206, as the publisher documents;
- image `...0075` has no ground-point observation, but may still contribute tie points;
- the supplied OPK solution used ground points as control and is not independent validation.

A proposed split (8 controls, 19 checkpoints, 3 low-observation points withheld) is stored separately and remains `proposed_not_locked`. The 51-row GCP candidate contains controls only. A role-blind review packet provides per-point crops and a blank observation decision worksheet. The image picks are publisher-provided Metashape measurements, not independent remeasurements.

A real EXIF-only ODM baseline has now been executed and structurally inspected. This establishes that the processing and output-inspection chain runs on actual data; it does not establish accuracy. The GCP-controlled variant, independent checkpoint evidence, checkpoint residuals, validation and release decision remain pending. Follow the authoritative seven-step sequence in [the rehearsal plan](rehearsal-plan.md): lock role-blind review before unblinding; approve the split; independently remeasure checkpoint image coordinates from original images; resolve horizontal and vertical references; then prepare the control-only GCP run and assess withheld checkpoints.


The role-blind point review packet is available as a separate artifact from [workflow run 44900854170](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44900854170/artifacts/14705374556). It contains the per-point image crops and blank 206-row review worksheet without the control/checkpoint role key. Artifact SHA-256: `d9744c9f8d05019f8915b7d63f140f7f01143bc4cabe9f62a098737516e8f117`.


## 10. Locking role-blind observation decisions

Use `lock_visual_review.py` after completing the role-blind 206-row worksheet. It validates that every source observation is present exactly once, the original point/image/pixel coordinates are unchanged, decisions and rationales are complete, timestamps include timezone offsets, and the source revision matches the acquisition manifest. It records hashes of the worksheet, visual summary, acquisition manifest and source-observation index.

The lock utility does not read the split key or unblind roles. It marks one reviewer as single-reviewer adjudication and does not claim independent validation. Multiple reviewer names do not prove independent review. Preserve the locked JSON record before any separate unblinding or checkpoint analysis.


## 11. Real EXIF-only ODM baseline — processing and structural inspection complete

The processing record reports success using OpenDroneMap 3.6.2 at digest `sha256:a96f56dbc4f775e352fb2b3acc472bb59f456c0948a699eb1c433659dccfbdf7`. A separate post-run inspection reports `inspected` with no blockers or warnings.

The orthophoto and DSM are readable GeoTIFFs, each 9172 × 7801 at 0.05 m pixels and EPSG:32632. The LAZ is readable with 1,963,721 points; LAS 1.4 / point format 7; finite coordinates; observed point count matches the header; no points fall outside header bounds. The LAZ WKT has no explicit EPSG authority identifier even though its Transverse Mercator parameters are consistent with UTM 32N; reconcile this with the raster EPSG:32632 metadata before authoritative use.

This baseline used EXIF camera positions only. It did not use GCPs, OPK or checkpoints. The point cloud has only class 0 and intensity range 0–0. No positional accuracy or product acceptance is established. See [processing run 44899855412](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44899855412), [output inspection run 44901305912](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44901305912), and [the evidence/product artifact](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44901305912/artifacts/14706410333).

The first inspection attempt lacked pyproj; the preserved products were re-inspected in a separate workflow with pyproj installed. Future manual baseline executions now include pyproj in the inspection environment.

# ODM end-to-end rehearsal plan

## Status

**Dataset acquisition, structural audit and role-blind visual-review material generation are complete. The real-data EXIF-only ODM baseline is currently executing; output inspection has not yet begun. Human target review and independent checkpoint remeasurement remain outstanding.**

### Verified evidence

- The [HEIG-VD real-data acquisition audit, run 7](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44899018230) completed successfully against publisher revision `e0dfeba2b6ed94ea1ae2bf773e742c39fb437b71`.
- All 36 files in the acquisition manifest passed byte-size and SHA-256 verification. All 32 source images decoded successfully at 5472 × 3648 pixels.
- The structural audit recorded 31 ground-point records, 206 image observations across 30 observed points, and 32 OPK records. It found no unmatched image references or out-of-bounds source observations, and documented the coincident/unobserved point 100/206 exception.
- The run generated 32 annotated image derivatives and two contact sheets. The review aid is **role-blind**: it reproduces the publisher-provided Metashape image picks but does not disclose which points are proposed controls or checkpoints. The artifact also includes a blank observation-level review-decision CSV template for recording decisions and reasons. The [workflow artifact](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44899018230) contains provenance, audit reports, source metadata, the provisional GCP list and visual-review material; it does not contain the original source imagery.
- The photogrammetry package test suite passed after correcting a fixture whose sample pixel coordinate was exactly on the excluded lower image boundary (70, 80 for a 100 × 80 image). [Passing test run](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44899065601).

### What this evidence does and does not establish

Acquisition hashes establish local byte agreement with the recorded manifest, not publisher authenticity, licence compliance, coordinate correctness, photogrammetric suitability or product accuracy. Structural consistency does not establish that a marker is centred on the intended physical target.

The supplied image observations were measured in Metashape. They are not independent checkpoint measurements. The supplied OPK orientations also derive from a Metashape adjustment using ground points as control and are not independent validation.

The proposed split remains `proposed_not_locked`. The annotated sheets are a review aid, not a human approval record. Reviewers must inspect target visibility, centring, occlusion, blur, ambiguity and image-to-target correspondence; checkpoints must then be independently remeasured before they can support an accuracy assessment.

### Next gates

Before any ODM run, follow the [LV95/LN02 coordinate-reference handling decision record](coordinate-reference-handling.md). The current GCP exporter carries LN02 numeric heights unchanged under a horizontal EPSG:2056 declaration; this does not encode or transform the vertical reference.


1. Complete a point-by-point, role-blind visual review of the annotated images and record explicit accept/reject/uncertain decisions with reasons.
2. Independently remeasure candidate checkpoint image coordinates without consulting the source Metashape picks. Preserve reviewer identity, method and measurement provenance.
3. After role-blind visual decisions are locked, independently remeasure checkpoint image coordinates using the separate [measurement protocol](independent-checkpoint-measurement-protocol.md) and [blank CSV template](independent-checkpoint-measurements.template.csv). Never copy the Metashape source picks into this record.
4. Reassess control/checkpoint geometry and image coverage; only then lock the partition and regenerate the control-only ODM GCP file.
5. Explicitly resolve the horizontal LV95 (EPSG:2056) and vertical LN02 handling before interpreting ODM outputs.
6. Run a documented image-only baseline and a control-constrained ODM reconstruction; evaluate withheld checkpoints using independent observations. Do not use the supplied OPK solution as independent truth.

No ODM reconstruction or accuracy claim is authorised by the current evidence.


## 15. First real-data acquisition and audit results

A hosted-runner acquisition and audit was completed against the immutable HEIG-VD revision `e0dfeba2b6ed94ea1ae2bf773e742c39fb437b71`.

- 36/36 selected source files verified against the acquisition manifest; no missing, modified, unmanifested or symlinked entries.
- 32/32 JPGs readable at 5472 × 3648 pixels; all 32 contain GPS metadata; camera make/model is senseFly S.O.D.A.
- Metadata: 31 surveyed-point records, 30 observed points, 206 image observations and 32 OPK records.
- Point 100 has no image observation and duplicates point 206; the publisher documents this exception. It is not a second independent point.
- Image `EB-02-00761_0101_0075` has no ground-point observation; this is not by itself a processing blocker.
- All 206 image observations fall within the documented pixel bounds.
- OPK rotation matrices are numerically orthogonal, but the supplied OPK solution used ground points as control and is not independent validation.

A proposed deterministic partition is recorded in `rehearsal-control-checkpoint-split.proposed.json`: 8 controls, 19 checkpoints and 3 low-observation points withheld from the primary split. The control-only GCP adapter prepared a 51-row candidate file from 8 controls, with observations across 29 images. The GCP file declares horizontal EPSG:2056; source heights are LN02.

The split remains `proposed_not_locked`. The source image picks are Metashape measurements and have not been independently remeasured or human-adjudicated. A role-blind visual-review packet now provides per-point 640 × 640 pixel crops across all available views and a blank 206-row decision worksheet. Review target identity, centring, visibility, blur, occlusion and ambiguity; lock decisions before unblinding roles.

**Current processing state:** the separate EXIF-only ODM baseline has been launched without GCP control. At the latest recorded check, its real ODM execution step remained in progress; product inspection and artifact publication had not started. The GCP candidate has not been used in processing. No checkpoint residuals, positional accuracy statistics or acceptance decision exist.

### Next gate

1. Complete and lock the role-blind image-observation review.
2. Confirm the control/checkpoint split and the separate horizontal EPSG:2056 / vertical LN02 treatment.
3. Resolve and pin an ODM container digest; record the exact execution environment.
4. Run a no-GCP EXIF baseline, then the approved control-GCP variant. Keep all checkpoint observations out of adjustment and tuning.
5. Independently establish checkpoint image positions or document the limitations of reusing source Metashape picks.
6. Inspect outputs, produce validation evidence and assemble the acquisition-bound dossier. A successful processing exit code is not an accuracy or release decision.


The role-blind review packet is published separately from the technical audit artifact: [download from workflow run 44900854170](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44900854170/artifacts/14705374556). It contains 30 per-point sheets, 206 observation rows in the blank decision worksheet and no role mapping. Artifact SHA-256: `d9744c9f8d05019f8915b7d63f140f7f01143bc4cabe9f62a098737516e8f117`.


## 16. Locking the human image-observation review

The role-blind review packet contains 206 observation rows. Reviewers must record target visibility, identity, centring, blur, occlusion, ambiguity, a decision and a rationale for every row. `lock_visual_review.py` validates complete coverage, exact source pixel coordinates, timezone-aware review timestamps and the acquisition revision; it hashes all source evidence and produces a locked review record without reading the split key.

The lock record must remain `unblinded: false`. A single reviewer is explicitly labelled single-reviewer adjudication, not independent validation. Multiple names do not prove independent review. Do not inspect the proposed control/checkpoint mapping until the review record is locked.

# ODM end-to-end rehearsal plan

## Status

**Dataset acquisition, structural audit, role-blind review-material generation, the real-data EXIF-only ODM run and structural inspection of its principal products are complete. Human target review, independent checkpoint remeasurement and approval of the control/checkpoint split remain outstanding.**

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


## Formal control/checkpoint split approval

The proposed partition is not an approved split. After the complete 206-row role-blind review is locked, a human reviewer must inspect the proposed control/checkpoint geometry, image coverage, point suitability and withholding boundary. Complete `control-checkpoint-split-approval.template.json` only after that assessment.

The approval record must explicitly identify the approver and UTC approval time, bind itself to the exact locked-review and decision-CSV SHA-256 hashes, mark geometry and coverage acceptable, confirm control/checkpoint separation and checkpoint withholding, state the coordinate-reference review disposition, and provide a rationale. The approval utility also rejects any selected control/checkpoint point with questioned or rejected image observations. Revise or exclude such points before approval; do not override the observation decisions in the approval record.

Run:

```bash
python approve_control_checkpoint_split.py \\
  rehearsal-control-checkpoint-split.proposed.json \\
  review-decisions.completed.csv \\
  locked-visual-review.json \\
  control-checkpoint-split-approval.json \\
  approved-control-checkpoint-split.json
```

The utility emits `status: approved_locked` only when the human approval record and linked evidence pass validation. It does not independently assess geometry, prove reviewer independence, establish survey accuracy or authorize processing. The coordinate-reference and controlled-GCP implementation gates in this plan remain in force. Never edit the proposed file into an approved file manually; preserve both records and their hashes.

### Next gates

The EXIF-only baseline and structural product inspection are complete. The following gates remain before a controlled-GCP reconstruction or any positional-accuracy assessment:

1. Complete the 206-observation role-blind visual review. Record visibility, target identity, centring, blur, occlusion, ambiguity, decision and rationale for every observation.
2. Validate and lock the complete review worksheet with `lock_visual_review.py`. Keep the resulting record `unblinded: false` until the role-blind review is locked.
3. Only after locking the review, unblind the proposed partition, reassess point-level suitability, control/checkpoint geometry and image coverage, and formally approve or revise the split. Keep checkpoints out of adjustment and tuning.
4. Independently remeasure checkpoint image coordinates from original, unannotated images, following [the independent measurement protocol](independent-checkpoint-measurement-protocol.md). Do not consult or copy the publisher's Metashape picks, annotated overlays or supplied OPK solution. Preserve reviewer, method, timestamp and source-image hash.
5. Resolve horizontal LV95 (EPSG:2056) and vertical LN02 handling explicitly using [the coordinate-reference decision record](coordinate-reference-handling.md). The current GCP exporter passes LN02 numeric heights unchanged under a horizontal EPSG:2056 declaration; that is not a vertical transformation or a complete vertical CRS declaration.
6. Regenerate and audit a control-only GCP file from the approved controls, then run the controlled-GCP ODM variant using the pinned engine image.
7. Evaluate withheld checkpoints using independent image measurements and reference coordinates with compatible horizontal and vertical reference systems. Report reference uncertainty, sample design, residuals and limitations before making any acceptance decision.

The existing EXIF-only reconstruction is not a controlled-GCP experiment. Its successful execution and structurally readable products do not establish positional accuracy, and no controlled-GCP reconstruction or accuracy claim is authorised by the current evidence.

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

**Current processing state:** the EXIF-only ODM baseline completed with exit code 0, and a separate post-run inspection completed with status `inspected`, no blockers and no warnings. The initial combined workflow's inspection step failed because `pyproj` was missing; the outputs and run record were preserved, then successfully inspected in a follow-up workflow with the dependency installed. The GCP candidate has not been used in processing. No checkpoint residuals, positional accuracy statistics or acceptance decision exist.

### Historical workflow milestones

The earlier checklist below is superseded by the single authoritative **Next gates** sequence at the top of this plan. The completed EXIF-only baseline and product-inspection milestones remain recorded in [the dedicated baseline section](#17-exif-only-baseline-execution-and-output-inspection). Do not use this historical section to reorder the remaining gates: role-blind review must be locked before unblinding the proposed split, and checkpoint image coordinates must be independently remeasured from original images before any checkpoint accuracy assessment.


The role-blind review packet is published separately from the technical audit artifact: [download from workflow run 44900854170](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44900854170/artifacts/14705374556). It contains 30 per-point sheets, 206 observation rows in the blank decision worksheet and no role mapping. Artifact SHA-256: `d9744c9f8d05019f8915b7d63f140f7f01143bc4cabe9f62a098737516e8f117`.


## 16. Locking the human image-observation review

The role-blind review packet contains 206 observation rows. Reviewers must record target visibility, identity, centring, blur, occlusion, ambiguity, a decision and a rationale for every row. `lock_visual_review.py` validates complete coverage, exact source pixel coordinates, timezone-aware review timestamps and the acquisition revision; it hashes all source evidence and produces a locked review record without reading the split key.

The lock record must remain `unblinded: false`. A single reviewer is explicitly labelled single-reviewer adjudication, not independent validation. Multiple names do not prove independent review. Do not inspect the proposed control/checkpoint mapping until the review record is locked.


## 17. EXIF-only baseline execution and output inspection

A real ODM baseline was executed on the verified 32-image source copy with no GCP file and no OPK adjustment. OpenDroneMap 3.6.2 was resolved to image digest `sha256:a96f56dbc4f775e352fb2b3acc472bb59f456c0948a699eb1c433659dccfbdf7`. The processing record reports `succeeded` with exit code 0.

A separate post-run inspection using Rasterio, laspy, lazrs and pyproj reports `inspected`, with no blockers or warnings:

- Orthophoto: 9172 × 7801, 0.05 m pixels, EPSG:32632.
- DSM: 9172 × 7801, 0.05 m pixels, EPSG:32632.
- LAZ: 1,963,721 points; LAS 1.4, point format 7; finite coordinates; header count and observed count match; no points outside header bounds.
- LAZ class counts contain only class 0; intensity range is 0–0.
- LAZ CRS WKT parses but has no explicit EPSG authority identifier; its Transverse Mercator parameters are consistent with UTM 32N. Raster products explicitly declare EPSG:32632.

The initial combined workflow's output inspection was blocked by a missing optional `pyproj` dependency. The processing outputs and run record were preserved; the separate post-run inspection workflow installed pyproj and completed successfully. Future manual baseline runs now install pyproj before output inspection.

This is a successful real processing and structural-inspection baseline, not an accuracy assessment. The run used camera EXIF positions only. No surveyed GCPs or independent checkpoints were used; the camera altitude reference remains unresolved. The GCP-controlled run must wait until the role-blind human observation review is locked.

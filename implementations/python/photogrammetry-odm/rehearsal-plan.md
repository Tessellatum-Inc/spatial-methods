# ODM end-to-end rehearsal plan

## Status

**Dataset acquisition, structural audit and role-blind visual-review material generation are complete. Human target review, independent checkpoint remeasurement and ODM processing remain outstanding.**

### Verified evidence

- The [HEIG-VD real-data acquisition audit, run 7](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44899018230) completed successfully against publisher revision `e0dfeba2b6ed94ea1ae2bf773e742c39fb437b71`.
- All 36 files in the acquisition manifest passed byte-size and SHA-256 verification. All 32 source images decoded successfully at 5472 × 3648 pixels.
- The structural audit recorded 31 ground-point records, 206 image observations across 30 observed points, and 32 OPK records. It found no unmatched image references or out-of-bounds source observations, and documented the coincident/unobserved point 100/206 exception.
- The run generated 32 annotated image derivatives and two contact sheets. The review aid is **role-blind**: it reproduces the publisher-provided Metashape image picks but does not disclose which points are proposed controls or checkpoints. The [workflow artifact](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44899018230) contains provenance, audit reports, source metadata, the provisional GCP list and visual-review material; it does not contain the original source imagery.
- The photogrammetry package test suite passed after correcting a fixture whose sample pixel coordinate was exactly on the excluded lower image boundary (70, 80 for a 100 × 80 image). [Passing test run](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44899065601).

### What this evidence does and does not establish

Acquisition hashes establish local byte agreement with the recorded manifest, not publisher authenticity, licence compliance, coordinate correctness, photogrammetric suitability or product accuracy. Structural consistency does not establish that a marker is centred on the intended physical target.

The supplied image observations were measured in Metashape. They are not independent checkpoint measurements. The supplied OPK orientations also derive from a Metashape adjustment using ground points as control and are not independent validation.

The proposed split remains `proposed_not_locked`. The annotated sheets are a review aid, not a human approval record. Reviewers must inspect target visibility, centring, occlusion, blur, ambiguity and image-to-target correspondence; checkpoints must then be independently remeasured before they can support an accuracy assessment.

### Next gates

1. Complete a point-by-point, role-blind visual review of the annotated images and record explicit accept/reject/uncertain decisions with reasons.
2. Independently remeasure candidate checkpoint image coordinates without consulting the source Metashape picks. Preserve reviewer identity, method and measurement provenance.
3. Reassess control/checkpoint geometry and image coverage; only then lock the partition and regenerate the control-only ODM GCP file.
4. Explicitly resolve the horizontal LV95 (EPSG:2056) and vertical LN02 handling before interpreting ODM outputs.
5. Run a documented image-only baseline and a control-constrained ODM reconstruction; evaluate withheld checkpoints using independent observations. Do not use the supplied OPK solution as independent truth.

No ODM reconstruction or accuracy claim is authorised by the current evidence.

# HEIG-VD role-blind reviewer handoff

## Assignment

Review the 206 publisher-supplied image observations in the HEIG-VD 2019 drone dataset. The task is to decide whether each source pick plausibly identifies the same discrete, stable physical target across its available views, and whether the pick is visible, unambiguous and centred well enough to be considered usable.

This is a human visual quality-control exercise. It is not a survey-coordinate validation, independent checkpoint measurement, photogrammetric accuracy assessment or product acceptance.

**The control/checkpoint split is intentionally withheld from reviewers. Do not request, search for or inspect the proposed split file until the role-blind review has been locked.**

## Fixed source identity

- Publisher: HEIG-VD Geomatics group
- Dataset: [HEIG-VD photogrammetry and LiDAR datasets](https://huggingface.co/datasets/heig-vd-geo/scop-datasets)
- Selected subset: `datasets/drone_heig_2019`
- Immutable dataset revision: `e0dfeba2b6ed94ea1ae2bf773e742c39fb437b71`
- Licence: CC BY 4.0; preserve attribution to HEIG-VD Geomatics group.
- Source image dimensions: 5472 × 3648 pixels.
- Review packet: download the `heig-vd-role-blind-review` artifact from [the acquisition/audit workflow run](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44903003891).

The artifact contains review derivatives, the blank decision worksheet, a visual-review summary and acquisition provenance. It does **not** contain the original full-resolution source imagery. The reviewer must acquire the original dataset separately at the exact revision above.

## 1. Prepare the review workspace

Use Python 3.10+ and install the acquisition dependencies:

```bash
python -m pip install "huggingface_hub>=0.30,<2" "Pillow>=10,<13"
```

From a clean checkout of this repository, acquire the exact immutable dataset snapshot:

```bash
python implementations/python/photogrammetry-odm/acquire_rehearsal_dataset.py \
  ./review-data --revision e0dfeba2b6ed94ea1ae2bf773e742c39fb437b71
```

Verify the acquired source files:

```bash
python implementations/python/photogrammetry-odm/verify_acquisition.py \
  ./review-data/snapshots/e0dfeba2b6ed94ea1ae2bf773e742c39fb437b71/acquisition-provenance.json \
  --json-out ./review-data/acquisition-verification.json
```

Continue only if the verification report status is `verified` and all expected files are verified. This confirms local byte agreement with the manifest; it does not establish publisher authenticity or semantic correctness.

Extract the downloaded `heig-vd-role-blind-review` artifact into a separate review-packet directory. Keep the immutable source snapshot, packet derivatives and completed reviewer worksheet in separate locations.

## 2. Conduct the review

Use the contact sheets for navigation, the per-point sheets for point-level context, and the original full-resolution source images when the target or centre is unclear. Yellow rings and labels reproduce the publisher's Metashape picks. They are not new measurements.

Review every observation row, all 206 of them. Assess:

- **Visibility:** can the relevant target be seen?
- **Identity:** is the intended physical target identifiable rather than an approximate area or nearby object?
- **Centring:** is the publisher pick on the defined target centre, not simply close to the feature?
- **Blur/sharpness:** is there enough detail to identify the target and centre?
- **Occlusion:** is the target obscured by objects, vegetation, shadow or other features?
- **Ambiguity:** could the pick plausibly refer to another nearby feature?
- **Correspondence:** is the same physical point recognisable in the other images for that point?

Do not infer the intended target from a yellow ring alone. If the dataset does not provide enough evidence to identify a precise physical target, use `questioned` or `rejected` and explain why. Do not convert uncertainty into acceptance to preserve the proposed point count.

## 3. Complete the decision worksheet

Make a working copy of `review-decisions-template.csv` (or the generated `review-decisions-template.csv`). Preserve the header and the publisher source fields exactly.

For each row, complete every field:

- `target_visible`, `target_identity_clear`, `marker_centred`: `yes`, `no` or `uncertain`.
- `blur`, `occlusion`, `ambiguity`: describe the observed condition; do not leave blank.
- `decision`: exactly `accepted`, `questioned` or `rejected`.
- `rationale`: concise evidence-based reason for the decision. Explain all questioned and rejected rows explicitly.
- `reviewer`: stable reviewer identifier or name.
- `reviewed_at`: ISO 8601 timestamp with timezone, for example `2026-11-21T14:30:00+03:00`.

Do not change `point_id`, `image_name`, `pixel_x` or `pixel_y`. Those fields identify the publisher's observation under review; they are not independently measured coordinates.

For a stronger review, retain each reviewer's original worksheet separately. If multiple reviewers work independently, they should not see each other's decisions before submitting. A designated adjudicator can then produce one final, one-row-per-observation decision worksheet. Keep the independent submissions and adjudication rationale as supporting evidence. Multiple reviewer names in the final worksheet do not, by themselves, prove independent review.

## 4. Lock the final role-blind worksheet

Run the lock utility using the review packet's own summary and acquisition manifest, and write the output to a new file:

```bash
python implementations/python/photogrammetry-odm/lock_visual_review.py \
  ./review-packet/review-decisions.completed.csv \
  ./review-packet/visual-review-summary.json \
  ./review-packet/acquisition-provenance.json \
  ./review-submission/locked-visual-review.json
```

The utility checks complete 206-row coverage, unique point/image keys, unchanged source pixel coordinates, allowed decisions, required fields, timezone-aware timestamps and source revision consistency. It records hashes and keeps `unblinded: false`.

A successful lock means the worksheet is structurally complete and linked to the source packet. It does not certify reviewer competence, independent review, physical target identity or survey accuracy.

## 5. Submit the evidence

Return the following files to the project maintainer through the agreed private project channel:

1. `review-decisions.completed.csv`
2. `locked-visual-review.json`
3. Any separate independent reviewer worksheets, if used.
4. Any adjudication record and rationale, if multiple submissions were reconciled.
5. A short issue list for targets that could not be identified from the available evidence.

Do not include the proposed split, control/checkpoint role labels or a guessed role assignment in the reviewer submission. Do not upload original imagery unless specifically requested; the immutable public source revision and hashes identify the image set.

## 6. What happens after submission

The maintainer will verify the lock and evidence hashes. Only then may the split key be unblinded for a separate post-review assessment of point suitability, spatial distribution, control/checkpoint separation and image coverage. A named human approver must complete the separate split-approval record; the approval utility will reject any selected point with questioned or rejected observations.

Independent checkpoint pixel measurements are a later, separate activity. They must be made from original unannotated source images without consulting the publisher's Metashape picks, annotated overlays, point-review crops, supplied OPK solution or prior Metashape project. The visual-review worksheet is never a checkpoint measurement register.

## Review ethics and attribution

Preserve the source dataset attribution and CC BY 4.0 licence notice. Do not claim that visual review establishes ground-coordinate correctness or positional accuracy. Record uncertainty honestly, retain rejected observations and avoid silently editing the publisher's source data.

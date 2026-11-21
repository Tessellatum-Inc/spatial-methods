# HEIG-VD rehearsal review status

**Status date:** 2026-11-21  
**Overall state:** technical preparation complete; human review pending  
**Dataset:** HEIG-VD 2019 drone subset, `datasets/drone_heig_2019`  
**Pinned publisher revision:** `e0dfeba2b6ed94ea1ae2bf773e742c39fb437b71`

This page is the operational status record for the real-data photogrammetry rehearsal. It distinguishes completed automation from decisions that require human evidence. Update it when a reviewer submission, adjudication, approval or measurement set is actually received and verified.

## Current evidence

| Item | State | Evidence |
|---|---|---|
| Immutable dataset acquisition and SHA-256 verification | Passed | [Audit workflow run 44916839984](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44916839984) |
| Dataset/image/GCP/observation/OPK structural audit | Passed | Same audit run; audit evidence artifact below |
| Role-blind visual-review packet generation | Passed | [Download review packet](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44916839984/artifacts/14712292151) |
| Photogrammetry package tests | Passed | [Run 44918457083](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44918457083) |
| Python examples tests | Passed | [Run 44918456981](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44918456981) |
| Reviewer handoff and pinned acquisition instructions | Published | [Reviewer handoff](reviewer-handoff.md) |
| External reviewer invitation brief | Published | [Reviewer invitation](reviewer-invitation.md) |
| Human review of all 206 observations | **Pending** | No completed reviewer worksheet or review lock recorded |
| Role-blind review lock | **Pending** | Must follow completed human review |
| Control/checkpoint split approval | **Pending** | Proposed split is not approved |
| Independent checkpoint image measurements | **Pending** | No independent measurements recorded |
| Vertical reference disposition | **Pending** | LN02 handling must be explicitly resolved before controlled-GCP processing |
| Controlled-GCP ODM run | **Blocked** | Do not run before the preceding gates |
| Withheld-checkpoint accuracy assessment | **Blocked** | Requires independent measurements and compatible reference systems |

### Artifact identities

- Role-blind packet: `heig-vd-role-blind-review`, artifact ID `14712292151`.
- Packet SHA-256: `d68445bcbc98c868a3fe293da4b5441bb8fef34c92855f53c9a60845707671ec`.
- Technical audit evidence artifact: [`heig-vd-audit-evidence`](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44916839984/artifacts/14712123031).
- Both artifacts are GitHub Actions artifacts and expire on 2026-12-21 unless retained elsewhere.

The role-blind packet contains review derivatives and the blank decision worksheet, not the original full-resolution imagery. Reviewers must acquire and verify the original images at the pinned publisher revision using the instructions in [reviewer-handoff.md](reviewer-handoff.md).

## Required sequence

1. **Conduct role-blind visual review.** Review every one of the 206 publisher observation rows. Retain original submissions if multiple reviewers work independently.
2. **Adjudicate and lock.** Produce one final row per observation, preserve disagreements and rationale, then run `lock_visual_review.py`. Keep the lock `unblinded: false`.
3. **Unblind and assess the proposed split.** Only after the lock is verified, inspect point suitability, spatial distribution, control/checkpoint separation and image coverage. Revise the proposed split if evidence requires it.
4. **Obtain named human approval.** Complete the split-approval record and run `approve_control_checkpoint_split.py`. Approval must be based on actual review evidence and an explicit geometry/coverage assessment; the utility does not perform those judgements.
5. **Measure checkpoints independently.** Use original unannotated images and the independent measurement protocol. Do not consult publisher Metashape picks, annotated derivatives, supplied OPK or prior Metashape project. Validate the complete checkpoint observation register.
6. **Resolve coordinate references.** Document the horizontal and vertical reference treatment, including LN02. Do not silently reinterpret or transform heights.
7. **Run controlled-GCP processing and evaluate withheld checkpoints.** Only after all preceding gates pass. Report structural output checks separately from positional accuracy.

## Decision boundaries

- The proposed control/checkpoint split is a hypothesis, not an approved design.
- Visual review assesses image-observation usability; it does not establish surveyed coordinate correctness.
- A successful lock validates worksheet structure, provenance links and required fields; it does not prove reviewer independence or competence.
- A successful split-approval utility run records a human decision; it does not independently establish geometric adequacy or accuracy.
- Independent checkpoint measurement validation checks register completeness and provenance; it does not prove that a person actually measured independently or identified the correct physical target.
- The completed EXIF-only ODM baseline is not a controlled-GCP experiment and is not an accuracy assessment.
- No accuracy, survey-quality or product-acceptance claim is authorised by the current evidence.

## Submission and update procedure

When evidence arrives:

1. Preserve original reviewer files unchanged and record who supplied them and when.
2. Verify the acquisition revision, packet identity and hashes before processing submissions.
3. Record disagreements and adjudication; do not overwrite source submissions.
4. Run the relevant validator and retain its JSON report and command/version context.
5. Update the table above with the evidence URL, artifact ID/hash and actual status. Never mark a gate complete based only on a workflow being green.
6. If any observation or point is questioned/rejected, document the disposition and reassess whether the proposed split remains defensible.

**Current next action:** identify and invite qualified reviewers using [reviewer-invitation.md](reviewer-invitation.md), then provide the [reviewer handoff](reviewer-handoff.md) and [role-blind packet](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44916839984/artifacts/14712292151) to qualified reviewers. No automated process should fabricate or infer their decisions.

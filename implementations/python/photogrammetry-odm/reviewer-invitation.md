# HEIG-VD photogrammetry rehearsal — reviewer invitation

## Invitation

We are seeking qualified photogrammetry / geomatics reviewers to independently assess the image observations in a small, real-world drone-photogrammetry dataset from HEIG-VD (Yverdon, Switzerland).

The purpose is to establish whether the published image observations are visually usable before we designate any ground points as processing controls or withheld checkpoints. This is a methods-validation exercise, not a request to endorse a processing result or certify survey accuracy.

### What the review involves

- Review all 206 supplied point-to-image observations across the 32-image dataset.
- Assess target visibility, target identity, centring, blur, occlusion and ambiguity.
- Mark each observation as `accepted`, `questioned` or `rejected`, with rationale for questioned or rejected observations.
- Record reviewer identity and timezone-aware review timestamps.
- Work role-blind: do not seek or infer which points are proposed controls versus checkpoints.
- Use the original, unannotated, full-resolution images when needed to resolve ambiguous targets.

The supplied review packet contains navigation derivatives and a blank decision worksheet; it does not contain the original full-resolution imagery. The dataset must be acquired from the pinned source revision using the handoff instructions.

### Materials

1. [Operational reviewer handoff](reviewer-handoff.md) — acquisition, verification, review procedure and submission requirements.
2. [Role-blind review packet](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44916839984/artifacts/14712292151) — blank worksheet and review materials. This artifact is scheduled to expire on 21 December 2026.
3. [Visual review protocol](visual-review-protocol.md) — assessment criteria and field definitions.
4. [Review status and gate record](REVIEW-STATUS.md) — current evidence and the sequence of decisions still pending.

### Dataset and attribution

- Source: HEIG-VD Geomatics group, `heig-vd-geo/scop-datasets`
- Subset: `datasets/drone_heig_2019`
- Pinned source revision: `e0dfeba2b6ed94ea1ae2bf773e742c39fb437b71`
- Licence: CC BY 4.0; retain attribution to the HEIG-VD Geomatics group.

### Independence and decision boundaries

Please complete the review without consulting the publisher's Metashape image-pick file, supplied OPK orientations, annotated image derivatives as a substitute for source imagery, or any prior Metashape project. The annotations in some packet derivatives reproduce the publisher's picks and are for navigation only.

This review evaluates image-observation usability. It does not establish the correctness of ground coordinates, reviewer independence by itself, photogrammetric accuracy, or product acceptance. No control/checkpoint split has been approved. No controlled-GCP processing or accuracy claim is authorised at this stage.

### Submission

Please return:
- your completed observation decision worksheet;
- reviewer identity and review date/time information as required by the worksheet;
- any separate notes or issue list explaining difficult targets or systematic concerns.

Do not edit the source dataset or overwrite another reviewer's submission. If multiple reviewers participate, their original submissions will be preserved and disagreements adjudicated transparently. The final consolidated worksheet will be validated and locked before the proposed point-role split is revealed.

**Contact / submission destination:** to be agreed directly with the project coordinator before review begins. Do not upload reviewer files to a public issue or public repository location.

Thank you for contributing specialist scrutiny to a reproducible, evidence-led photogrammetry methods exercise.

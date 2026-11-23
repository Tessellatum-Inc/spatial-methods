# External reviewer recruitment and intake

## Purpose

Recruit suitably experienced reviewers for the HEIG-VD role-blind image-observation review. This document governs reviewer selection, independence safeguards, secure handoff and intake. It does not change the technical review protocol or approve the proposed control/checkpoint split.

## Recommended review design

Use **two reviewers working independently** through the complete 206-observation worksheet, followed by a separately documented adjudication of disagreements. If a second reviewer cannot be secured, a single-reviewer review may still be recorded as a limited usability assessment, but it must not be described as independent validation or multi-reviewer consensus.

Where feasible, appoint an adjudicator who did not perform either initial review. The adjudicator should resolve only the disputed observations using the original unannotated imagery and recorded rationales. Preserve both original submissions unchanged; never merge them by overwriting one reviewer's file.

## Reviewer suitability

Seek people with demonstrable experience in one or more of:

- close-range or aerial photogrammetry and image-based measurement;
- geomatics surveying, ground-control identification or photogrammetric QA;
- interpretation of small ground targets in high-resolution UAV imagery;
- quality assurance of image observations and measurement uncertainty.

Prior experience with this exact HEIG-VD dataset is not required and should be disclosed. A reviewer should be able to explain how they distinguish a visible target from a merely plausible location and when an observation should be marked uncertain.

Do not select solely on job title, academic seniority or institutional affiliation. Record a short, factual basis for suitability (relevant role, project experience, publications, or practical work) without collecting unnecessary personal information.

## Independence and conflict-of-interest disclosure

Before granting access, ask each reviewer to disclose:

1. prior work with this dataset, its publisher-supplied Metashape project, image picks or OPK file;
2. involvement in preparing the proposed point partition, GCP selection or this rehearsal's processing;
3. any financial, supervisory, authorship or close collaboration relationship that could reasonably affect impartiality;
4. whether they can complete the review without consulting the publisher's source pixel picks, supplied OPK orientations or prior Metashape project.

A disclosed connection does not automatically disqualify someone. The coordinator records the disclosure and decides whether to exclude the reviewer from the independent-review role, retain them as a specialist adviser, or proceed with a documented limitation. Do not describe a review as independent if the reviewer has seen or used the prohibited measurements or role mapping.

## Role-blind safeguards

- Do not share the proposed control/checkpoint split or point-role mapping before the consolidated review is locked.
- Give every reviewer the same pinned dataset revision, packet version, protocol and blank worksheet schema.
- Keep the reviewer packet free of point-role labels.
- Ask reviewers not to search repository history or other project files for the split.
- Do not share another reviewer's decisions before independent submissions are complete.
- Keep the coordinator's role separate from observation decisions wherever practical.
- Record any accidental unblinding or exposure; assess its effect rather than silently continuing.

The packet's annotated derivatives reproduce publisher-supplied picks and are navigation aids only. Original unannotated full-resolution images govern difficult or ambiguous decisions.

## Invitation and intake sequence

1. Send [reviewer-invitation.md](reviewer-invitation.md) privately to prospective reviewers.
2. Confirm interest, relevant experience, availability and any compensation/expenses before sharing project materials. No compensation is implied by the invitation.
3. Collect the conflict-of-interest and prior-exposure disclosures above.
4. Assign a neutral reviewer code (for example, `R01`, `R02`) for worksheet tracking. Keep the identity-to-code key private.
5. Provide the same [operational handoff](reviewer-handoff.md), pinned source revision and [review packet](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44916839984/artifacts/14712292151).
6. Agree a private transfer channel and submission deadline directly with each reviewer. Do not ask reviewers to upload completed worksheets to public GitHub issues, pull requests or repository commits.
7. Confirm receipt and hash each original submission before opening or adjudicating it.
8. Once independent submissions are complete, compare decisions, preserve disagreements, adjudicate, and create the final 206-row decision worksheet.
9. Validate and lock the final worksheet while keeping `unblinded: false`.
10. Only then may the coordinator reveal the proposed split and proceed to the separate geometry/coverage assessment and human approval gate.

## Submission package

Each reviewer submits:

- completed 206-row decision worksheet in the canonical CSV schema;
- a short reviewer note identifying relevant experience and any limitations;
- a list of observations that were difficult to interpret, if any;
- confirmation that the original unannotated images were used where needed;
- disclosure of any prohibited source material accidentally consulted or any role exposure.

The coordinator records receipt time, reviewer code, original filename, byte size and SHA-256. Preserve the original bytes read-only. Do not silently correct a reviewer's entries; return a query to the reviewer or record the correction in the adjudication log.

## Minimal intake register

Maintain a private register with these fields:

| Field | Purpose |
|---|---|
| Reviewer code | Pseudonymous worksheet identity |
| Reviewer identity | Private coordinator-only key |
| Relevant experience summary | Basis for suitability |
| Dataset/project prior exposure | Independence assessment |
| Conflict disclosure | Potential bias or role conflict |
| Role exposure status | None / accidental / prior |
| Materials and packet version | Equal treatment and reproducibility |
| Invitation and acceptance dates | Audit trail |
| Submission received at | Intake chronology |
| Original submission SHA-256 | Immutable identity |
| Review status | Invited / accepted / reviewing / submitted / queried / closed |
| Coordinator disposition | Include / specialist-only / exclude, with rationale |

Do not place private contact details, identity documents, signatures or unnecessary personal information in the public repository. Keep the identity key and original worksheets in access-controlled storage.

## Adjudication rules

- Compare the two independent submissions observation by observation.
- Agreement does not prove the target identity or measurement accuracy; it is evidence of reviewer agreement only.
- Any accept/questioned/rejected disagreement must be explicitly resolved or remain questioned.
- Preserve each original decision, rationale and reviewer code.
- Record adjudicator, UTC timestamp, evidence consulted, final decision and rationale.
- A questioned or rejected observation affecting a proposed selected point blocks automatic split approval under the current approval utility.
- Do not change the proposed split merely to make the review pass. Reassess the point selection and geometry on their merits after the review lock.

## Data handling and publication

The source subset is published under CC BY 4.0; retain attribution to the HEIG-VD Geomatics group. The review packet is a generated derivative and does not include the full-resolution source imagery. Reviewers must acquire the pinned public source snapshot using the handoff instructions.

Completed worksheets may identify reviewers and contain review notes. Keep them private unless reviewers explicitly agree to publication and the coordinator has reviewed the disclosure implications. Publish only the minimum evidence needed to make the methods and decision trail auditable. Do not publish private contact details or confidential correspondence.

## Current state

No external reviewer has been recruited or submitted a worksheet as of this document's creation. This plan is operational guidance, not evidence that recruitment or review has occurred. The proposed split remains unapproved, and controlled-GCP processing remains blocked.

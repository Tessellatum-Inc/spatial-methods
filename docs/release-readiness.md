# Release readiness and completion ledger

**Snapshot:** 18 November 2026  
**Repository:** `geo-dev-hub/spatial-analysis`  
**Working branch:** `completion/section-22-atomic-audit`  
**Integration target:** `main`  
**Pull request:** [#3](https://github.com/geo-dev-hub/spatial-analysis/pull/3) — draft, open, unmerged

This file is the release-gate record. It deliberately distinguishes a healthy software build from completion of the source compendium. A green CI run is necessary, but it is not evidence that the source bibliography, technical claims or reuse rights have been verified.

## Current engineering checkpoint

- Branch head at this update: `791fea00ddf79933cd5e7c573326078e2280352d`.
- The historical 58/58 workflow run [44208356316](https://github.com/geo-dev-hub/spatial-analysis/actions/runs/44208356316) is green, but is **not** the current-head run.
- Current-head workflow run [44221714064](https://github.com/geo-dev-hub/spatial-analysis/actions/runs/44221714064) returned **30 jobs, all 30 successful**. This observed page includes Python package shards, notebook shards, Clipper2 checks and the internal-link/catalogue/CI-checker job.
- The 30/30 result is not evidence that every workflow required by the earlier 58-job run has completed on this head. Exact-head CI remains **partially confirmed**, not fully green. The latest combined commit-status endpoint returned no status entries. Any later source change requires another exact-head run before release.

## Source-review checkpoint

The current [source review dashboard](../catalog/review-dashboard.md), recalculated from all 22 section indexes on 18 November 2026, records:

| Review label | Entries |
|---|---:|
| Total source-entry rows | 695 |
| Partial | 306 |
| Intake only / not checked | 389 |
| Fully verified | 0 |

These are source-entry review labels, not implementation counts or a completion percentage. A partial row can point to a tested implementation while still lacking complete identity, bibliography, technical-claim or rights review. Grouped entries may need to be split into multiple canonical child records.

## Decisions already made

- Original code, tests, scripts and executable examples: Apache-2.0.
- Original explanatory prose, tutorials, exercises, narrative notebook content and project-created diagrams: CC BY 4.0.
- Future contributions: DCO 1.1 sign-off on each contribution commit.
- Third-party material and the preserved source transcription are excluded from blanket project licensing unless the specific reuse basis is established.
- The GitHub archive remains the complete public technical resource. Patreon may sell guided learning, curation, support and community services; it must not imply exclusive rights over material already released under public licences.

See [licensing and reuse](licensing-and-reuse.md), the [licensing decision record](licensing-decision-proposal.md), [licence scope register](../LICENSES.md) and [compendium provenance](compendium-provenance.md).

## Release gates

| Gate | Current state | Evidence required to close |
|---|---|---|
| Preserve all 47 source pages and 22 sections | Complete | Source transcription and section indexes remain intact |
| Keep catalogue dashboard reconciled | Complete at this snapshot | Automated recount passes on the release candidate |
| Resolve identity and grouped source entries | Open | Each source entry is split where needed and linked to authoritative identities or explicitly retained as ambiguous/not found |
| Verify bibliography | Open | Primary or authoritative records for each applicable child entry |
| Check technical claims | Open | Equations, assumptions, guarantees, units, variants and limitations checked against primary evidence |
| Reconcile canonical lessons and implementations | In progress | Every in-scope child has an appropriate treatment and an explicit bounded scope |
| Verify third-party reuse rights | Open | Per-asset licence/permission records; remove or link-only where rights are unclear |
| Code and notebook CI | Passed at recorded head | Re-run on the exact release candidate after all changes |
| DCO policy for future contributions | Implemented | DCO checker and tests remain green; historical PR #3 is explicitly exempt from retroactive sign-off |
| Rendered navigation and heading anchors | Open | Rendered-site link/anchor audit |
| Mobile and assistive-technology review | Open | Phone-sized layout, keyboard navigation and screen-reader review |
| Release metadata and public edition scope | Open | Versioned release notes, changelog, scope statement and final sign-off |

## Integration policy

1. Continue substantive work on `completion/section-22-atomic-audit` while PR #3 remains the review and integration vehicle.
2. Do not rewrite historical commits merely to retrofit DCO sign-offs. The policy applies prospectively.
3. Do not merge the 217-commit branch into `main` merely because CI is green. The source-review, rights and publishing-accessibility gates remain material.
4. Before integration, reconcile the branch's final dashboard, roadmap, README, licence notices and release notes against the exact tree.
5. Once the gates required for the declared public edition are satisfied, mark PR #3 ready for review, obtain the required review, and merge it into `main`. The merged `main` commit becomes the authoritative release candidate.
6. Run the full workflow on that exact `main` commit, tag the verified release, and keep later work in normal reviewed pull requests.

## What “complete” means

There are two different milestones and they must not be conflated:

- **Engineering foundation complete:** the repository structure, extension rules, licence model, CI, tested implementation conventions and public learning pathways are stable enough for ongoing additions and maintenance.
- **Full compendium review complete:** every source entry and its applicable child records have completed identity, bibliography, technical-claim, implementation/reproduction and rights review, with the public learning experience checked.

The first milestone can be achieved before the second. The repository must not claim the second while the dashboard still reports zero fully verified source entries. New algorithms and implementations can continue to be added through the extension protocol without weakening that standard.

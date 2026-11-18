# Release readiness and completion ledger

**Snapshot:** 18 November 2026  
**Repository:** `Tessellatum-Inc/spatial-methods`  
**Integration target:** `main`  
**Latest main commit:** `335ee479a0b6f9cc088da9a29c1fbea641dd0503` — Fix broken global autocorrelation links

This is the single release-gate record. It distinguishes a maintainable engineering foundation from complete source-entry verification. Closeout is focused on concrete release blockers, not repeated broad audits.

## Current engineering checkpoint

- PR #3 (compendium foundation), PR #4 (Patreon launch foundation), and PR #6 (Spatial Methods identity) are merged.
- PR #5 was superseded by PR #6. PR #2's Bowyer–Watson work was completed within the compendium foundation; do not reopen the stale branch.
- The README is restored to its original welcoming Spatial Analysis text with only the heading renamed to Spatial Methods. Standalone logo removed. Its navigation and links remain.
- Latest main workflow [44278892636](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44278892636) completed successfully on 18 November 2026, following the latest main commit. It verifies the configured Python examples workflow; it does not replace the broader full-workflow evidence recorded below.
- Patreon pathway is updated to the current Spatial Methods URL in the README and issue-template contact configuration.
- The earlier 58/59-job CI result and link/anchor integrity checks remain historical evidence for the prior candidate, not a fresh count for this commit.

## Source-review checkpoint

The [source review dashboard](../catalog/review-dashboard.md) last recorded 695 source-entry rows on 18 November 2026:

| Review label | Entries |
|---|---:|
| Total source-entry rows | 695 |
| Partial | 306 |
| Intake only / not checked | 389 |
| Fully verified | 0 |

These are source-entry review statuses, not repository completion percentages. Entries may link to lessons or implementations while identity, bibliography, technical claims, reproduction or rights review remains incomplete. Preserve uncertainty labels; do not promote entries without evidence.

## Decisions already made

- Original code, tests, scripts and executable examples: Apache-2.0.
- Original explanatory prose, tutorials, exercises, narrative notebook content and project-created diagrams: CC BY 4.0.
- Future contributions: DCO 1.1 sign-off on each contribution commit; do not rewrite historical commits retroactively.
- Third-party material and the preserved source transcription are excluded from blanket project licensing unless a specific reuse basis is established.
- The public repository is the technical resource. Patreon may sell guided learning, curation, support and community services—not exclusive rights over publicly licensed material.

See [licensing and reuse](licensing-and-reuse.md), [licensing decision record](licensing-decision-proposal.md), [licence scope register](../LICENSES.md) and [compendium provenance](compendium-provenance.md).

## Release candidate notes

Draft versioned notes: [Engineering Foundation 0.1.0](releases/engineering-foundation-0.1.0.md). This is scope documentation, not a published release or tag.

## Closeout

### Stabilization — complete based on recorded evidence

- [x] Repository foundation and major integration work merged.
- [x] Python/package tests, notebooks, Clipper2 checks and integrity checks passed on the prior candidate (recorded as 58 successful, 0 failed, 1 expected skip).
- [x] Markdown/notebook link and heading-anchor checks are wired into CI.
- [x] README identity correction restored and committed on main.
- [x] Freeze feature additions unless a release-critical defect is found.

### Closure — remaining bounded tasks

- [ ] Reconcile final release notices, scope statement and release notes against the current main tree.
- [ ] Keep unverified source claims and uncertain third-party material clearly labelled or excluded/link-only.
- [ ] Review clean-install/setup instructions and obvious packaging/navigation defects; fix only confirmed defects.
- [ ] Conduct a focused rendered/mobile/accessibility pass; report limitations honestly.

### Release decision — pending

- [ ] Run the complete CI workflow on the exact release candidate after closure edits.
- [ ] Confirm license/attribution exclusions and bounded release scope.
- [ ] Make a single release decision: tag the public engineering foundation or defer for one named material blocker.

## Gates

| Gate | State | Release rule |
|---|---|---|
| 47-page source preservation and 22-section navigation | Complete | Preserve the source record |
| Catalogue/dashboard structure | Established; status snapshot dated 18 Nov | Recount once at release candidate |
| Python examples, notebooks, CI and checks | Prior candidate passed; latest README workflow green | Run exact candidate once; fix failures only |
| Implementation scope and limitations | In place, uneven coverage | Keep teaching-baseline/bounded labels |
| Source identity and bibliography across all entries | Open | Keep unknowns explicit; not a foundation-release blocker unless public claims mislead |
| Technical claims across all entries | Open | Do not claim full verification; continue as research backlog |
| Third-party asset rights | Open | Remove, replace or link-only unclear material; retain exclusions |
| Transcription rights | Open | Keep source transcription outside blanket licence |
| Rendered/mobile/accessibility review | Open | Fix obvious critical defects; no certification claims |
| Release notes, scope and version | Pending | Finish bounded release notes and explicit scope |

## Integration policy

1. Work on concrete closure items only.
2. No new methods, feature work, broad research sweeps or speculative cleanup during release closeout.
3. Isolate unclear rights material rather than starting an unbounded legal review.
4. Do not merge or tag solely because CI is green; complete the stated scope and review.
5. Run full CI on the exact release candidate, tag that verified commit, and handle later additions through normal reviewed changes.

## Completion definitions

- **Engineering foundation release:** the 22-section structure, extension rules, licence boundaries, tested examples, CI, catalogue integrity and public learning paths are stable for ongoing maintenance. Unverified source rows and rights-excluded content remain clearly labelled and are not presented as validated or licensed.
- **Full compendium verification:** all 695 source-entry rows and their child records receive identity, bibliography, technical-claim, implementation/reproduction and rights reviews. This is a long-term research programme, not a prerequisite for a transparent foundation release.

Closeout targets the engineering foundation. Full source verification must not become an indefinite release blocker.

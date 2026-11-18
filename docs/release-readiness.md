# Release readiness and completion ledger

**Snapshot:** 18 November 2026  
**Repository:** `geo-dev-hub/spatial-analysis`  
**Working branch:** `completion/section-22-atomic-audit`  
**Integration target:** `main`  
**Pull request:** [#3](https://github.com/geo-dev-hub/spatial-analysis/pull/3) — draft, open, unmerged

This is the single release-gate record. It distinguishes an engineering-ready foundation from complete source-entry verification. The project is no longer in its build phase; remaining work is stabilization, closure, and a release decision. Do not reopen broad audits without a concrete defect or release blocker.

## Current engineering checkpoint

- Current head before this ledger update: `a9aae51ee2eefd9c9fe50a47f2cd0c046c2e7994`.
- Current-head PR workflow [44227052820](https://github.com/geo-dev-hub/spatial-analysis/actions/runs/44227052820) completed: **58 of 59 jobs succeeded; 0 failed; 1 skipped**. The skipped job was contributor-sign-off verification, which is not applicable to this PR event. The separate push workflow [44227046308](https://github.com/geo-dev-hub/spatial-analysis/actions/runs/44227046308) also succeeded on the same head.
- The passing matrix covers the repository's isolated Python-package tests, notebook execution, Clipper2 checks and integrity checks. It is CI evidence, not proof that every method in the source compendium is technically verified.
- Latest changes included internal-link/anchor checking and numeric overflow guards for Hansen–Hurwitz. No additional code changes are required by the current CI result.

## Source-review checkpoint

The current [source review dashboard](../catalog/review-dashboard.md), recounted from all 22 section indexes on 18 November 2026:

| Review label | Entries |
|---|---:|
| Total source-entry rows | 695 |
| Partial | 306 |
| Intake only / not checked | 389 |
| Fully verified | 0 |

These counts describe source-entry status, not repository completion percentages. Many entries point to lessons, implementations, or related records, but their complete identity, bibliography, technical-claim, or rights review remains incomplete. The dashboard is transparent about this and must not be changed to imply verification that has not occurred.

## Decisions already made

- Original code, tests, scripts and executable examples: Apache-2.0.
- Original explanatory prose, tutorials, exercises, narrative notebook content and project-created diagrams: CC BY 4.0.
- Future contributions: DCO 1.1 sign-off on each contribution commit; do not rewrite historical commits to retroactively add sign-offs.
- Third-party material and the preserved source transcription are excluded from blanket project licensing unless a specific reuse basis is established.
- The public repository is the technical resource. Patreon may sell guided learning, curation, support and community services—not exclusive rights over publicly licensed material.

See [licensing and reuse](licensing-and-reuse.md), [licensing decision record](licensing-decision-proposal.md), [licence scope register](../LICENSES.md) and [compendium provenance](compendium-provenance.md).

## Three-batch closeout

### Batch 1 — Stabilization: complete

- [x] Latest head's CI passes (58 success; 1 expected skip; no failures).
- [x] Internal Markdown/notebook link and heading-anchor checks are wired into CI.
- [x] Recent implementation fixes are included.
- [x] Freeze feature additions unless a release-critical defect is discovered.

### Batch 2 — Closure: in progress

- [ ] Reconcile README, catalogue/dashboard, licence notices and release notes to the final head.
- [ ] Keep uncertain source claims clearly labelled as unverified; do not inflate source verification statuses.
- [ ] Keep questionable third-party material out of the licensed public release or link to it only.
- [ ] Close obvious navigation, setup, packaging, or documentation defects found in the consolidated pass.
- [ ] Publish a bounded-scope release note and clear extension/maintenance instructions.

### Batch 3 — Release decision: pending

- [ ] One consolidated final checklist on the exact release candidate; no audit loops.
- [ ] Confirm CI green on exact candidate.
- [ ] Confirm release-scope statement, attribution and rights exclusions.
- [ ] Decide whether to merge and tag a public **engineering foundation release** or defer for a named material blocker.

## Gates and how they will be handled

| Gate | State | Closeout rule |
|---|---|---|
| 47-page source preservation and 22-section navigation | Complete | Preserve as source record; no scope loss |
| Catalogue/dashboard reconciliation | Complete at current snapshot | Recount once on release candidate |
| Python examples, notebooks, CI and checks | Passed on current head | Re-run after final changes; fix failures only |
| Implementation scope and limitations | In place, uneven coverage | Preserve bounded/teaching-baseline labels; don't promise production readiness |
| Source identity and bibliography across all entries | Open | Transparently retain unknown/ambiguous items; do not block engineering-foundation release unless public claims mislead |
| Technical claims across all entries | Open | Do not label fully verified; queue future verification work |
| Third-party asset rights | Open | Remove, replace or link-only any unclear third-party material in the release; retain exclusions |
| Transcription rights (47-page source) | Open | Keep excluded from blanket licensing; revisit only if a rights-cleared edition is intended |
| Rendered/mobile/accessibility review | Not yet complete | Fix obvious and critical usability defects in the final pass; disclose any unperformed review, don't claim certification |
| Release notes, scope and version | Pending | Complete in closeout, with an explicit foundation-release scope |

## Integration policy

1. Work only on concrete closure items on this branch.
2. Avoid new methods, features, broad research sweeps, or speculative cleanups during closeout.
3. If a rights concern is identified, remove or isolate the material from the release rather than expanding into a legal research loop.
4. Once the declared engineering-foundation gates are met, mark PR #3 ready for review and merge only after the required review and release decision. Do not merge solely on a green CI result.
5. Run the full workflow on the exact merged `main` commit, tag that verified candidate, and handle later additions through normal reviewed PRs.

## Completion definitions

- **Engineering foundation release:** the 22-section structure, extension rules, licence boundaries, tested examples, CI, catalogue integrity and public learning pathways are stable enough for ongoing maintenance and additions. Unverified source rows and rights-excluded content are clearly labelled and not presented as validated or licensed.
- **Full compendium verification:** all 695 source-entry rows and their child records receive appropriate identity, bibliography, technical-claim, implementation/reproduction and rights reviews. This is a separate long-term research programme—not a prerequisite for releasing a transparent engineering foundation.

The closeout is explicitly aimed at the first milestone. Do not let the second milestone turn into an indefinite release blocker.

# Verification work queue — long-term research backlog

Snapshot: 18 November 2026

This is a prioritised research backlog, **not a release checklist**. The engineering-foundation release can proceed with the current explicit uncertainty labels and rights exclusions. This queue governs future source verification; it does not justify reopening completed engineering work. Status is defined by the [source-entry verification protocol](../catalog/verification-protocol.md) and [review dashboard](../catalog/review-dashboard.md).

**Structural crosswalks:** [Catalogue alignment audit](catalogue-alignment-audit.md) and crosswalk batches [1](../catalog/catalogue-crosswalk-batch-1.md), [2](../catalog/catalogue-crosswalk-batch-2.md), [3](../catalog/catalogue-crosswalk-batch-3.md), and [4](../catalog/catalogue-crosswalk-batch-4.md). These resolve documented aliases and implementation mappings; they do not claim exhaustive source or orphan verification.

## Work rules

- Keep the original source label and page provenance intact.
- Split grouped labels into child records when methods, variants, or rights differ.
- Record primary evidence and the exact claim checked; a DOI/title lookup alone does not verify technical claims.
- Label teaching baselines, library wrappers and reproductions accurately; passing tests do not certify production readiness.
- Rights checks are independent. If reuse is unclear, link to the source rather than copying.
- Update source-entry labels and the dashboard only after evidence has been collected and reviewed.

## Priority backlog

### A — Source identity and reconciliation
1. Resolve ambiguous names and alias relationships.
2. Split multi-method entries into reviewable children while preserving parent groupings.
3. Retain ambiguous or untraceable names as unresolved rather than guessing.
4. Reconcile children with lessons, implementations, tests, notebooks and external references.

### B — Technical review, prioritised by reuse and risk
1. Geometry and overlay: boundary conventions, precision, robustness.
2. Spatial indexes: invariants, operations, complexity and workload assumptions.
3. Network methods: directedness, weight semantics, admissible heuristics and tie rules.
4. Raster: grid alignment, NoData, units, neighbourhood and resampling semantics.
5. Spatial statistics: weights, null models, edge correction, estimands, inference and multiple testing.

### C — Bibliography and rights
- Verify authoritative bibliographic records for foundational methods.
- Verify third-party code, data and figures individually.
- Remove, replace or link-only assets with unclear rights.
- Record stable evidence URLs/DOIs and access dates.

### D — Learning and reproducibility improvements
- Review rendered navigation, mobile layout, keyboard use, screen-reader structure and alt text.
- Test clean-environment setup for packages as changes warrant.
- Keep notebooks reproducible, ordered and free of hidden-state dependence.
- Improve issue templates, contribution guidance and licence notices when needed.

## Backlog handling

Do this work opportunistically as contributors, readers, users or new releases surface needs. Do not conduct another broad audit merely to refresh the table. Verify specific records in small, evidence-backed batches and retain the distinction between source preservation, technical verification and reuse rights.

**Release boundary:** this queue does not block the declared engineering-foundation milestone. The release ledger identifies the actual closeout gates.

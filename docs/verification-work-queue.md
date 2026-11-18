# Verification work queue — Batch 1

Snapshot: 18 November 2026

This is a prioritisation queue for a practical verification sprint, not a claim that these topics have been verified. Status remains governed by the [source-entry verification protocol](verification-protocol.md) and the [review dashboard](review-dashboard.md).\n\n**Structural audits:** [Catalogue alignment audit — Batch 1](catalogue-alignment-audit.md) and three README-level crosswalk batches ([Batch 1](../catalog/catalogue-crosswalk-batch-1.md), [Batch 2](../catalog/catalogue-crosswalk-batch-2.md), [Batch 3](../catalog/catalogue-crosswalk-batch-3.md)). These reconcile confirmed aliases and record unresolved package-name questions; they are not complete orphan audits.

## Work rules

- Keep the source's original label and provenance intact.
- Split grouped labels into child items before verification when different methods, variants, or rights apply.
- Record primary evidence and the exact claim checked; a DOI/title lookup alone does not verify technical claims.
- Use teaching-baseline, library-wrapper, or reproduction labels accurately; passing tests does not certify production readiness.
- Rights checks are separate. Where reuse is not clear, link to the source rather than copying.
- Update section-index statuses and the dashboard only after evidence is collected and reviewed.

## Priority batches

### Batch A — identity and source cleanup
1. Resolve obvious duplicate names and alias relationships across all 22 sections.
2. Split multi-method source rows into individual children, preserving parent grouping.
3. Flag ambiguous, unavailable, or untraceable names as unresolved instead of guessing.
4. Reconcile each child with existing lessons, implementations, tests, and notebooks.

### Batch B — foundational claims and high reuse
1. Geometry predicates and overlay families: contracts, boundary conventions, precision and robustness.
2. Spatial indexing and query structures: invariants, supported queries, workload assumptions.
3. Graph and network methods: directedness, weight semantics, admissible heuristics and tie rules.
4. Raster methods: grid alignment, NoData propagation, units, neighbourhood definitions and resampling semantics.
5. Spatial statistics: weights, null models, edge corrections, estimands, inference and multiple testing.

### Batch C — citations and rights
- Verify primary bibliographic records for foundational methods.
- Verify third-party code/data/figures individually.
- Correct, replace, or link-only any assets with uncertain reuse rights.
- Preserve evidence URLs/DOIs and access dates.

### Batch D — release UX and reproducibility
- Check Markdown heading anchors and internal navigation in the rendered site.
- Test install and execution from clean environments.
- Review notebook order, hidden state, outputs and reproducibility.
- Check mobile readability, keyboard navigation, screen-reader structure and alt text.
- Confirm issue templates, contribution instructions and license notices.

## Sprint log

| Batch | State | Evidence |
|---|---|---|
| A | In progress | Structural inventory exists; direct slug mismatches are documented but manual alias crosswalk is still outstanding |
| B | Queued | Existing tests and lessons are evidence for specific scopes only |
| C | Queued | Asset-level rights audit not completed |
| D | Queued | Rendered/mobile/accessibility release audit not completed |

**Do not promote any source-entry review label from this queue alone.** This document defines work order; verification requires actual evidence attached to the reviewed record.

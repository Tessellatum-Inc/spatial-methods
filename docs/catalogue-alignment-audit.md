# Catalogue alignment audit — Batch 1

**Snapshot:** 18 November 2026  
**Branch:** `completion/section-22-atomic-audit`  
**Tree audited:** `fb1242427bc7e00db84cf13ff7defd0dabd5c59c`  
**Method:** Git tree inventory and direct slug matching only.

## Inventory

| Resource | Count |
|---|---:|
| Canonical verification records | 218 |
| Python implementation package READMEs | 321 |
| Notebook files under `notebooks/` | 180 |
| Verification record ↔ package exact-slug overlap | 109 |

The direct slug comparison yielded 109 verification filenames without a same-named Python package and 212 Python package names without an exact verification filename.

## Interpretation — no orphan verdicts

These are **name-alignment signals, not confirmed orphan counts**. Canonical verification records and implementation packages often use different names for the same concept (e.g., family names, aliases, implementation-specific scope, or grouped methods). Exact matching alone cannot establish whether a record lacks an implementation or whether a package lacks source/verification coverage.

No source status was promoted and no item was declared orphaned based on this scan.

## Next reconciliation step

For the 109 direct-mismatch signals, create explicit crosswalk entries (canonical record ↔ package slug ↔ notebook ↔ source-section row) where a relationship is supported by reading the underlying files. Split true multi-method families into child records when necessary; mark unresolved mapping questions rather than infer equivalence from similar names.

## Scope and reproducibility

This audit inventories paths from the recursive Git tree and compares file/package names. It does not inspect implementation code, tests, notebook contents, source bibliographic evidence, technical claims, or third-party asset rights. It is therefore a preliminary structural audit only—not catalogue quality certification, orphan detection, or compendium verification.

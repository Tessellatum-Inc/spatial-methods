# Spatial Analysis — Engineering Foundation 0.1.0 (release candidate notes)

**Status:** Draft release candidate; not tagged or merged.  
**Date:** 18 November 2026

## Scope

This milestone establishes a maintainable public foundation for a growing spatial-analysis learning and implementation compendium. It preserves the original 47-page, 22-section source inventory while adding a navigable catalogue, canonical lessons, reproducible examples, tests, notebooks, benchmarks, research notes and contributor/extension conventions.

It is a foundation release—not a complete verification of the original compendium, not a production certification of every implementation, and not a blanket relicensing of third-party material.

## Included

- Twenty-two indexed source sections with coverage and review dashboards.
- Algorithm lessons and bounded implementations across geometry, statistics, geostatistics, raster/terrain, remote sensing, optimization, mobility, decision methods, GeoAI and geodesy.
- Python implementation packages with isolated CI shards; notebook execution shards; catalogue, coverage and internal-link checks; and Clipper2 C# smoke checks.
- Contribution guidance, record-type taxonomy, research/teaching standards, extension protocol and publishing model.
- Explicit source-entry statuses, known implementation boundaries and rights exclusions.
- Project licensing decisions for original contributions: Apache-2.0 for code and CC BY-4.0 for original documentation/learning material; DCO sign-off applies prospectively.

## Validation checkpoint

The current pre-closeout head `a9aae51ee2eefd9c9fe50a47f2cd0c046c2e7994` passed the PR workflow with 58 of 59 jobs successful, zero failures, and one skipped contributor-sign-off job (not applicable to the PR event). Its push workflow also succeeded. Any edits made after that checkpoint require a fresh exact-head CI run before tagging or merging.

## Known limitations and exclusions

- The source review dashboard currently records 695 source-entry rows: 306 partial, 389 intake-only, and 0 fully verified. This is not a percentage-complete measure; it is an honest verification inventory.
- Identity, bibliography and technical claims are not comprehensively verified across all entries. Grouped source entries may still require child records and authoritative research.
- The preserved 47-page transcription is excluded from blanket project licensing pending page-level rights review. Third-party content is linked, removed, or individually scoped unless reuse permission is established.
- Some code is intentionally a teaching baseline or bounded implementation. Passing tests do not establish production suitability, performance guarantees or correctness for all inputs.
- Rendered/mobile/accessibility reviews are not fully certified; the closeout pass should address obvious usability defects and disclose what has not been formally evaluated.

## Release checklist

- [ ] Final exact-head CI passes.
- [ ] Release ledger, README, dashboard and licence scope are consistent.
- [ ] No unresolved third-party asset is included as though licensed by the project.
- [ ] Versioned scope and release notes are reviewed.
- [ ] PR #3 receives required review and is merged before a tag is made.
- [ ] CI runs on the exact merged commit; tag that verified commit.

## Next maintenance

Future work should be additive and evidence-led: add or improve methods, resolve source entries, strengthen tests, and improve lessons when a concrete need appears. Do not block this foundation on an indefinite exhaustive audit. Keep the technical resource free and public under its stated licences; paid offerings may provide guided learning, support, workshops and community without claiming exclusive rights over public material.

# Spatial Methods — Engineering Foundation 0.1.0 (release candidate notes)

**Status:** Draft release candidate; not tagged. The foundation PRs are merged; final closeout and release approval remain pending.  
**Updated:** 21 November 2026

## Scope

This milestone establishes a maintainable public foundation for Spatial Methods. It preserves the original 47-page, 22-section spatial-analysis source inventory while adding a navigable catalogue, canonical lessons, reproducible examples, tests, notebooks, benchmarks, research notes and contributor/extension conventions. The wider Spatial Methods architecture now connects four permanent pillars—Spatial Algorithms, Spatial Recipes, Spatial Data Collection and Theoretical Foundations—with applications as cross-cutting contexts. This release establishes the engineering foundation; it does not claim that all four pillars or the wider subject universe are comprehensively populated.

It is a foundation release—not a complete verification of the original compendium, not a production certification of every implementation, and not a blanket relicensing of third-party material.

## Included

- Twenty-two indexed source sections with coverage and review dashboards.
- Algorithm lessons and bounded implementations across geometry, statistics, geostatistics, raster/terrain, remote sensing, optimization, mobility, decision methods, GeoAI and geodesy.
- Python implementation packages with isolated CI shards; notebook execution shards; catalogue, coverage and internal-link checks; and Clipper2 C# smoke checks.
- Contribution guidance, record-type taxonomy, research/teaching standards, extension protocol and publishing model.
- Explicit source-entry statuses, known implementation boundaries and rights exclusions.
- Project licensing decisions for original contributions: Apache-2.0 for code and CC BY-4.0 for original documentation/learning material; DCO sign-off applies prospectively.

## Validation checkpoint

The current main head is `8f1306a7b962161b5098937387f12b2e9c1f0841` (21 November 2026). The Photogrammetry ODM package-test workflow passed on this exact head: [run 44921406757](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44921406757). The full Python examples workflow [run 44921406761](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44921406761) was queued at the time of this update. Prior exact runs on `23f8082c8cf00a5a7cd223cdea51a15105dec8e9` passed both the Python examples and package-test workflows, but are not substitutes for current-head evidence. A release tag must wait for all required workflows to pass on one exact candidate commit.

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
- [x] PR #3 (source compendium foundation), PR #4 (Patreon launch foundation) and PR #6 (Spatial Methods identity) are merged.
- [ ] CI runs on the exact merged commit; tag that verified commit.

## Next maintenance

After the foundation release, future work should be additive and evidence-led: improve methods, resolve source entries, strengthen tests and improve learning experiences when a concrete need appears. The wider four-pillar architecture should guide additions, while the original compendium remains a traceable intake source rather than the boundary of the project. Do not block this foundation on an indefinite exhaustive audit. Keep the technical resource free and public under its stated licences; paid offerings may provide guided learning, support, workshops and community without claiming exclusive rights over public material.

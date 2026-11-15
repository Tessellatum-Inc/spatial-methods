# Source review dashboard

Snapshot: 15 November 2026 (source-entry labels retained; implementation reconciliation expanded MFD routing, compositional geometry, change-point detectors and spatial sampling)

This dashboard counts the source-entry review labels in the 22 item-level section indexes. It is an inventory of review progress, not a claim that the entries have been technically verified.

## Current position

| Measure | Entries | Meaning |
|---|---:|---|
| Source-entry rows counted | 694 | Rows with a source-entry review status in the section indexes |
| Partial | 85 | A related canonical record or selected citation check exists, but the grouped source entry remains unverified |
| Not checked — intake only | 609 | The source wording is preserved, but no independent review is recorded |
| Fully verified | 0 | No row is currently labelled fully verified across the independent review dimensions |

Note: the 22 indexes also contain implementation inventories and explanatory tables. Those are not source-entry rows and are excluded from these counts.

## By section

| Section | Source entries | Partial | Intake only |
|---:|---:|---:|---:|
| 1 — Core GIS | 33 | 18 | 15 |
| 2 — Spatial statistics | 27 | 9 | 18 |
| 3 — Geostatistics | 26 | 3 | 23 |
| 4 — Raster, terrain and hydrology | 27 | 2 | 25 |
| 5 — Remote sensing | 36 | 2 | 34 |
| 6 — Optimization, mobility and transport | 30 | 3 | 27 |
| 7 — Domain modeling | 48 | 1 | 47 |
| 8 — GeoAI | 54 | 2 | 52 |
| 9 — Geodesy, cartography and infrastructure | 39 | 1 | 38 |
| 10 — Classical statistical and computational additions | 30 | 22 | 8 |
| 11 — GeoAI and computer-vision additions | 26 | 0 | 26 |
| 12 — Signal, GNSS and regional science | 28 | 14 | 14 |
| 13 — GeoFM workflows, urban mobility and LLMs | 29 | 0 | 29 |
| 14 — Databases, graphics, morphology and hazards | 33 | 1 | 32 |
| 15 — Vision, registration and vector extraction | 33 | 0 | 33 |
| 16 — Flows, regions, deformation and marine | 25 | 0 | 25 |
| 17 — Geometry, scalability, design and siting | 27 | 0 | 27 |
| 18 — Moving objects, routing, transit and water | 32 | 1 | 31 |
| 19 — African applications, addressing and finance | 32 | 0 | 32 |
| 20 — Indices, microwave, events and information | 25 | 2 | 23 |
| 21 — Neural fields, climate accounting and robust geometry | 26 | 2 | 24 |
| 22 — Inference, covariance, spherical methods and asset monitoring | 28 | 2 | 26 |
| **Total** | **694** | **84** | **610** |

## How to interpret this

- **Partial does not mean verified.** A row may link to a lesson that covers one member of a long grouped list. The remaining variants and the source entry's identity, bibliography, claims and rights still need review.
- **Intake only does not mean incorrect.** It means the wording has been preserved but not independently checked.
- **No single verification badge is sufficient.** Follow the [source-entry verification protocol](verification-protocol.md) and track identity, bibliography, technical claims, implementation/reproduction and rights independently.
- **Do not use the percentage of linked lessons as a proxy for catalogue quality.** A small number of deeply checked records is more useful than many shallow links.

## Recommended review order

1. Resolve ambiguous names and split grouped rows into child entries where different members need different evidence.
2. Verify identity and bibliographic metadata against primary or authoritative records.
3. Check the specific equations, assumptions, guarantees and limitations planned for each lesson.
4. Record whether the implementation is a wrapper, teaching baseline, reproduced method or production-grade implementation.
5. Check rights for each reused text, figure, dataset, code sample and other artefact.
6. Update the source index and this dashboard only after the underlying row labels change.

## Scope of this snapshot

The counts were recalculated from the row-level labels present in all 22 section indexes on 15 November 2026, after restoring Section 12's implementation-linked review states and reconciling Section 2 and Section 10. They are a dated snapshot and must be recalculated when source-entry labels are revised. They do not count canonical lesson pages, implementation inventories, software lists or supplementary methods as additional source entries.
## Implementation reconciliation — 15 November 2026

The `compendium/section-01-geometry-continuation` branch head (`97d508fb767b9e395cfef4d7885d5d33411ce3ed`) is now a direct parent of `main` merge commit `f7038ac9cc48ba4341b642eb967e6122f4d268d2`; it is ancestral to current `main`, not a divergent history to merge wholesale. The merge added 281 branch-only paths, retained `main` versions for 76 overlapping file paths, and preserved both parent histories. A follow-up semantic audit found that several retained `main` source indexes had lost implementation-linked status detail even though their target materials existed. A focused review of high-value same-path implementation differences also found three useful older-branch methods that were not present in the retained `main` files: the first-principles Felzenszwalb–Huttenlocher raster EDT, a variable-sized block-kernel MMD permutation test, and a pure-Python Lucas–Kanade reference. These have now been added as complementary implementations rather than replacing the more comprehensive `main` versions. Section 12's 14 partial rows and 14 intake-only rows have now been restored from the richer indexed record; Section 2 now records nine partial and 18 intake-only rows, including the point-process implementation; Section 10 now includes additional cross-cutting method and package references. The 22-section review counts are now 85 partial, 609 intake-only and zero fully verified. This remains an inventory measure, not proof of complete source-entry verification. Section 1's grouped distance/extent row links to sampled-point Hausdorff, discrete and continuous Fréchet (Alt–Godau free-space decision with bisection approximation), randomized Welzl minimum circle, rotating-calipers convex diameter, Polylabel for polygons with holes, a transparent O(h²) minimum-area oriented rectangle baseline plus a four-support O(h) rotating-calipers sweep after hull construction, and an additive-tolerance largest-empty-circle search constrained to the sites' convex hull. The geometry-metrics suite's earlier 22-test local baseline has since been extended with continuous Fréchet, largest-empty-circle and O(h) rectangle-calipers tests; the expanded suite is awaiting the latest CI run. CI now includes a test-matrix entry for all 132 Python implementation directories and executes all 126 notebooks; the latest full workflow run is queued, so repository-wide CI success is not yet established.


A subsequent Section 1 implementation batch adds tested reference encoders/decoders for Morton (Z-order), Hilbert distance and Geohash, with a source-linked algorithm guide, implementation walkthrough and verification record. H3, S2, quadkeys and HEALPix remain distinct open systems; the grouped source row is therefore partial, not complete. The batch is committed directly to `main` as `848807b391f7edee78db02867882650ed328c889`; its full Python/notebook workflow is pending.


The Section 1 source reconciliation has also added repeated-Dijkstra many-to-many shortest paths and cutoff-Dijkstra network isochrones (including directed frontier arcs) to the existing shortest-path package, with tests, a walkthrough and a source-linked method/verification record. This is a bounded static-graph baseline, not a shared-preprocessing production routing engine. The 22-section source-entry label totals remain 85 partial, 609 intake-only and zero fully verified; the Section 1 count remains 18 partial and 15 intake-only.


The new `spatial-encodings` package has been added to the Python CI matrix and has its own `requirements.txt`; it is now included in the 132 package test jobs. It adds no separate notebook, so the explicit notebook execution list remains 126.

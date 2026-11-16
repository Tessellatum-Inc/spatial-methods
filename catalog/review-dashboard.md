# Source review dashboard

Snapshot: 17 November 2026 (recounted from the 22 current section indexes)

This dashboard counts the source-entry review labels in the 22 item-level section indexes. It is an inventory of review progress, not a claim that the entries have been technically verified.

## Current position

| Measure | Entries | Meaning |
|---|---:|---|
| Source-entry rows counted | 693 | Rows with a source-entry review status in the section indexes |
| Partial | 173 | A related canonical record or selected citation check exists, but the grouped source entry remains unverified |
| Not checked — intake only | 520 | The source wording is preserved, but no independent review is recorded |
| Fully verified | 0 | No row is currently labelled fully verified across the independent review dimensions |

Note: the 22 indexes also contain implementation inventories and explanatory tables. Those are not source-entry rows and are excluded from these counts.

## By section

| Section | Source entries | Partial | Intake only |
|---:|---:|---:|---:|
| 1 — Core GIS | 33 | 26 | 7 |
| 2 — Spatial statistics | 28 | 14 | 14 |
| 3 — Geostatistics | 26 | 3 | 23 |
| 4 — Raster, terrain and hydrology | 26 | 22 | 4 |
| 5 — Remote sensing | 36 | 16 | 20 |
| 6 — Optimization, mobility and transport | 31 | 4 | 27 |
| 7 — Domain modeling | 48 | 1 | 47 |
| 8 — GeoAI | 54 | 2 | 52 |
| 9 — Geodesy, cartography and infrastructure | 39 | 1 | 38 |
| 10 — Classical statistical and computational additions | 30 | 22 | 8 |
| 11 — GeoAI and computer-vision additions | 26 | 0 | 26 |
| 12 — Signal, GNSS and regional science | 28 | 14 | 14 |
| 13 — GeoFM workflows, urban mobility and LLMs | 29 | 0 | 29 |
| 14 — Databases, graphics, morphology and hazards | 33 | 1 | 32 |
| 15 — Vision, registration and vector extraction | 33 | 3 | 30 |
| 16 — Flows, regions, deformation and marine | 25 | 9 | 16 |
| 17 — Geometry, scalability, design and siting | 26 | 11 | 15 |
| 18 — Moving objects, routing, transit and water | 32 | 7 | 25 |
| 19 — African applications, addressing and finance | 32 | 0 | 32 |
| 20 — Indices, microwave, events and information | 24 | 7 | 17 |
| 21 — Neural fields, climate accounting and robust geometry | 26 | 3 | 23 |
| 22 — Inference, covariance, spherical methods and asset monitoring | 28 | 6 | 22 |
| **Total** | **693** | **173** | **520** |

The 17 November recount finds **173 partial**, **520 intake-only** and **zero fully verified** source-entry rows across **693 rows**. The row count is recalculated from the 22 current indexes; three rows previously included in the dashboard total were not present in the current source-entry tables. Counts are derived from the current source-entry tables in all 22 section indexes, classifying rows with an implementation-linked or partial status as partial and intake-only rows as not checked. Section 4's storage/compression row is retained as intake-only; implementation-linked rows in Sections 17 and 20 are counted as partial. Some section indexes have changed row counts since the prior snapshot, so the table below supersedes all historical totals in the reconciliation notes.

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

The counts were recalculated from the row-level labels present in all 22 section indexes on 15 November 2026, after reconciling all 22 current source-entry tables. They are a dated snapshot and must be recalculated when source-entry labels are revised. They do not count canonical lesson pages, implementation inventories, software lists or supplementary methods as additional source entries.
## Implementation reconciliation — 15 November 2026

The `compendium/section-01-geometry-continuation` branch head (`97d508fb767b9e395cfef4d7885d5d33411ce3ed`) is now a direct parent of `main` merge commit `f7038ac9cc48ba4341b642eb967e6122f4d268d2`; it is ancestral to current `main`, not a divergent history to merge wholesale. The merge added 281 branch-only paths, retained `main` versions for 76 overlapping file paths, and preserved both parent histories. A follow-up semantic audit found that several retained `main` source indexes had lost implementation-linked status detail even though their target materials existed. A focused review of high-value same-path implementation differences also found three useful older-branch methods that were not present in the retained `main` files: the first-principles Felzenszwalb–Huttenlocher raster EDT, a variable-sized block-kernel MMD permutation test, and a pure-Python Lucas–Kanade reference. These have now been added as complementary implementations rather than replacing the more comprehensive `main` versions. Section 12's 14 partial rows and 14 intake-only rows have now been restored from the richer indexed record; Section 2 now records nine partial and 18 intake-only rows, including the point-process implementation; Section 10 now includes additional cross-cutting method and package references. The 22-section review counts were 85 partial, 609 intake-only and zero fully verified at that snapshot; the current 17 November reconciliation below now records 86 partial, 608 intake-only and zero fully verified. This remains an inventory measure, not proof of complete source-entry verification. Section 1's grouped distance/extent row links to sampled-point Hausdorff, discrete and continuous Fréchet (Alt–Godau free-space decision with bisection approximation), randomized Welzl minimum circle, rotating-calipers convex diameter, Polylabel for polygons with holes, a transparent O(h²) minimum-area oriented rectangle baseline plus a four-support O(h) rotating-calipers sweep after hull construction, and an additive-tolerance largest-empty-circle search constrained to the sites' convex hull. The geometry-metrics suite's earlier 22-test local baseline has since been extended with continuous Fréchet, largest-empty-circle and O(h) rectangle-calipers tests; the expanded suite is awaiting the latest CI run. CI now includes a test-matrix entry for all 137 Python implementation directories and executes all 126 notebooks; the latest full workflow run is queued, so repository-wide CI success is not yet established.


A subsequent Section 1 implementation batch adds tested reference encoders/decoders for Morton (Z-order), Hilbert distance and Geohash, with a source-linked algorithm guide, implementation walkthrough and verification record. H3, S2, quadkeys and HEALPix remain distinct open systems; the grouped source row is therefore partial, not complete. The batch is committed directly to `main` as `848807b391f7edee78db02867882650ed328c889`; its full Python/notebook workflow is pending.


The Section 1 source reconciliation has also added repeated-Dijkstra many-to-many shortest paths and cutoff-Dijkstra network isochrones (including directed frontier arcs) to the existing shortest-path package, with tests, a walkthrough and a source-linked method/verification record. This is a bounded static-graph baseline, not a shared-preprocessing production routing engine. At the time of that routing update, source-entry label totals were 85 partial and 609 intake-only; subsequent reconciliations are recorded below.


The new `spatial-encodings` package has been added to the Python CI matrix and has its own `requirements.txt`; it is now included in the 133 package test jobs. It adds no separate notebook, so the explicit notebook execution list remains 126.


## Implementation reconciliation — network centrality batch

Section 1's directed centrality entry now links to a dependency-free implementation of Brandes node betweenness (BFS and strictly-positive weighted Dijkstra variants), inward directed closeness with the Wasserman–Faust reachability correction, and weighted PageRank with dangling-node redistribution and personalization. Analytical graph fixtures, disconnected cases, weighted paths, convergence and input-validation tests are included. The row remains partial because space-syntax integration and street-network metrics are separate methods in the grouped source entry. The new package is included in the Python CI matrix; package count is now 137 and notebook execution count remains 126. The source-entry dashboard is 86 partial, 608 intake-only, zero fully verified.


## Implementation reconciliation — point-pattern G, F and J

The Section 2 point-process package now implements the empirical nearest-neighbour G function, a reproducible Monte Carlo empty-space F function based on uniform locations in a rectangular window, and J=(1-G)/(1-F), with undefined tail values represented as NaN. Tests cover monotonicity, seeded reproducibility, the G/F/J relationship and invalid controls. The source row remains partial because these are uncorrected rectangular-window teaching estimators; advanced edge correction, simulation envelopes, and broader point-process models remain open. The package already participates in the Python CI matrix. No source-entry count changes were made by this additive implementation because the grouped G/F/J source row was already partial.


## Implementation reconciliation — label propagation

Section 1's grouped community-detection entry now links to a seeded asynchronous unweighted label-propagation baseline. It symmetrises adjacency, retains isolates, uses random tie breaking, and includes tests for disconnected components, reproducibility and invalid controls. The source row remains partial: Louvain, Leiden, Infomap and the listed graph partitioning algorithms are not implemented by this addition. The source-entry label totals are now 87 partial, 607 intake-only and zero fully verified; Section 1 is 20 partial and 13 intake-only. The new package is added to the Python CI matrix, taking the package count to 134; notebook count remains 126.


## Implementation reconciliation — maximum flow and minimum cut

Section 1's flows-and-trees entry now links to a Dinic maximum-flow/minimum-cut reference implementation with distinct residual arcs for parallel and antiparallel input edges. Tests cover the classic six-node maximum-flow value of 23, equality with cut capacity, flow conservation, capacity constraints, disconnected sinks and invalid inputs. The grouped source row remains partial: minimum spanning tree, Steiner tree and k-core decomposition are not included in this batch. Source-entry totals are now 88 partial, 606 intake-only and zero fully verified; Section 1 is 21 partial and 12 intake-only. The package is added to the Python CI matrix, taking it to 135 packages; notebook count remains 126.


## Implementation reconciliation — minimum spanning tree

The Section 1 flows-and-trees source entry now also links to a Kruskal minimum spanning tree/forest implementation using disjoint-set union with path compression and union by rank. Tests cover a known MST, disconnected forests, negative and parallel edges, self-loops, deterministic ties and invalid inputs. The source row remains partial because Steiner tree and k-core are still outstanding. No source-entry status count changes were made because this grouped row was already partial. The Python CI matrix now covers 136 implementation packages; notebook execution remains 126.


## Implementation reconciliation — exact small-terminal Steiner tree

The Section 1 flows-and-trees source entry now also includes an exact Dreyfus–Wagner subset dynamic program with shortest-path closure. It reconstructs a terminal-spanning tree, supports parallel edges by retaining the minimum-weight edge, and imposes a default 12-terminal guard because the method is exponential. Tests cover two-terminal shortest paths, a star with a non-terminal Steiner vertex, a terminal triangle, one-terminal cases, disconnected terminals and invalid inputs. The grouped row remains partial because k-core decomposition is still open. No source-entry status count changes were made. The Python CI matrix now covers 137 packages; notebook execution remains 126.


## Implementation reconciliation — k-core and Kernighan–Lin batch

The Section 1 flows-and-trees entry now links to an undirected k-core degree-peeling implementation with core-number and induced-subgraph outputs. The community-detection/partitioning entry now also links to a balanced weighted/unweighted Kernighan–Lin bisection baseline using locked swap pairs and the best positive cumulative-gain prefix. Both packages have dedicated tests, READMEs, algorithm notes and verification records, and both are included in the Python CI matrix. The two new test suites were executed in the working environment: k-core 9 passed; Kernighan–Lin 7 passed. The Python package matrix now contains 139 implementation directories; the explicit notebook execution list remains 126. These two additions do not by themselves change the source-entry review counts: the grouped Section 1 rows remain partial pending full source-entry identity, bibliography, technical-claim and rights review.


## Louvain implementation reconciliation

Added a seeded multilevel weighted Louvain reference implementation, modularity evaluator, unit tests, algorithm note, verification record and executable notebook. The implementation preserves contracted internal edge weight as self-loops between aggregation levels. The grouped Section 1 community-detection entry remains partial: Leiden, Infomap, spectral partitioning and METIS-style methods are not implemented, and independent source identity, bibliography, claims and rights review remains outstanding.


## Implementation reconciliation — Louvain and spectral partitioning

The community-detection source row now links to a seeded multilevel weighted Louvain implementation, a modularity evaluator, unit tests, a verification record and an executable notebook. Contracted internal edge weights are preserved as self-loops between levels. The same Section 1 family now links to normalized-Laplacian spectral bisection with a Fiedler-vector sweep over normalized cut; the dense eigensolver baseline covers weighted graphs, disconnected components and isolates. These additions bring the Python implementation matrix to 141 packages and the explicit notebook execution list to 127. Louvain remains heuristic; spectral bisection is a dense small/medium teaching baseline. Leiden, Infomap, sparse large-graph spectral solvers and METIS-style multilevel partitioning remain outstanding. The grouped source-entry review state remains partial.


## Implementation reconciliation — 17 November 2026

Section 15 now has a generalized ICP implementation alongside point-to-point and point-to-plane ICP. It remains partial because NDT, colored ICP, FPFH/RANSAC, TEASER++ and learned registration are not represented by this addition. Section 16 now has additive-tolerance least-cost raster corridors and a climate-velocity package covering Mahalanobis analog ranking and gradient-derived isocline displacement. These are bounded numerical methods, not complete operational climate-refugia or corridor-planning systems. The current row recount is 695 source entries: 160 partial, 535 intake-only and zero fully verified. Independent bibliographic, technical-claim, rights and full-source-row review remains required.


A Mogi point-source elastic half-space displacement implementation has since moved one Section 16 source row from intake-only to partial. The source-entry total remains 696; the current review-label totals are 163 partial and 533 intake-only.


The Section 2 source-entry recount also identifies an implementation-linked Ripley's K/L entry whose status description is more detailed than the standard “Partial” label. It is counted as partial rather than intake-only. Section 16's intervening-opportunities entry is now also implementation-linked. The current row totals are 696 source entries, 163 partial and 533 intake-only.

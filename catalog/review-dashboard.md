# Source review dashboard

Snapshot: 17 November 2026 (recounted from the 22 current section indexes)

This dashboard counts the source-entry review labels in the 22 item-level section indexes. It is an inventory of review progress, not a claim that the entries have been technically verified.

## Current position

| Measure | Entries | Meaning |
|---|---:|---|
| Source-entry rows counted | 695 | Rows with a source-entry review status in the section indexes |
| Partial | 291 | A related canonical record or selected citation check exists, but the grouped source entry remains unverified |
| Not checked — intake only | 404 | The source wording is preserved, but no independent review is recorded |
| Fully verified | 0 | No row is currently labelled fully verified across the independent review dimensions |

Note: the 22 indexes also contain implementation inventories and explanatory tables. Those are not source-entry rows and are excluded from these counts.

## By section

| Section | Source entries | Partial | Intake only |
|---:|---:|---:|---:|
| 1 — Core GIS | 33 | 32 | 1 |
| 2 — Spatial statistics | 27 | 27 | 0 |
| 3 — Geostatistics | 26 | 22 | 4 |
| 4 — Raster, terrain and hydrology | 27 | 23 | 4 |
| 5 — Remote sensing | 36 | 30 | 6 |
| 6 — Optimization, mobility and transport | 31 | 10 | 21 |
| 7 — Domain modeling | 48 | 11 | 37 |
| 8 — GeoAI | 54 | 8 | 46 |
| 9 — Geodesy, cartography and infrastructure | 39 | 8 | 31 |
| 10 — Classical statistical and computational additions | 30 | 23 | 7 |
| 11 — GeoAI and computer-vision additions | 26 | 2 | 24 |
| 12 — Signal, GNSS and regional science | 28 | 15 | 13 |
| 13 — GeoFM workflows, urban mobility and LLMs | 29 | 0 | 29 |
| 14 — Databases, graphics, morphology and hazards | 33 | 9 | 24 |
| 15 — Vision, registration and vector extraction | 33 | 4 | 29 |
| 16 — Flows, regions, deformation and marine | 25 | 9 | 16 |
| 17 — Geometry, scalability, design and siting | 27 | 16 | 11 |
| 18 — Moving objects, routing, transit and water | 32 | 9 | 23 |
| 19 — African applications, addressing and finance | 32 | 8 | 24 |
| 20 — Indices, microwave, events and information | 25 | 9 | 16 |
| 21 — Neural fields, climate accounting and robust geometry | 26 | 6 | 20 |
| 22 — Inference, covariance, spherical methods and asset monitoring | 28 | 10 | 18 |
| **Total** | **695** | **291** | **404** |

The current by-section subtotals reconcile exactly with the aggregate: **695 source-entry rows, 291 partial, 404 intake-only and zero fully verified**. Counts are derived directly from the current source-entry tables in all 22 section indexes. Intake-only rows are classified as not checked; explicit fully verified rows are counted separately; all other non-empty statuses—including implementation-linked records—remain partial. Section 4's storage/compression row is retained as intake-only; implementation-linked rows in Sections 17 and 20 are counted as partial. Historical snapshots below are retained as audit history; the current table above is authoritative.

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

The counts were recalculated from the status column in every source-entry table in all 22 section indexes on 17 November 2026. The checker now performs this recount directly rather than merely checking arithmetic in a manually maintained ledger. They are a dated snapshot and must be recalculated when source-entry labels are revised. They do not count canonical lesson pages, implementation inventories, software lists or supplementary methods as additional source entries.
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


**Historical reconciliation note (17 November 2026):** the following narrative records an earlier snapshot of 693 source-entry rows (187 partial, 506 intake-only); the current authoritative totals are in the section table above (693, 220, 473).


**Historical reconciliation note (17 November 2026):** the following narrative records an earlier snapshot of 693 source-entry rows (188 partial, 505 intake-only); the current authoritative totals are in the section table above (693, 220, 473).


**Historical reconciliation note (17 November 2026):** the following narrative preserves an earlier 693-row snapshot (200 partial, 493 intake-only); the current authoritative totals are in the section table above (693, 220, 473).


## Implementation reconciliation — Open Location Code

Section 19's location-encoding family now links to a tested full-code Open Location Code (Plus Code) encoder/decoder with decimal-safe cell-boundary handling and bounds output. The existing geohash implementation remains alongside it. Short-code recovery, what3words, S2 and H3 remain open, and the grouped source row remains partial. The Python CI matrix now includes the new package; its full workflow has not yet been verified.


## Implementation reconciliation — fractional-cover regression

Section 5's fractional-cover source row now links to a deterministic CART regression-tree baseline for field-labelled fractions, alongside the existing FCLS spectral-unmixing implementation. The new package includes independent tests for piecewise response recovery, minimum leaf size, constant targets, multifeature splitting and invalid inputs, and is registered as a standalone GitHub Actions job. This does not implement vegetation-continuous-fields products, spatial validation, uncertainty calibration or sensor-specific processing; the grouped source row remains partial. Section 5 now has 23 partial and 13 intake-only entries; the dashboard aggregate is 201 partial, 492 intake-only and zero fully verified.


## Implementation reconciliation — Brown-Conrady lens distortion

Section 5's grouped lens-calibration/workflow row now links to a tested Brown-Conrady radial/tangential forward model and Newton inverse in normalized camera-plane coordinates. Independent tests cover identity, radial-plus-tangential round trips, array dimensions and invalid controls; a local numerical smoke check recovered coordinates to floating-point precision. The new package is registered as a standalone CI job. The source row remains partial: estimating camera intrinsics/distortion coefficients, boresight calibration, orthomosaic generation and mesh texturing remain open. Section 5 now has 24 partial and 12 intake-only rows; the dashboard aggregate is 202 partial, 491 intake-only and zero fully verified.


## Implementation reconciliation — progressive morphological ground filtering

Section 5's point-cloud filtering/registration entry now links to a rasterised progressive morphological filter baseline for projected XYZ data. The method progressively opens a minimum-elevation grid, applies a slope-scaled height threshold and returns a point-aligned ground mask. Tests cover flat-ground/object separation, sloped terrain, input-order invariance and invalid/grid-size controls; local checks passed these fixtures. Existing point-cloud registration records already cover point-to-point, point-to-plane, GICP and NDT baselines. The grouped source row remains partial because Cloth Simulation Filtering (CSF) and RANSAC shape fitting are not included in this addition. Section 5 now has 25 partial and 11 intake-only rows; aggregate review state is 203 partial, 490 intake-only and zero fully verified.


## Implementation reconciliation — RANSAC plane fitting

Section 5's grouped point-cloud processing entry now also links to a NumPy RANSAC plane estimator with deterministic random seeds, orthogonal residual scoring, consensus selection and SVD refinement. Independent tests cover a noisy plane with outliers, repeatability, invalid controls and collinear degeneracy; local smoke checks recovered all 150 noisy plane samples and rejected all 50 injected outliers in the fixture. The entry remains partial because CSF ground filtering and multi-primitive RANSAC are not implemented by this single-plane baseline. Section 5 now has 26 partial and 10 intake-only rows; aggregate review state is 204 partial, 489 intake-only and zero fully verified.


## Implementation reconciliation — CHM watershed crown segmentation

Section 5's tree-segmentation source entry now links to a canopy-height-model workflow that detects local maxima, collapses connected peak plateaus to deterministic markers and segments the canopy mask with marker-controlled watershed. Tests cover two synthetic crowns, plateau handling, no qualifying treetops, invalid controls and NoData exclusion; a local synthetic two-crown check returned two distinct labels. The entry remains partial because Dalponte segmentation, point-cloud-native crown delineation and CHM production are not implemented here. Section 5 now has 27 partial and nine intake-only entries; aggregate review state is 205 partial, 488 intake-only and zero fully verified.


## Implementation reconciliation — marching-cubes isosurface extraction

Section 5's grouped surface-reconstruction entry now links to a validated integration of scikit-image's Lewiner marching-cubes implementation, with explicit voxel spacing, origin and coordinate-axis contract. Tests cover a synthetic sphere, anisotropic voxel spacing, invalid volumes and invalid controls; local geometry checks confirmed the sphere radius and voxel-centre offset. This is a maintained-library wrapper, not a from-scratch lookup-table implementation. The grouped entry remains partial because Poisson reconstruction, mesh simplification, NeRF and 3D Gaussian splatting remain open. Section 5 now has 28 partial and eight intake-only rows; aggregate review state is 206 partial, 487 intake-only and zero fully verified.


## Implementation reconciliation — contextual thermal-hotspot screening

Section 5's thermal/fire entry now links to a generic local-context thermal anomaly baseline combining an absolute temperature threshold with a local median and MAD-derived robust scale. Tests cover isolated hotspot detection, absolute-threshold rejection, NaN exclusion, uniform scenes and invalid controls; local checks confirmed the synthetic hotspot and NoData cases. This is not a reproduction of MODIS active-fire, volcanic retrieval or MCD64A1 burned-area products. The source row remains partial because sensor-specific spectral/contextual algorithms, cloud/smoke screening and burned-area mapping remain open. Section 5 now has 29 partial and seven intake-only entries; aggregate review state is 207 partial, 486 intake-only and zero fully verified.


## Implementation reconciliation — point-cloud voxelization

Section 5's point-cloud processing entry now links to a sparse voxelization baseline that assigns points using half-open, axis-aligned cells and returns occupied voxel indices, point-to-voxel mappings, counts, centroids and per-axis minima/maxima. Independent tests cover aggregation, exact boundaries, negative coordinates, anisotropic cell sizes, invalid inputs and mapping/count consistency. The grouped entry remains partial because semantic classification, strip adjustment and GEDI/ICESat-2 sensor-specific processing remain open. Section 5 now has 30 partial and six intake-only rows; aggregate review state is 208 partial, 485 intake-only and zero fully verified.


## Implementation reconciliation — Vecchia Gaussian-process approximation

Section 3's large-data Gaussian-process entry now links to a nearest-predecessor Vecchia likelihood baseline using a squared-exponential covariance. The implementation selects nearest prior sites, evaluates local Gaussian conditional means/variances and returns the approximate log-likelihood; with all predecessors it matches the dense Gaussian likelihood to numerical tolerance. Independent tests cover exact-likelihood equivalence, ordering invariance, sparse-neighbour outputs and invalid controls; local numerical checks passed. The source row remains partial because NNGP prediction, covariance tapering, fixed-rank/predictive processes, lattice kriging and multi-resolution approximations remain open. Section 3 now has 13 partial and 13 intake-only rows; aggregate review state is 209 partial, 484 intake-only and zero fully verified.


## Implementation reconciliation — Knox space-time interaction test

Section 3's space-time testing entry now links to a Knox test implementation that counts pairs close in both space and time and evaluates excess interaction using a plus-one upper-tail Monte Carlo p-value from temporal-label permutations. Tests cover designed clustering, reproducibility, constant-time nulls and invalid controls. The entry remains partial because space-time K functions, scan statistics, space-time cubes and emerging-hotspot analysis are separate methods not implemented by this test. Section 3 now has 14 partial and 12 intake-only rows; aggregate review state is 210 partial, 483 intake-only and zero fully verified.

## Implementation reconciliation — RAPTOR and CSA correctness audit (17 November 2026)

The Section 18 transit implementation audit corrected two independent timetable-routing edge cases. RAPTOR now validates each ride segment against the preceding stop's departure time (rather than comparing the wrong adjacent events), and applies access-footpath closure before the first boarding round so a passenger can walk from an access stop to a boarding stop. Regression tests cover impossible segment chronology, initial access walking and zero-duration footpath cycles. CSA now keeps initial access arrivals separate from transit-derived arrivals: an earlier transit arrival must not overwrite a later but still boardable access label, while the minimum transfer time continues to apply to transit-to-transit changes. Paired regression tests demonstrate both the permitted access boarding and the correctly blocked transfer. The RAPTOR and CSA READMEs and algorithm notes document these contracts. These are tested implementation corrections, not source-entry verification; the Section 18 grouped source row and the 22-section review totals are unchanged. The current repository tree contains 284 Python implementation directories, each with a README and at least one test module, and the CI manifest contains all 284 directories across 240 deterministic shards. The latest workflow for this commit is still queued; no repository-wide CI pass is claimed.

## Implementation reconciliation — 17 November 2026 (continued)

The Section 4 flow-routing entry now links the D-infinity facet-routing lesson and a dedicated verification record. Its expanded regression suite covers an analytic planar facet and angular split, elevation-offset invariance, anisotropic cells, downhill/unit-sum invariants, sinks/flats, NoData edges, singleton and one-row grids, seeded random DEMs, invalid inputs and accumulation conservation. The method remains a scoped teaching implementation: independent comparison with TauDEM, WhiteboxTools or GRASS GIS, depression conditioning and flat resolution remain outstanding. The Section 4 source-entry status remains partial.

Section 18 now also links a standalone transit headway and expected-wait implementation. It reports consecutive departure headways and computes passenger-arrival-weighted expected wait over a declared service window, including the initial and terminal partial intervals. The implementation has regression fixtures for regular and irregular headways, boundary gaps, extended service-day times, one-departure and no-service windows, and invalid schedules. It is a deterministic frequency-service component, not GTFS parsing or network-level accessibility. The grouped Section 18 source entry remains partial and no source-review count is changed.

The Python CI manifest now contains 285 implementation packages. The workflow has been reduced from 240 one/two-package shards to 48 deterministic shards (24 maximum parallel jobs) to reduce matrix overhead while retaining complete package coverage. Pull-request path filters now include catalogue, source-inventory and documentation changes as well as implementation and notebook changes. The latest workflow for commit `3f12515423e87999c20e96394da4cd557a4ccfe3` is queued; all 51 jobs were still queued at the latest inspection, so no full CI pass is claimed.

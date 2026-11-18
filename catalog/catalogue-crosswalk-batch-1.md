# Catalogue crosswalk — Batch 1 (confirmed aliases)

**Snapshot:** 18 November 2026  
**Tree:** `e264b26d9eef53ac08f0667b3c9b8ec76b9bba5d`

This crosswalk records file-level alias/name differences confirmed by reading the verification record and implementation README. It is not a full source-entry audit. Matching does not upgrade source verification status or imply that every grouped method is implemented.

| Verification record | Python package | Relationship |
|---|---|---|
| [`area-opening-closing`](verification/area-opening-closing.md) | [`area-morphology`](../implementations/python/area-morphology/README.md) | Same scope or explicit package naming alias; package README inspected |
| [`binary-mathematical-morphology`](verification/binary-mathematical-morphology.md) | [`binary-morphology`](../implementations/python/binary-morphology/README.md) | Same scope or explicit package naming alias; package README inspected |
| [`compositional-data-analysis`](verification/compositional-data-analysis.md) | [`compositional-data`](../implementations/python/compositional-data/README.md) | Same scope or explicit package naming alias; package README inspected |
| [`fourier-destriping`](verification/fourier-destriping.md) | [`fourier-filtering`](../implementations/python/fourier-filtering/README.md) | Same scope or explicit package naming alias; package README inspected |
| [`floating-catchment-accessibility`](verification/floating-catchment-accessibility.md) | [`floating-catchment`](../implementations/python/floating-catchment/README.md) | Same scope or explicit package naming alias; package README inspected |
| [`maximum-flow-min-cut`](verification/maximum-flow-min-cut.md) | [`max-flow-min-cut`](../implementations/python/max-flow-min-cut/README.md) | Same scope or explicit package naming alias; package README inspected |

## Confirmed mapping notes

- **Area opening/closing → area morphology:** grayscale area filters are housed in a package named `area-morphology`; its README explicitly describes grayscale area opening/closing. The package also includes additional area-filter functionality beyond the verification file's title.
- **Binary mathematical morphology → binary morphology:** package name differs by suffix; the README includes the operations listed in the verification record, with a wider documented scope (granulometry, grayscale area filtering, thinning).
- **Compositional data analysis → compositional data:** name shortened in the package; README confirms closure, CLR/ALR/ILR and Aitchison distance.
- **Fourier destriping → Fourier filtering:** record points to this package; README not found at the expected `fourier-destriping` slug. The canonical package uses the broader `fourier-filtering` slug; package content should be inspected before treating it as exact coverage.
- **Floating catchment accessibility → floating catchment:** record/package names differ by shortened suffix; README confirms 2SFCA/E2SFCA and distance-decay kernels.
- **Maximum flow/minimum cut → max-flow-min-cut:** package name uses an abbreviated slug; README documents Edmonds–Karp maximum flow and min-cut.

## Additional name overlap inspected (not yet crosswalked)

- **Voronoi/Delaunay:** package `voronoi-delaunay` is a SciPy/Qhull wrapper. It is not equivalent to the dependency-free Bowyer–Watson package, which is separately implemented. Keep these distinct.
- **Network flow:** `network-flow` implements Dinic, while `max-flow-min-cut` implements Edmonds–Karp. They are related algorithm families but different implementations and must not be merged as one record.

## Audit limits

This pass confirms six mappings from the file-level evidence. It does not read the source section rows, algorithm implementations, tests or notebook contents exhaustively, and does not establish completeness of source bibliography, technical claims, rights, or package correctness. A larger crosswalk remains open.
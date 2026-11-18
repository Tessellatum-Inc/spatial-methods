# Catalogue crosswalk — Batch 3: direct-name package inspection

**Snapshot:** 18 November 2026  
**Tree:** `abce9ea3ddb06aa53615f3a4d00ba3645a38b9a6`

This batch inspected 20 candidate package paths. Eleven direct-name matches were found and inspected; four GNSS verification slugs did not exist as package slugs under those names, and five additional candidate paths could not be retrieved. No mapping was guessed from absence.

## Confirmed inspected direct matches

- [`geohash`](../implementations/python/geohash/README.md) ↔ [verification record](verification/geohash.md)
- [`glcm-texture`](../implementations/python/glcm-texture/README.md) ↔ [verification record](verification/glcm-texture.md)
- [`greiner-hormann`](../implementations/python/greiner-hormann/README.md) ↔ [verification record](verification/greiner-hormann.md)
- [`haar-wavelet`](../implementations/python/haar-wavelet/README.md) ↔ [verification record](verification/haar-wavelet.md)
- [`hilbert-rtree`](../implementations/python/hilbert-rtree/README.md) ↔ [verification record](verification/hilbert-rtree.md)
- [`hough-lines`](../implementations/python/hough-lines/README.md) ↔ [verification record](verification/hough-lines.md)
- [`huff-model`](../implementations/python/huff-model/README.md) ↔ [verification record](verification/huff-model.md)
- [`insar-coherence`](../implementations/python/insar-coherence/README.md) ↔ [verification record](verification/insar-coherence.md)
- [`k-core`](../implementations/python/k-core/README.md) ↔ [verification record](verification/k-core.md)
- [`k-means`](../implementations/python/k-means/README.md) ↔ [verification record](verification/k-means.md)
- [`k-medoids`](../implementations/python/k-medoids/README.md) ↔ [verification record](verification/k-medoids.md)

## Not resolved in this batch

- `gnss-geometry-free-cycle-slip-screening`
- `gnss-integer-ambiguity-resolution`
- `gnss-lambda-integer-ambiguity-resolution`
- `gnss-melbourne-wubbena-cycle-slip-screening`
- `gnss-residual-raim-fde`
- `hansen-hurwitz`
- `hausdorff-frechet`
- `harris-market-potential`
- `inhomogeneous-ripley-k`

These remain name-mapping questions; a missing path in this inspection is not an orphan classification. Some may be represented by differently named package slugs.

## Important scope notes from README inspection

- **Geohash:** hierarchical rectangular address cells; not a metric distance measure.
- **GLCM:** comparison between scenes requires consistent quantisation range.
- **Greiner–Hormann:** restricted to simple hole-free rings and rejects certain touching/collinear boundary events.
- **Haar:** this is a 2-D Haar-only transform with even-dimension constraints.
- **Hilbert-packed R-tree:** immutable bulk-loaded structure, not a mutable production R-tree.
- **Hough lines:** standard normal-form line accumulator; not finite-segment detection or probabilistic Hough.
- **Huff model:** returns probabilistic allocation; does not estimate parameters or model facility capacity/strategic entry.
- **InSAR coherence:** requires aligned coregistered complex arrays; local window definition and crop behaviour are explicit.
- **k-core:** graph input is symmetrised; this is an undirected core decomposition, not directed-core analysis.
- **k-means:** Lloyd squared-Euclidean partitioning; caller controls k and scaling.
- **k-medoids:** PAM, CLARA and CLARANS use a precomputed dissimilarity matrix and are not equivalent to k-means.

## Limits

The audit reads README-level contracts only. It does not execute code, inspect tests, validate scientific claims against primary literature, inspect source-section indexes, or review third-party rights. No verification statuses are changed by this crosswalk.

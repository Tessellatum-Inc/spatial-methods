# Learning Release 01 — Do Two Line Segments Meet?

**Spatial Methods · Computational Geometry**

This release studies the pairwise intersection of two closed line segments, from the orientation determinant to an exact-arithmetic Python implementation.

## Choose your route

| Resource | Best used for |
|---|---|
| [Field guide](field-guide.md) | Independent study: intuition, formal method, implementation contract and limits |
| [Educator companion](educator-companion.md) | Lesson sequence, demonstrations, discussion prompts and assessment |
| [Canonical technical lesson](../../algorithms/geometry/segment-intersection.md) | Full technical explanation |
| [Python implementation](../../implementations/python/segment-intersection/README.md) | Runnable implementation and tests |
| [Implementation walkthrough](../../implementations/python/segment-intersection/implementation-walkthrough.md) | Read the code step by step |
| [Geometry foundations path](../../learning-paths/geometry-foundations.md) | Place this method in a wider learning sequence |

## Visual resources

- [Orientation cases](../../assets/learning-packs/01-segment-intersection/orientation.svg)
- [Intersection cases](../../assets/learning-packs/01-segment-intersection/intersection-cases.svg)
- [Decision flow](../../assets/learning-packs/01-segment-intersection/decision-flow.svg)

## Scope and technical contract

The accompanying reference implementation uses integer-coordinate endpoints, rejects zero-length segments, assumes a planar Cartesian coordinate system, and uses exact integer orientation arithmetic with rational coordinates for proper crossings. It does not provide a general floating-point geometry engine, coordinate snapping, CRS handling or an all-segment intersection sweep.

## Learning depth

- **FOUNDATIONS:** distinguish lines from segments and predict geometric cases.
- **METHOD:** derive and interpret the orientation determinant.
- **IMPLEMENTATION:** run the Python example and inspect tests.
- **ANALYSIS:** reason about degeneracies, exactness and complexity.
- **RESEARCH:** compare robust predicates and sweep-line algorithms.
- **TEACHING:** adapt the educator companion and original diagrams.

## Citation and reuse

Please retain Spatial Methods attribution and check the repository's [licensing and reuse policy](../../docs/licensing-and-reuse.md). Third-party references and materials retain their own terms.

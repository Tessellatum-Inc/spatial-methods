# Research Digest 01 — Robust Geometric Computation

**Spatial Methods · Research briefing**  
**Theme:** Why geometric software needs robust predicates  
**Status:** Editorial research note · Version 1.0

## Executive summary

A geometric algorithm can be mathematically correct and still fail in software when finite-precision arithmetic changes a decision near a boundary. In computational geometry, the most consequential decisions are often predicates: is a point left or right of a directed line, do two segments intersect, is a point inside a polygon, or which event occurs first?

A tiny numerical error can change a predicate's sign. That is not merely a small coordinate error: it can change the topology of the result, producing missing intersections, impossible polygon structures or inconsistent spatial relationships.

The practical lesson is to separate **predicates** (decisions about geometric relationships) from **constructions** (coordinates computed from those relationships), then choose an explicit precision strategy for each.

## 1. The failure mechanism

For points A, B and C, the orientation determinant is

\[
\operatorname{orient}(A,B,C) =
(B_x-A_x)(C_y-A_y) - (B_y-A_y)(C_x-A_x).
\]

Its sign classifies C as left of, right of or collinear with directed line AB. When the true value is close to zero, floating-point rounding can produce the wrong sign or turn a nonzero value into zero.

That can cause a downstream algorithm to take the wrong branch. In a segment-intersection routine, for example, the orientation signs determine whether segments straddle each other's supporting lines. A wrong sign can mean a missed crossing or a false contact.

The key distinction: the output may be numerically close to the expected coordinate while the underlying relationship is categorically wrong.

## 2. Predicates versus constructions

A **predicate** answers a discrete question: left/right/collinear, inside/outside, intersect/do not intersect. A **construction** creates a numerical object: an intersection coordinate, a circumcentre or a clipped geometry.

Robustness requires both to be considered, but they have different failure modes. Exact or adaptive predicates can preserve the correct combinatorial decisions. Constructions still need a deliberate representation and precision policy.

For integer coordinates, arbitrary-precision integer arithmetic can evaluate the orientation determinant exactly. For rational intersections, a rational representation can preserve exact values. These strategies are useful in teaching and selected workflows, but they are not automatically efficient or appropriate for every production workload.

## 3. Adaptive precision

Shewchuk's work on adaptive-precision floating-point arithmetic develops predicates that first use fast ordinary floating-point calculations with an error bound. If the result is safely separated from zero, the sign can be trusted. If it is uncertain, the calculation is refined using additional precision.

The broad engineering pattern is valuable:

1. use a fast approximate calculation;
2. estimate whether its error could change the decision;
3. accept the result only when it is certified;
4. fall back to more precise arithmetic when necessary.

This avoids paying the full cost of high-precision arithmetic for every easy case while protecting decisions in numerically difficult cases.

## 4. Why spatial systems care

Robust geometric decisions sit underneath many common spatial operations:

- overlay and clipping;
- polygon validity and boundary noding;
- spatial joins and topology construction;
- triangulation and mesh generation;
- line-network connectivity;
- map generalisation and geometric simplification.

A failure in one low-level predicate can propagate into higher-level data products. The issue is especially important when independently processed datasets are expected to share boundaries or topology.

## 5. Precision models are not a substitute for robust predicates

A precision model defines how coordinates are represented or quantised. Snapping can be a valid domain policy, for example when a workflow intentionally aligns data to a grid. But snapping changes the geometry and may collapse narrow features or alter relationships.

Robust predicates answer a different question: given the represented input coordinates, can the algorithm classify their geometric relationship reliably?

A sound system documents both:
- the coordinate and precision model used to represent input data;
- the numerical strategy used to make geometric decisions.

Neither should be hidden behind an unexplained tolerance.

## 6. Engineering checklist

When evaluating a geometry workflow, ask:

- Are coordinates integers, fixed precision, floating point or another representation?
- Which predicates control branching?
- Are error bounds or exact fallbacks used?
- Are constructed coordinates exact, rounded or grid-snapped?
- What happens for collinear, coincident, nearly coincident and degenerate inputs?
- Are results deterministic across platforms and execution paths?
- Are tests built around adversarial cases, not only visually obvious examples?
- Does the documented precision policy match the application's domain requirements?

## 7. Research and implementation route

1. Re-derive the orientation determinant and identify where its sign controls an algorithm.
2. Run the Spatial Methods [segment-intersection implementation](../implementations/python/segment-intersection/README.md).
3. Construct nearly collinear examples and compare exact integer results with floating-point calculations.
4. Read Shewchuk's paper and examine the adaptive error-bound strategy.
5. Compare the precision policies of geometry libraries used in your own GIS stack.

## 8. Selected references

- Shewchuk, J. R. (1997). “Adaptive Precision Floating-Point Arithmetic and Fast Robust Geometric Predicates.” *Discrete & Computational Geometry*, 18, 305–363. https://doi.org/10.1007/PL00009321
- IEEE 754-2019. *IEEE Standard for Floating-Point Arithmetic*. https://standards.ieee.org/standard/754-2019.html
- CGAL, *2D and 3D Linear Geometry Kernel* (documentation). https://doc.cgal.org/latest/Kernel_23/index.html
- GEOS, *Robustness* (project documentation). https://libgeos.org/usage/faq/

## Scope note

This digest is a curated technical orientation, not a systematic literature review or a substitute for library-specific documentation. Claims about a particular geometry engine should be checked against the exact version and precision model in use.

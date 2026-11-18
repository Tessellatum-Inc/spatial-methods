# Learning release 01: Do two line segments meet?

**Subject:** Computational geometry  
**Depth:** FOUNDATIONS · METHOD · IMPLEMENTATION · ANALYSIS · TEACHING  
**Prerequisites:** Basic coordinate geometry. Python familiarity is needed only for the implementation exercises.  
**Suggested study time:** 60–90 minutes for the core; additional study paths are provided below.

This is a guided companion to the public [segment intersection lesson](../algorithms/geometry/segment-intersection.md) and its [tested Python implementation](../implementations/python/segment-intersection/README.md).

## Why this method matters

Given two finite line segments, determine whether they do not meet, meet at one point, or share a segment.

A line extends forever. A segment does not. Checking whether two supporting lines intersect is not enough: the intersection may lie outside one or both finite segments.

This small geometric question appears in topology, map processing, CAD, computer graphics, robotics and spatial data validation. It is also a useful case study in how mathematical predicates, implementation details and data assumptions affect computational results.

## Choose your route

The core explanation is shared. Choose the additional depth that matches your purpose; these are entry points, not separate audiences or locked academic tracks.

- **Learner:** work through the intuition, classification table, guided exercises and worked answers.
- **Educator:** use the concept sequence, visual classification cases and exercise prompts to build a lesson or practical session.
- **Researcher:** examine predicate robustness, degeneracies, exact arithmetic, algorithmic variants and the boundary between pairwise testing and all-intersections problems.
- **Practitioner:** focus on precision policy, coordinate reference systems, geometry validity, spatial indexing and production-tool selection.
- **Developer:** run the reference implementation, inspect its tests, extend edge-case coverage and compare implementation strategies.

## Learning outcomes

By the end, you should be able to:
- distinguish a proper crossing, endpoint contact, collinear touch, collinear overlap and disjoint pair;
- explain why orientation tests are central to segment intersection;
- understand why exact integer predicates and rational intersection coordinates are useful;
- describe the boundary of this teaching implementation and when a more robust geometry engine is appropriate;
- identify why pairwise intersection and finding all intersections in a large collection are different computational problems.

## The key idea: orientation

For three points A, B and C, the signed 2D cross product is:

(B.x − A.x) × (C.y − A.y) − (B.y − A.y) × (C.x − A.x)

It indicates whether C lies to the left of, to the right of, or on the directed line from A to B.

For integer coordinates, Python integer arithmetic computes this determinant exactly. That avoids a common class of floating-point sign errors in the predicate itself.

For two non-collinear segments AB and CD, a proper crossing occurs when C and D lie on opposite sides of AB and A and B lie on opposite sides of CD. Boundary cases need additional handling: collinearity, endpoints and overlap.

## Classification table

| Case | What happens | Classification |
|---|---|---|
| Proper crossing | Interior of each segment crosses the other | One shared point |
| Endpoint contact | One endpoint lies on the other segment | One shared point |
| Collinear touch | Collinear segments meet at one endpoint only | One shared point |
| Collinear overlap | They share a positive-length interval | Shared segment |
| Parallel/disjoint | No point is shared | No intersection |
| Collinear but separated | Same supporting line, disjoint finite ranges | No intersection |

## Guided practice

Use the public implementation as the reference. Run its tests before changing anything:

    cd implementations/python/segment-intersection
    python -m pip install -r requirements.txt
    python -m pytest -q

Then work through the exercises. Write down expected classifications before changing the implementation.

### Exercise 1 — classify by inspection

For each pair, classify the result as no intersection, one point or a shared segment.

1. A=(0,0), B=(4,4); C=(0,4), D=(4,0)
2. A=(0,0), B=(4,0); C=(4,0), D=(7,2)
3. A=(0,0), B=(5,0); C=(2,0), D=(7,0)
4. A=(0,0), B=(2,0); C=(3,0), D=(5,0)
5. A=(1,1), B=(1,5); C=(-1,3), D=(3,3)

### Exercise 2 — why the bounding range matters

Two collinear segments lie on the x-axis: AB from x=1 to x=3, and CD from x=5 to x=8.

Their supporting lines coincide. Explain why the segments do not intersect, and identify the interval test that rules out an overlap.

### Exercise 3 — orientation signs

For A=(0,0), B=(4,0), calculate the orientation determinant for C=(2,3), D=(2,-3) and E=(2,0). State the sign and geometric meaning of each result.

### Exercise 4 — adversarial boundaries

Create one test case for each:
- a vertical segment crossing a horizontal segment;
- a zero-length segment whose point lies on another segment;
- a collinear overlap where the second segment is reversed;
- two segments that are almost parallel but do not meet.

Write the expected classification before running tests.

### Exercise 5 — choose the right tool

The teaching implementation uses integer endpoints and exact rational output for a pair of segments. Your production dataset contains millions of floating-point geometries in mixed coordinate reference systems.

Explain at least four additional concerns before using this pairwise function in production. Consider robust predicates, coordinate reference systems, spatial indexing, precision policy, geometry validity and the cost of testing every pair.

## Educator extension

A short teaching sequence can be organised around three questions:

1. Why is testing infinite lines insufficient for finite segments?
2. How can the orientation of three points be determined without calculating angles?
3. Why do collinear and endpoint cases require explicit treatment?

Ask learners to predict each classification before revealing the result. Use the six-row classification table as a formative assessment prompt. For a longer session, have learners design test cases before inspecting the implementation.

## Research extension

Use these questions to move beyond the introductory predicate:

- What guarantees are required of an orientation predicate for a geometric algorithm to remain topologically consistent?
- When are exact integer arithmetic and rational constructions practical, and when do coordinate magnitude or representation constraints matter?
- How do adaptive-precision predicates differ from applying an arbitrary floating-point epsilon?
- What changes when the task is to report every intersection among n segments rather than test one pair?
- Compare a pairwise predicate with a sweep-line approach such as Bentley–Ottmann. What assumptions affect the complexity and robustness of each?
- Which degeneracies must an implementation define and handle explicitly?

A research treatment should consult primary literature and robust computational geometry references before making claims about guarantees or performance. This pack is a starting point, not a literature review or claim of novel research.

## Practitioner extension

Before using a pairwise segment function in a production workflow, document:
- the coordinate reference system and units;
- the coordinate precision and tolerance policy;
- geometry validity assumptions;
- the exact meaning of intersection required by the application;
- how candidate pairs are selected (for example, spatial indexing);
- the geometry engine and predicate semantics;
- expected data volume and performance requirements;
- validation against representative and adversarial cases.

A pairwise teaching function is not a scalable overlay pipeline.

## Hints

- A segment's bounding box is a cheap necessary condition for intersection.
- Orientation signs detect which side of a directed line a point lies on.
- Collinear cases cannot be decided by orientation alone; compare coordinate intervals.
- A zero-length segment is a point and deserves explicit treatment.
- Pairwise intersection is not the same problem as finding every intersection among a large set of segments.

## Worked answers

### Exercise 1

1. One point: the segments cross at (2,2).
2. One point: they share endpoint (4,0).
3. Shared segment: the overlap is from x=2 to x=5 on y=0.
4. No intersection: the intervals are separated.
5. One point: the vertical and horizontal segments cross at (1,3).

### Exercise 2

The segments occupy disjoint finite intervals. Their x-ranges are [1,3] and [5,8], so max(1,5) is greater than min(3,8); there is no overlap. Coincident supporting lines do not imply overlapping finite segments.

### Exercise 3

For A=(0,0), B=(4,0), the determinant simplifies to 4 × C.y.

- C=(2,3): +12, left of AB.
- D=(2,-3): −12, right of AB.
- E=(2,0): 0, collinear with AB.

### Exercise 4

There are many valid answers. Check that each expected result matches finite segment geometry, not merely the infinite supporting lines. For nearly parallel floating-point inputs, the expected classification should follow a stated precision model rather than an arbitrary epsilon.

### Exercise 5

At minimum: transform data to an appropriate common CRS; define precision and validity policies; use a spatial index or sweep-line method to avoid all-pairs comparisons; use robust predicates appropriate to floating-point coordinates; document geometry-engine semantics; and benchmark realistic data. A pairwise teaching function is not a scalable overlay pipeline.

## Self-check

You are ready to move on when you can explain:
- why a line intersection may fall outside the segments;
- why collinear cases need interval comparisons;
- why exact predicates help with integer inputs;
- why a pairwise function is not an all-segment algorithm;
- which assumptions you would document before applying the method to real data.

## Continue learning

- Public concept: [Segment intersection](../algorithms/geometry/segment-intersection.md)
- Public implementation and tests: [Python walkthrough](../implementations/python/segment-intersection/implementation-walkthrough.md)
- Related all-segment method: [Bentley–Ottmann sweep line](../algorithms/geometry/bentley-ottmann.md)
- Related path: [Geometry foundations](../learning-paths/geometry-foundations.md)

## Member discussion prompt

Where have you encountered geometry that appears to intersect on a map but fails a computational test—or the reverse? Describe the data, coordinate system and precision assumptions. Avoid sharing confidential client data.

## Scope note

This is a multi-entry guided learning resource, not a complete treatment of computational geometry, a formal verification, a production deployment guide or an exhaustive research review. Follow the linked canonical lesson, implementation and references for the technical source material; report corrections or missing cases through the repository's contribution process.

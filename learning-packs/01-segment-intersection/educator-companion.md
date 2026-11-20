# Educator Companion — Learning Release 01

**Topic:** Pairwise line-segment intersection  
**Audience:** Undergraduate and postgraduate teaching, short courses, professional training  
**Suggested duration:** 60–90 minutes, adaptable  
**Prerequisites:** Coordinate geometry; determinants are helpful but can be introduced during the session.

## Teaching purpose

This companion helps an instructor teach the reasoning behind a segment-intersection predicate rather than only demonstrate a software function. It can support lectures, tutorials, practical labs or independent study.

It is not a prescribed curriculum or an accreditation-aligned syllabus. Adapt examples, notation and assessment to the learners and course context.

## Learning objectives

Learners should be able to:
1. distinguish infinite lines from finite segments;
2. explain the orientation determinant and interpret its sign;
3. describe the strict straddling condition for a proper crossing;
4. explain why endpoint and collinear cases need additional tests;
5. distinguish pairwise intersection from the all-segment reporting problem;
6. identify the limits of an integer-coordinate teaching implementation.

## Suggested lesson sequence

| Time | Activity | Teaching move |
|---|---|---|
| 0–10 min | Pose the problem | Show two visually crossing segments; ask what a computer must decide |
| 10–20 min | Line versus segment | Use a crossing of supporting lines outside the finite segment |
| 20–35 min | Orientation | Derive the determinant and interpret positive, negative and zero |
| 35–50 min | Intersection cases | Compare proper crossing, endpoint touch, collinear touch and overlap |
| 50–65 min | Algorithm and implementation | Walk through the predicate and run the test suite |
| 65–80 min | Scale and robustness | Discuss floating-point predicates, CRS and all-pairs complexity |
| 80–90 min | Exit task | Ask learners to construct and classify a boundary case |

## Demonstration sequence

### Demonstration A — proper crossing

Use AB = (0,0)–(4,4) and CD = (0,4)–(4,0). Ask learners to predict the intersection before calculating it. The result is (2,2).

### Demonstration B — endpoint contact

Use AB = (0,0)–(4,0) and CD = (4,0)–(7,2). The segments share one endpoint. Emphasise that strict opposite-side signs alone do not capture this case.

### Demonstration C — collinear overlap

Use AB = (0,0)–(5,0) and CD = (2,0)–(7,0). The shared geometry is a segment, not a single point.

### Demonstration D — collinear separation

Use AB = (0,0)–(2,0) and CD = (3,0)–(5,0). Their supporting lines coincide, but the finite segments do not meet.

## Discussion prompts

- Why does the orientation determinant avoid calculating angles?
- Why does collinearity require a separate interval test?
- Should an API return a Boolean, a point, or a richer geometry result?
- What can go wrong if an application rounds constructed intersection coordinates?
- Why is testing every pair potentially expensive?
- Which assumptions change when coordinates are longitude and latitude?

## Assessment tasks

1. Calculate the orientation determinant for A=(0,0), B=(4,0), C=(2,3), then interpret the result.
2. Construct two collinear but disjoint segments and explain why they do not intersect.
3. Give an example where two supporting lines intersect but their finite segments do not.
4. Explain why a zero-length segment falls outside the reference implementation's input contract.
5. For n=500 segments, calculate the number of unordered pairs in an all-pairs test.

**Instructor note:** 500 × 499 / 2 = 124,750 pair tests.

## Practical lab

Use the repository implementation:

```bash
cd implementations/python/segment-intersection
python -m pip install -r requirements.txt
python -m pytest -q
python segment_intersection.py
```

Ask learners to inspect the tests, predict the output of a new case, and add a test before changing implementation code.

The implementation rejects zero-length segments. Treat that as an explicit contract decision, not as evidence that zero-length geometries never occur in spatial datasets.

## Extension routes

**For advanced mathematical study**
- Prove the strict straddling condition for non-collinear proper crossings.
- Explore exact predicates and rational constructions.
- Examine degeneracies in geometric algorithms.

**For research seminars**
- Read Bentley and Ottmann (1979).
- Compare the general-position assumptions of the classical sweep-line algorithm with real GIS data.
- Read Shewchuk (1997) on adaptive-precision predicates.

**For professional training**
- Compare coordinate reference systems and precision policies.
- Examine geometry-engine semantics.
- Discuss spatial indexing and candidate-pair generation.
- Use a representative dataset and document the limitations of the selected tool.

## Instructor reuse and attribution

This companion is part of Spatial Methods. Check the repository's licence and attribution notices before adapting or redistributing it. Third-party figures and references retain their own terms. Do not imply that this resource is accredited or a substitute for an institution's course requirements.

## Source material

- [Segment-intersection technical lesson](../../algorithms/geometry/segment-intersection.md)
- [Python implementation](../../implementations/python/segment-intersection/README.md)
- [Implementation walkthrough](../../implementations/python/segment-intersection/implementation-walkthrough.md)
- Bentley & Ottmann (1979): https://doi.org/10.1109/TC.1979.1675432
- Shewchuk (1997): https://doi.org/10.1007/PL00009321

# Static slab point locator

This package implements a restricted static point-location structure for a set of valid, pairwise interior-disjoint polygon faces with linear ring boundaries.

It returns:
- the face identifier when a query lies inside one polygon face;
- None for the outside/unbounded face;
- BOUNDARY when the query lies on a represented boundary.

## Run

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Example

~~~python
from slab_locator import SlabPointLocator

faces = {
    "west": [[(0, 0), (2, 0), (2, 2), (0, 2), (0, 0)]],
    "east": [[(2, 0), (4, 0), (4, 2), (2, 2), (2, 0)]],
}
locator = SlabPointLocator(faces)
print(locator.locate(1, 1))
print(locator.locate(3, 1))
print(locator.locate(2, 1))
~~~

## Complexity and limitations

The straightforward preprocessing stores an edge event in every x-slab it crosses, so storage and construction can be O(n²) in the worst case. A query uses binary search over x-events and the slab's preordered edge groups, giving O(log n) comparisons for points strictly inside a slab. Queries on x-event lines use a boundary-aware fallback scan.

This is not Seidel's randomized trapezoidal map and does not implement its expected bounds. It assumes non-crossing polygon boundaries and pairwise interior-disjoint faces. The input ring structure and polygon topology must be valid; this package does not validate arbitrary planar arrangements. It is a teaching implementation of a static slab locator. Use the [interactive point-location lab](../../../notebooks/point-location-lab.ipynb) to inspect the x-event lines, slab crossing groups, holes and boundary-query contract.


## Randomized trapezoidal map with persistent history DAG

The adjacent `randomized_trapezoidal_map.py` module adds a second, deliberately narrower model: a set of pairwise disjoint, non-vertical segments in general position inside a bounding rectangle. It merges consecutive slab intervals with identical bounding segments into trapezoids, then builds a balanced x-decision tree and per-slab y-decision trees with shared decision subtrees. Queries return the containing trapezoid, `BOUNDARY` on an original segment, or `None` outside the bounding box.

Run the same package test command to exercise both locators.

**Important algorithmic qualification:** segments are visited in a seeded random permutation, but this reference implementation rebuilds the decomposition after each insertion. Each decomposition also exposes reciprocal left/right trapezoid-neighbor IDs across shared vertical sides. Insertion now applies corridor replacements to a persistent cell-graph snapshot: crossed cells are removed, uncrossed endpoint caps are retained, and compatible lower/upper fragments are coalesced. Each snapshot is checked for reciprocal neighbor links and full-domain coverage. Neighbor links are currently re-derived for the full snapshot, and an experimental persistent history DAG is now updated by replacing old trapezoid leaves with endpoint x-decisions and segment y-decisions. Public point queries now traverse the persistent history DAG; the independently rebuilt slab locator remains available as a private differential oracle. Seeded randomized query tests compare both structures across multiple insertion orders. It does not claim the classic expected (O(n\log n)) construction bound. Its purpose is to establish and test the trapezoid/search invariants under explicit general-position assumptions. The DAG currently lacks a proven asymptotic bound and fully local neighbor maintenance; further work is needed before claiming a complete optimized Seidel implementation.

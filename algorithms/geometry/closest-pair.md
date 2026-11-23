# Closest pair of planar points

Given a finite set of at least two planar point occurrences, the closest-pair problem asks for the pair with minimum Euclidean distance. A pairwise scan is simple but costs O(n²); divide and conquer reduces the asymptotic running time to O(n log n).

## Divide-and-conquer algorithm

1. Sort points by x-coordinate (breaking ties by y and original index) and separately by y-coordinate.
2. Split the x-sorted sequence into two balanced halves.
3. Recursively find the closest pair in each half.
4. Let δ be the smaller of those two distances. Any better cross-half pair must lie within horizontal distance δ of the split line.
5. Scan this vertical strip in y-order. Planar packing bounds the number of successors that need inspection by a constant (the familiar seven-successor bound).
6. Return the best pair, with a deterministic tie rule.

The y-sorted order is carried through recursive calls by partitioning on original point identity. Re-sorting each strip at every level would add avoidable logarithmic work.

## Correctness intuition

A closest pair is either entirely in the left half, entirely in the right half, or crosses the split. The recursive calls find the first two categories. In the crossing case, both endpoints must be within δ horizontally of the split; otherwise their horizontal separation alone is at least δ. In y-order, the packing argument limits how many points can be closer than δ to a given strip point, so the constant-neighbour scan finds every potentially improving cross pair.

## Complexity and implementation contract

Sorting costs O(n log n). The recursive work satisfies T(n)=2T(n/2)+O(n), hence O(n log n). The teaching implementation stores x/y partitions and recursive strips, using O(n log n) total temporary allocation in its straightforward form (the standard optimized implementation can achieve O(n) auxiliary space).

The implementation accepts duplicate coordinates, treats repeated coordinates as distinct input occurrences, and returns zero distance when any duplicate pair exists. It requires finite 2D coordinates and at least two points. Distances and predicates use floating-point arithmetic, so this is not an exact-predicate computational-geometry kernel.

## Reproduction

See the [Python implementation and tests](../../implementations/python/closest-pair/README.md). Seeded random clouds are checked against an independent O(n²) oracle; duplicate, collinear, negative-coordinate and invalid-input cases are included.

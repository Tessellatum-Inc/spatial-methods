# Hausdorff and Fréchet distances

Two geometries can be compared by asking how far their represented locations are from one another. The answer depends on whether order matters and whether the input is treated as a set of points or as a traversed curve.

## Directed and symmetric Hausdorff distance

For finite point sets A and B, the directed Hausdorff distance is

\[
h(A,B)=\max_{a\in A}\min_{b\in B} d(a,b).
\]

The symmetric Hausdorff distance is

\[
H(A,B)=\max\{h(A,B),h(B,A)\}.
\]

It measures the worst nearest-neighbour mismatch between the sampled point sets. It ignores vertex order and does not measure distance to the continuous segments between vertices. The straightforward implementation costs O(|A||B|); spatial indexing can accelerate nearest-neighbour queries.

## Discrete Fréchet distance

For ordered sequences P=(p_1,\ldots,p_m) and Q=(q_1,\ldots,q_n), the discrete Fréchet dynamic program is

\[
C(i,j)=\max\left(d(p_i,q_j),\min\{C(i-1,j),C(i-1,j-1),C(i,j-1)\}\right),
\]

with the first row and column initialized by cumulative maxima. The result is the minimum leash length needed to traverse both vertex sequences monotonically, allowing one sequence to pause while the other advances.

The rolling-row implementation uses O(mn) time and O(min(m,n)) memory by placing the shorter sequence in the DP columns. It is sensitive to sampling and is not the continuous Fréchet distance between piecewise-linear curves.

## Choose the right comparison

- Use Hausdorff for unordered sampled point sets and worst-case spatial discrepancy.
- Use discrete Fréchet when traversal order and progression along a line matter.
- Use continuous Fréchet when the geometry between vertices matters. The Alt–Godau free-space diagram decides whether a leash of length ε can connect the two curve endpoints through reachable free space; bisection over ε approximates the minimum leash length.
- Confirm both inputs share a projected planar CRS and compatible units.

## References

- Hausdorff, F. (1914). *Grundzüge der Mengenlehre*. Leipzig: Veit.
- Eiter, T. and Mannila, H. (1994). *Computing Discrete Fréchet Distance*. Technical Report CD-TR 94/64, Vienna University of Technology.

The [tested Python package](../../implementations/python/geometry-metrics/README.md) provides sampled-set Hausdorff, discrete Fréchet, and continuous Fréchet implementations, tests and [interactive lab](../../notebooks/geometry-metrics-lab.ipynb).


## Continuous Fréchet distance: free-space reachability

For a threshold ε, the free-space diagram contains parameter pairs (s,t) for which the two curve positions are at most ε apart. Each cell corresponds to one segment from each curve. The free-space portion inside a cell is convex, so reachability can be propagated along its top and right boundaries from reachable bottom and left intervals. A path from the lower-left to upper-right parameter-space corners exists exactly when the continuous Fréchet distance is at most ε.

The package implements this decision procedure in O(mn) time and O(min(m,n)) auxiliary memory for m and n segments by retaining only the previous and current free-space boundary rows. It approximates the distance by bisection on ε until an absolute tolerance is reached. The returned value is an upper bound within that tolerance, subject to floating-point arithmetic; it is not a symbolic exact value.

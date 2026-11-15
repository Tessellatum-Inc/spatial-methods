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

The rolling-row implementation uses O(mn) time and O(n) memory. It is sensitive to sampling and is not the continuous Fréchet distance between piecewise-linear curves.

## Choose the right comparison

- Use Hausdorff for unordered sampled point sets and worst-case spatial discrepancy.
- Use discrete Fréchet when traversal order and progression along a line matter.
- Use a continuous Fréchet method when the geometry between vertices matters.
- Confirm both inputs share a projected planar CRS and compatible units.

## References

- Hausdorff, F. (1914). *Grundzüge der Mengenlehre*. Leipzig: Veit.
- Eiter, T. and Mannila, H. (1994). *Computing Discrete Fréchet Distance*. Technical Report CD-TR 94/64, Vienna University of Technology.

The [tested Python package](../../implementations/python/geometry-metrics/README.md) provides the sampled-set Hausdorff and discrete Fréchet baselines, tests and [interactive lab](../../notebooks/geometry-metrics-lab.ipynb).

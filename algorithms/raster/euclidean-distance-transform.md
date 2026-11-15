# Euclidean distance transform: distance from every cell to a target

Stable ID: `SA-RASTER-EUCLIDEAN-DISTANCE-TRANSFORM` · Draft 0.1 · Source compendium section 4, page 6

## The question

Given a raster mask of target cells, how far is each other cell from its nearest target? This appears in proximity analysis, buffer-like raster operations, habitat distance, facility access screening and many image-processing workflows.

An exact Euclidean distance transform calculates the straight-line distance between cell centres. It is not a least-cost path and does not account for barriers.

## Definition

Let $T$ be the set of target-cell indices. For cell $p=(r,c)$, with row spacing $s_r$ and column spacing $s_c$, the distance is:

$$
D(p)=\min_{q=(r_q,c_q)\in T}
\sqrt{(s_r(r-r_q))^2+(s_c(c-c_q))^2}.
$$

The spacing terms convert row and column offsets into map units. If cell dimensions differ, the distance is anisotropic in array-index space even though it is Euclidean in map coordinates.

## A small grid

For a target at the centre of a 5 by 5 grid:

~~~text
4  3  2  3  4
3  2  1  2  3
2  1  0  1  2
3  2  1  2  3
4  3  2  3  4
~~~

This illustration assumes square unit cells and shows the centre-to-centre distances. With non-square cells, diagonal and horizontal/vertical distances change according to the supplied spacing.

## Algorithm family

The exact Euclidean distance transform can be computed efficiently using separability of the squared Euclidean distance and one-dimensional lower-envelope computations. Felzenszwalb and Huttenlocher describe a linear-time method for sampled functions and grids. This differs from a chamfer transform, which uses an approximate neighbourhood metric, and from cost-distance, which accumulates costs over a movement model.

### One-dimensional lower envelope

For a sampled cost function \(f(i)\) and spacing \(s\), the squared transform is
\[
D(q)=\min_i\{f(i)+s^2(q-i)^2\}.
\]
Every finite sample defines a parabola. The algorithm maintains the lower envelope using two arrays: \(v\) stores the indices of the active parabolas and \(z\) stores the intersection coordinates where the active minimum changes. A new parabola removes any previous parabola whose active interval it entirely dominates. Once the envelope is built, a single forward scan evaluates the minimum at every grid index.

The binary-image transform starts with \(f=0\) at target cells and \(f=+\infty\) elsewhere. The implementation skips infinite candidates, so rows with no target remain infinite during the first pass.

### Separable two-dimensional transform

The squared Euclidean distance separates into row and column contributions. Apply the 1-D transform to every row with column spacing, then to every column with row spacing. The result is the exact squared distance to the nearest target; take its square root for map-unit distances. The two passes require O(HW) work for a fixed 2-D grid.

The [Python implementation](../../implementations/python/raster-distance/README.md) implements both the 1-D lower-envelope routine and the 2-D separable transform directly, rather than delegating to SciPy.

## Raster-specific decisions

- **Cell spacing:** pass row and column spacing in map units; do not assume square cells.
- **CRS:** use a suitable projected grid when interpreting distances as ground units.
- **Cell support:** the calculation is between cell centres, not between polygon boundaries.
- **Targets:** True marks target cells; at least one target is required.
- **NoData:** this teaching wrapper does not infer NoData or barrier semantics. Decide how invalid cells should be handled.
- **Movement model:** barriers and travel costs require a different method, such as cost-distance or least-cost path.

## Complexity and implementation

The Felzenszwalb–Huttenlocher family computes the exact transform in time linear in the number of grid cells for a fixed-dimensional grid. The teaching package implements the lower-envelope construction and both separable passes in NumPy/Python. The one-dimensional routine is also exposed for arbitrary finite sampled costs plus positive infinity.

## Exercises

1. Change the target from one cell to several. Explain why each cell takes the distance to the nearest target.
2. Change cell spacing from $(1,1)$ to $(2,5)$. Predict the distance to a diagonal neighbour before running the code.
3. Compare the Euclidean result with a Manhattan-distance approximation. Which directions differ most?
4. Add a NoData region. Decide whether distance should be calculated across it, masked there or constrained by it.
5. Explain why a road-network travel-time surface cannot be computed by this Euclidean transform.

## References

- Felzenszwalb, P. F. and Huttenlocher, D. P. (2012), [Distance Transforms of Sampled Functions](https://doi.org/10.4086/toc.2012.v008a019), Theory of Computing, 8, 415–428.
- The algorithm is derived from the published lower-envelope method; no source code or figures are copied.

**Scope:** exact Euclidean distance on a regular 2D raster grid; no cost surface, obstacle-aware path or NoData policy is implemented.

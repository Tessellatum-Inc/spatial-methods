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

The [Python example](../../implementations/python/raster-distance/README.md) implements the lower-envelope algorithm directly. Its one-dimensional routine is independently testable and its two-dimensional transform applies separable row and column passes.

## Raster-specific decisions

- **Cell spacing:** pass row and column spacing in map units; do not assume square cells.
- **CRS:** use a suitable projected grid when interpreting distances as ground units.
- **Cell support:** the calculation is between cell centres, not between polygon boundaries.
- **Targets:** True marks target cells; at least one target is required.
- **NoData:** this teaching wrapper does not infer NoData or barrier semantics. Decide how invalid cells should be handled.
- **Movement model:** barriers and travel costs require a different method, such as cost-distance or least-cost path.

## Complexity and implementation

The Felzenszwalb–Huttenlocher family computes the exact transform in time linear in the number of grid cells for a fixed-dimensional grid. The teaching package implements the Felzenszwalb–Huttenlocher lower-envelope method directly in NumPy. The 1D envelope construction and evaluation are O(n); applying it once per row and once per column gives O(HW) time for an H-by-W grid.

## Exercises

1. Change the target from one cell to several. Explain why each cell takes the distance to the nearest target.
2. Change cell spacing from $(1,1)$ to $(2,5)$. Predict the distance to a diagonal neighbour before running the code.
3. Compare the Euclidean result with a Manhattan-distance approximation. Which directions differ most?
4. Add a NoData region. Decide whether distance should be calculated across it, masked there or constrained by it.
5. Explain why a road-network travel-time surface cannot be computed by this Euclidean transform.

## References

- Felzenszwalb, P. F. and Huttenlocher, D. P. (2012), [Distance Transforms of Sampled Functions](https://doi.org/10.4086/cgt.2012.004), Theory of Computing, 8, 415–428.
- The implementation is checked against brute-force minimisation on seeded one- and two-dimensional cases; SciPy's `distance_transform_edt` can also serve as an independent external comparison.

**Scope:** exact Euclidean distance on a regular 2D raster grid; no cost surface, obstacle-aware path or NoData policy is implemented.


## Eight-neighbour chamfer distance

The companion `chamfer_distance_to_targets` computes an 8-neighbour path metric. Cardinal moves cost the corresponding row or column spacing, and diagonal moves cost

$$w_d=\sqrt{\Delta x^2+\Delta y^2}.$$

A forward raster scan relaxes north, northwest, northeast and west predecessors; a reverse scan relaxes the opposite directions. With no barriers, shortest paths can be chosen monotone in row and column, so these two scans recover the shortest path on this eight-neighbour graph. The result is a chamfer approximation to Euclidean distance, not the exact centre-to-centre Euclidean distance produced by the lower-envelope transform above. The package tests both against independent brute-force references. This implementation does not model barriers or variable traversal costs.

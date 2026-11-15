# Discrete Lloyd iteration for centroidal Voronoi tessellations

A NumPy-only baseline for weighted Lloyd iteration over a finite set of sample points. Each iteration assigns each sample to its nearest generator and moves each nonempty generator to the weighted centroid of its assigned samples.

Run from this directory with `python -m pytest -q`.

## Scope

This is a **discrete sample approximation** to a centroidal Voronoi tessellation (CVT). It does not integrate over exact continuous cells, clip cells to polygon boundaries, compute power diagrams, enforce capacities, solve semi-discrete optimal transport, or operate intrinsically on a mesh or curved surface. Euclidean distance is used in the supplied coordinate space; geographic longitude/latitude must not be used as if it were a planar metric.

Empty or zero-mass clusters retain their previous generator. Initial seeds affect the local solution. The algorithm is a local iterative method, not a guarantee of a globally optimal partition. Objective values can depend on sample density, weights, initialization and stopping tolerance.

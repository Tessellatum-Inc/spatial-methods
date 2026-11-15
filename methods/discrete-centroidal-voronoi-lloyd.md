# Discrete centroidal Voronoi tessellation with Lloyd iteration

A Voronoi cell assigns each point in a domain to its nearest generator. A centroidal Voronoi tessellation (CVT) is a special case in which each generator is also the mass centroid of its own cell. Lloyd iteration alternates between nearest-generator assignment and centroid updates.

## Implemented baseline

The [NumPy implementation](../implementations/python/voronoi-lloyd/README.md) operates on a finite sample of points. For each sample point (x_i), it assigns the nearest generator (z_j), then updates each nonempty generator to the weighted mean of its assigned samples:
[
z_j^{(t+1)} =
rac{sum_{iin V_j^{(t)}} w_i x_i}
{sum_{iin V_j^{(t)}} w_i}.
]
This is a discrete approximation to the continuous CVT energy. The implementation returns generators, assignments, objective history and iteration count.

## Limitations and spatial cautions

This is not a polygon-clipped continuous CVT solver. It does not construct exact Voronoi polygons, power diagrams, capacity-constrained regions or semi-discrete optimal transport. It uses Euclidean coordinates, so projected metric coordinates are needed for geographic work. Initial seeds can lead to different local solutions; empty/zero-mass cells retain their previous generator. The method does not guarantee a global optimum.

For spatial service allocation, ordinary nearest-seed CVT does not enforce equal population, capacity, compactness, barriers, travel networks or administrative constraints. Those require distinct constrained formulations.

## Sources

- Du, Q., Faber, V., & Gunzburger, M. (1999). “Centroidal Voronoi Tessellations: Applications and Algorithms.” *SIAM Review*, 41(4), 637–676. [DOI](https://doi.org/10.1137/S0036144599352836).
- Du, Q., Emelianenko, M., & Ju, L. (2006). “Convergence of the Lloyd Algorithm for Computing Centroidal Voronoi Tessellations.” *SIAM Journal on Numerical Analysis*, 44(1), 102–119. [DOI](https://doi.org/10.1137/040617364).

No source text, figures or datasets are reproduced.

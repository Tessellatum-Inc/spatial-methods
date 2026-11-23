# Biodiversity occurrence and grid metrics

## Extent of occurrence

The extent of occurrence (EOO) baseline is the area of the convex hull around known occurrence coordinates. The implementation returns the hull vertices and planar area. Fewer than three unique non-collinear occurrences have zero area. The convex hull is a broad range envelope; it does not model habitat suitability, barriers or disjunct subpopulations.

## Area of occupancy

The area of occupancy (AOO) baseline counts distinct cells containing at least one occurrence on a caller-aligned square grid. With projected coordinates in metres and a 2,000 m cell size, each occupied cell contributes 4 km². Grid origin and alignment affect the result and must be declared; the code does not project coordinates or choose the assessment grid.

## Species richness and weighted endemism

For a binary cells-by-species presence matrix, species richness is the row sum. Weighted endemism for cell i is

\[
WE_i=\sum_{s\in S_i}\frac{1}{R_s},
\]

where S_i is the set of species present in cell i and R_s is the number of cells occupied by species s in the supplied matrix. Species restricted to fewer cells therefore contribute more weight.

## Scope and caveats

These are metric kernels, not a complete IUCN Red List assessment. They do not implement alpha hulls, range fragmentation, sampling-bias correction, taxonomic uncertainty, temporal range change, key-biodiversity-area criteria or phylogenetic diversity. Use suitable equal-area projected coordinates for area calculations and document grid origin and resolution.

## Verification

Tests use an analytic triangle hull, degenerate collinear/singleton cases, independently enumerated occupied cells and direct inverse-range-size calculations.

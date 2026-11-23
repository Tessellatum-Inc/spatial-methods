# Categorical landscape metrics: patches, edges and diversity

Landscape metrics summarize the composition and configuration of a categorical raster. They depend on map resolution, class definitions, raster alignment, NoData treatment and the chosen neighborhood rule.

## Patch delineation

A patch is a connected component of cells belonging to the same class. Four-neighbour connectivity uses shared edges; eight-neighbour connectivity also treats diagonal contact as connected. The choice changes patch counts and should be reported. For each class, the reference implementation reports patch count, total class area, mean patch area and largest-patch index:

\[
LPI_c=100\frac{A_{c,\max}}{A_{landscape}}.
\]

## Internal edge density

The implementation counts horizontal and vertical shared cell sides where both cells are valid and their class labels differ. If cell width is (s), each such boundary contributes length (s). Edge density is

\[
ED=\frac{E\,s}{A_{landscape}/10{,}000},
\]

where (E) is the number of unlike-class shared sides and cell size (s) is in metres. The result is metres of internal class boundary per hectare. The raster perimeter and boundaries against NoData are excluded; this convention is intentionally explicit and differs from metrics that include background or landscape boundaries.

## Shannon class diversity

For class proportions (p_i) across valid cells,

\[
H'=-\sum_i p_i\ln(p_i).
\]

This measures compositional diversity, not spatial configuration. Two rasters with the same class proportions have the same Shannon value even if one is highly fragmented and the other is contiguous.

## Scope and cautions

The package implements these baseline metrics alongside extent of occurrence, area of occupancy, species richness and weighted endemism. It is not a complete FRAGSTATS replacement and does not implement contagion, interspersion/juxtaposition, core area, shape metrics, patch cohesion, IIC/PC connectivity, or alpha/beta diversity. Use a suitable projected grid, document cell size and alignment, and test sensitivity to resolution and connectivity. These metrics alone do not establish ecological function or conservation value.

Independent tests use small categorical rasters with hand-computable patch counts, edge counts, areas, connectivity changes, NoData behavior and Shannon values.

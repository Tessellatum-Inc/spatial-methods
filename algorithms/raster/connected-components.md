# Connected-component labeling in raster masks

Stable ID: SA-RASTER-CONNECTED-COMPONENTS · Draft 0.1 · Source compendium section 4, page 6

## The problem

A binary raster mask marks cells that satisfy a condition: water, buildings, vegetation, detected objects or another class. Connected-component labeling assigns a unique identifier to each connected foreground region.

The operation is common in image analysis, raster GIS, object extraction and preprocessing for region-level measurements.

## Connectivity changes the result

- **4-connectivity:** cells connect through shared edges (north, south, east, west).
- **8-connectivity:** diagonal neighbours also connect.

Two pixels that touch only at a corner are separate under 4-connectivity and connected under 8-connectivity. Choose the rule to match the meaning of adjacency in the application.

## Breadth-first labeling

The [Python baseline](../../implementations/python/raster-components/README.md) scans the grid in row-major order. When it finds an unlabelled foreground cell, it starts a breadth-first traversal, assigning one positive component label to every reachable foreground neighbour.

Label zero represents background and invalid cells. A separate valid mask can mark NoData cells as barriers.

Every cell is visited at most once, giving:

$$T(R,C)=O(RC)$$

The label raster requires O(RC) memory; the queue can grow to the size of the largest component.

## Flood fill and run-length encoding

The same package includes seed-based **flood fill**: it returns the exact-value
region connected to a seed under 4- or 8-neighbour connectivity. A validity
mask makes NoData cells barriers; a seed on an invalid cell returns an empty
mask. Equality is exact, so continuous-valued rasters should be quantized or
processed with a separate tolerance rule before using this operation.

The package also includes a simple lossless **run-length encoding (RLE)**
representation. It scans a finite numeric 2-D array in row-major order and
stores consecutive equal values as (value, count) pairs alongside shape and
dtype metadata. Decoding validates the run total and restores the original
shape and dtype. RLE is effective for long homogeneous runs, but can expand
high-entropy imagery and is not a standardized file format.

## Interpretation and limitations

- Component IDs are arbitrary identifiers assigned by scan order, not class values or importance rankings.
- 4- and 8-connectivity can produce different component counts and sizes.
- This baseline does not polygonize components, compute shape descriptors or reconcile labels across distributed tiles. The RLE format is not bit-packed, entropy-coded, tiled or interoperable with external raster formats.
- Production implementations may use run-length encoding, union-find or tiled algorithms to improve memory use and throughput.

## Exercises

1. Label the same mask under 4- and 8-connectivity. Which regions merge?
2. Insert a NoData barrier. Does it split a component?
3. Compare breadth-first labeling with a two-pass union-find method.
4. Why is a component label not a stable feature ID across changed inputs?
5. Describe how tiled processing must reconcile components that cross tile boundaries.

## References

- Rosenfeld, A. and Pfaltz, J. L. (1966), *Sequential operations in digital picture processing*, Journal of the ACM, 13(4), 471–494.
- Haralick, R. M. and Shapiro, L. G. (1992), *Computer and Robot Vision, Volume I*, Addison-Wesley.

**Scope:** 2D boolean masks with 4/8 connectivity and optional validity barriers; no vectorization or distributed component reconciliation.

# Binary mathematical morphology

Mathematical morphology studies image sets through interactions with a structuring element. For binary set \(A\) and structuring element \(B\), dilation expands foreground support and erosion retains positions where the translated structuring element fits entirely within the foreground.

For a finite raster, the boundary convention is part of the algorithm. This package treats every sample outside the raster as background (false), so erosion can remove border pixels while dilation can extend foreground only where an in-bounds translated element overlaps the image.

## Operators

- **Erosion** removes foreground locations where any active structuring-element sample misses foreground.
- **Dilation** adds locations reached by translating any active element sample over foreground.
- **Opening** is erosion followed by dilation; it removes small foreground components and is idempotent.
- **Closing** is dilation followed by erosion; it fills small gaps and is idempotent.
- **Hit-or-miss** simultaneously matches a foreground template and a background template.
- **Geodesic reconstruction** repeatedly dilates a marker, intersects with a mask, and stops at a fixed point. It extracts mask components connected to the marker under the selected neighbourhood.
- **Connected-component labelling** identifies foreground components under 4- or 8-neighbour connectivity.

## Implementation scope

The NumPy package uses explicit shifts and logical operations for clarity. It is a 2-D binary reference implementation, not a high-performance image library. Grayscale morphology, component trees, thinning, contour tracing, granulometry and interactive segmentation are separate algorithms.

## Reproducibility

Run `python -m pytest -q` in `implementations/python/binary-morphology`. Tests cover boundary handling, idempotence, monotonicity/duality, template detection, reconstruction convergence and connectivity.

## References

- Serra, J. (1982). *Image Analysis and Mathematical Morphology*. Academic Press.
- Soille, P. (2003). *Morphological Image Analysis: Principles and Applications*, 2nd ed. Springer.
- Vincent, L. (1993). Morphological grayscale reconstruction in image analysis: applications and efficient algorithms. *IEEE Transactions on Image Processing*, 2(2), 176–201. https://doi.org/10.1109/83.217222.

## Zhang-Suen thinning

The package also includes the two-subiteration Zhang-Suen parallel thinning rule. For each foreground pixel, it counts its eight neighbours and the 0-to-1 transitions around the ring. A pixel is a deletion candidate when it has two to six foreground neighbours and exactly one circular transition. Two different triplet constraints are applied in alternating subiterations to avoid deleting pixels that would break the local skeleton structure. Iteration stops when a full pair of subiterations removes no pixels.

This is a binary topology-preserving thinning baseline for suitable raster masks, not a medial-axis transform: it does not compute maximal inscribed discs or metric distance-to-boundary information. Pixel connectivity and raster boundary conventions matter. The implementation zero-pads outside the raster and uses 8-neighbour foreground connectivity.


## Grayscale max-trees and min-trees

The package now includes an explicit connected-component hierarchy for grayscale rasters. A max-tree links connected components of upper-level sets as the threshold descends; a min-tree links connected components of lower-level sets as the threshold rises. Nodes store their birth level, pixel membership, area and parent. The implementation supports 4- and 8-connectivity and preserves deterministic row-major component ordering.

This is a transparent threshold-relabeling reference, not the quasi-linear union-find algorithms used by production morphology libraries. It recomputes components at every distinct gray level and stores pixel membership for each node, so its time and memory costs can be high. It does not implement alpha trees or attribute-filter pruning. Tests cover nested components, parent containment, level ordering, plateaus, connectivity, constant rasters and invalid inputs.

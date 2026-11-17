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

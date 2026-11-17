# Binary mathematical morphology

A dependency-light NumPy reference package for finite 2-D binary rasters.

## Included algorithms

- Binary erosion and dilation with explicit structuring elements.
- Opening and closing.
- Binary granulometry using a homothetic family of centred square structuring elements, returning scale-wise foreground areas and pattern spectrum.
- Grayscale area opening and area closing through explicit max-tree/min-tree component hierarchies.
- Hit-or-miss pattern detection.
- Geodesic reconstruction by dilation under a mask.
- 4- and 8-connected component labelling with flood-fill and two-pass union-find implementations.\n- Zhang-Suen iterative binary thinning/skeletonisation.

All operators use a false/background value outside the raster. Structuring elements are centred at floor(shape/2), including even-sized elements. The implementation favours inspectability over speed and is not a production replacement for SciPy ndimage, OpenCV or specialised connected-component libraries.

## Contracts and limitations

Inputs must be non-empty finite 2-D arrays and are interpreted as boolean masks. A structure must be a non-empty 2-D array with at least one active cell. Reconstruction requires marker subset mask and terminates at a fixed point; an optional iteration cap raises rather than returning an incomplete result. Component labels are deterministic in row-major seed order.

Granulometry accepts strictly increasing non-negative integer radii and constructs full centred square structuring elements of side 2r+1; its pattern spectrum is the area removed between successive openings. The grayscale area filter removes upper-level bright or lower-level dark connected components smaller than a pixel-count threshold, using the max-tree for area opening and min-tree for area closing. It is checked against an independent threshold-set oracle for both 4- and 8-connectivity. The max/min component-tree reference recomputes connected components at every distinct gray level; the alpha-tree reference thresholds absolute adjacent-pixel differences to form quasi-flat zones. The alpha-tree is checked against an independent threshold-component flood-fill oracle for 4- and 8-connectivity. These references store pixel membership per node. It is intended for small teaching rasters; memory use can grow substantially with raster size and number of gray levels. Contour tracing, random-walker or GrabCut segmentation, and MSPA remain separate work.

## Reproduce

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~


## References

- Vincent, L. (1993). Grayscale area openings and closings, their efficient implementation and applications. *Proceedings of the EURASIP Workshop on Mathematical Morphology and Its Applications to Signal Processing*, Barcelona, 22–27. This package uses an inspectable threshold-set/component-tree reference, not Vincent's efficient implementation.
- Breen, E. J., & Jones, R. (1996). Attribute openings, thinnings, and granulometries. *Computer Vision and Image Understanding*, 64(3), 377–389. https://doi.org/10.1006/cviu.1996.0066

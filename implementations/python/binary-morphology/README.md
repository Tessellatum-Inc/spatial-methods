# Binary mathematical morphology

A dependency-light NumPy reference package for finite 2-D binary rasters.

## Included algorithms

- Binary erosion and dilation with explicit structuring elements.
- Opening and closing.
- Binary granulometry using a homothetic family of centred square structuring elements, returning scale-wise foreground areas and pattern spectrum.
- Hit-or-miss pattern detection.
- Geodesic reconstruction by dilation under a mask.
- 4- and 8-connected component labelling with flood-fill and two-pass union-find implementations.\n- Zhang-Suen iterative binary thinning/skeletonisation.

All operators use a false/background value outside the raster. Structuring elements are centred at floor(shape/2), including even-sized elements. The implementation favours inspectability over speed and is not a production replacement for SciPy ndimage, OpenCV or specialised connected-component libraries.

## Contracts and limitations

Inputs must be non-empty finite 2-D arrays and are interpreted as boolean masks. A structure must be a non-empty 2-D array with at least one active cell. Reconstruction requires marker subset mask and terminates at a fixed point; an optional iteration cap raises rather than returning an incomplete result. Component labels are deterministic in row-major seed order.

Granulometry accepts strictly increasing non-negative integer radii and constructs full centred square structuring elements of side 2r+1; its pattern spectrum is the area removed between successive openings. The implementation does not include grayscale morphology, distance transforms, max/min component trees, alpha trees, contour tracing, random-walker or GrabCut segmentation, or MSPA. These are distinct methods and remain separate work.

## Reproduce

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

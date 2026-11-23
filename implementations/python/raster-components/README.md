# Raster connected-component labeling

This package labels connected foreground regions in a 2D boolean raster mask using breadth-first search.

## Run

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Contract

- Foreground is a 2D boolean-like mask.
- Connectivity is either 4-neighbour or 8-neighbour.
- An optional valid mask marks cells included in the analysis; invalid cells are barriers.
- Label zero means background or invalid. Positive labels are assigned in deterministic row-major discovery order.
- The function returns the label raster and a mapping from label to cell count.
- This is a simple BFS baseline; it does not implement run-length/union-find optimizations, distributed labeling or vector polygonization.

Read the [canonical lesson](../../../algorithms/raster/connected-components.md) and [intern walkthrough](implementation-walkthrough.md).


## Three-dimensional voxel connected components

The module also provides `connected_components_3d` for binary volumes. Choose 6-connectivity (face neighbours), 18-connectivity (faces and edges) or 26-connectivity (faces, edges and corners). An optional valid-voxel mask makes invalid cells barriers. Labels are deterministic in z/y/x scan order and component sizes are returned.

This is a basic spatial-volume primitive that can support event-object extraction from time stacks or 3-D model outputs. It does not perform temporal object linking, split/merge tracking, periodic-boundary handling or tiled/parallel reconciliation. Tests cover connectivity distinctions, barriers and invalid inputs.


## Flood fill and run-length encoding

The package also provides seed-based exact-value flood fill with 4/8
connectivity and optional validity barriers. `run_length_encode` and
`run_length_decode` provide a lossless row-major value/count representation
for finite numeric 2-D arrays, preserving shape and NumPy dtype. This simple
RLE format is a teaching representation, not a standardized interchange
format or a substitute for compression tuned to arbitrary imagery.


## Multiresolution box pyramid

`build_box_pyramid` constructs a spatial pyramid for 2-D rasters or
(row, column, band) arrays. Each level averages non-NoData values in each
2x2 spatial block, including partial blocks at odd edges. NaNs are ignored;
an all-NoData output block remains NaN. Levels include the original array and
stop early at 1x1. This is a transparent box-reduction baseline, not a
Gaussian/Laplacian pyramid or a scale-space implementation.

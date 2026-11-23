# Three-dimensional connected-component labeling

## Problem

Given a binary voxel volume, identify maximal sets of foreground voxels connected under a chosen neighbourhood. This is useful for volumetric segmentation, space-time event masks, storm-object extraction and 3-D raster analysis.

## Neighbourhood definitions

For a voxel at (z,y,x), inspect offsets in {-1,0,1}^3 excluding (0,0,0):

- **6-connectivity:** face neighbours only; exactly one coordinate changes.
- **18-connectivity:** face and edge neighbours; at most two coordinates change.
- **26-connectivity:** face, edge and corner neighbours; any of the 26 surrounding voxels.

Connectivity changes the object definition. Two voxels touching only at a corner are separate under 6- and 18-connectivity but connected under 26-connectivity.

## Breadth-first labeling

Scan voxels in deterministic z/y/x order. When an unlabeled valid foreground voxel is found, assign a new label and perform breadth-first search over the selected neighbour offsets. Each reached voxel is labeled once. The output contains zero for background or invalid cells, positive integer component labels, and a label-to-voxel-count mapping.

An optional validity mask makes invalid voxels barriers. This is important for NoData gaps, but it is not equivalent to filling missing voxels.

## Implementation

The [raster-components package](../../implementations/python/raster-components/README.md) provides both 2-D connected components (4/8) and 3-D voxel connected components (6/18/26). The 3-D implementation is a transparent O(N) breadth-first reference method for N voxels, with memory proportional to the volume and queue frontier.

## Space-time interpretation

A 3-D array may represent x/y/time or x/y/z. The connectivity choice therefore encodes a substantive rule about which events are considered continuously connected. For time stacks, a voxel may be adjacent across time and space; this does not itself identify object motion or resolve split/merge events. Object tracking requires a separate association step between labeled time slices or volumes.

## Limitations

- Input is a finite binary volume; continuous-valued thresholding is a separate operation.
- No periodic boundaries, chunked/tiled seam reconciliation, distributed labeling or GPU implementation.
- No component-shape, intensity, persistence or motion descriptors.
- No temporal identity linking or split/merge tracking.

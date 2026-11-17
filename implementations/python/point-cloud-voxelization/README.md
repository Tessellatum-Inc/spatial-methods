# Point-cloud voxelization

A NumPy reference for assigning XYZ points to a regular axis-aligned voxel
grid and aggregating point counts, centroids, minima and maxima.

## Coordinate contract

Voxel coordinates are integer indices computed with floor((point-origin)/size).
Cells are half-open along each axis. Voxel size may be scalar or a three-axis
vector. If origin is omitted, the minimum input coordinate is used.

The returned point_to_voxel vector maps every input point to a row of the
sorted voxel summary arrays.

## Run

Install with python -m pip install -r requirements.txt, then run
python -m pytest -q.

## Limits

This is grid indexing and aggregation, not semantic point classification,
adaptive octree construction, point-cloud compression, normal estimation or
sensor-specific LiDAR waveform processing. The dense voxel grid is not
materialised, so memory scales with occupied cells and points rather than
the full coordinate extent.

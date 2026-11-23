# Point-cloud voxelization

Voxelization partitions three-dimensional space into axis-aligned cells and
assigns each point to an integer cell index. For origin o and per-axis voxel
size s, the index is

    v = floor((p - o) / s).

The half-open cell convention gives a deterministic assignment at boundaries.
Per-voxel summaries such as counts, centroids, minima and maxima support
downstream filtering, visualization and coarse spatial indexing.

See [the Python implementation](../../implementations/python/point-cloud-voxelization/README.md).
It stores only occupied voxel keys and a point-to-voxel mapping; it does not
materialise a potentially huge dense grid. Voxelization is not semantic
classification and does not replace adaptive octrees or sensor-specific
processing.

# Raster object tracking by overlap association

This baseline links already-segmented objects between consecutive raster frames. For labels A and B in adjacent frames, it computes intersection size and intersection-over-union (IoU), then records every pair meeting the minimum overlap and IoU thresholds.

All qualifying edges are retained so that split and merge topology is visible. Persistent IDs are propagated through a deterministic greedy one-to-one matching ordered by descending IoU, then overlap size, then label IDs. Unmatched objects receive new IDs. This separates the association graph from the single primary identity path.

The method supports 2-D rasters and 3-D labeled volumes, but it is not a full storm/cyclone tracker. It requires spatial overlap between consecutive frames; it does not model advection, intensity evolution, temporal gaps, occlusion, object birth/death physics, or uncertainty. The greedy assignment is not a globally optimal multi-object tracking solution. For atmospheric systems, segmentation thresholds, grid geometry, time cadence and domain-boundary rules must be specified by the scientific workflow.

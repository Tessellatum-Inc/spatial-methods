# OBIA object-feature verification

- Scope: geometry, per-band summaries and 4-neighbour adjacency from supplied integer labels.
- Implementation: implementations/python/obia-object-features/object_features.py.
- Tests: implementations/python/obia-object-features/test_object_features.py.
- Checks: area, centroid, bounding box, 4-edge perimeter, multiband statistics, shared-edge adjacency, negative background labels and NaN handling.
- Limits: pixel-space geometry; labels supplied externally; compactness is the 4-edge pixel-grid measure.
- Not covered: segmentation, texture, multiscale objects, classification, topology repair or geospatial area calculations.
- Status: scoped implementation and authored tests; CI execution pending.

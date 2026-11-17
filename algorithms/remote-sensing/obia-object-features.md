# Object-based image-analysis features

Object-based image analysis (OBIA) works with segmented image regions rather
than treating every pixel independently. This reference component accepts a
segmentation label raster and computes object pixel area, row/column centroid,
half-open bounding box, 4-neighbour perimeter, compactness, per-band finite
mean and standard deviation, and a region adjacency graph weighted by the
number of shared pixel edges.

See the [implementation](../../implementations/python/obia-object-features/README.md)
and [tests](../../implementations/python/obia-object-features/test_object_features.py).

This component does not perform segmentation or classification. It does not
provide multiscale hierarchies, texture descriptors, rule-based classification,
topology repair or geospatial area calculations. Pixel counts and centroids
must be interpreted with the raster's coordinate transform and pixel geometry.

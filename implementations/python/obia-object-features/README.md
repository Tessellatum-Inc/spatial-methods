# Object-based image-analysis features

Extracts geometry, per-band summary statistics and a 4-neighbour region
adjacency graph from a raster and an integer segmentation-label raster.
Negative label IDs are ignored as background; NaN image values are omitted
from spectral summaries.

Run:
    python -m pip install -r requirements.txt
    pytest -q

The package does not create segments. Supply labels from a segmentation
method such as SLIC, watershed or a domain-specific classifier. The output
contains pixel area, row/column centroid, half-open bounding box, 4-edge
perimeter, compactness and per-band mean/standard deviation.

This is a feature-extraction component, not a complete OBIA workflow. It does
not implement segmentation, multiscale object hierarchies, shape descriptors
beyond compactness, texture features, object classification, rule sets,
training, topology repair or geospatial area calculations. Pixel geometry is
not ground-area geometry unless the raster grid is appropriate and corrected.

# Rasterization algorithms

Dependency-free implementations with explicit pixel/cell contracts:

- **DDA:** floating incremental sampling with nearest-pixel rounding (half ties upward).
- **Bresenham:** integer thin-line rasterization for all octants.
- **Wu:** antialiased line intensities returned as coverage-like display weights; not exact geometric area coverage.
- **Supercover:** conservative closed-cell segment intersection; edge- and corner-only touches are included.
- **Scanline polygon fill:** even–odd fill sampled at cell centres with a half-open crossing convention.

Run with `python -m pytest -q` from this directory.

These functions operate in grid coordinates only. They do not apply CRS transformations, affine georeferencing, clipping to an arbitrary raster mask, polygon holes/ring hierarchy, nonzero winding fill, fractional polygon coverage, or NoData handling. The supercover routine is a transparent small-grid reference implementation with work proportional to the segment's bounding-box area, not an optimized Amanatides–Woo traversal.

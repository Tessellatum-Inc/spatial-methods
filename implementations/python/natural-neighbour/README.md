# Sibson natural-neighbour interpolation

A dependency-free planar reference implementation of Sibson natural-neighbour interpolation. It inserts each query into the Voronoi diagram conceptually, computes the area stolen from each original site's Voronoi cell by half-plane clipping, and normalises those areas into interpolation weights.

## Contract

- Distinct, finite Cartesian 2D sample coordinates in a consistent projected CRS.
- Queries strictly inside the sample convex hull. Extrapolation and hull-boundary limits are rejected.
- Scalar or multi-output values; exact sample-coordinate queries return the stored value.
- O(m n²) work for m queries and n sites. This is a transparent reference implementation, not a large-data index.

## Run

Install NumPy and pytest, then run pytest -q in this directory.

See the [algorithm note](../../../algorithms/interpolation/natural-neighbour.md) for the construction and limitations.

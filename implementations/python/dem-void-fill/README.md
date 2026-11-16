# DEM inverse-distance void filling

Dependency-free local inverse-distance weighting (IDW) for raster elevation
grids with missing cells. Missing values may be None, NaN, or an explicit
NoData sentinel. Existing valid elevations are preserved.

## Method

For valid neighbours i at map distances d_i, the algorithm computes

    z_hat = sum(z_i / d_i^p) / sum(1 / d_i^p)

The caller controls neighbourhood radius, minimum neighbour count, distance
power, pixel dimensions and number of synchronous passes. Synchronous updates
avoid dependence on raster scan order. Multiple iterations allow newly filled
cells to support later passes. Cells without enough neighbours remain None.

## Limits

This is a generic local interpolation baseline, not a hydrologically
conditioned DEM reconstruction. It does not infer valley/ridge structure,
enforce drainage, use breaklines, model uncertainty, fuse sensors, classify
bare earth or distinguish true depressions from data voids. Large voids can
be smoothed or biased; inspect the filled mask and validate against terrain
context before using the result for derivatives or hydrological modelling.

## Tests

    python -m pytest -q

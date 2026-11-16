# Local raster map algebra and categorical lookup

Stable ID: SA-RASTER-LOCAL-MAP-ALGEBRA · Draft 0.1 · Source compendium section 4, page 6

## Local operations

Local map algebra evaluates an operation independently at each aligned cell location. Inputs must share shape, grid alignment, CRS, resolution and NoData semantics; matching array dimensions alone do not establish geospatial alignment.

The reference implementation provides cellwise arithmetic, comparisons and reducers (sum, mean, minimum, maximum and product). It requires identical array shapes and treats non-finite values as NoData. Reducers can propagate missingness or ignore missing inputs; binary operations always require both operands. Division by zero is NoData.

## Categorical lookup

A lookup table maps each input class code to an output value. The implementation makes unknown categories explicit: convert them to NoData, retain the original numeric code, or raise an error. This is safer than silently mapping unknown classes to zero.

## Important limits

The package does not align grids, reproject, resample, parse arbitrary expressions, execute distributed operations or implement focal/zonal/global neighbourhood algorithms. Verify CRS, affine transform, resolution, units and temporal meaning before combining rasters.

## Exercises

1. Calculate a two-date difference raster and identify how NoData propagates.
2. Calculate a mean from three rasters with one missing observation per cell.
3. Recode land-cover classes with an explicit unknown-category policy.
4. Explain why equal array shape does not prove equal grid alignment.

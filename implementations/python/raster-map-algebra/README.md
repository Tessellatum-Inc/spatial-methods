# Local raster map algebra and categorical lookup

Provides cellwise arithmetic, reductions and explicit categorical recoding for already aligned rasters. It does not align or reproject inputs.

## Operations

Reducers: sum, mean, min, max and product. Binary operations: add, subtract, multiply, divide, greater, less and equal. Reducers accept two or more arrays; binary operations require exactly two.

All inputs must have identical two-dimensional shapes. Division by zero yields NoData. Non-finite inputs are treated as NoData.

## NoData

Reducers support propagate (default: every input must be valid) and ignore (use available cells). Binary operations always require both operands. Categorical lookup supports unknown="nodata" (default), "keep" or "error"; existing non-finite cells remain NoData.

## Scope

These are local, cell-aligned operations. They do not handle CRS transformations, grid alignment, resampling, lazy/distributed arrays, expression parsing or focal/zonal/global neighbourhood operations. Equal array dimensions do not prove spatial alignment.

Install and test with python -m pip install -r requirements.txt and python -m pytest -q.

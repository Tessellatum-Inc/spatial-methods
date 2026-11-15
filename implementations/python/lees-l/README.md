# Lee's L in Python

A dependency-free teaching implementation of the global bivariate spatial association statistic from Lee (2001), using the row-standardized weights form (equations 13–14).

## Run

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Example

~~~python
from lees_l import lees_l

weights = [
    [0, 1, 0, 1],
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [0, 0, 1, 0],
]
result = lees_l([1, 2, 4, 3], [1, 2, 4, 3], weights)
print(result["L"])
print(result["spatial_smoothing_scalar_x"])
print(result["spatial_smoothing_scalar_y"])
~~~

The result includes global L, the two spatial smoothing scalars and both spatial lag vectors.

## Contract

- Both variables must be finite, one-dimensional, equal-length numeric sequences with non-zero variance.
- W must be a finite, non-negative square matrix aligned to the observation order.
- Self-weights and islands are rejected.
- W is row-standardized internally.
- The formula centres spatial lags using the original-variable means, following Lee (2001), equations 13–14.
- The statistic is symmetric in x and y; exchanging the two variables does not change the global value.
- This package calculates the statistic only. It does not provide local L, permutation inference, confidence intervals, or multiple-testing correction.

## Important distinction

Lee's L is not bivariate Moran's I. Bivariate Moran's I combines a variable with the spatial lag of the other variable. Lee's L combines the spatial lags of both variables and scales by the original variables' sums of squares.

This implementation deliberately states one formula and its weights contract. Other software packages document related computational conventions and additional local/inferential outputs; do not assume byte-for-byte equivalence without matching definitions.

## Complexity and limitations

The dense implementation takes O(n²) time to form the two spatial lags and O(n²) memory for W. It is intended for small learning examples. It does not construct spatial neighbours, align feature IDs, handle missing values or validate whether a chosen weights matrix is substantively appropriate.

See the [canonical lesson](../../../algorithms/statistics/lees-l.md) and [implementation walkthrough](implementation-walkthrough.md).

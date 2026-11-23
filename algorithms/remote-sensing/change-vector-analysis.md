# Bitemporal change detection: CVA and post-classification comparison

## Question

How can two aligned multispectral dates be compared, and how can categorical
maps be summarized as transitions?

## Change Vector Analysis

For band vectors at dates 1 and 2, define

`d(x,y) = X_2(x,y) - X_1(x,y)`.

The Euclidean change magnitude is

`M_E(x,y) = sqrt(sum_b d_b(x,y)^2)`.

It measures the size of the spectral displacement but discards its direction.
The implementation also calculates a covariance-standardized magnitude:

`M_M(x,y) = sqrt(d(x,y)^T (Sigma + lambda I)^(-1) d(x,y))`.

The covariance is supplied by the analyst or estimated from valid bitemporal
difference vectors. The positive ridge `lambda` stabilizes inversion. This
is a descriptive distance, not a calibrated probability or a universal
change threshold.

## Post-classification comparison

Given class rasters `C_1` and `C_2`, count every valid pixel in a
from-class/to-class matrix:

`T_ij = count(C_1 = class_i and C_2 = class_j)`.

Rows are earlier classes and columns are later classes. The diagonal counts
persistence; off-diagonal cells count transitions. Non-finite cells in
either date are excluded. Class order should be supplied when matrices from
multiple areas or periods must be compared.

## Implementation and tests

The [NumPy reference package](../../implementations/python/remote-sensing-change/README.md)
contains CVA and post-classification comparison, including NoData masks,
explicit class ordering, covariance regularization and input validation.
Tests include a separate pixelwise transition-count oracle and direct
linear-algebra checks for Mahalanobis distance.

## Assumptions and limits

- Both dates must already share a grid, projection, pixel alignment and
  compatible radiometric scale.
- CVA is sensitive to residual registration, illumination, atmosphere,
  phenology and sensor differences.
- Estimated covariance reflects the observed change-vector population; it
  may be dominated by real changes or contaminated pixels.
- Post-classification transitions inherit errors and class-definition
  differences from both classification maps.
- This is not IR-MAD, a learned Siamese/ChangeFormer model, or a full
  accuracy-adjusted land-change accounting workflow.

## Further reading

- Singh (1989), “Digital change detection techniques using remotely-sensed
  data,” *International Journal of Remote Sensing*, 10(6), 989–1003,
  [https://doi.org/10.1080/01431168908903939](https://doi.org/10.1080/01431168908903939).
- Bruzzone and Prieto (2000), “Automatic analysis of the difference image
  for unsupervised change detection,” *IEEE Transactions on Geoscience and
  Remote Sensing*, 38(3), 1171–1182,
  [https://doi.org/10.1109/36.843009](https://doi.org/10.1109/36.843009).

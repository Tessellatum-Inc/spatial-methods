# Source verification — tensor-product B-spline P-surface

## Identity and bibliography
- Eilers & Marx (1996), “Flexible smoothing with B-splines and penalties,” *Statistical Science*, 11(2), 89–102, DOI 10.1214/ss/1038425655.
- Wood (2017), “P-splines with derivative based penalties and tensor product smoothing of unevenly distributed data,” *Statistics and Computing*, 27, 985–989, DOI 10.1007/s11222-016-9666-x.

## Technical claims
- P-splines combine B-spline bases with discrete quadratic difference penalties on coefficients.
- Tensor-product bases combine marginal spline bases; separate directional penalties control smoothness along each coordinate.
- The implementation uses a Greville-abscissa second divided-difference penalty and dense Gaussian-response least squares; it is not a generalized additive model or a large-data array algorithm.

## Implementation and tests
- Cox–de Boor basis evaluation, open-uniform knots, tensor-product design, x/y second divided-difference penalties, dense least-squares fit and in-domain prediction.
- Tests cover bilinear null-space preservation, finite interior prediction, unequal directional penalties, basis rank, invalid inputs and prediction-before-fit.

## Limits and rights
Dense matrices; no automatic smoothing selection, sparse/array algorithms, uncertainty, missing-data handling, boundary conditions or extrapolation. Original implementation and explanatory text; bibliographic metadata only. No source figures, code or datasets are reproduced.

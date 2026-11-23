# Source verification — spatial thin-plate smoothing spline

## Identity and bibliography
- Wood, S. N. (2003), “Thin plate regression splines,” *Journal of the Royal Statistical Society: Series B*, 65(1), 95–114, DOI 10.1111/1467-9868.00374.
- R mgcv documentation distinguishes thin-plate regression splines as low-rank isotropic smoothers and Duchon splines as a broader family. The constructor notes describe optimal truncation of the full thin-plate basis: https://stat.ethz.ch/R-manual/R-devel/library/mgcv/help/tprs.html.

## Technical claims
- The two-dimensional thin-plate radial kernel is proportional to r² log(r).
- The affine polynomial null space is unpenalized for the standard second-order two-dimensional thin-plate penalty.
- Thin-plate regression splines are constructed by transforming and optimally truncating the full thin-plate basis; the penalty retains its original interpretation. This was cross-checked against Wood (2003) and the mgcv constructor documentation.

## Implementation/reproduction
Implemented: (1) full-knot 2-D radial basis smoothing spline; (2) rank-truncated TPRS basis using QR projection of the affine null space, dense eigendecomposition of the projected kernel, largest-eigenvalue retention and penalty-normalising transform. Tests compare full-rank TPRS with the full-knot solver, check affine null-space recovery, interpolation, rank/dimension, predictions and invalid inputs.

Not implemented: mgcv-style Lanczos/subsampled basis construction, GAM/GAMM fitting, automatic smoothing selection, Duchon/soap-film/Bayesian P-splines, generalized likelihoods, boundary constraints or uncertainty estimates. Dense basis construction remains cubic in sample count. Test files are not evidence of a passing repository test run.

## Rights
Original explanatory text and bibliographic metadata only; no source figures, code or datasets reproduced.

# Source verification — spatial thin-plate smoothing spline

## Identity and bibliography
- Wood, S. N. (2003), “Thin plate regression splines,” *Journal of the Royal Statistical Society: Series B*, 65(1), 95–114, DOI 10.1111/1467-9868.00374.
- R mgcv documentation distinguishes thin-plate regression splines as low-rank isotropic smoothers and Duchon splines as a broader family.

## Technical claims
- The two-dimensional thin-plate radial kernel is proportional to r² log(r).
- The affine polynomial null space is unpenalized for the standard second-order two-dimensional thin-plate penalty.
- Thin-plate regression splines are low-rank constructions derived from the full thin-plate smoothing-spline problem; this repository implementation is not that reduced-rank construction.

## Implementation/reproduction
Implemented: full-knot 2-D radial basis smoothing spline with affine null space and user-selected nonnegative penalty; fit/predict APIs. Tests are authored for interpolation, affine null-space recovery, new-point prediction and input validation.

Not implemented: low-rank TPRS, GAM/GAMM fitting, automatic smoothing selection, Duchon/soap-film/Bayesian P-splines, generalized likelihoods, boundary constraints or uncertainty estimates. Test files are not evidence of a passing repository test run.

## Rights
Original explanatory text and bibliographic metadata only; no source figures, code or datasets reproduced.

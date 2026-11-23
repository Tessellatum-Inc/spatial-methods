# Space-time K-function

The space-time K-function summarizes the expected number of further events within spatial radius r and absolute time lag τ of a typical event, divided by intensity. For a rectangular spatial window W and observation duration T, the translation-corrected estimator is

\[
\widehat K(r,\tau)=\frac{|W|T}{n(n-1)}
\sum_{i\ne j}
\frac{\mathbf 1(d_{ij}\le r, |t_i-t_j|\le\tau)}
{w_s(x_i-x_j)w_t(t_i-t_j)}.
\]

The spatial overlap fraction is the product of remaining x/y widths divided by area; temporal overlap is (T-|Δt|)/T. The implementation loops over unordered pairs and doubles their contribution.

## Scope and limits

The NumPy baseline accepts planar event coordinates, times, radii and symmetric absolute time lags. It assumes a homogeneous stationary process over a rectangular window and fixed observation interval. Pairs with zero translation overlap are omitted. It does not implement inhomogeneous K, anisotropic metrics, mark correlation, border/isotropic corrections or irregular polygons. It is a second-order descriptive statistic, not a cluster-significance test.

## Sources
- Diggle, P. J., Chetwynd, A. G., Haggkvist, R., & Morris, S. E. (1995). Second-order analysis of space-time clustering. *Statistical Methods in Medical Research*, 4(2), 124–136. https://doi.org/10.1177/096228029500400203.
- Ohser, J. (1983). On estimators for the reduced second moment measure of point processes. *Mathematical Operationsforschung und Statistik, Series Statistics*, 14, 63–71.

Implementation: [point-process package](../../implementations/python/point-process/README.md).

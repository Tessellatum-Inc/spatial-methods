# Point-pattern second-order summaries

For a stationary isotropic point process with intensity \(\lambda\), Ripley's K-function is defined so that \(\lambda K(r)\) is the expected number of additional events within distance \(r\) of a typical event. Under complete spatial randomness (a homogeneous Poisson process), \(K(r)=\pi r^2\). Values above this reference can indicate clustering at the corresponding scales; values below can indicate inhibition/regularity, subject to sampling uncertainty and model assumptions.

The pair-correlation function is related by
\[
g(r)=\frac{K'(r)}{2\pi r}.
\]
It is a local-scale summary, whereas K is cumulative.

## Rectangular translation correction

For a rectangular observation window, shifting the window by pair displacement \((\Delta x,\Delta y)\) gives overlap fraction
\[
w(\Delta x,\Delta y)=
\left(1-\frac{|\Delta x|}{W}\right)
\left(1-\frac{|\Delta y|}{H}\right).
\]
The implementation weights each ordered pair by \(1/w\), then applies the homogeneous K normalization. This corrects the first-order loss of observable neighbors at rectangular boundaries under the stated stationary model.

The [Python package](../implementations/python/point-process/README.md) also provides nearest-neighbor distances and their empirical CDF. It does not estimate intensity surfaces, implement inhomogeneous K, generate simulation envelopes or support irregular polygon windows.

## Interpretation cautions

Use projected coordinates with meaningful distance units. K and pair correlation are not self-interpreting significance tests: compare against a suitable null model and account for the observation window, intensity variation, covariates and parameter selection. Inhomogeneous patterns can appear clustered under a homogeneous analysis simply because intensity varies across the region.

## Sources

- Ripley, B. D. (1976). “The Second-Order Analysis of Stationary Point Processes.” *Journal of Applied Probability*, 13(2), 255–266. [DOI](https://doi.org/10.2307/3212829).
- Ripley, B. D. (1977). “Modelling Spatial Patterns.” *Journal of the Royal Statistical Society: Series B*, 39(2), 172–212. [DOI](https://doi.org/10.1111/j.2517-6161.1977.tb01615.x).
- Baddeley, A., Rubak, E., & Turner, R. (2015). *Spatial Point Patterns: Methodology and Applications with R*. CRC Press. Edge correction and practical inference.

No source text or figures are reproduced.

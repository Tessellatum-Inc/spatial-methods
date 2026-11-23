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

## Inhomogeneous K with supplied intensities

When first-order intensity varies across the window, the homogeneous K-function can confound trend with interaction. The inhomogeneous K-function reweights each point by its inverse intensity. For a rectangular window and supplied intensity estimates \(\hat\lambda_i=\hat\lambda(x_i)>0\), the translation-corrected estimator implemented here is

\[
\widehat K_{\mathrm{inhom}}(r)=
\sum_{i\ne j} \frac{\mathbf 1(d_{ij}\le r)}
{\hat\lambda_i\hat\lambda_j\,|W\cap(W+(x_j-x_i))|}.
\]

For \(W=[x_{min},x_{max}]\times[y_{min},y_{max}]\), the overlap area is
\[
|W\cap(W+\Delta)|=(W_x-|\Delta x|)(W_y-|\Delta y|)
\]
when the displacement is within both window dimensions; otherwise the pair contributes zero. The function accepts the intensity values at the observed points and deliberately does not estimate them. A parametric trend model or carefully tuned leave-one-out smoother should be selected separately; oversmoothing can leave residual trend and undersmoothing can absorb interaction.

The inhomogeneous target is \(K_{\mathrm{inhom}}(r)=\pi r^2\) for an inhomogeneous Poisson process when the intensity reweighting assumptions hold. This is not a guarantee that a finite-sample curve will follow that reference. The estimator assumes second-order intensity-reweighted stationarity and uses a rectangular translation correction only. It does not offer border/isotropic corrections, renormalisation options, intensity fitting, irregular windows or simulation envelopes. The existing finite-difference pair-correlation function can be applied to the resulting K curve, but numerical differentiation amplifies noise.

The [Python package](../implementations/python/point-process/README.md) provides homogeneous and inhomogeneous K estimators, nearest-neighbor distances, pair correlation and a circular Poisson scan baseline.

## Circular Poisson spatial scan statistic

For areal case counts, a circular scan searches for a region with a higher case rate than the remainder of the study area while adjusting for population at risk. Let C be the total cases, P the total population, and for a candidate zone Z let c_Z and P_Z be the observed cases and population inside. Under the constant-risk null, the expected cases inside are

\[
E_Z=C\frac{P_Z}{P}.
\]

The high-rate log-likelihood ratio is

\[
LLR(Z)=
\begin{cases}
c_Z\log(c_Z/E_Z)+(C-c_Z)\log((C-c_Z)/(C-E_Z)), & c_Z>E_Z,\
0, & c_Z\le E_Z.
\end{cases}
\]

The implementation centres circles on each supplied region centroid, expands each radius through the sorted centroid distances, and includes all equal-distance ties. Candidate zones are restricted by a maximum population fraction (0.5 by default). The reported zone maximises the LLR. A relative risk is also reported for the selected zone.

The Monte Carlo test conditions on the observed total case count and draws simulated areal counts from a multinomial distribution with probabilities proportional to population. It compares the observed maximum LLR with the simulated maxima and uses the plus-one p-value \((1+b)/(1+B)\), where b is the number of simulated maxima at least as large as observed and B is the number of simulations. Use enough simulations for the resolution required by the analysis; 99 simulations are only a notebook demonstration.

This is a bounded centroid-based circular Poisson scan, not a full SaTScan reproduction. It assumes planar projected coordinates, a population offset and a constant-risk null. It does not adjust for covariates, use Bernoulli case-control data, search elliptical or arbitrary zones, model time, extract secondary clusters or account for uncertain areal boundaries. The scan statistic's maximum already accounts for the candidate-window search in the Monte Carlo calibration, but it does not remove the need to justify the study design and candidate-zone family.

## Quadrat counts for complete spatial randomness

A quadrat test partitions the rectangular observation window into equal-area cells and compares the observed cell counts with the equal-count expectation under homogeneous complete spatial randomness (CSR). For m quadrats and n observed points,

\[
E_j=n/m,\qquad
X^2=\sum_{j=1}^{m}\frac{(N_j-E_j)^2}{E_j}.
\]

Conditioning on n under homogeneous CSR gives a multinomial distribution with equal cell probabilities. This implementation simulates that conditional null directly and reports the upper-tail Monte Carlo p-value with the plus-one correction. It does not use the asymptotic chi-square p-value, which requires adequate expected counts. The grid dimensions, alignment and scale affect the result. A significant result can reflect clustering, regularity or unmodelled first-order intensity variation; it does not identify the cause.

The quadrat test is a coarse, grid-dependent diagnostic. It discards within-cell positions and should be paired with visual inspection and distance-based summaries. It does not replace K, inhomogeneous K or a fitted point-process model.

## Interpretation cautions

Use projected coordinates with meaningful distance units. K and pair correlation are not self-interpreting significance tests: compare against a suitable null model and account for the observation window, intensity variation, covariates and parameter selection. Inhomogeneous patterns can appear clustered under a homogeneous analysis simply because intensity varies across the region.

## Sources

- Ripley, B. D. (1976). “The Second-Order Analysis of Stationary Point Processes.” *Journal of Applied Probability*, 13(2), 255–266. [DOI](https://doi.org/10.2307/3212829).
- Ripley, B. D. (1977). “Modelling Spatial Patterns.” *Journal of the Royal Statistical Society: Series B*, 39(2), 172–212. [DOI](https://doi.org/10.1111/j.2517-6161.1977.tb01615.x).
- Baddeley, A., Møller, J., & Waagepetersen, R. (2000). “Non- and semi-parametric estimation of interaction in inhomogeneous point patterns.” *Statistica Neerlandica*, 54, 329–350. [DOI](https://doi.org/10.1111/1467-9574.00144).
- Kulldorff, M. (1997). “A spatial scan statistic.” *Communications in Statistics—Theory and Methods*, 26(6), 1481–1496. [DOI](https://doi.org/10.1080/03610929708831995).
- [smerc scan.test documentation](https://cran.r-project.org/web/packages/smerc/refman/smerc.html) — circular centroid-based candidate zones and conditional multinomial Monte Carlo testing.
- Baddeley, A., Rubak, E., & Turner, R. (2015). *Spatial Point Patterns: Methodology and Applications with R*. CRC Press. Edge correction and practical inference.

No source text or figures are reproduced.

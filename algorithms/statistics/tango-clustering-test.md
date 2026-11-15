# Tango's general spatial clustering test

Stable ID: SA-TANGO-GLOBAL-CLUSTER · Draft 0.1 · Source compendium section 2

## Purpose

Tango's test asks whether regional case proportions depart from population-proportional expectations in a spatially coherent way. Unlike a local scan, it is a global quadratic-form statistic: it evaluates the pattern of all regional deviations together, weighted by a matrix describing how close each pair of regions is.

Inputs are projected planar centroids, nonnegative integer case counts, positive population values and a prespecified spatial scale \(\phi\).

## Statistic

Let \(O_i\) be observed cases and \(E_i\) the expected cases under a constant-risk null. Define the observed and expected proportions

\[
r_i=\frac{O_i}{O_+}, \qquad p_i=\frac{E_i}{E_+}.
\]

For a population-offset null, \(p_i=P_i/P_+\). Let \(D_{ij}\) be the Euclidean distance between region centroids. The exponential closeness matrix used here is

\[
A_{ij}=\exp(-D_{ij}/\phi).
\]

Tango's statistic is

\[
C_G=(\mathbf r-\mathbf p)^\mathsf{T}A(\mathbf r-\mathbf p).
\]

The diagonal is one, and off-diagonal influence decays with distance. A larger \(\phi\) gives more distant regions greater mutual influence. The statistic is a global measure; it does not identify one unique cluster boundary or a local p-value for each region.

## Conditional Monte Carlo inference

The implementation uses a conditional Monte Carlo null rather than relying on a chi-square/gamma approximation. It fixes the observed total number of cases and allocates each replicate among regions with multinomial probabilities \(P_i/P_+\). It recomputes the statistic for every replicate. The upper-tail p-value is

\[
p=\frac{1+\#\{C_G^{(b)}\ge C_G^{obs}\}}{B+1}.
\]

This simulation calibrates the statistic for the chosen centroids, population distribution, \(\phi\), and conditional constant-risk null. It does not correct for trying many \(\phi\) values and reporting the most significant one. Choose the scale before examining the result, or include scale selection in a properly designed global simulation.

## Implementation

The tested NumPy implementation is in [spatial_scan.py](../../implementations/python/point-process/spatial_scan.py):

- tango_statistic returns the quadratic-form statistic, proportions, residuals and closeness matrix.
- monte_carlo_tango_test returns a conditional Monte Carlo p-value and the simulated reference statistics.

The chosen exponential kernel is \(e^{-d/\phi}\), as documented by the DCluster implementation of Tango's 1995 statistic. Other spatial-closeness kernels exist; changing the kernel changes the test and should be reported as a different specification.

## Assumptions and limitations

- Coordinates must be projected planar values in a common linear unit.
- The null is constant individual risk, conditional on the observed total cases.
- Population is the exposure/at-risk denominator; raw case proportions alone are not the expected proportions.
- The scale \(\phi\) is substantive and must be selected in advance.
- This implementation uses Monte Carlo inference only; it does not implement Tango's analytic moment/chi-square or gamma approximation.
- It is global and does not return a most-likely zone, local significance map, temporal scan or covariate-adjusted result.
- Monte Carlo precision is limited by \(B\); the smallest attainable p-value is \(1/(B+1)\).

## References

- Tango, T. (1995). “A class of tests for detecting ‘general’ and ‘focused’ clustering of rare diseases.” *Statistics in Medicine*, 14, 2323–2334.
- [DCluster: Tango's statistic](https://rdrr.io/cran/DCluster/man/tango.html) documents \(C=(r-p)^\mathsf{T}A(r-p)\) and the exponential centroid-distance closeness matrix.
- [smerc: Tango statistic and test](https://search.r-project.org/CRAN/refmans/smerc/html/tango.stat.html) documents the statistic components and Monte Carlo test interface.

## Exercises

1. How does increasing \(\phi\) change the spatial scale represented by \(A\)?
2. Why must the expected proportions reflect population at risk?
3. Why does the Monte Carlo null preserve the total case count?
4. Why is choosing \(\phi\) after looking at the p-values a multiple-testing problem?

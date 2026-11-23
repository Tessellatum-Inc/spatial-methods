# Elliptical spatial scan statistic

Stable ID: SA-ELLIPTICAL-SPATIAL-SCAN · Draft 0.1 · Source compendium section 2

## Purpose

The elliptical spatial scan is a shape-generalisation of the circular spatial scan. It searches for elevated-risk zones whose geometry can be elongated and oriented, rather than restricting every candidate to a circle. This can improve sensitivity when a plausible cluster follows a corridor, river valley or other anisotropic spatial pattern.

The method retains the likelihood-ratio scan framework: define a finite collection of candidate zones, score each zone, retain the maximum, and calibrate that maximum under a null model. The candidate-zone construction is the defining difference from the circular scan.

## Poisson likelihood ratio

For a candidate zone Z, let c_Z be observed cases inside, C the total cases, and mu_Z = C(P_Z/P) the expected cases under the constant-risk null, where P_Z and P are population inside and overall. The one-sided elevated-risk log likelihood ratio is

\[
LLR(Z)=
\begin{cases}
c_Z\log(c_Z/\mu_Z)+(C-c_Z)\log((C-c_Z)/(C-\mu_Z)), & c_Z>\mu_Z,\\
0, & \text{otherwise.}
\end{cases}
\]

The scan statistic is the maximum over the candidate ellipse set. The candidate set and all its tuning choices must be held fixed in every null replicate.

## Finite-grid candidate construction in this repository

This teaching implementation uses centroid-centred ellipses on a finite grid:

1. Each area centroid is used in turn as a candidate ellipse centre.
2. The user supplies major-to-minor axis ratios s >= 1 and orientations theta in [0,180 degrees).
3. For each centre, ratio and orientation, coordinates are rotated into major/minor-axis coordinates.
4. Areas are ordered by the normalized elliptical radial coordinate

\[
q_i=\sqrt{(u_i/s)^2+v_i^2}.
\]

5. Nested prefixes of that order define candidate zones. All numerical ties at a boundary are retained.
6. Candidates are screened by minimum case count and maximum population fraction, then scored by the elevated one-sided Poisson LLR.

For a candidate threshold q, the semimajor and semiminor axes are sq and q. A ratio of one is the circular special case.

This is an explicit finite-grid approximation, not an exact reproduction of the candidate-generation algorithms, eccentricity penalty or secondary-cluster procedures in SaTScan or the original paper. Results depend on the supplied ratios, orientations, population cap and centroid representation.

## Global Monte Carlo inference

The null fixes the observed total case count and reallocates cases among areas with multinomial probabilities proportional to population. Each replicate repeats the entire ellipse search and records its maximum LLR. The plus-one p-value is

\[
p=\frac{1+\#\{LLR_{\max}^{(b)}\ge LLR_{\max}^{obs}\}}{B+1}.
\]

Re-running the complete search accounts for the multiplicity across the candidate ellipses in the specified grid. It does not account for trying several grids, population caps or minimum-case settings and reporting whichever result is most significant.

## Implementation and scope

The dependency-light NumPy implementation is in [spatial_scan.py](../../implementations/python/point-process/spatial_scan.py):

- elliptical_poisson_scan returns the most likely elevated ellipse, its member indices, LLR, relative risk, centre, axis ratio, orientation and semi-axes.
- monte_carlo_elliptical_poisson_scan returns the conditional Monte Carlo p-value and simulated maximum LLRs.

Coordinates must be projected planar centroids in a common linear unit. Population values must be positive, and cases must be nonnegative integers. This is an areal centroid approximation: it does not clip ellipses against administrative polygon boundaries or calculate exact polygon-ellipse intersections.

There is no eccentricity penalty, covariate adjustment, low-rate alternative, temporal dimension, secondary-cluster extraction, or automatic selection of shape/orientation grids. For applied surveillance, use a validated implementation such as SaTScan and report the candidate-window settings.

## Relationship to other scans

- The circular Poisson scan is the special case s = 1.
- The elliptical scan broadens the candidate geometry but still searches a restricted family of zones.
- Flexible/irregular scans search more general connected shapes and require different candidate-generation heuristics.
- Besag–Newell and Tango answer different questions: fixed-case nearest-neighbour neighbourhood size and global distance-weighted concentration, respectively.

## References

- Kulldorff, M., Huang, L., Pickle, L. and Duczmal, L. (2006). “An elliptic spatial scan statistic.” Statistics in Medicine, 25, 3929–3943. [doi:10.1002/sim.2490](https://doi.org/10.1002/sim.2490).
- Kulldorff, M. (1997). “A spatial scan statistic.” Communications in Statistics—Theory and Methods, 26(6), 1481–1496.
- [SaTScan paper: spatial scan statistic](https://www.satscan.org/papers/k-jrssa2001.pdf) explains the maximum likelihood ratio and Monte Carlo calibration.
- [smerc elliptic.test documentation](https://search.r-project.org/CRAN/refmans/smerc/help/elliptic.test.html) describes finite shape/orientation settings and the Poisson scan interface.

## Exercises

1. Why does a ratio of one recover the circular candidate family?
2. How does the chosen orientation grid affect which elongated clusters can be found?
3. Why must every Monte Carlo replicate repeat the full ellipse search?
4. What changes when polygon intersections replace centroid membership?
5. How could an eccentricity penalty change the trade-off between elongated zones and compact zones?

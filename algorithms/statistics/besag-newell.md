# Besag–Newell cluster detection

Stable ID: SA-BESAG-NEWELL · Draft 0.1 · Source compendium section 2

## Question and data

Besag–Newell is a local cluster-detection procedure for areal case counts. It asks: starting from a region, how many nearby regions must be combined before a prespecified number of cases is reached? A small neighbourhood containing the target number of cases is evidence of spatial concentration relative to the population at risk.

Inputs are one projected planar centroid, integer case count and integer population at risk for each area. A cluster-size threshold \(k\) is selected before scanning. Centroid distances define the neighbourhood ordering; they do not imply that administrative polygons are circular.

## Local statistic

For each centre \(i\), order areas by increasing centroid distance, including the centre itself first. Let \(M_i\) be the smallest prefix of this ordering whose cumulative cases reach at least \(k\). The observed local statistic is the number of areas in that prefix (equivalently, the distance to the final included tie group). Smaller neighbourhoods indicate more concentrated cases.

This implementation includes all areas tied at the boundary distance. That policy prevents arbitrary ordering of equidistant regions from changing the selected cluster. Its public API is an explicitly area-centred formulation; historical implementations differ in whether they centre on each case or each area and in how they handle selection bias. Do not treat the variants as interchangeable.

## Exact conditional local probability

Let \(N\) be total population, \(C\) total cases, \(P_i\) the population in the selected neighbourhood, and \(c_i\) its observed cases. Under the null that each individual is equally likely to be a case, conditional on the fixed total \(C\), the neighbourhood case count follows

\[
X_i\sim\operatorname{Hypergeometric}(N,P_i,C).
\]

The one-sided local probability is

\[
p_i=\Pr(X_i\ge c_i).
\]

The implementation evaluates this upper tail using log-combinations to avoid direct factorial overflow. It reports the selected areas, observed and expected cases, neighbourhood population and local p-value. Local significance is assessed against the supplied \(\alpha\); users should not mistake the resulting collection of local p-values for family-wise error control.

## Global Monte Carlo assessment

Besag and Newell also describe a global assessment based on the number \(R_\alpha\) of significant centres. Each null replicate reallocates the observed total number of cases among areas with probabilities proportional to population, reruns the entire local scan and records the number of significant centres. The global p-value is

\[
p_{\mathrm{global}}=\frac{1+\#\{R_\alpha^{(b)}\ge R_\alpha^{\mathrm{obs}}\}}{B+1}.
\]

The implementation uses the plus-one correction. This global statistic addresses the multiplicity induced by scanning all centres under the specified null and scan settings; it does not correct for analyst choices made after inspecting results (such as trying many values of \(k\)).

## Implementation scope and cautions

The dependency-light implementation is in [spatial_scan.py](../../implementations/python/point-process/spatial_scan.py), with tests in [test_spatial_scan.py](../../implementations/python/point-process/test_spatial_scan.py).

- Population values must be integer counts, and total population must be at least total cases.
- Coordinates must be projected planar centroids in a common linear unit.
- The neighbourhood is defined by centroid distance, not polygon adjacency or network distance.
- All ties at the last included distance are retained.
- The local exact hypergeometric tail conditions on the total case count and treats individuals as exchangeable under a constant-risk null.
- The global Monte Carlo test conditions on the total cases and reallocates them according to population shares.
- The current interface uses one common \(k\) and one common \(\alpha\); it does not implement stratified risk, covariates, event counts with repeated events per person, or a full range of historical case-centred conventions.
- Local p-values alone do not establish a globally significant cluster. Use the global simulation when making a scan-wide claim.

The method is not the Kulldorff likelihood-ratio scan: it fixes the target number of cases and measures how many nearest areas are needed to reach it, rather than maximising a zone likelihood ratio.

## References

- Besag, J. and Newell, J. (1991). “The detection of clusters in rare diseases.” *Journal of the Royal Statistical Society: Series A*, 154, 143–155.
- Rosychuk, R. J. and Stuber, J. L. (2010). “An exact test to detect geographic aggregations of events.” *International Journal of Health Geographics*, 9, 28. [doi:10.1186/1476-072X-9-28](https://doi.org/10.1186/1476-072X-9-28). Its methods section states the hypergeometric formulation for cases and the global Monte Carlo assessment; it also explains why repeated events require a different model.
- [DCluster Besag–Newell documentation](https://search.r-project.org/CRAN/refmans/DCluster/html/besagnewell.html) documents the nearest-area accumulation idea and original reference.

## Exercises

1. Why does the null use the population inside the selected neighbourhood rather than its area count alone?
2. How does including all equidistant regions affect reproducibility?
3. Why is the global simulation required to repeat the entire scan rather than test only the observed selected neighbourhood?
4. Compare the method's fixed-\(k\) neighbourhood statistic with a circular Poisson likelihood-ratio scan.

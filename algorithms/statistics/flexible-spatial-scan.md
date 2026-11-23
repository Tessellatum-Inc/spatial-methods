# Flexibly shaped spatial scan statistic

Stable ID: SA-FLEXIBLE-SPATIAL-SCAN · Draft 0.1 · Source compendium section 2

## Purpose

The flexibly shaped spatial scan statistic (FleXScan) detects elevated-risk clusters whose administrative areas form an irregular but connected shape. Tango and Takahashi's method retains a likelihood-ratio scan but replaces the circular candidate windows with connected subsets of a bounded local neighbourhood.

This matters when the plausible cluster follows a river, transport corridor or other non-circular structure. It also increases the number of candidate zones dramatically, so maximum cluster size is a major computational control.

## Candidate windows

For each root area i:

1. Order all other areas by centroid distance from i.
2. Form a local candidate universe consisting of i and its K-1 nearest neighbours.
3. Use the supplied areal adjacency graph to define connectedness.
4. Enumerate every connected subset of that universe that contains i and has at most K areas.
5. Score each candidate zone and retain the global maximum over all roots and all candidate subsets.

The root condition prevents the same arbitrary connected subset from being enumerated from every possible starting point, although overlapping candidate zones from different roots remain possible. The exhaustive enumeration is combinatorial; the original paper reports that the approach is useful for small-to-moderate clusters and becomes impractical as K grows.

## Poisson likelihood ratio

Let c_Z be the observed cases in candidate zone Z, C the total cases, and mu_Z the null expected cases in Z. Under a constant-risk population-offset null,

\[
\mu_Z=C\frac{P_Z}{P},
\]

where P_Z is population in the zone and P is total population. The one-sided elevated-risk log likelihood ratio is

\[
LLR(Z)=
\begin{cases}
c_Z\log(c_Z/\mu_Z)+(C-c_Z)\log((C-c_Z)/(C-\mu_Z)), & c_Z>\mu_Z,\\
0, & \text{otherwise.}
\end{cases}
\]

The most likely cluster is the candidate connected zone with the largest LLR. As with circular and elliptical scans, statistical significance is calibrated by Monte Carlo simulation of the maximum statistic, not by treating the selected zone as if it had been specified in advance.

## Bounded exhaustive implementation in this repository

The NumPy implementation is in [spatial_scan.py](../../implementations/python/point-process/spatial_scan.py):

- flexible_poisson_scan accepts a symmetric undirected adjacency matrix and a maximum cluster size K.
- For each root, the candidate universe is the root plus its K-1 nearest centroid neighbours.
- It enumerates every connected subset containing the root, up to K members, exactly once per root.
- monte_carlo_flexible_poisson_scan reallocates the fixed total cases according to population shares and repeats the complete exhaustive scan in every replicate.

The implementation caps K at 15 to prevent accidental exponential workloads. This is a deliberate safety boundary for a teaching implementation, not a statistical property of the original method. The neighbour budget is also deterministic: equal-distance neighbours are ordered by their input index when the K-1 budget is filled.

The adjacency matrix must be symmetric, finite and have a zero diagonal. Any nonzero off-diagonal entry denotes an edge. Supply a graph appropriate to the study geography (for example, shared-boundary contiguity); Euclidean proximity is used only to restrict the local candidate universe, not to define connectivity.

## Important limitations

- This is a bounded exact enumeration of the specified candidate family, not an optimized production implementation of FleXScan.
- Runtime grows combinatorially with K and the number of connected subsets; do not increase the cap casually.
- The local candidate universe uses centroid-nearest areas. It does not guarantee that every geographically plausible irregular zone is considered.
- The graph is supplied by the caller; incorrect or asymmetric topology changes the candidate family and is rejected.
- The implementation returns one most-likely cluster only. It does not implement secondary-cluster extraction or the restricted likelihood ratio variant.
- The population-offset Poisson model is one-sided for elevated risk; low-rate scans, covariates, temporal scans and polygon-boundary geometry are not included.
- Monte Carlo inference must repeat the full candidate enumeration for each simulated dataset.

## Comparison

| Method | Candidate geometry | Main control |
|---|---|---|
| Circular scan | Nested centroid-centred circles | Maximum population fraction |
| Elliptical scan | Finite grid of centroid-centred ellipses | Axis ratios and orientations |
| Flexible scan | Connected subsets of a local nearest-neighbour universe | Maximum cluster size K and adjacency |

The methods share the likelihood-ratio and Monte Carlo framework but test different candidate families. Their maximum LLRs and detected zones should not be compared without aligning their candidate-size restrictions and null simulation settings.

## References

- Tango, T. and Takahashi, K. (2005). “A flexibly shaped spatial scan statistic for detecting clusters.” *International Journal of Health Geographics*, 4, 11. [doi:10.1186/1476-072X-4-11](https://doi.org/10.1186/1476-072X-4-11).
- [Full text of Tango and Takahashi (2005)](https://pmc.ncbi.nlm.nih.gov/articles/PMC1173134/) describes the local K-nearest-neighbour universe, connected-subset enumeration, Poisson likelihood ratio and Monte Carlo calibration.
- [rflexscan package paper](https://www.jstatsoft.org/article/download/v099i13/4153) describes the flexible and circular candidate-window families and practical implementation details.

## Exercises

1. Why is a connectedness graph needed in addition to centroid distances?
2. Why restrict candidate subsets to the root plus K-1 nearest neighbours?
3. Why does exhaustive enumeration become expensive as K grows?
4. Why must each Monte Carlo replicate repeat the full connected-subset search?
5. How would changing the adjacency definition alter the detected cluster?

# Circular Poisson spatial scan statistic

Stable ID: SA-SPATIAL-POISSON-SCAN · Draft 0.1 · Source compendium section 14

## Purpose and data model

The spatial scan statistic searches for a geographic zone whose observed case rate is higher than the rate outside the zone, adjusting for population at risk. This implementation accepts one projected planar centroid, integer case count and positive population value per areal unit.

## Null expectation and likelihood ratio

Let C be the total case count and P the total population. For a candidate zone Z, let c_Z and P_Z be its observed cases and population. Under the constant-risk null,

\[
E_Z=C\frac{P_Z}{P}.
\]

For an elevated cluster, the log-likelihood ratio is

\[
LLR(Z)=
\begin{cases}
c_Z\log(c_Z/E_Z)+(C-c_Z)\log((C-c_Z)/(C-E_Z)), & c_Z>E_Z,\\
0, & c_Z\le E_Z.
\end{cases}
\]

The scan statistic is the maximum LLR over the candidate zones. The returned relative risk compares the estimated case rate inside the selected zone with the rate outside.

## Candidate circles

The implementation centres a circle on each supplied centroid. For each centre, it sorts all centroid distances and expands the radius through each distinct distance. Equal-distance ties are included together. Candidate zones whose population exceeds the user-supplied maximum fraction (0.5 by default) are excluded, as are zones containing fewer than min_cases.

This is a bounded candidate-zone family: circles are centred at observed centroids, not arbitrary continuous locations. Coordinates must be projected into a meaningful planar distance unit.

## Monte Carlo calibration

The null simulation conditions on the observed total number of cases. Each replication draws areal counts from a multinomial distribution with probabilities proportional to population. The maximum LLR is recomputed for each replication. With B replications and b simulated maxima at least as large as observed, the plus-one p-value is

\[
p=\frac{1+b}{1+B}.
\]

The notebook uses 99 replications only as a demonstration. More simulations are required for fine p-value resolution.

## Limitations

- This is a circular Poisson scan with a population offset, not a full SaTScan reproduction.
- The separate [finite-grid elliptical scan](statistics/elliptical-spatial-scan.md) extends the candidate shapes with explicit axis-ratio and orientation grids. Neither teaching baseline implements covariate adjustment, Bernoulli case-control, temporal scans, arbitrary zones, secondary clusters or polygon-boundary geometry.
- No correction for uncertain centroids or population estimates.
- It detects elevated-rate clusters only; low-rate cluster scans are not implemented.
- The scan statistic's Monte Carlo calibration accounts for maximising over the implemented candidate circles, but does not justify the study design or chosen candidate-zone family.

## Implementation and source verification

The [point-process package](../implementations/python/point-process/README.md) contains the centroid-based scan and conditional multinomial Monte Carlo calibration in `spatial_scan.py`, with regression cases in `test_spatial_scan.py`. See the [source-verification note](../catalog/verification/spatial-scan-statistic.md) for bibliographic identity and limits. Explore the [interactive scan lab](../notebooks/spatial-scan-statistic-lab.ipynb) to vary the candidate-zone population cap and Monte Carlo replication count.

## References

- Kulldorff, M. (1997). “A spatial scan statistic.” *Communications in Statistics—Theory and Methods*, 26(6), 1481–1496. https://doi.org/10.1080/03610929708831995.
- [smerc scan.test documentation](https://cran.r-project.org/web/packages/smerc/refman/smerc.html) documents centroid-based circular candidate zones and conditional multinomial simulation.

## Exercises

1. Why is the expected count inside a candidate zone proportional to its population share?
2. Compare a case-count hotspot with a high-rate cluster after population adjustment.
3. What changes when the maximum population fraction is reduced from 0.5 to 0.1?
4. Why must the Monte Carlo simulation recompute the maximum over all candidate circles?


## Space-time cylindrical scan

A companion [discrete space-time Poisson scan](statistics/space-time-scan-statistic.md) searches centroid-centred circular spatial zones crossed with contiguous time-bin intervals. It uses area-time population exposure as the Poisson offset and conditional multinomial simulations to calibrate the maximum cylinder likelihood ratio. It is a discrete-grid teaching baseline, not a full continuous-time SaTScan reproduction.

# Discrete space-time cylindrical Poisson scan

## Model

The space-time scan searches for elevated incidence in a cylinder formed by a spatial zone and a contiguous time interval. The spatial zone is a centroid-centred circle; the temporal zone is a sequence of ordered discrete bins. For cases C total and exposure E total, the expected cases inside a candidate cylinder with exposure E_z are

\[
\mathbb{E}(C_z)=C\frac{E_z}{E}.
\]

The elevated-rate Poisson log-likelihood ratio compares the inside and outside counts with their exposure-proportional expectations. The scan statistic is the maximum over all candidate circles and temporal intervals.

## Implemented scope

The NumPy baseline accepts N planar centroids and T-by-N arrays of integer cases and nonnegative population exposure. It enumerates tied centroid-radius zones and contiguous time intervals within caller-supplied minimum/maximum lengths and maximum exposure fraction. Conditional multinomial simulations distribute the fixed total case count over area-time cells in proportion to exposure and recalculates the maximum statistic for each replicate.

## Limits

This is a finite-grid, discrete-time teaching implementation. It is not a continuous-time SaTScan reproduction. It uses centroid circles, constant relative risk under the null, fixed exposure, and a conditional multinomial calibration. It does not implement elliptical or arbitrary zones in space-time, covariate adjustment, prospective sequential scanning, time-varying baseline risk, polygon boundaries, secondary-cluster hierarchies or continuous event-time likelihoods.

## Sources

- Kulldorff, M. (1997). A spatial scan statistic. *Communications in Statistics—Theory and Methods*, 26(6), 1481–1496. https://doi.org/10.1080/03610929708831995.
- Kulldorff, M., Athas, W. F., Feurer, E. J., Miller, B. A., & Key, C. R. (1998). Evaluating cluster alarms: A space-time scan statistic and brain cancer in Los Alamos. *American Journal of Public Health*, 88(9), 1377–1380. https://doi.org/10.2105/AJPH.88.9.1377.

Implementation: [point-process package](../../implementations/python/point-process/README.md).

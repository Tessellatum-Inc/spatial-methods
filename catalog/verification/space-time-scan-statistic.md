# Source verification — discrete space-time cylindrical Poisson scan

## Identity and bibliography
- Kulldorff (1997), “A spatial scan statistic,” *Communications in Statistics—Theory and Methods*, 26(6), 1481–1496, DOI 10.1080/03610929708831995.
- Kulldorff et al. (1998), “Evaluating cluster alarms: A space-time scan statistic and brain cancer in Los Alamos,” *American Journal of Public Health*, 88(9), 1377–1380, DOI 10.2105/AJPH.88.9.1377.

## Technical claims
- The scan zone is a spatial circle crossed with a contiguous time interval.
- Expected counts under the null are proportional to population-at-risk exposure.
- Conditional multinomial simulation preserves the total case count and calibrates the maximum scan statistic.

## Implementation and tests
- T-by-N integer case counts and nonnegative exposure, centroid-radius zones with equal-distance ties, contiguous discrete time windows and maximum exposure fraction.
- Tests cover a planted space-time cluster, exposure offsets, time-window bounds, seeded Monte Carlo calibration and invalid controls.

## Limits and rights
Discrete-time, centroid-circle baseline only; no continuous-time event histories, covariate adjustment, prospective scanning, secondary clusters or polygon geometry. Original implementation and explanatory text; bibliographic metadata only.

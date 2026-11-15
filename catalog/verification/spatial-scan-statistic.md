# Source verification — circular Poisson spatial scan

## Identity and bibliography

Kulldorff, M. (1997). “A spatial scan statistic.” *Communications in Statistics—Theory and Methods*, 26(6), 1481–1496. DOI: 10.1080/03610929708831995.

## Technical claims

The bounded implementation searches centroid-centred circular zones under a Poisson model with a population offset. Under the constant-risk null, the expected cases inside a candidate zone equal the total cases multiplied by the zone's share of total population. The elevated-cluster log-likelihood ratio is maximised over the implemented candidate circles. Conditional Monte Carlo calibration preserves the observed total case count and samples areal counts from a multinomial distribution proportional to population; the p-value uses the plus-one correction.

## Implementation and reproduction

The NumPy package implements centroid distance ordering, tied-radius inclusion, a maximum population fraction, minimum case count, relative risk and conditional multinomial simulation. Regression tests cover compact clusters, population adjustment, equal-distance ties, no elevated candidate, reproducibility and invalid inputs.

## Limits

This is not a full SaTScan reproduction. It does not implement covariates, temporal scans, elliptical or arbitrary zones, secondary clusters, low-rate scans, polygon-window geometry or uncertain population/centroid models. Coordinates must be projected planar coordinates with meaningful linear units. The Monte Carlo replication count controls p-value resolution.

## Rights

Only the published method and bibliographic metadata are paraphrased; no source code or figures are reproduced.

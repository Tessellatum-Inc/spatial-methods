# Source verification — circular Poisson spatial scan

## Identity and bibliography
Kulldorff, M. (1997). “A spatial scan statistic.” *Communications in Statistics—Theory and Methods*, 26(6), 1481–1496. DOI 10.1080/03610929708831995. The article extends scan statistics to spatial clusters and allows varying window sizes and inhomogeneous Poisson/Bernoulli baselines.

## Technical claims
For a Poisson model conditioned on the total number of cases, the null expected count in a candidate zone is total cases multiplied by the zone's population share. The high-rate likelihood ratio compares the inside and outside rates and is set to one (log statistic zero) when the inside rate is not elevated. Candidate circles are centred on region centroids and expanded by radius. Monte Carlo calibration compares the observed maximum with maxima from conditional multinomial simulations.

## Implementation/reproduction
Implemented: centroid-centred circular zones, tie-inclusive sorted radii, maximum population-fraction constraint, high-rate Poisson log-likelihood ratio, relative risk, and conditional multinomial Monte Carlo p-value with plus-one correction. Tests cover a known compact cluster, population offset, distance ties, zero elevated-cluster statistic, deterministic Monte Carlo output and invalid inputs.

Not implemented: covariate adjustment, Bernoulli model, temporal scan, elliptical/arbitrary zones, secondary clusters, polygon boundaries or full SaTScan-compatible output. The implementation is a bounded educational baseline, not a complete reproduction of SaTScan. Repository CI is required to establish passing status.

## Rights
Only mathematical definitions and bibliographic metadata are paraphrased; no source code, datasets or figures are reproduced.

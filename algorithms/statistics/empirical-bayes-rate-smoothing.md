# Empirical Bayes smoothing of area rates

Smooth unstable area-level disease or mortality rates by pooling information across areas. Crude rates from small-population areas are often more variable; empirical Bayes shrinkage pulls them toward a pooled mean, with less shrinkage where exposure is large.

This lesson implements the moment-based global and local estimators described by Marshall (1991):

- **Global:** shrink every crude rate toward the overall exposure-weighted rate. It ignores spatial arrangement.
- **Local:** shrink each crude rate toward a pooled rate calculated from an analyst-supplied neighbourhood. The neighbourhood graph and local homogeneity assumption matter.

The [Python implementation](../../implementations/python/empirical-bayes-rates/README.md) reports crude rates, shrinkage factors and moment estimates.

## Assumptions and limits
The sampling model is conditionally independent Poisson counts with positive exposure. This is not a CAR/BYM model, a scan statistic or a full Bayesian disease map. No age standardisation, covariates, posterior intervals, automatic contiguity construction or cluster significance testing is included. A smoothed map is not evidence of a statistically significant cluster.

## Reference
Marshall, R. J. (1991). “Mapping Disease and Mortality Rates Using Empirical Bayes Estimators.” *Journal of the Royal Statistical Society: Series C*, 40(2), 283–294. DOI 10.2307/2347593.

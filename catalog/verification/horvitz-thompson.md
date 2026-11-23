# Source verification — Horvitz–Thompson estimator

## Identity and bibliography
- Horvitz, D. G., & Thompson, D. J. (1952). “A generalization of sampling without replacement from a finite universe.” *Journal of the American Statistical Association*, 47(260), 663–685. DOI 10.1080/01621459.1952.10483446.

## Technical claims
- The total estimator is the sum of observed values divided by first-order inclusion probabilities.
- Its design-based variance uses first- and second-order inclusion probabilities.
- The population mean is the estimated total divided by known population size.

## Implementation and tests
- NumPy implementation validates finite positive first-order and pairwise probabilities, symmetry, diagonal agreement and pairwise upper bounds.
- Tests cover an SRS-without-replacement hand calculation, census zero variance, invalid inclusion designs and invalid values/population size.

## Limits and rights
The variance estimator requires positive pairwise inclusion probabilities for all sampled pairs; designs with zero joint inclusion probabilities need a different variance treatment. Original code and explanatory text; bibliographic metadata only.

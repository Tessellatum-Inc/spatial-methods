# Source verification — Hansen–Hurwitz estimator

## Identity and bibliography
- Hansen, M. H., & Hurwitz, W. N. (1943). “On the theory of sampling from finite populations.” *The Annals of Mathematical Statistics*, 14(4), 333–362. DOI 10.1214/aoms/1177731356.

## Technical claims
- For independent with-replacement draws, the total estimator is the average of observed values divided by their draw probabilities.
- The variance estimator is the sample variance of the draw-level inverse-probability weights divided by draw count.

## Implementation and tests
- NumPy implementation supports duplicate draws, optional population mean, and explicitly unavailable variance for a single draw.
- Tests cover a hand-computed with-replacement sample, mean scaling, single-draw behavior, invalid probabilities, misaligned arrays and population size.

## Limits and rights
Requires independent with-replacement draws and the correct per-draw selection probabilities. It is not the Horvitz–Thompson estimator for a without-replacement sample. Original implementation and explanatory text; bibliographic metadata only.

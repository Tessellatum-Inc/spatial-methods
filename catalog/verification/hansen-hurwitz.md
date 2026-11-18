# Source verification — Hansen–Hurwitz estimator

## Identity and bibliography
- Hansen, M. H., & Hurwitz, W. N. (1943). “On the theory of sampling from finite populations.” *The Annals of Mathematical Statistics*, 14(4), 333–362. DOI: https://doi.org/10.1214/aoms/1177731356.

## Technical claims
- Under independent with-replacement draws with known per-draw selection probability (p_i), the draw-level estimate is (y_i/p_i), and the total estimator averages those draw-level estimates.
- Its estimated variance is the sample variance of the draw-level estimates divided by draw count. This variance estimate is unavailable for a single draw.
- Duplicate draws remain separate observations in the ordered sample. This is not the Horvitz–Thompson estimator for without-replacement inclusion probabilities.

## Implementation and tests
- A new NumPy baseline was added at [implementations/python/hansen-hurwitz](../../implementations/python/hansen-hurwitz/README.md).
- It accepts aligned ordered draw values and probabilities, validates inputs, returns total and draw-level estimates, and optionally scales to population mean/variance using a supplied population size.
- Tests cover a hand-calculated example, repeated draws, total/mean scaling, one-draw variance unavailability, and invalid arrays/probabilities/population sizes.
- **CI:** pending at the time this record was updated. Tests are not claimed to have passed until the current PR-head workflow completes.

## Limits and rights
Requires independent with-replacement draws and the correct per-draw selection probabilities. It is not a Horvitz–Thompson estimator for a without-replacement design. The implementation is an educational baseline; no spatial autocorrelation, cluster sampling variance, nonresponse adjustment, sampling design generation or confidence interval is included. Bibliographic metadata and original explanatory text only; no paper text, figure or data is reproduced.
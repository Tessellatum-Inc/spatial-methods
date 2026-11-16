# Global Moran's I with permutation inference

## Question

Do values exhibit positive or negative global spatial autocorrelation relative to a random allocation of the observed values over fixed spatial weights?

## Statistic

For mean-centred observations \(z_i=x_i-\bar{x}\), weights \(w_{ij}\), and \(S_0=\sum_i\sum_jw_{ij}\),

\[
I=\frac{n}{S_0}\frac{\sum_i\sum_jw_{ij}z_iz_j}{\sum_i z_i^2}.
\]

For zero-diagonal weights, the conditional randomization expectation is \(-1/(n-1)\). The weights are used exactly as supplied; they need not be symmetric, but their direction and scaling affect the statistic and interpretation.

## Permutation procedure

1. Centre the observed values once and calculate the observed statistic.
2. Randomly permute the centred values over the fixed observation locations, preserving the weights matrix.
3. Recalculate the statistic for each permutation.
4. Calculate the Monte Carlo p-value with the plus-one correction: \((b+1)/(B+1)\).

The two-sided alternative compares absolute deviations from the randomization expectation. Greater and less alternatives compare simulated statistics directly with the observed statistic. A seed makes the simulation reproducible.

## Implementation

Runnable reference: [morans_i_permutation.py](../../implementations/python/spatial-econometrics/morans_i_permutation.py).

The result includes the observed statistic, theoretical randomization expectation, permutation mean and standard deviation, selected alternative, p-value, and all simulated statistics.

## Assumptions and limits

- The permutation null treats observed values as exchangeable across locations. This is not automatically justified for clustered sampling, trends, covariates, unequal measurement precision or other structured null hypotheses.
- This is a global test, not a local cluster detector.
- The plus-one p-value avoids zero Monte Carlo p-values; its resolution is \(1/(B+1)\).
- The standard randomization expectation applies to zero-diagonal weights. The implementation requires nonnegative weights and a positive total weight, but does not row-standardise or symmetrise them.
- The two-sided rule is a deviation-from-expectation randomization test, not a doubled one-sided tail probability.
- Permutations quantify uncertainty under the stated randomization null, not uncertainty from choosing the weights matrix.

## Validation

Tests independently reconstruct the statistic and seeded permutation distribution, check one-sided alternatives with asymmetric weights, and exercise invalid inputs. Run the package suite with `python -m pytest -q`.

## References

- Moran, P. A. P. (1950). Notes on continuous stochastic phenomena. *Biometrika*, 37(1/2), 17–23.
- Cliff, A. D., & Ord, J. K. (1981). *Spatial Processes: Models & Applications*. Pion.

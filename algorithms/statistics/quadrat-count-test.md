# Quadrat count test for complete spatial randomness

## Question

Are points distributed evenly across a chosen equal-area partition of the observation window, as expected under a homogeneous Poisson process?

## Statistic

Partition a rectangular window into m = nx × ny equal-area quadrats. If n points are observed and N_j is the count in quadrat j, the expected count under homogeneous complete spatial randomness (CSR), conditional on n, is E_j = n/m. The Pearson statistic is

\[
X^2=\sum_{j=1}^{m}\frac{(N_j-E_j)^2}{E_j}.
\]

Conditional on n, homogeneous CSR implies multinomial cell counts with equal probabilities 1/m. This implementation simulates that conditional null and computes an upper-tail Monte Carlo p-value with the plus-one correction.

## Interpretation

A large statistic indicates uneven counts across the selected grid. This can reflect aggregation, regularity, or a spatially varying first-order intensity. The test alone cannot distinguish these explanations. Results depend on the number, size and alignment of quadrats, and the method discards within-cell locations.

## Scope

The implementation supports a rectangular window, equal-area grid, conditional multinomial Monte Carlo calibration and a reproducible random seed. It does not fit an inhomogeneous intensity model, support irregular windows or adaptive tessellations, or replace K-function and pair-correlation analysis. The asymptotic chi-square approximation is intentionally not used; Monte Carlo calibration avoids the large-expected-count requirement for that approximation.

## References

- Baddeley, A., Rubak, E. and Turner, R. (2015). *Spatial Point Patterns: Methodology and Applications with R*. CRC Press.
- Baddeley, A. and Turner, R. Documentation for spatstat's quadrat test, including the Pearson statistic and conditional multinomial Monte Carlo method.
- Myllymäki, M. et al. (2022). “Should We Condition on the Number of Points When Modelling Spatial Point Patterns?” *The International Statistical Review*, 90(3), 551–562. DOI [10.1111/insr.12501](https://doi.org/10.1111/insr.12501).

## Repository implementation

A dependency-light implementation is available in [`implementations/python/point-process`](../../implementations/python/point-process/README.md), in `point_patterns.py` as `quadrat_count_test`. It uses conditional multinomial Monte Carlo calibration with a plus-one upper-tail p-value and a reproducible seed. The package test suite includes quadrat-count fixtures in [`test_point_patterns.py`](../../implementations/python/point-process/test_point_patterns.py). The method is limited to a rectangular window partitioned into equal-area quadrats; it does not provide irregular-window or adaptive-grid inference.

## Repository implementation

A dependency-light implementation is available in [`implementations/python/point-process`](../../implementations/python/point-process/README.md), in `point_patterns.py` as `quadrat_count_test`. It uses conditional multinomial Monte Carlo calibration with a plus-one upper-tail p-value and a reproducible seed. The package test suite includes quadrat-count fixtures in [`test_point_patterns.py`](../../implementations/python/point-process/test_point_patterns.py). The method is limited to a rectangular window partitioned into equal-area quadrats; it does not provide irregular-window or adaptive-grid inference.

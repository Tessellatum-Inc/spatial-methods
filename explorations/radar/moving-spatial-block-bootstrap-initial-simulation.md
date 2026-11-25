# Moving spatial-block bootstrap: initial coverage simulation

**Status:** exploratory simulation; not a validation claim  
**Implementation:** `spatial_moving_block_bootstrap.py`  
**Simulation script:** `simulate_moving_spatial_block_bootstrap.py`  
**Design:** 30 × 30 mean-zero separable Gaussian AR(1) fields; 150 Monte Carlo fields per correlation/window-width combination; 400 bootstrap replicates per field; fixed seed 20261126.  
**Known estimand:** population mean = 0.

## Status: numerical results superseded

The table below is retained as an historical record only and **must not be interpreted as valid evidence for the current implementation**. A code review identified that the earlier replicate statistic divided by the random number of sampled block occurrences. With irregular or boundary-truncated windows, window sizes vary and this ratio can introduce finite-sample weighting bias. The implementation has since been corrected to divide by the fixed number of sampled windows multiplied by $k^2$, consistent with equal first-order inclusion of every eligible block. The coverage experiment must be rerun before reporting numerical conclusions.

## Historical results (superseded)

The table reports empirical coverage of nominal 95% percentile intervals and mean interval width. Window width 1 is the ordinary independent-block bootstrap comparator.

| Spatial correlation ρ | Window width (base blocks) | Coverage | Mean interval width |
|---:|---:|---:|---:|
| 0.3 | 1 | 0.707 | 0.1287 |
| 0.3 | 2 | 0.833 | 0.1646 |
| 0.3 | 3 | 0.880 | 0.1858 |
| 0.3 | 4 | 0.887 | 0.1925 |
| 0.3 | 5 | 0.887 | 0.1988 |
| 0.6 | 1 | 0.373 | 0.1283 |
| 0.6 | 2 | 0.567 | 0.1997 |
| 0.6 | 3 | 0.647 | 0.2522 |
| 0.6 | 4 | 0.720 | 0.2868 |
| 0.6 | 5 | 0.780 | 0.3183 |
| 0.8 | 1 | 0.193 | 0.1255 |
| 0.8 | 2 | 0.380 | 0.2178 |
| 0.8 | 3 | 0.460 | 0.2916 |
| 0.8 | 4 | 0.540 | 0.3626 |
| 0.8 | 5 | 0.593 | 0.4048 |

## Interpretation

1. **Overlapping windows improve coverage relative to independent resampling in every tested correlated scenario.** The gain is substantial, especially at ρ=0.6 and 0.8.
2. **Larger windows widen intervals and generally improve coverage**, but the benefit is not monotonic in every row. At ρ=0.8, widths 4 and 5 both achieve only 0.54 coverage.
3. **The method is not calibrated by this experiment.** None of the settings reaches nominal 0.95 coverage at ρ=0.6 or 0.8. At ρ=0.3, width 5 reaches 0.907, still below nominal.
4. **Window width cannot be selected by the observed result.** A width that improves coverage under one correlation structure may remain inadequate under another. The dependence scale is not known in advance for the Nairobi residual contrasts.

## Monte Carlo uncertainty

With 150 simulated fields, coverage estimates have appreciable Monte Carlo error. Near 0.5, the approximate binomial standard error is 0.041; near 0.9 it is 0.024. These results are useful for rejecting the assumption that the moving-window percentile bootstrap is automatically valid, not for declaring a universally optimal window size.

## Important limitations

- The data-generating process is stationary, Gaussian and separable with the same AR(1) parameter along both axes.
- The study uses a complete square grid; irregular eligibility masks, holes, anisotropy, nonstationarity, heavy tails and spatially varying variance have not yet been tested.
- The target is the global mean of a stationary zero-mean field, not the matched land-cover contrast or the full Nairobi analysis pipeline.
- No confidence interval for the coverage rate is used as a decision threshold.
- The bootstrap windows overlap by design; this carries local dependence into replicates but does not guarantee valid coverage.
- The simulation does not establish that a single window width is suitable for the empirical data.

## Decision

Keep the moving-window bootstrap as an experimental candidate, not a replacement for the existing block and superblock sensitivity analyses. Before applying it to Nairobi, extend simulations to irregular masks, anisotropic and nonstationary fields, and the matched-strata/block-contrast estimand. Evaluate coverage over a predeclared grid of dependence scales and window widths. If no robust setting achieves acceptable coverage, report that limitation rather than tune a width to the observed Nairobi result.

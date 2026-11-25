# Moving spatial-block bootstrap: initial coverage simulation

**Status:** exploratory simulation; not a validation claim  
**Implementation:** `spatial_moving_block_bootstrap.py`  
**Simulation script:** `simulate_moving_spatial_block_bootstrap.py`  
**Design:** 30 × 30 mean-zero separable Gaussian AR(1) fields; 150 Monte Carlo fields per correlation/window-width combination; 400 bootstrap replicates per field; fixed seed 20261126.  
**Known estimand:** population mean = 0.

## Results

The table reports empirical coverage of nominal 95% percentile intervals and mean interval width. Window width 1 is the ordinary independent-block bootstrap comparator.

| Spatial correlation ρ | Window width (base blocks) | Coverage | Mean interval width |
|---:|---:|---:|---:|
| 0.3 | 1 | 0.640 | 0.1289 |
| 0.3 | 2 | 0.833 | 0.1649 |
| 0.3 | 3 | 0.833 | 0.1855 |
| 0.3 | 4 | 0.853 | 0.1927 |
| 0.3 | 5 | 0.907 | 0.1968 |
| 0.6 | 1 | 0.360 | 0.1272 |
| 0.6 | 2 | 0.573 | 0.2001 |
| 0.6 | 3 | 0.633 | 0.2535 |
| 0.6 | 4 | 0.720 | 0.2874 |
| 0.6 | 5 | 0.813 | 0.3141 |
| 0.8 | 1 | 0.180 | 0.1243 |
| 0.8 | 2 | 0.280 | 0.2176 |
| 0.8 | 3 | 0.427 | 0.2976 |
| 0.8 | 4 | 0.540 | 0.3646 |
| 0.8 | 5 | 0.540 | 0.4094 |

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

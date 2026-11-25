# Moving spatial-block bootstrap: initial coverage simulation

**Status:** exploratory diagnostic; the implementation passes structural tests but is not calibrated.  
**Implementation:** `spatial_moving_block_bootstrap.py`  
**Simulation scripts:** `simulate_moving_spatial_block_bootstrap.py`, `simulate_moving_spatial_block_bootstrap_expanded.py`  
**Design:** 30 × 30 mean-zero separable Gaussian AR(1) fields; 150 Monte Carlo fields per correlation/window-width combination; 400 bootstrap replicates per field.  
**Known estimand:** population mean = 0.  
**Validation run:** [GitHub Actions run 45660180206](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45660180206)

## Corrected implementation results

The equal-inclusion normalization correction was validated by seven unit tests. The corrected Monte Carlo experiment completed successfully. The table reports empirical coverage of nominal 95% percentile intervals and mean interval width.

| Spatial correlation ρ | Window width (base blocks) | Coverage | 95% Wilson interval for coverage | Mean interval width |
|---:|---:|---:|---:|---:|
| 0.3 | 1 | 0.707 | 0.629–0.774 | 0.1287 |
| 0.3 | 2 | 0.833 | 0.766–0.884 | 0.1544 |
| 0.3 | 3 | 0.880 | 0.818–0.923 | 0.1636 |
| 0.3 | 4 | 0.887 | 0.826–0.928 | 0.1591 |
| 0.3 | 5 | 0.887 | 0.826–0.928 | 0.1548 |
| 0.6 | 1 | 0.373 | 0.300–0.453 | 0.1283 |
| 0.6 | 2 | 0.567 | 0.487–0.643 | 0.1874 |
| 0.6 | 3 | 0.647 | 0.567–0.719 | 0.2222 |
| 0.6 | 4 | 0.720 | 0.643–0.786 | 0.2378 |
| 0.6 | 5 | 0.780 | 0.707–0.839 | 0.2490 |
| 0.8 | 1 | 0.193 | 0.138–0.264 | 0.1255 |
| 0.8 | 2 | 0.380 | 0.306–0.460 | 0.2044 |
| 0.8 | 3 | 0.460 | 0.382–0.540 | 0.2582 |
| 0.8 | 4 | 0.540 | 0.460–0.618 | 0.3014 |
| 0.8 | 5 | 0.593 | 0.513–0.669 | 0.3186 |

The Wilson intervals quantify Monte Carlo uncertainty in the estimated coverage proportion; they are not confidence intervals for the bootstrap estimand. Even the upper endpoints remain below 0.95 in every tested condition. The undercoverage is therefore not plausibly explained by the finite 150-simulation Monte Carlo sample alone.

## Expanded-width diagnostic

A second experiment evaluated widths 1, 2, 3, 4, 5, 6, 8, 10 and 12 on the same 30 × 30 grid, using an independent simulation seed (20261127). It completed in the same successful workflow. Selected results:

| Spatial correlation ρ | Window width | Coverage | 95% Wilson interval |
|---:|---:|---:|---:|
| 0.3 | 4 | 0.913 | 0.857–0.949 |
| 0.3 | 8 | 0.867 | 0.803–0.912 |
| 0.3 | 12 | 0.873 | 0.811–0.917 |
| 0.6 | 4 | 0.727 | 0.650–0.792 |
| 0.6 | 8 | 0.873 | 0.811–0.917 |
| 0.6 | 12 | 0.827 | 0.758–0.879 |
| 0.8 | 4 | 0.547 | 0.467–0.624 |
| 0.8 | 8 | 0.647 | 0.567–0.719 |
| 0.8 | 12 | 0.807 | 0.736–0.862 |

The wider-window experiment reinforces the same conclusion: coverage can improve substantially as windows widen, but no tested setting reaches 0.95. Even at width 12, coverage under ρ=0.8 is only 0.807 (Wilson upper bound 0.862). Width 12 also leaves very few sampled windows per replicate, so simply increasing width is not a defensible general solution. Width 4 under ρ=0.3 approaches nominal coverage but does not establish robustness across dependence structures.

The two experiments use different seeds, so small differences in overlapping conditions are expected. Do not interpret them as contradictory; both show material undercoverage under moderate and strong dependence.

## Interpretation

1. Overlapping windows improve coverage relative to independent one-block resampling in every tested correlated scenario.
2. Larger windows generally improve coverage, but the tested widths do not achieve nominal 95% coverage robustly.
3. The failure is severe under moderate and strong dependence: the best selected coverage is 0.873 at ρ=0.6 and 0.807 at ρ=0.8 in the expanded run.
4. This is evidence against treating the current percentile moving-window bootstrap as calibrated. It is not evidence that the equal-inclusion point estimator is biased; point-estimator expectation and interval coverage are separate properties.
5. Do not select a window width by looking for the best coverage in one synthetic scenario, and do not tune it to Nairobi results.

## Important limitations

- The data-generating process is stationary, Gaussian and separable with the same AR(1) parameter along both axes.
- Both experiments use complete square grids; irregular eligibility masks, holes, anisotropy, nonstationarity, heavy tails and spatially varying variance remain untested for coverage.
- The target is the global mean of a stationary zero-mean field, not the matched land-cover contrast or full Nairobi analysis pipeline.
- The bootstrap windows overlap by design. Equal first-order inclusion and unbiased replicate expectation do not guarantee correct variance estimation or nominal coverage.
- The simulations do not establish that any single window width is suitable for empirical data.

## Decision

Keep this method explicitly experimental. Do not use its intervals as inferential evidence for Nairobi or as a replacement for existing block/superblock sensitivity analyses. Next validation should test irregular masks, directional/anisotropic dependence, nonstationarity and the actual matched-strata/block-contrast estimand. Predeclare scenarios and candidate widths. If no defensible setting achieves acceptable coverage across relevant scenarios, retire this percentile interval approach or replace it with a method whose uncertainty properties can be justified.

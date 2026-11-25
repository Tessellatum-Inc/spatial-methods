# Paired spatial uncertainty comparison

**Status:** exploratory head-to-head comparison; all estimator unit tests and the paired Monte Carlo workflow passed. No candidate achieved nominal 95% coverage across the tested dependence levels.  
**Script:** `compare_spatial_uncertainty_methods.py`  
**Validation run:** [GitHub Actions run 45662565493](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45662565493)  
**Artifact:** `paired-spatial-uncertainty-comparison`  
**Design:** 30 × 30 mean-zero separable Gaussian AR(1) fields; 100 fields per correlation; identical field realizations passed to all methods and tuning widths; 300 moving-window bootstrap replicates; seed 20261130.

## Paired results

| ρ | Method | Width | Coverage | 95% Wilson interval | Mean interval width |
|---:|---|---:|---:|---:|---:|
| 0.3 | Moving window | 4 | 0.820 | 0.733–0.883 | 0.1919 |
| 0.3 | HAC | 4 | 0.870 | 0.790–0.922 | 0.1964 |
| 0.3 | Subsampling | 4 | 0.870 | 0.790–0.922 | 0.1976 |
| 0.3 | Moving window | 8 | 0.840 | 0.756–0.899 | 0.2050 |
| 0.3 | HAC | 8 | 0.880 | 0.802–0.930 | 0.2076 |
| 0.3 | Subsampling | 8 | 0.860 | 0.779–0.915 | 0.2017 |
| 0.3 | Moving window | 12 | 0.870 | 0.790–0.922 | 0.2045 |
| 0.3 | HAC | 12 | 0.850 | 0.767–0.907 | 0.2029 |
| 0.3 | Subsampling | 12 | 0.790 | 0.700–0.858 | 0.1770 |
| 0.6 | Moving window | 4 | 0.780 | 0.689–0.850 | 0.2866 |
| 0.6 | HAC | 4 | 0.780 | 0.689–0.850 | 0.2928 |
| 0.6 | Subsampling | 4 | 0.780 | 0.689–0.850 | 0.2967 |
| 0.6 | Moving window | 8 | 0.880 | 0.802–0.930 | 0.3523 |
| 0.6 | HAC | 8 | 0.880 | 0.802–0.930 | 0.3618 |
| 0.6 | Subsampling | 8 | 0.850 | 0.767–0.907 | 0.3534 |
| 0.6 | Moving window | 12 | 0.890 | 0.814–0.937 | 0.3755 |
| 0.6 | HAC | 12 | 0.900 | 0.826–0.945 | 0.3772 |
| 0.6 | Subsampling | 12 | 0.830 | 0.745–0.891 | 0.3358 |
| 0.8 | Moving window | 4 | 0.520 | 0.423–0.615 | 0.3618 |
| 0.8 | HAC | 4 | 0.510 | 0.413–0.606 | 0.3631 |
| 0.8 | Subsampling | 4 | 0.540 | 0.443–0.634 | 0.3690 |
| 0.8 | Moving window | 8 | 0.730 | 0.636–0.807 | 0.5286 |
| 0.8 | HAC | 8 | 0.710 | 0.615–0.790 | 0.5254 |
| 0.8 | Subsampling | 8 | 0.710 | 0.615–0.790 | 0.5157 |
| 0.8 | Moving window | 12 | 0.770 | 0.678–0.842 | 0.6089 |
| 0.8 | HAC | 12 | 0.800 | 0.711–0.867 | 0.5923 |
| 0.8 | Subsampling | 12 | 0.740 | 0.646–0.816 | 0.5201 |

## Interpretation

1. Using the same simulated fields removes one source of between-experiment variation. The three methods show broadly similar behaviour at matched tuning widths.
2. Under weak dependence, all candidates under-cover moderately (0.79–0.88).
3. Under moderate dependence, the best observed coverage is 0.90 for HAC at width 12; moving window reaches 0.89 and subsampling 0.85.
4. Under strong dependence, the best observed coverage is 0.80 for HAC at width 12; moving window reaches 0.77 and subsampling 0.74.
5. Wilson intervals overlap materially. These 100-field experiments do not establish a statistically meaningful ranking between candidates.
6. Increasing width improves coverage under stronger dependence, but none reaches nominal 0.95. Larger widths also produce wider intervals and eventually fewer effective spatial units.

## Decision

Do not select a winner from this experiment. Keep all three methods as experimental candidates and do not use their current intervals as calibrated Nairobi inference. The next discriminating experiment is anisotropic dependence with separate row/column bandwidths, followed by irregular masks and nonstationarity. The matched-strata/block-contrast estimand must then be tested directly. Predeclare the scenario grid and tuning ranges; do not optimize to the observed Nairobi result.

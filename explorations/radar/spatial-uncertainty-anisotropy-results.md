# Directional dependence: spatial uncertainty coverage experiment

**Status:** exploratory anisotropy diagnostic; estimator tests and CI simulation passed. Directional HAC bandwidths respond to the axis of stronger dependence, but no tested setting reaches nominal 95% coverage.  
**Script:** `simulate_spatial_uncertainty_anisotropy.py`  
**Validation run:** [GitHub Actions run 45662982994](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45662982994)  
**Artifact:** `spatial-uncertainty-anisotropy`  
**Design:** 30 × 30 separable Gaussian AR(1) fields; 100 fields per orientation; same fields evaluated by all methods/configurations; seed 20261201.

## Orientation A: stronger row dependence

$\rho_{row}=0.8$, $\rho_{column}=0.3$.

| Method | Row width | Column width | Coverage | 95% Wilson interval |
|---|---:|---:|---:|---:|
| HAC | 4 | 4 | 0.710 | 0.615–0.790 |
| HAC | 8 | 4 | 0.810 | 0.722–0.875 |
| HAC | 12 | 4 | 0.860 | 0.779–0.915 |
| HAC | 4 | 8 | 0.700 | 0.604–0.781 |
| HAC | 4 | 12 | 0.690 | 0.594–0.772 |
| HAC | 8 | 8 | 0.820 | 0.733–0.883 |
| HAC | 12 | 12 | 0.850 | 0.767–0.907 |
| Moving window | 8 | 8 | 0.820 | 0.733–0.883 |
| Moving window | 12 | 12 | 0.840 | 0.756–0.899 |
| Subsampling | 8 | 8 | 0.790 | 0.700–0.858 |
| Subsampling | 12 | 12 | 0.760 | 0.668–0.833 |

The best tested HAC configuration uses a longer row bandwidth (12) and shorter column bandwidth (4), matching the stronger row dependence. Reversing that choice (4,12) performs worse than the isotropic baseline.

## Orientation B: stronger column dependence

$\rho_{row}=0.3$, $\rho_{column}=0.8$.

| Method | Row width | Column width | Coverage | 95% Wilson interval |
|---|---:|---:|---:|---:|
| HAC | 4 | 4 | 0.680 | 0.583–0.763 |
| HAC | 8 | 4 | 0.740 | 0.646–0.816 |
| HAC | 12 | 4 | 0.740 | 0.646–0.816 |
| HAC | 4 | 8 | 0.850 | 0.767–0.907 |
| HAC | 4 | 12 | 0.900 | 0.826–0.945 |
| HAC | 8 | 8 | 0.840 | 0.756–0.899 |
| HAC | 12 | 12 | 0.870 | 0.790–0.922 |
| Moving window | 8 | 8 | 0.850 | 0.767–0.907 |
| Moving window | 12 | 12 | 0.870 | 0.790–0.922 |
| Subsampling | 8 | 8 | 0.770 | 0.678–0.842 |
| Subsampling | 12 | 12 | 0.740 | 0.646–0.816 |

The best tested HAC configuration uses a longer column bandwidth (4,12), again matching the axis of stronger dependence. This is directional evidence, not nominal calibration: its coverage is 0.900 and the Wilson upper bound is 0.945.

## Interpretation

1. Direction-specific HAC bandwidths matter. The best orientation-specific bandwidth pairs follow the direction of longer correlation.
2. Isotropic square windows cannot express that distinction; moving-window and square subsampling results are similar under the two orientations.
3. Even with directional tuning, HAC remains below 95% in both orientations.
4. The two orientation experiments are deliberately symmetric and support the interpretation that row/column labels, not a particular axis, drive the result.
5. Bandwidth selection must be based on a predeclared dependence diagnostic or sensitivity envelope, not by selecting the configuration with the highest observed coverage or most favourable empirical interval.

## Decision

Retain directional HAC as a stronger candidate for anisotropic dependence, but not as a calibrated inference method. Next add irregular masks and spatially varying/nonstationary dependence. Then test the actual matched-strata block-contrast estimand and compare all methods on identical realizations. No current interval should be used as calibrated Nairobi uncertainty.

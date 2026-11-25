# Spatial subsampling: initial stationary-field coverage diagnostic

**Status:** experimental; tests and CI simulation pass, but the tested fixed-size subsampling intervals under-cover under all three dependence levels.  
**Implementation:** `spatial_subsampling.py`  
**Tests:** `test_spatial_subsampling.py` (4 tests)  
**Simulation:** `simulate_spatial_subsampling.py`  
**Validation run:** [GitHub Actions run 45662313379](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45662313379)  
**Artifact:** `spatial-subsampling-coverage`  
**Design:** 30 × 30 mean-zero separable Gaussian AR(1) fields; 150 fields per condition; seed 20261129.

## Method

For each complete 30 × 30 grid, enumerate every overlapping square subsample of width $b$. Form the subsampling statistic
\[
T_b=\sqrt{b^2}(\bar y_b-\bar y_N).
\]
Its empirical quantiles approximate the distribution of the full-grid statistic $\sqrt{N}(\bar y_N-\mu)$. Therefore invert using the full-grid scale $\sqrt{N}$:
\[
[\bar y_N-q_{0.975}/\sqrt{N},\;\bar y_N-q_{0.025}/\sqrt{N}].
\]
The initial implementation deliberately rejects irregular masks rather than silently applying fixed-size scaling to variable-size subsamples.

## Results

| Correlation ρ | Subsample width (blocks) | Coverage | 95% Wilson interval | Mean interval width |
|---:|---:|---:|---:|---:|
| 0.3 | 4 | 0.873 | 0.811–0.917 | 0.1973 |
| 0.3 | 6 | 0.880 | 0.818–0.923 | 0.2060 |
| 0.3 | 8 | 0.873 | 0.811–0.917 | 0.2034 |
| 0.3 | 10 | 0.867 | 0.803–0.912 | 0.1945 |
| 0.3 | 12 | 0.807 | 0.736–0.862 | 0.1825 |
| 0.3 | 15 | 0.747 | 0.672–0.810 | 0.1600 |
| 0.3 | 20 | 0.560 | 0.480–0.637 | 0.1163 |
| 0.6 | 4 | 0.687 | 0.609–0.755 | 0.2933 |
| 0.6 | 6 | 0.773 | 0.700–0.833 | 0.3393 |
| 0.6 | 8 | 0.793 | 0.722–0.850 | 0.3553 |
| 0.6 | 10 | 0.753 | 0.679–0.815 | 0.3485 |
| 0.6 | 12 | 0.740 | 0.664–0.804 | 0.3295 |
| 0.6 | 15 | 0.647 | 0.567–0.719 | 0.2841 |
| 0.6 | 20 | 0.480 | 0.402–0.559 | 0.2013 |
| 0.8 | 4 | 0.507 | 0.427–0.586 | 0.3731 |
| 0.8 | 6 | 0.613 | 0.533–0.688 | 0.4673 |
| 0.8 | 8 | 0.647 | 0.567–0.719 | 0.5184 |
| 0.8 | 10 | 0.680 | 0.602–0.749 | 0.5336 |
| 0.8 | 12 | 0.673 | 0.595–0.743 | 0.5186 |
| 0.8 | 15 | 0.620 | 0.540–0.694 | 0.4606 |
| 0.8 | 20 | 0.427 | 0.350–0.507 | 0.3239 |

The Wilson intervals quantify Monte Carlo uncertainty in the coverage proportion, not uncertainty in the mean. No tested setting approaches nominal 95% coverage under moderate or strong dependence. The best observed coverage is 0.880 at ρ=0.3, 0.793 at ρ=0.6 and 0.680 at ρ=0.8.

## Interpretation

1. Moderate subsample widths perform better than very large widths in this finite 30 × 30 experiment.
2. Very large subsamples leave too few distinct spatial windows and substantially under-cover.
3. The method is sensitive to subsample width; there is no robust width that works across dependence strengths.
4. The initial implementation is limited to complete regular grids. It does not claim validity for irregular masks.
5. The first run used the wrong inversion scale (subsample size); those initial over-wide intervals and apparent overcoverage are superseded. The results in this report use the corrected full-grid $\sqrt{N}$ inversion and passed the updated CI tests.

## Comparison and decision

On the same broad stationary isotropic Gaussian design, spatial subsampling under-covers more severely than the best moving-window bootstrap settings and is broadly comparable to or weaker than the spatial HAC candidate. These are separate-seed experiments, not paired comparisons. None of the three candidates has demonstrated nominal 95% coverage across dependence strengths.

Retain spatial subsampling as a research comparator only. Do not apply its current intervals to Nairobi or irregular empirical block masks. Next validation should use paired random fields and compare all candidates on identical realizations, then introduce anisotropy, irregular eligibility, nonstationarity and the matched-strata/block-contrast estimand.

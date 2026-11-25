# Spatial HAC: initial stationary-field coverage diagnostic

**Status:** experimental estimator; unit tests and CI simulation pass, but nominal coverage is not achieved under moderate or strong dependence.  
**Implementation:** `spatial_hac.py`  
**Tests:** `test_spatial_hac.py` (6 tests)  
**Simulation:** `simulate_spatial_hac.py`  
**Validation run:** [GitHub Actions run 45661356905](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/45661356905)  
**Artifact:** `spatial-hac-coverage`  
**Design:** 30 × 30 mean-zero separable Gaussian AR(1) fields; 150 fields per condition; 95% normal intervals; seed 20261128.

## Estimator

The equal-block mean is paired with a spatial HAC variance estimate using a separable product-Bartlett kernel over row and column offsets. Separate row/column bandwidths are accepted. This experiment uses equal bandwidths along both axes and a complete regular grid.

## Results

Empirical coverage of nominal 95% intervals:

| Correlation ρ | Bandwidth (blocks) | Coverage | 95% Wilson interval | Mean interval width |
|---:|---:|---:|---:|---:|
| 0.3 | 1 | 0.713 | 0.636–0.780 | 0.1302 |
| 0.3 | 2 | 0.833 | 0.766–0.884 | 0.1672 |
| 0.3 | 3 | 0.860 | 0.795–0.907 | 0.1860 |
| 0.3 | 4 | 0.893 | 0.834–0.933 | 0.1964 |
| 0.3 | 6 | 0.907 | 0.849–0.944 | 0.2056 |
| 0.3 | 8 | 0.907 | 0.849–0.944 | 0.2080 |
| 0.3 | 12 | 0.887 | 0.826–0.928 | 0.2058 |
| 0.6 | 1 | 0.373 | 0.300–0.453 | 0.1297 |
| 0.6 | 2 | 0.587 | 0.507–0.662 | 0.2036 |
| 0.6 | 3 | 0.667 | 0.588–0.737 | 0.2556 |
| 0.6 | 4 | 0.720 | 0.643–0.786 | 0.2928 |
| 0.6 | 6 | 0.760 | 0.686–0.821 | 0.3387 |
| 0.6 | 8 | 0.787 | 0.714–0.845 | 0.3624 |
| 0.6 | 12 | 0.813 | 0.743–0.868 | 0.3764 |
| 0.8 | 1 | 0.167 | 0.116–0.234 | 0.1240 |
| 0.8 | 2 | 0.287 | 0.220–0.364 | 0.2167 |
| 0.8 | 3 | 0.420 | 0.344–0.500 | 0.2929 |
| 0.8 | 4 | 0.527 | 0.447–0.605 | 0.3552 |
| 0.8 | 6 | 0.607 | 0.527–0.681 | 0.4465 |
| 0.8 | 8 | 0.653 | 0.574–0.725 | 0.5047 |
| 0.8 | 12 | 0.713 | 0.636–0.780 | 0.5591 |

Wilson intervals quantify Monte Carlo uncertainty in the estimated coverage proportion. They are not intervals for the spatial mean. None of the tested settings reaches nominal 95% coverage. The best observed coverage is 0.907 under ρ=0.3 (bandwidth 6 or 8), 0.813 under ρ=0.6 (bandwidth 12), and 0.713 under ρ=0.8 (bandwidth 12). The upper Wilson limits remain below 0.95 in all conditions.

## Interpretation

1. Increasing bandwidth generally increases coverage under stronger dependence, but does not restore nominal coverage in the tested range.
2. The largest bandwidth is not uniformly best: under ρ=0.3, coverage declines from 0.907 at bandwidths 6–8 to 0.887 at 12.
3. The diagonal-only bandwidth 1 behaves like an independence-based variance estimate and severely undercovers as dependence rises.
4. A positive-semidefinite kernel ensures a nonnegative quadratic-form variance estimate; it does not ensure finite-sample calibration.
5. These results do not validate the estimator for irregular masks, anisotropy, nonstationarity, heavy tails, or the matched-strata block-contrast estimand.

## Comparison with moving-window bootstrap

Both candidates materially under-cover under moderate and strong dependence in the current synthetic experiment. The moving-window percentile method reached higher coverage at some tested settings, but it also failed to reach 95%. The HAC estimator has the advantage of an explicit covariance/bandwidth interpretation and separate directional bandwidths; it has not demonstrated better calibration. The experiments use different seeds, so this is a qualitative cross-experiment comparison, not a paired ranking.

## Decision

Retain spatial HAC as a candidate diagnostic, not an inferential default. Do not apply either method's current intervals as calibrated Nairobi uncertainty. Next test anisotropic fields with separate row/column bandwidths, irregular masks, nonstationarity and the actual matched-strata/block-contrast estimand. Compare HAC with spatial subsampling under the same generated fields and seeds. Predeclare bandwidth grids; do not select settings to support a preferred empirical conclusion.

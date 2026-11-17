# Verification record: syndromic surveillance

## Implemented scope

- Two-sided tabular CUSUM with caller-specified target, allowance and threshold.
- Explicit EARS-style C1, C2 and C3 scores with lagged baseline windows.
- Farrington-style seasonal quasi-Poisson exceedance baseline: same-period historical windows, log-linear trend, Poisson IRLS, optional residual reweighting, Pearson overdispersion and cube-root normal upper prediction approximation.

## Tests

Tests cover CUSUM recursions and alarm state, EARS baseline timing and score arithmetic, Farrington seasonal-reference selection, synthetic outbreak exceedance, stable no-outbreak baseline, and invalid controls/history. The detector uses no external numerical dependency. CI status is tied to the commit containing the tests.

## Limits

The Farrington-style routine is deliberately bounded. It does not reproduce every detail of the original GLIM algorithm or the Noufaily et al. improved flexible method; its upper bound uses a cube-root normal approximation, not the full predictive-distribution options of established surveillance software. It does not model weekday effects, holidays, covariates, reporting delays, population offsets or multisite dependence. Thresholds require local calibration and an alarm is not an outbreak diagnosis.

## Bibliography

- Farrington, C. P., Andrews, N. J., Beale, A. D., & Catchpole, M. A. (1996). A statistical algorithm for the early detection of outbreaks of infectious disease. *Journal of the Royal Statistical Society: Series A*, 159(3), 547–563. https://doi.org/10.2307/2983331
- Noufaily, A., Enki, D. G., Farrington, P., Garthwaite, P., Andrews, N., & Charlett, A. (2013). An improved algorithm for outbreak detection in multiple surveillance systems. *Statistics in Medicine*, 32, 1206–1222. https://doi.org/10.1002/sim.5595

## Rights

Only mathematical definitions and bibliographic metadata are paraphrased; no source code, datasets or figures are reproduced.

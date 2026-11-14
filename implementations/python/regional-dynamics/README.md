# Regional distribution dynamics

NumPy teaching implementations for balanced regional panels:

- pooled-quantile Markov transition counts and row probabilities;
- spatial Markov matrices conditioned on the lagged spatial-lag class;
- LISA/Moran-quadrant state transitions (HH, HL, LH, LL);
- cross-sectional sigma-dispersion by period.

Run with `python -m pytest -q` from this directory.

## Conventions and limitations

Input shape is **(time, regions)**. The panel must be balanced and finite; missing observations require an explicit common-sample or missing-data design. Quantile breaks are pooled over all region-period observations. Ties can reduce the effective number of classes, which is returned. Empty origin-state rows remain zero after row normalization.

Spatial weights are dense, nonnegative and zero-diagonal. Every row must have positive weight and is row-standardized internally. The spatial Markov conditioning variable is the lag of the continuous observed value, not a causal exposure. LISA transitions use period-specific z-scores and spatial lags, assign zero to the low side, and report descriptive quadrant transitions only. They do not calculate local Moran statistics, permutation p-values or multiple-testing corrections.

These routines do not estimate beta-convergence regressions, spatial panel models, continuous distribution dynamics, kernel transition densities, confidence intervals, bootstrap uncertainty or causal effects. Results depend on class count, pooled breakpoints, spatial weights, temporal spacing and region composition. Do not interpret a transition matrix as evidence of convergence without sensitivity analysis and an explicit economic model.

- **Beta convergence:** cross-sectional absolute/conditional log-growth regression with OLS and HC1 standard errors; spatial error dependence, endogeneity and panel estimators remain out of scope. See the [beta-convergence lesson](../../../methods/regional-beta-convergence.md) and [lab notebook](../../../notebooks/regional-beta-convergence-lab.ipynb).

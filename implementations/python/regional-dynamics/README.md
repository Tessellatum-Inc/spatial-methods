# Regional distribution dynamics

NumPy teaching implementations for balanced regional panels:

- pooled-quantile Markov transition counts and row probabilities;
- spatial Markov matrices conditioned on the lagged spatial-lag class;
- LISA/Moran-quadrant state transitions (HH, HL, LH, LL);
- cross-sectional sigma-dispersion by period.

Run with `python -m pytest -q --import-mode=importlib` from this directory.

## Conventions and limitations

Input shape is **(time, regions)**. The panel must be balanced and finite; missing observations require an explicit common-sample or missing-data design. Quantile breaks are pooled over all region-period observations. Ties can reduce the effective number of classes, which is returned. Empty origin-state rows remain zero after row normalization.

Spatial weights are dense, nonnegative and zero-diagonal. Every row must have positive weight and is row-standardized internally. The spatial Markov conditioning variable is the lag of the continuous observed value, not a causal exposure. LISA transitions use period-specific z-scores and spatial lags, assign zero to the low side, and report descriptive quadrant transitions only. They do not calculate local Moran statistics, permutation p-values or multiple-testing corrections.

These Markov/LISA routines do not estimate spatial panel models, continuous distribution dynamics, kernel transition densities, confidence intervals, bootstrap uncertainty or causal effects. A separate beta_convergence.py module provides a cross-sectional OLS beta-convergence baseline; it is not a spatial panel estimator. Results depend on class count, pooled breakpoints, spatial weights, temporal spacing and region composition. Do not interpret a transition matrix as evidence of convergence without sensitivity analysis and an explicit economic model.

- **Beta convergence:** cross-sectional absolute/conditional log-growth regression with OLS and HC1 standard errors; spatial error dependence, endogeneity and panel estimators remain out of scope. See the [beta-convergence lesson](../../../methods/regional-beta-convergence.md) and [lab notebook](../../../notebooks/regional-beta-convergence-lab.ipynb).

- **PPML gravity:** cross-sectional Poisson pseudo-maximum-likelihood regression with log link, optional offset, Newton/IRLS scoring and HC0 sandwich covariance. Zero outcomes are retained; high-dimensional fixed effects, clustered covariance and separation handling are not implemented. See the [PPML lesson](../../../methods/poisson-pseudo-maximum-likelihood-gravity.md) and [synthetic lab](../../../notebooks/regional-gravity-ppml-lab.ipynb).

- **Harris-style market potential:** destination market mass weighted by inverse-power generalized travel cost, with optional self-potential exclusion. This is a descriptive index, not an estimated gravity or equilibrium model. See the [method](../../../methods/harris-market-potential.md) and [lab](../../../notebooks/harris-market-potential-lab.ipynb).


- **Constrained gravity flows:** unconstrained, production-constrained, attraction-constrained and doubly constrained flows; the latter uses iterative proportional fitting. A Wilson-style exponential-cost entropy-maximising variant is included. This complements, but does not replace, the PPML regression estimator.


- **Intervening opportunities:** a cumulative exponential opportunity-acceptance model allocates origin mass to destination groups in increasing generalized-cost order. Equal-cost destinations share the group's probability in proportion to their opportunities; unallocated survival mass is returned explicitly. This is a stated Stouffer-style teaching formulation, not a calibrated competing-destinations model. See the [method note](../../../algorithms/spatial-interaction/intervening-opportunities.md).

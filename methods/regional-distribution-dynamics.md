# Regional distribution dynamics: Markov, spatial Markov and LISA transitions

Regional convergence is not a single algorithm. Distribution-dynamics analysis asks whether regions move between relative-position classes over time, whether those movements depend on neighboring conditions, and whether local spatial-association states persist or change.

## Implemented algorithms

The [Python package](../implementations/python/regional-dynamics/README.md) provides four bounded baselines.

1. **Markov transition matrix.** Pool region-period observations, assign quantile classes, count adjacent-period transitions and row-normalize. This is a first-order descriptive summary; stationarity and time homogeneity are not tested.
2. **Spatial Markov transition matrix.** Compute a row-standardized spatial lag from the continuous panel at time t, classify it using pooled quantile breaks, and estimate a separate class-transition matrix for each lag class. This conditions transition patterns on neighboring context; it does not establish spillover causality.
3. **LISA/Moran-quadrant transition matrix.** Standardize each period across regions, calculate the spatial lag of standardized values, and classify each region into HH, HL, LH or LL. Count transitions between those states. These are quadrant labels, not significance-tested local Moran clusters.
4. **Sigma-dispersion.** Report cross-sectional population standard deviation by period. A declining series is descriptive sigma-convergence, but does not by itself establish beta-convergence or explain mechanisms.

## Data and weights contract

Input is a balanced finite panel with shape `(time, regions)`. Rows of the weights matrix are regions; columns are neighbors. The implementation requires nonnegative weights, zero diagonal and at least one positive-weight neighbor per region, then row-standardizes. Quantile thresholds are pooled over all region-period observations; tied observations can reduce the effective class count. The same region ordering must be used in the panel and weights matrix.

## Interpretation and sensitivity

A transition matrix compresses temporal movement and loses within-class variation. Results can change with class count, quantile convention, sample period, region boundaries, spatial weights, row standardization and treatment of ties. A first-order Markov matrix assumes transition probabilities depend on the current state rather than the full history; time homogeneity is another substantive assumption. Report these choices and test alternatives.

The spatial Markov conditioning class is based on a lagged spatial average, not a causal treatment. LISA quadrants are descriptive; significance requires a permutation design and multiplicity strategy not implemented here. Sigma-convergence is distinct from beta-convergence, conditional convergence, spatial panel regression and distributional convergence.

## Sources

- Rey, S. J. (2001). “Spatial Empirics for Economic Growth and Convergence.” *Geographical Analysis*, 33(3), 195–214. [DOI](https://doi.org/10.1111/j.1538-4632.2001.tb00444.x). Develops spatial extensions to classical Markov transition matrices for regional income dynamics.
- Rey, S. J., & Janikas, M. V. (2005). “Regional convergence, inequality, and space.” *Journal of Economic Geography*, 5(2), 155–176. [DOI](https://doi.org/10.1093/jnlecg/lbh044). Reviews spatial dependence, heterogeneity and scale in regional convergence research.
- Anselin, L. (1995). “Local Indicators of Spatial Association—LISA.” *Geographical Analysis*, 27(2), 93–115. [DOI](https://doi.org/10.1111/j.1538-4632.1995.tb00338.x). Foundational local spatial-association framework.

No source text, figures or datasets are reproduced.

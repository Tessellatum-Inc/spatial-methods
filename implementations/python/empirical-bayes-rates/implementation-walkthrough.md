# Empirical Bayes rate smoothing — implementation walkthrough

## 1. Inputs
Each area contributes a nonnegative integer event count and a positive population or person-time exposure. The crude rate is count divided by exposure. Unequal exposure means crude rates have unequal sampling variances.

## 2. Global moment estimator
The pooled rate estimates the prior mean. A population-weighted sample variance of crude rates estimates total marginal variation. Subtracting the expected Poisson sampling component estimates between-area variance, truncated at zero. Each crude rate is shrunk toward the pooled mean with a factor that increases with exposure and prior heterogeneity.

## 3. Local moment estimator
The analyst supplies one neighbourhood index list per area, including the area itself. The same moment calculation is repeated within each local set. The focal area's rate is shrunk toward its local pooled rate. This captures adjacency only through the caller's neighbourhoods; the code does not infer polygons or contiguity.

## 4. Tests and limits
Tests verify the published moment equations, exposure-dependent shrinkage, global permutation invariance, zero-heterogeneity behaviour, zero counts, local neighbourhood behaviour and invalid input rejection. This is Marshall's moment-based global/local shrinkage baseline, not a CAR/BYM model, INLA/SPDE model or full Bayesian disease map.

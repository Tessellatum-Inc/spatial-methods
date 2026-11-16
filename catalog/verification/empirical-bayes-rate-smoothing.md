# Source verification — empirical Bayes area-rate smoothing

## Identity and bibliography
Marshall, R. J. (1991). “Mapping Disease and Mortality Rates Using Empirical Bayes Estimators.” *Journal of the Royal Statistical Society: Series C (Applied Statistics)*, 40(2), 283–294. DOI 10.2307/2347593. The publisher article identifies global moment shrinkage and a local neighbourhood variant. The maintained R package spdep documents its global Poisson estimator as following Marshall (1991), pp. 284–285.

## Technical claims
The observation model is conditionally Poisson with mean exposure times area-specific rate. The global moment method estimates the pooled mean, subtracts the Poisson sampling variance from a weighted rate variance to estimate between-area variance, truncates a negative estimate to zero, and uses the resulting best-linear-Bayes shrinkage coefficient. The local version repeats the moment calculation over analyst-defined neighbourhoods and shrinks toward the local pooled mean. Marshall notes that the global estimator is spatially invariant and the local estimator requires neighbourhood homogeneity assumptions.

## Implementation and reproduction
Implemented: global and local moment shrinkage for counts and positive exposures. Tests check equations, exposure-dependent shrinkage, area-order invariance of the global estimator, zero-variance pooling, zero counts and invalid inputs. The caller supplies local neighbourhood indices; the code does not infer adjacency.

Not implemented: Clayton–Kaldor iterative maximum likelihood, CAR/BYM, INLA/SPDE, covariates, age standardisation, posterior intervals, spatially correlated latent effects or cluster inference. Repository CI is required to establish the committed tests pass in its target environment.

## Rights
Equations are independently typeset and paraphrased. No publisher code, figures or article text is reproduced.

# Fay-Herriot implementation walkthrough

1. **Inputs.** Each area contributes a direct estimate, its known sampling
   variance and optionally a row of auxiliary covariates. An intercept-only
   design is used when covariates are omitted.
2. **Model.** The observation variance is A + D_i, where A is the
   between-area random-effect variance and D_i is the supplied sampling
   variance.
3. **REML.** For each candidate A, the implementation obtains GLS fixed
   effects and evaluates the restricted log likelihood. A bounded scalar
   search on log variance is compared with the boundary A = 0.
4. **Prediction.** The EBLUP is the regression component plus the shrunken
   direct-estimate residual. The shrinkage factor is A/(A + D_i).
5. **Uncertainty.** The plug-in MSE combines sampling and fixed-effect
   estimation terms. It does not include uncertainty in estimated A.

Tests cover a boundary fit, finite predictions and MSE, covariate recovery,
shrinkage bounds and invalid inputs. These checks do not establish that the
model is suitable for a particular survey or geographic domain.

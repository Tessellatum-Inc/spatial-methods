# Source verification — compositional data log-ratio transforms

## Identity and bibliography
- Aitchison, J. (1982). “The statistical analysis of compositional data.” *Journal of the Royal Statistical Society: Series B*, 44(2), 139–160. DOI 10.1111/j.2517-6161.1982.tb01195.x.
- Egozcue, J. J., Pawlowsky-Glahn, V., Mateu-Figueras, G. and Barceló-Vidal, C. (2003). “Isometric logratio transformations for compositional data analysis.” *Mathematical Geology*, 35(3), 279–300. DOI 10.1023/A:1023818214614.

## Technical claims
Compositional information is relative and invariant to common positive scaling. Closure maps a nonnegative vector with positive total to the unit simplex. CLR coordinates sum to zero. ILR projects log parts onto an orthonormal basis of the zero-sum subspace and preserves Aitchison geometry. ALR depends on its denominator part.

## Implementation/reproduction
Implemented: closure, CLR, ALR and inverse ALR, ILR and inverse ILR using a Helmert basis, plus Aitchison distance. Tests cover scale invariance, CLR centring, basis orthonormality, transform round trips, isometry and invalid/zero inputs.

Not implemented: zero replacement, missing-part imputation, compositional regression, compositional kriging, spatial covariance, Bayesian models or uncertainty propagation. Zero replacement is deliberately not automated because structural, rounded and censored zeros have different interpretations. Repository CI is required to establish passing status.

## Rights
Only mathematical definitions and bibliographic metadata are paraphrased; no source code or figures are reproduced.

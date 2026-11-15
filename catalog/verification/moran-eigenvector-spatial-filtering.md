# Source verification — Moran eigenvector spatial filtering

## Identity and bibliography
Griffith (2003), *Spatial Autocorrelation and Spatial Filtering*, provides the theoretical treatment. Griffith and Peres-Neto (2006) discuss eigenfunction spatial analysis. Tiefelsdorf and Griffith (2007), “Semiparametric Filtering of Spatial Autocorrelation: The Eigenvector Approach,” *Environment and Planning A*, 39(5), 1193–1221, DOI 10.1068/a37378, develops a selection procedure for eigenvector filters. The maintained spatialreg vignette documents the HWM eigenvector basis and the importance of subset selection.

## Technical claims
The intercept-centered matrix HWH produces orthogonal eigenvectors representing distinct spatial patterns. Positive eigenvalues correspond to positive spatial autocorrelation patterns. A selected subset may be added to a regression as synthetic covariates; choosing the subset is central to the method.

## Implementation and reproduction
Implemented: symmetric-weight validation, HWH construction, eigendecomposition, positive/negative eigenvector options, leading-component selection, and fixed-size OLS with caller-supplied covariates. Tests cover centering, orthonormality, ordering, OLS equivalence, nested fit, and invalid inputs.

Not implemented: automatic selection by residual Moran's I/AIC/p-values, general M_X W M_X projection, Spatial+, restricted spatial regression, GLM filters or inferential corrections. Repository CI is required to establish committed tests pass.

## Rights
Independent implementation from published definitions and maintained documentation; no external source code or figures are copied.

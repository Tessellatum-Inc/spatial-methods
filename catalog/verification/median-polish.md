# Source verification — Tukey median polish

## Identity and bibliography
Tukey (1977), *Exploratory Data Analysis*, introduces median polish. R's maintained stats::medpolish documentation describes the additive overall + row + column model, alternating removal of row and column medians, proportional reduction in absolute residual sum for convergence, and optional missing-value removal.

## Technical claims
The procedure iteratively removes row and column medians and recentres effects to identify an additive decomposition. It is robust to isolated cell outliers but does not fit interactions or spatial covariance.

## Implementation and reproduction
Implemented: two-way median polish, overall/row/column effects, residuals, optional missing-value handling, iteration history and proportional-residual-reduction convergence. Tests cover exact additive tables, the documented parachuting-deaths example, residual outliers, missing rows/columns and invalid controls.

Not implemented: weighted median polish, interactions, multiway arrays, inferential tests or spatial neighbourhood structure. Repository CI is required to establish committed tests pass.

## Rights
Independent implementation of the published algorithm; no source code or figures copied.

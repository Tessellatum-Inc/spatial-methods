# Source verification — Fay–Herriot area-level model

## Identity and bibliography
- Fay, R. E., & Herriot, R. A. (1979). “Estimates of income for small places: An application of James-Stein procedures to census data.” *Journal of the American Statistical Association*, 74(366a), 269–277. DOI 10.1080/01621459.1979.10482505.

## Technical claims
- The area-level normal-normal model separates known sampling variances from between-area random-effect variance.
- REML estimates the random-effect variance; generalized least squares estimates fixed effects.
- The EBLUP shrinks direct estimates toward the regression component by area-specific factors.

## Implementation and tests
- SciPy scalar REML optimization, full-rank fixed-effect design, EBLUP predictions and plug-in MSE approximation.
- Tests cover finite predictions, bounded shrinkage, covariate regression, zero-variance boundary and invalid inputs.

## Limits and rights
The reported plug-in MSE omits variance-component estimation uncertainty. This is the area-level model only; unit-level, spatially structured and spatiotemporal extensions are not included. Original code and explanatory text; bibliographic metadata only.

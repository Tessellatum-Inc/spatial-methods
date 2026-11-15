# Moran eigenvector filtering — implementation walkthrough

1. Validate a symmetric nonnegative spatial weights matrix with zero diagonal.
2. Construct H = I - 11'/n and center the weights as H W H.
3. Use a symmetric eigensolver; retain positive eigenvalues above tolerance and sort descending.
4. Select the requested number of leading eigenvectors.
5. Fit OLS with an intercept, supplied covariates and the selected eigenvectors.
6. Inspect coefficients, fitted values and residuals. Selection is a modelling decision; this baseline does not automatically minimize residual spatial autocorrelation.

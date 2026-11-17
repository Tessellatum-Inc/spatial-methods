# Implementation walkthrough: principal-axis factor analysis

1. Validate an observations-by-variables matrix; reject non-finite values, constant columns and undersized samples.
2. Standardize variables and form the sample correlation matrix.
3. Initialize communalities from squared multiple correlations using the Moore–Penrose inverse.
4. Replace the correlation matrix diagonal with current communalities.
5. Extract the leading eigenpairs and scale eigenvectors by square-root eigenvalues.
6. Update communalities from row-wise sums of squared loadings until tolerance or iteration cap.
7. Optionally apply varimax. Orthogonal rotation changes axes but preserves each variable's communality.
8. Inspect loadings and uniquenesses. This is exploratory principal-axis factoring, not a likelihood fit or an OAC classification.

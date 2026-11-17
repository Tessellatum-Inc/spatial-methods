# Principal component analysis

Principal component analysis (PCA) transforms correlated variables into
orthogonal linear combinations ordered by explained variance. For centered
observations X, covariance PCA solves the symmetric eigensystem of

\[
S=\frac{1}{n-1}X^\mathsf{T}X.
\]

The leading eigenvectors define the component axes; projecting observations
onto them yields component scores. Standardizing each feature before forming
the covariance matrix produces correlation PCA instead, and changes the
relative influence of variables.

The repository's NumPy implementation fits the covariance eigensystem,
orders components by descending eigenvalue, supports an optional valid-row
mask and projects data using the fitted mean and scale. It also contains a
separate caller-supplied Tasseled Cap linear transform; that is not PCA.

## Scope and limitations

PCA is sensitive to feature scaling and can be influenced by outliers.
Eigenvector signs are arbitrary. A separate [principal-axis factor-analysis baseline](factor-analysis.md) models common variance and optional varimax rotation; it is not PCA and does not implement maximum-likelihood or confirmatory factor analysis. MNF/noise whitening, robust PCA, OAC-style geodemographic classification and spatially constrained component analysis remain separate topics.

See the [tested implementation](../../implementations/python/pca-transform/README.md)
and [tests](../../implementations/python/pca-transform/test_pca_transform.py).

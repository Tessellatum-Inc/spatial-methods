# Principal component analysis (PCA) for multispectral imagery

PCA rotates a centred multiband sample cloud into orthogonal axes ordered by sample variance. In imagery, each valid pixel is a sample and each spectral band is a variable. The leading components can compress correlated bands, expose dominant variation and support visualization or downstream classification.

## Definition

For an (n\times p) matrix (X), subtract the per-band mean and form the sample covariance (S=Z^T Z/(n-1)). Solve (Sv_k=\lambda_kv_k), ordered so \(\lambda_1\ge\cdots\ge\lambda_p\ge0\). Scores are (T=ZV). Explained-variance proportions are \(\lambda_k/\sum_j\lambda_j\).

## Choices and caveats

- Covariance PCA preserves original band scales; standardizing first produces correlation PCA and may amplify low-variance/noisy bands.
- Exclude cloud, shadow, saturation and NoData pixels before fitting. The implementation also excludes rows containing non-finite values.
- Fit on a representative spatial/temporal sample if the full raster is too large, then apply the same mean, scale and loadings to every tile.
- Component signs are arbitrary. Nearly tied eigenvalues can make individual axes unstable even when their joint subspace is stable.
- PCA maximizes total variance, not signal-to-noise ratio. It is not minimum noise fraction (MNF), which requires an explicit noise covariance estimate and noise whitening.

## Complexity

For (n) pixels and (p) bands, covariance formation costs (O(np^2)), the eigensolve (O(p^3)), and projection (O(npk)) for (k) retained components. For very large images, use streaming covariance accumulation or randomized/iterative SVD.

## Implementation

See [the NumPy implementation](../../implementations/python/pca-transform/README.md). The fit returns loadings, eigenvalues, explained-variance ratios and row-validity metadata; transform applies a fitted model.

## Verification status

See [the verification ledger](../../catalog/verification/pca-transform.md).

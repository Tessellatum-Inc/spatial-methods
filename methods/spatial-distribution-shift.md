# Spatial distribution shift with block-level MMD permutations

## Maximum mean discrepancy

For distributions \(P\) and \(Q\) and a positive-definite kernel \(k\), maximum mean discrepancy (MMD) compares their kernel mean embeddings:

\[
\operatorname{MMD}^2(P,Q)=E k(X,X')+E k(Y,Y')-2E k(X,Y).
\]

The implementation uses the unbiased two-sample estimator, omitting within-group diagonal terms, and a Gaussian/RBF kernel \(k(x,y)=\exp(-\|x-y\|^2/(2h^2))\).

## Spatial block adaptation

Ordinary random permutation of individual observations is not automatically valid for spatially autocorrelated data. This implementation treats each supplied spatial block as one exchangeable unit. Each block must belong to exactly one of two groups. It computes the mean pairwise RBF similarity between every pair of blocks, calculates unbiased MMD over the block-kernel matrix, then permutes group labels across whole blocks while preserving group block counts.

This tests differences in distributions of block-level feature embeddings, not an iid point-level null. The block-level permutation construction is an explicit teaching adaptation; it is not a procedure claimed to be reproduced from Gretton et al.

## Validity is a design assumption

The test is defensible only when blocks are plausibly exchangeable under the null. Blocks should be designed to reduce dependence and should be comparable in sampling design and support. Arbitrary neighboring raster tiles are not thereby independent. Spatial trends, unequal sampling effort, edge effects, unequal support and block-size confounding can invalidate the permutation reference distribution. Consider matched or stratified designs, spatially separated sampling and sensitivity analysis.

## Scope

The implementation does not implement the full range of Gretton et al.'s asymptotic, bootstrap or distribution-free MMD thresholds. It does not select block size, prove exchangeability, correct for covariates, implement conditional MMD or supply a universal spatial permutation scheme. Automatic bandwidth is the median of positive pairwise feature distances; domain-informed bandwidth sensitivity is recommended. Computation is dense and intended for small teaching datasets.

## Reproduction

Run from implementations/python/distribution-shift:

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q --import-mode=importlib
~~~

## References

- Gretton, A., Borgwardt, K. M., Rasch, M. J., Schölkopf, B., & Smola, A. (2012). A Kernel Two-Sample Test. *Journal of Machine Learning Research*, 13, 723–773.
- Gretton, A., et al. (2009). A Fast, Consistent Kernel Two-Sample Test. *Advances in Neural Information Processing Systems*.

This lesson paraphrases the method and does not reproduce source code, figures or data.

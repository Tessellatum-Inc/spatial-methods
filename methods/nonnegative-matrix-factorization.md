# Non-negative matrix factorization

NMF approximates a non-negative data matrix \(V\in\mathbb{R}_{+}^{m\times n}\) by two non-negative factors:
\[
V\approx WH,\qquad W\in\mathbb{R}_{+}^{m\times r},\quad H\in\mathbb{R}_{+}^{r\times n}.
\]
The columns of W are basis patterns and columns of H are their non-negative coefficients. The non-negativity constraint restricts the reconstruction to additive combinations and can yield parts-based representations, but it does not guarantee interpretable or independent components.

## Euclidean multiplicative updates

The Lee–Seung Euclidean update rules are
\[
H\leftarrow H\odot\frac{W^TV}{W^TWH},\qquad
W\leftarrow W\odot\frac{VH^T}{WHH^T},
\]
where division and multiplication are elementwise. The objective is non-increasing under the stated update rules, but the joint problem is non-convex and convergence is to a stationary/local solution, not necessarily a global optimum. The scale ambiguity \(W H=(W\Lambda)(\Lambda^{-1}H)\) is often controlled by normalizing basis columns.

## Spatial-data applications and cautions

Rows may represent pixels/features and columns observations, scenes or time steps. NMF can discover additive patterns in non-negative spectral, land-cover or event-count data. It does not automatically model spatial adjacency, temporal dynamics, uncertainty or physical processes. Centered/standardized data can contain negative values and therefore violate the basic NMF contract; choose transformations carefully and retain their meaning.

The [Python implementation](../implementations/python/matrix-factorization/README.md) provides deterministic, pure-Python Euclidean updates for small matrices. It does not implement generalized-KL NMF, ICA, maximum autocorrelation factors, dictionary learning, sparse coding or compressive sensing.

## Sources

- Lee, D. D., & Seung, H. (1999). “Learning the Parts of Objects by Non-negative Matrix Factorization.” *Nature*, 401, 788–791. [DOI](https://doi.org/10.1038/44565).
- Lee, D. D., & Seung, H. S. (2001). “Algorithms for Non-negative Matrix Factorization.” *Advances in Neural Information Processing Systems 13*. [Proceedings paper](https://proceedings.neurips.cc/paper_files/paper/2000/file/f9d1152547c0bde01830b7e8bd60024c-Paper.pdf).

No source text or figures are reproduced.

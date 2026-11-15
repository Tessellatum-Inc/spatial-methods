# Source verification — non-negative matrix factorization

## Identity and bibliography
Lee & Seung (1999), Nature 401, 788–791, DOI 10.1038/44565, establishes NMF as a non-negative factorization for parts-based representations. Lee & Seung (2001), Advances in Neural Information Processing Systems 13, presents the multiplicative update algorithms for Euclidean and generalized-KL objectives.

## Technical claims checked
The implementation uses the Euclidean/Frobenius multiplicative updates, not the generalized-KL/Poisson variant. The joint objective is non-convex; alternating updates do not promise a global optimum. Non-negativity is a constraint, not a guarantee of semantic interpretability.

## Implementation and reproduction
The pure-Python implementation uses deterministic positive initialization, alternating H/W updates and W-column normalization. Tests cover a rank-one reconstruction, deterministic repeatability, non-negativity and invalid input. It is designed for small teaching matrices and does not implement ICA, MAF, dictionary learning, sparse coding or compressive sensing. Run repository tests/CI independently.

## Rights
Only bibliographic metadata and paraphrased equations are included; no source text or figures are copied.

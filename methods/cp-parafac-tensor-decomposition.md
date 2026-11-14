# CP/PARAFAC tensor decomposition by alternating least squares

A three-way tensor can be approximated as a sum of rank-one outer products:
[
X_{ijk} approx sum_{r=1}^{R} lambda_r A_{ir}B_{jr}C_{kr}.
]
The CP/PARAFAC model shares latent components across all modes. It differs from Tucker decomposition, which introduces a core tensor and mode-specific factor matrices.

## Implemented baseline

The [NumPy implementation](../implementations/python/tensor-decomposition/README.md) fits a fully observed dense three-way tensor by alternating least squares. It updates one factor matrix at a time using a mode unfolding, a Khatri–Rao product of the other factors and the pseudoinverse of the Hadamard product of their Gram matrices. It normalizes factor columns and reports relative Frobenius reconstruction error.

## Limitations

This is a small unconstrained dense teaching baseline. It does not handle missing data, sparse tensors, nonnegative or regularized factors, streaming updates, automatic rank selection, Tucker, tensor train or t-SVD. ALS can be sensitive to initialization and ill-conditioning. Factor identifiability and uniqueness require additional conditions; reconstruction quality alone does not validate interpretation. Spatial applications should consider whether the tensor modes represent meaningful axes such as location, time and variable, and whether a Euclidean low-rank model is appropriate.

## Sources

- Carroll, J. D., & Chang, J. J. (1970). “Analysis of individual differences in multidimensional scaling via an N-way generalization of ‘Eckart-Young’ decomposition.” *Psychometrika*, 35, 283–319. [DOI](https://doi.org/10.1007/BF02310791).
- Harshman, R. A. (1970). “Foundations of the PARAFAC procedure: Models and conditions for an ‘explanatory’ multi-modal factor analysis.” UCLA working paper.
- Kolda, T. G., & Bader, B. W. (2009). “Tensor Decompositions and Applications.” *SIAM Review*, 51(3), 455–500. [DOI](https://doi.org/10.1137/07070111X).

No source text, figures or datasets are reproduced.

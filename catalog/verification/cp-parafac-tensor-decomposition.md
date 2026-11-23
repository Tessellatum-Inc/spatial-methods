# Source verification — CP/PARAFAC tensor decomposition

## Identity and bibliography
- Carroll & Chang (1970), *Psychometrika* 35, 283–319, DOI 10.1007/BF02310791.
- Harshman (1970), “Foundations of the PARAFAC procedure,” UCLA working paper.
- Kolda & Bader (2009), *SIAM Review* 51(3), 455–500, DOI 10.1137/07070111X.

## Technical and implementation scope
Implemented: dense, fully observed, unconstrained three-way CP/PARAFAC via alternating least squares with factor normalization and relative Frobenius reconstruction error.

Not implemented: Tucker, tensor train, t-SVD, missing-data completion, sparse/streaming tensors, nonnegative or regularized CP, automatic rank selection, uncertainty or factor identifiability analysis.

## Reproduction
Tests are authored for rank-one reconstruction, deterministic initialization, zero tensor handling and invalid inputs. Repository CI/test status must be checked separately; test files are not evidence of passing tests.

## Rights
Bibliographic metadata and original explanatory text only. No source figures, code or datasets are reproduced.

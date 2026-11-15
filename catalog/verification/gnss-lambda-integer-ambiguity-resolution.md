# Verification record: GNSS LAMBDA integer least squares

## Identity and classification
- Implementation: implementations/python/gnss-ambiguity/lambda_ils.py
- Classification: LAMBDA integer decorrelation reduction with depth-first conditional integer search; stand-alone ILS, not an observation estimator.

## Bibliographic and technical checks
- Teunissen (1995), DOI 10.1007/BF00863419, defines the least-squares ambiguity decorrelation adjustment and its integer transformation/search formulation.
- Chang, Yang & Zhou (2005), DOI 10.1007/s00190-005-0004-x, describes MLAMBDA search improvements.
- The implementation follows the documented LAMBDA covariance factorisation, integer Gauss transforms, permutations and transformed-space search structure. RTKLIB's public lambda.c provides a cross-check of the reduction/search identities; this implementation is independently written.
- Tests check integer-unimodular transformation, Qz = Z.T @ Q @ Z, Qz = L.T @ diag(D) @ L, original-space objective preservation and best-two agreement with exhaustive enumeration on small correlated cases.

## Reproduction and rights
- NumPy-only implementation and deterministic synthetic tests.
- No RTKLIB source, code or data is redistributed.
- Ratio is descriptive; no universal fix/float decision threshold is claimed.
- Repository CI status is tracked separately from these mathematical checks.

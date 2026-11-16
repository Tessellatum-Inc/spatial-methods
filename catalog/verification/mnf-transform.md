# Verification ledger — Minimum Noise Fraction

- **Source inventory:** Section 5, source page 8; exact source-to-code trace remains pending.
- **Implementation:** `implementations/python/mnf-transform/`
- **Tests:** supplied covariance ordering, masked pixels, adjacent-difference covariance and rejection of indefinite noise covariance.
- **Verification state:** implementation and tests committed; test execution and independent generalized-eigenproblem comparison not yet recorded.
- **Scope:** noise whitening, signal covariance eigendecomposition, descending components and optional adjacent-difference noise estimation.
- **Limits:** noise stationarity/independence assumptions; no sensor-specific noise model or MNF denoising policy.
- **Next:** execute tests; compare loadings/eigenvalues against an independent generalized symmetric eigensolver; test singular and ill-conditioned covariance cases.

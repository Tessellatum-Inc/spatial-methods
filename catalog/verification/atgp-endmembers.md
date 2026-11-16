# Verification ledger — ATGP

- **Source:** Section 5 hyperspectral endmember extraction, source page 8; line-by-line source trace pending.
- **Code:** `implementations/python/atgp-endmembers/`
- **Tests authored:** distinct selected pixels, output shape and mask exclusion.
- **Execution:** not yet recorded.
- **Scope:** iterative maximum residual-energy selection with orthogonal projection.
- **Limitations:** candidate generation only; no noise model, semantic labelling or physical-purity guarantee.
- **Next verification:** run tests; compare projections to independent QR/SVD reference calculations and test rank-deficient signatures.

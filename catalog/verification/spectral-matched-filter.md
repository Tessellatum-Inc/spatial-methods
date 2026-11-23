# Verification ledger — Spectral matched filter

- **Source inventory:** Section 5, hyperspectral target detection, source page 8; source-to-code trace remains pending.
- **Implementation:** `implementations/python/spectral-matched-filter/`
- **Tests:** injected target response, background mask, output dimensions and degenerate target rejection.
- **Verification state:** implementation and tests committed; test execution and independent covariance-weighted formula comparison not recorded.
- **Scope:** global adaptive matched filter with supplied or empirical background covariance.
- **Limits:** one global background distribution; no local filter, ACE, CEM or matched-subspace detector.
- **Next:** execute tests; compare scores with direct linear solves and test target/background contamination and covariance conditioning.

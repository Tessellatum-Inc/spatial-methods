# Verification ledger — Vertex Component Analysis

- **Source inventory:** Section 5, hyperspectral analysis, source page 8; source-to-code trace remains pending.
- **Implementation:** `implementations/python/vca-endmembers/`
- **Tests:** deterministic seeded extraction, selected-pixel index validity, mask exclusion and one-endmember edge case.
- **Verification state:** implementation and tests committed; test execution and independent synthetic-mixture recovery assessment not recorded.
- **Scope:** SVD signal-subspace projection and seeded vertex selection from observed pixel spectra.
- **Limits:** pure-pixel assumption; simplified reproducible baseline, not every canonical/noise-aware VCA variant.
- **Next:** execute tests; compare recovered vertices on controlled pure-pixel simplices; quantify sensitivity to noise, endmember count and seed.

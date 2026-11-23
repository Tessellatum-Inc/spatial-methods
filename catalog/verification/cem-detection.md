# Verification ledger — CEM

- **Source:** Section 5 hyperspectral target detection, source page 8; line-by-line source trace pending.
- **Code:** `implementations/python/cem-detection/`
- **Tests authored:** unit target response, injected-target score, indefinite matrix rejection.
- **Execution:** not yet recorded.
- **Scope:** global uncentred correlation-matrix CEM with eigenvalue flooring.
- **Limitations:** global background second moment; no local or subspace CEM variant; scores are not probabilities.
- **Next verification:** run tests; compare weights with direct linear-system solutions and check singular-matrix regularisation sensitivity.

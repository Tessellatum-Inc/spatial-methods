# Verification ledger — N-FINDR

- **Source:** Section 5 hyperspectral endmember extraction, source page 8; line-by-line source trace pending.
- **Code:** `implementations/python/nfindr-endmembers/`
- **Tests authored:** pure-pixel synthetic simplex fixture, unique selections, output shape, mask exclusion.
- **Execution:** not yet recorded.
- **Scope:** SVD subspace projection and iterative determinant-volume vertex replacement.
- **Limitations:** direct candidate scanning is expensive; seed and iteration count affect result; pure-pixel assumption.
- **Next verification:** run tests; compare determinant against exhaustive combinations on small synthetic scenes; assess convergence and seed sensitivity.

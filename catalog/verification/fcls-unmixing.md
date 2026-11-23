# Verification ledger — Fully Constrained Least Squares

- **Source inventory:** Section 5, hyperspectral analysis, source page 8; source-to-code trace remains pending.
- **Implementation:** `implementations/python/fcls-unmixing/`
- **Tests:** noise-free synthetic mixtures, nonnegative and sum-to-one constraints, abundance recovery and single-endmember case.
- **Verification state:** implementation and tests committed; test execution and independent constrained-QP oracle comparison not recorded.
- **Scope:** per-pixel linear unmixing with nonnegative abundances and sum-to-one equality constraint.
- **Limits:** SLSQP numerical solver; no spatial regularisation or shade/unmodelled-material model.
- **Next:** execute tests; compare against exhaustive active-set solutions on small endmember counts; record solver failures and residual distributions.

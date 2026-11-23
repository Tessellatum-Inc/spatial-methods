# Verification ledger — Global RX anomaly detector

- **Source inventory:** Section 5, source page 8; source-to-code mapping pending.
- **Implementation:** `implementations/python/rx-anomaly/`
- **Tests:** injected spectral outlier, masked background positions and rejection of indefinite covariance.
- **Verification state:** implementation and tests committed; execution and independent Mahalanobis-distance comparison not recorded.
- **Scope:** global Gaussian-background RX with empirical or supplied covariance and eigenvalue regularisation.
- **Limits:** no local/kernel/subspace RX or calibrated false-alarm threshold.
- **Next:** execute tests; compare scores to a direct solve-based Mahalanobis oracle; test background contamination and heterogeneous backgrounds.

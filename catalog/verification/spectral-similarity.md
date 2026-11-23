# Verification ledger — SAM and SID

- **Source inventory:** Section 5, source page 8; source-to-code mapping pending.
- **Implementation:** `implementations/python/spectral-similarity/`
- **Tests:** orthogonal and identical spectra, SID identity/symmetry, map shapes, zero norms and negative-input rejection.
- **Verification state:** implementation and tests committed; execution and independent reference comparison not recorded.
- **Scope:** Spectral Angle Mapper in radians and symmetric Spectral Information Divergence.
- **Limits:** no bad-band handling, spectral resampling, endmember extraction or atmospheric correction.
- **Next:** execute tests; compare against independent formulas and evaluate numerical behaviour near zero-valued spectra.

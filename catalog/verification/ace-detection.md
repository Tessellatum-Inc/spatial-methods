# Verification ledger — ACE

- **Source:** Section 5 hyperspectral target detection, source page 8; line-by-line source trace pending.
- **Code:** `implementations/python/ace-detection/`
- **Tests authored:** bounded scores, injected-target response and degenerate-target rejection.
- **Execution:** not yet recorded.
- **Scope:** global covariance-whitened squared cosine target detector.
- **Limitations:** one global background distribution; no local covariance or calibrated false-alarm model.
- **Next verification:** run tests; compare against explicit whitening/cosine calculation and assess covariance conditioning.

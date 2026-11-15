# Spectral matched filter

Install requirements and run `pytest -q`. This global adaptive matched filter estimates a background mean and covariance, then scores pixels against a known target signature using the covariance-whitened target contrast. A background mask or supplied covariance may be used. Scores are normalized so a perfect target contrast has unit response under the model.

This is the global adaptive matched filter baseline, not the matched subspace detector, constrained energy minimisation (CEM), adaptive coherence estimator (ACE), or local matched filter. It assumes one representative background distribution and a known target spectrum in the same band space and radiometric domain. Scores are not automatically calibrated probabilities; select thresholds using a representative background and desired false-alarm rate.

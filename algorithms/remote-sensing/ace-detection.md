# Adaptive Coherence Estimator (ACE)

ACE measures squared cosine similarity between each mean-centred pixel and a target contrast vector in a background-covariance-whitened spectral space. The global implementation returns scores bounded to [0, 1], subject to numerical precision.

It assumes a representative global background covariance and a target signature in the same band and radiometric space. ACE scores are not automatically false-alarm probabilities. Thresholds require representative background calibration.

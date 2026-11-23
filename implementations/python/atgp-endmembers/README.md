# Automatic Target Generation Process (ATGP)

Run `pytest -q`. ATGP selects a high-energy pixel first, then repeatedly selects the pixel with greatest residual energy after orthogonal projection away from the span of already selected signatures. It returns observed spectra and flattened pixel indices.

This is an unsupervised candidate-signature extraction baseline, not a semantic target classifier. Selected signatures may be redundant or represent noise/outliers; the method does not guarantee physically meaningful endmembers. It uses a global Euclidean geometry and has no spatial or sensor-noise model.

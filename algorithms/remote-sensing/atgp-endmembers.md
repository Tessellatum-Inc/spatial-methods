# Automatic Target Generation Process (ATGP)

ATGP selects candidate spectral signatures iteratively. It starts with a high-energy pixel and then selects pixels with maximum energy remaining after projection away from the span of already selected signatures.

The reference implementation returns observed candidate spectra and source pixel indices. ATGP is an unsupervised candidate-generation method, not a semantic classifier; outliers and noise can be selected. It uses a global Euclidean geometry without a sensor-noise model.

# Vertex Component Analysis (VCA)

Install requirements and run `pytest -q`. Input is a finite rows × columns × bands cube. The reference implementation estimates a leading signal subspace with SVD and selects observed pixel spectra using seeded random directions and orthogonalisation. It returns endmember spectra and their flattened pixel indices.

This is an educational, reproducible VCA baseline, not a complete reproduction of every published VCA variant or noise-aware mode. VCA assumes a linear mixture model and the presence of sufficiently pure pixels (the pure-pixel assumption). It does not estimate abundances or guarantee that every selected pixel is a physically pure endmember. Validate extracted spectra against field/library signatures and assess sensitivity to endmember count, noise and preprocessing.

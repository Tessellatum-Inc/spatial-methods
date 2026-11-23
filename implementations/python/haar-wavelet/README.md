# 2-D Haar wavelet transform

Install requirements and run `pytest -q`. The implementation performs orthonormal, critically sampled 2-D Haar decomposition into approximation (LL) and horizontal, vertical and diagonal detail subbands, recursively decomposing LL. The inverse reconstructs the original array to floating-point precision.

Each level requires even dimensions; no implicit padding or boundary extension is performed. This is the Haar/Daubechies-1 wavelet only, not a general wavelet toolbox. Coefficient orientation is defined by the equations in the source. Thresholding, denoising and wavelet packet decompositions are not included.

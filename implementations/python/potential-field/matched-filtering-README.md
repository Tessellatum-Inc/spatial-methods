# Potential-field matched bandpass decomposition

The matched_bandpass_decomposition function separates a regular grid into equivalent-layer components using a supplied radial spectral model. For each layer, the model amplitude is B * k^n * exp(-k*z); the transfer function is that layer's amplitude divided by the sum across layers.

The caller supplies positive B, non-negative depth z and n in {-1, 0, 1}. The implementation does not estimate layer parameters from the observed spectrum. It uses radians per coordinate unit, a regular-grid 2D FFT and a documented DC convention: the mean is assigned to the selected dc_layer.

This is an amplitude matched-bandpass teaching baseline. The companion `radial_spectrum.py` adds annular mean-amplitude spectra and a bounded single-layer log-linear fit for `log(A)=log(B)+n*log(k)-z*k`; it selects `n` from {-1, 0, 1} and reports fit diagnostics. It does not estimate a multi-layer model. Nonlinear multi-layer refinement, automatic layer-count selection, azimuthal filtering, windowing and physical interpretation remain open. See matched-filtering-walkthrough.md, radial-spectrum tests and the synthetic lab.

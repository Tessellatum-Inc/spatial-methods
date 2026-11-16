# Fourier transforms and frequency filtering

Run `pip install -r requirements.txt` and `pytest -q`. The NumPy implementation computes a centered 2-D FFT and inverse, plus ideal, Gaussian and Butterworth radial low/high/band-pass transfer functions. Cutoffs are in cycles per pixel.

This is a foundational frequency-domain implementation, not a complete image-restoration system. It does not estimate a degradation model, perform notch filtering, handle geospatial NoData masks, or address boundary discontinuities beyond the periodic extension inherent in the DFT. Window/taper the image when edge seams dominate. Real output is appropriate for real-valued input and real symmetric transfer functions.

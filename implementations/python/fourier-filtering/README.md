# Fourier transforms and frequency filtering

Example: `destripe_periodic(image, centers=[(0.0, 0.125)], radius=0.01)` targets a vertical stripe component at 0.125 cycles/pixel across columns. Frequencies are in cycles/pixel and the notch is paired with its conjugate to preserve a real-valued inverse transform.

Run `pip install -r requirements.txt` and `pytest -q`. The NumPy implementation computes a centered 2-D FFT and inverse, plus ideal, Gaussian and Butterworth radial low/high/band-pass transfer functions. Cutoffs are in cycles per pixel.

The package also provides user-guided conjugate-symmetric Gaussian/ideal notch rejection and a `destripe_periodic` helper for attenuating known periodic stripe frequencies. The caller must identify the frequency peaks (for example, from a log-magnitude spectrum); automatic peak detection and a complete sensor-specific degradation model are not included. It does not handle geospatial NoData masks or remove boundary discontinuities beyond the periodic extension inherent in the DFT. Window/taper the image when edge seams dominate. Real output is appropriate for real-valued input and real symmetric transfer functions.

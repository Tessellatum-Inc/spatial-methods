# Discrete Radon transform

Install requirements and run `pytest -q`. The sinogram contains approximate line integrals for supplied angles (degrees) and regularly spaced signed offsets rho. The line convention is x cos(theta) + y sin(theta) = rho, with image-centred coordinates. Bilinear interpolation samples each line at unit pixel intervals.

This is a direct educational reference implementation, not a fast FFT-based filtered back-projection pipeline. It does not implement inverse Radon reconstruction, detector geometry calibration or statistical corrections. The `circle` option masks samples outside the inscribed circle for square images. Sampling, interpolation and finite support create discretisation error.

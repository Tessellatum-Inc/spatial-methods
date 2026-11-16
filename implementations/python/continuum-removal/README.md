# Spectral continuum removal

NumPy implementation of upper-convex-hull continuum removal for reflectance spectra. The final axis is spectral band; leading axes identify independent spectra. Wavelengths must be strictly increasing and reflectance non-negative.

Returns the piecewise-linear continuum, continuum-removed ratio, absorption depth (1 - ratio), and integrated absorption area. This is a geometric preprocessing baseline; it does not identify mineral species, choose diagnostic wavelength windows, or calibrate sensor response.

Run pytest -q after installing requirements.

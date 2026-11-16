# Spectral continuum removal and absorption features

Continuum removal normalizes an absorption spectrum against a local or global continuum. This reference implementation constructs the upper convex hull of each spectrum in wavelength–reflectance space, linearly interpolates between hull vertices, and divides the original spectrum by that continuum.

It returns the continuum-removed reflectance, absorption depth (one minus the ratio), and wavelength-integrated absorption area. The implementation accepts multiple spectra in one array and requires strictly increasing wavelengths. It is intended as a transparent baseline for hyperspectral feature analysis, not as a mineral classifier or a complete absorption-feature workflow. Diagnostic feature windows, band-center fitting, sensor spectral-response functions and uncertainty propagation remain analyst responsibilities.

# Spectral similarity: SAM and SID

Install requirements and run `pytest -q`. Spectral Angle Mapper compares the angle between spectra and is invariant to positive multiplicative brightness scaling. Spectral Information Divergence treats nonnegative band values as normalized distributions and measures symmetric divergence. Both scalar/vector operations and cube-to-reference maps are included.

SAM returns radians. Zero-norm spectra produce NaN by default (or zero when explicitly requested). SID requires nonnegative inputs and adds a small epsilon before normalization; document whether values are reflectance, radiance or another nonnegative representation. Neither method automatically handles bad bands, atmospheric correction, band resampling or endmember selection.

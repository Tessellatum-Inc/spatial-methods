# Spectral Angle Mapper and Spectral Information Divergence

## Purpose

Spectral similarity methods compare an observed pixel spectrum with a reference or endmember. SAM measures angular separation and is insensitive to positive brightness scaling; SID compares normalized spectral distributions through a symmetric information divergence.

## Implemented scope

The NumPy implementation provides scalar/vector metrics and cube-to-reference maps. SAM returns radians and explicitly handles zero-norm spectra. SID requires nonnegative inputs and uses an explicit epsilon. See [implementation](../../implementations/python/spectral-similarity/README.md).

## Cautions

Band alignment, bad-band removal, atmospheric correction and endmember selection must be handled before comparison. SID depends on the interpretation and scaling of nonnegative spectral values; it is not interchangeable with SAM.

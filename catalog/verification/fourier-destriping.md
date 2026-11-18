# Verification — user-guided Fourier notch destriping

**Implementation:** [Fourier filtering package](../../implementations/python/fourier-filtering/README.md)  
**Lesson:** [Fourier transforms and frequency-domain filtering](../../algorithms/remote-sensing/fourier-filtering.md)

## Verified scope

- A centered 2-D frequency grid in cycles per pixel.
- User-specified notch centres paired with conjugate-frequency locations.
- Gaussian and ideal notch-reject transfer functions.
- Periodic stripe attenuation using a caller-supplied frequency peak and radius.
- Conjugate symmetry of the transfer function and preservation of the DC component.

## Synthetic checks

A seeded-free deterministic synthetic scene combines a smooth planar background with a known vertical sinusoidal stripe. The test checks reconstruction error after targeting the known frequency. Additional tests check conjugate symmetry, notch locations, DC preservation and invalid parameter rejection.

## Limits

This is a user-guided frequency-domain baseline, not an automatic destriping pipeline. It does not detect stripe peaks, distinguish stripe artefacts from real periodic scene content, estimate a sensor degradation model, mask geospatial NoData, or guarantee edge preservation. The DFT assumes periodic extension; windowing may reduce leakage but changes border pixels. Wavelet destriping, hyperspectral band-dependent handling and independent real-scene validation remain open.

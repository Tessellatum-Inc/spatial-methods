# Vertex Component Analysis (VCA)

## Purpose

VCA extracts candidate endmember spectra from hyperspectral imagery under a linear mixture model and the pure-pixel assumption.

## Implemented scope

The NumPy reference estimates a signal subspace and uses seeded projection directions to select observed pixel spectra. It returns spectra and source pixel indices. See [implementation](../../implementations/python/vca-endmembers/README.md).

## Limitations

The pure-pixel assumption may fail in real scenes. Results depend on endmember count, noise, preprocessing and random directions. This implementation is a reproducible educational baseline, not a claim of exact equivalence to every published VCA variant.

# Pixel Purity Index (PPI)

The Pixel Purity Index is a stochastic candidate-endmember screening method for hyperspectral imagery. For each random direction in spectral space, pixel spectra are projected onto that direction and the minimum and maximum projections receive votes. Repeating this process produces a vote count intended to highlight spectrally extreme pixels.

For a centred spectrum vector x_i and random unit vector r_j, the projection is p_ij = x_i^T r_j. Each projection increments the scores of the minimum- and maximum-projection pixels. The implementation uses seeded Gaussian directions, normalized to unit length, and stable row-major tie ordering.

The method is useful for narrowing a large image to a smaller candidate set before expert review, VCA/N-FINDR extraction or constrained unmixing. It is not a classifier, does not estimate abundance, and does not guarantee that selected pixels are physically pure. Results depend on projection count, spectral preprocessing, noise and the population of valid pixels. The reference implementation accepts a boolean mask and returns a score raster with -1 for excluded cells.

# Brovey pan-sharpening

The Brovey transform injects a high-resolution panchromatic image into
co-registered multispectral bands by scaling each spectral band with a
common per-pixel factor. For N bands:

    output_i = input_i * PAN * N / sum(input bands)

The common scale preserves the input per-pixel band ratios, but can alter
radiometric range and spectral interpretation. The implementation returns
None at pixels with missing inputs or a zero multispectral sum, and does not
clip the result.

The method assumes that the PAN image and all multispectral bands have
already been aligned and resampled to the same grid. It does not implement
IHS, Gram-Schmidt, wavelet, Bayesian, spatiotemporal or learned fusion, nor
does it compensate for sensor point-spread functions or modulation transfer
functions. See the Python reference package for code and tests.

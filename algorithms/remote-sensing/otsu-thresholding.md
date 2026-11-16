# Otsu thresholding

Stable ID: `SA-RS-OTSU` · Draft 0.1 · Source compendium section 5, page 8

## Purpose

Otsu's method divides a scalar image into two classes by maximising weighted
between-class variance:

    sigma_B^2 = omega_0 omega_1 (mu_0 - mu_1)^2

Here omega denotes class proportion and mu denotes class mean. The method
selects an intensity split; it does not identify the semantic meaning of
either class.

## Implementation

The [NumPy implementation](../../implementations/python/otsu-thresholding/README.md)
sorts unique observed values and evaluates every possible split. It returns
the midpoint between adjacent levels around the best split, choosing the
first split in a tie. Non-finite and masked pixels are excluded. The
binarizer defines foreground as intensity strictly greater than the threshold.

## Assumptions and failure modes

- A single global two-class partition must be meaningful.
- Shadows, illumination gradients, noise and overlapping class distributions
  can defeat the global histogram assumption.
- Otsu does not replace radiometric correction, cloud masking, calibration or
  validation against reference labels.
- Multi-level and adaptive/local thresholding are separate methods.

## Exercises

1. Construct a bimodal array and calculate its threshold.
2. Compare the threshold before and after adding a constant to every pixel.
3. Explain why a global threshold may fail across sunlit and shadowed areas.

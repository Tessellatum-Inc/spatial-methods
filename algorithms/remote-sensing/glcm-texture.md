# Gray-level co-occurrence matrix (GLCM) texture

A GLCM counts how often a pixel with quantized gray level (i) occurs at a specified displacement from a pixel with level (j). It captures second-order spatial texture, unlike single-pixel spectral indices.

## Method

Quantize valid image values into (L) levels, choose an offset ((\Delta r,\Delta c)), and count valid pixel pairs. Symmetrization adds the transpose; normalization divides by total pair count. Common features include contrast, dissimilarity, homogeneity, angular second moment (ASM), energy and correlation.

## Feature definitions

With normalized matrix (P), levels (i,j\in\{0,\ldots,L-1\}):
- Contrast: \(\sum_{ij}P_{ij}(i-j)^2\)
- Dissimilarity: \(\sum_{ij}P_{ij}|i-j|\)
- Homogeneity: \(\sum_{ij}P_{ij}/(1+(i-j)^2)\)
- ASM: \(\sum_{ij}P_{ij}^2\); energy is its square root.
- Correlation: covariance of the two marginal level variables divided by their standard deviations.

## Practical cautions

Quantization range, number of levels, offset, direction aggregation, symmetry, window size and edge handling all affect the result. Use a fixed radiometric range for temporal comparisons; independently stretching each scene changes the meaning of gray levels. GLCM features are not scale-free and can be computationally expensive for large windows and many levels.

## Implementation and scope

See [the NumPy implementation](../../implementations/python/glcm-texture/README.md). It computes offset-specific matrices and features; it does not yet provide a moving-window raster feature stack or all 14 classic Haralick statistics.

## Verification status

See [the verification ledger](../../catalog/verification/glcm-texture.md).

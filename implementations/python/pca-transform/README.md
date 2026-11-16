# PCA transform

A NumPy PCA baseline for multiband imagery represented as a matrix of pixels by bands. It centres bands, optionally standardizes them, solves the symmetric sample covariance eigensystem, and projects rows into descending-variance component space.

```python
from pca_transform import fit_pca, transform_pca
model = fit_pca(pixel_by_band, n_components=3, mask=valid_pixels)
pc_scores = transform_pca(pixel_by_band, model)
```

Rows containing non-finite values are excluded during fitting; the optional mask is an additional boolean row filter. Projection does not silently mask invalid rows, so callers should apply their own output mask. Eigenvector signs are arbitrary. PCA is not MNF: it does not estimate or whiten a noise covariance. Standardization changes the analysis from covariance PCA to correlation PCA and should be chosen deliberately.

Run tests with `pytest -q` from this directory.


## Tasseled Cap transform

The same package applies a caller-supplied sensor-specific coefficient matrix to pixel-by-band data, optionally subtracting a per-band offset first. Supply a matrix with shape (bands, components); the common first components are brightness, greenness and wetness, but band order, coefficients and scaling depend on sensor and product. The implementation deliberately does not silently reuse Landsat coefficients for Sentinel or another sensor. The transform is a linear projection, not PCA fitted from the current image.

"""Principal component analysis for multiband raster arrays (pixels x bands)."""
from __future__ import annotations
import numpy as np

def fit_pca(data, n_components=None, *, mask=None, standardize=False):
    """Fit PCA to a (samples, bands) array, ignoring invalid/masked rows.

    Returns a dictionary containing mean, scale, eigenvalues, eigenvectors,
    explained_variance_ratio, and the fitted-row mask. Eigenvectors are columns,
    ordered by descending eigenvalue; their signs are not uniquely determined.
    """
    x = np.asarray(data, dtype=float)
    if x.ndim != 2 or x.shape[0] < 2 or x.shape[1] < 1:
        raise ValueError("data must be a 2-D (samples, bands) array with >=2 rows")
    valid = np.all(np.isfinite(x), axis=1)
    if mask is not None:
        m = np.asarray(mask)
        if m.shape != (x.shape[0],) or m.dtype != np.bool_:
            raise ValueError("mask must be a boolean vector with one value per sample")
        valid &= m
    if valid.sum() < 2:
        raise ValueError("at least two valid samples are required")
    xv = x[valid]
    mean = xv.mean(axis=0)
    scale = xv.std(axis=0, ddof=1) if standardize else np.ones(x.shape[1])
    if np.any(scale <= np.finfo(float).eps):
        raise ValueError("cannot standardize a constant band")
    z = (xv - mean) / scale
    cov = (z.T @ z) / (len(z) - 1)
    vals, vecs = np.linalg.eigh(cov)
    order = np.argsort(vals)[::-1]
    vals, vecs = np.maximum(vals[order], 0.0), vecs[:, order]
    total = vals.sum()
    ratios = vals / total if total > 0 else np.zeros_like(vals)
    k = x.shape[1] if n_components is None else n_components
    if not isinstance(k, (int, np.integer)) or isinstance(k, (bool, np.bool_)) or not 1 <= k <= x.shape[1]:
        raise ValueError("n_components must be an integer from 1 through number of bands")
    return {"mean": mean, "scale": scale, "eigenvalues": vals[:k],
            "components": vecs[:, :k], "explained_variance_ratio": ratios[:k],
            "valid_rows": valid, "n_components": k}

def transform_pca(data, model):
    """Project samples onto the component columns returned by fit_pca."""
    x = np.asarray(data, dtype=float)
    if x.ndim != 2 or x.shape[1] != len(model["mean"]):
        raise ValueError("data band count does not match fitted PCA model")
    return ((x - model["mean"]) / model["scale"]) @ model["components"]


def tasseled_cap_transform(data, coefficients, *, offset=None):
    """Apply a sensor-specific Tasseled Cap linear transform.

    Data is (samples, bands); coefficients are (bands, components), with
    columns commonly representing brightness, greenness and wetness. Optional
    offset is a per-band vector subtracted before projection. Coefficients
    must be supplied for the sensor/product and reflectance convention in use;
    no cross-sensor universal matrix is assumed.
    """
    x = np.asarray(data, dtype=float)
    matrix = np.asarray(coefficients, dtype=float)
    if x.ndim != 2 or x.shape[0] < 1 or x.shape[1] < 1 or not np.all(np.isfinite(x)):
        raise ValueError("data must be a finite non-empty (samples, bands) matrix")
    if matrix.ndim != 2 or matrix.shape[0] != x.shape[1] or matrix.shape[1] < 1 or not np.all(np.isfinite(matrix)):
        raise ValueError("coefficients must be finite (bands, components) matching data bands")
    if offset is None:
        bias = np.zeros(x.shape[1])
    else:
        bias = np.asarray(offset, dtype=float)
        if bias.shape != (x.shape[1],) or not np.all(np.isfinite(bias)):
            raise ValueError("offset must be a finite vector with one value per band")
    return (x - bias) @ matrix

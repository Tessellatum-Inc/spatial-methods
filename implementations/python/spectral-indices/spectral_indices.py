"""Spectral indices with explicit validity and NoData handling."""
import numpy as np


def _ratio_index(a, b, *, nodata=None, valid_mask=None):
    a, b = np.asarray(a, dtype=np.float64), np.asarray(b, dtype=np.float64)
    if a.shape != b.shape:
        raise ValueError("band arrays must have the same shape")
    valid = np.isfinite(a) & np.isfinite(b)
    if valid_mask is not None:
        mask = np.asarray(valid_mask)
        if mask.shape != a.shape:
            raise ValueError("valid_mask must have the same shape as bands")
        if mask.dtype != np.bool_:
            raise TypeError("valid_mask must be boolean")
        valid &= mask
    if nodata is not None:
        valid &= (a != nodata) & (b != nodata)
    denominator = a + b
    valid &= denominator != 0
    out = np.full(a.shape, np.nan, dtype=np.float64)
    np.divide(a - b, denominator, out=out, where=valid)
    return out


def ndvi(nir, red, *, nodata=None, valid_mask=None):
    """NDVI = (NIR - red) / (NIR + red)."""
    return _ratio_index(nir, red, nodata=nodata, valid_mask=valid_mask)


def ndre(nir, red_edge, *, nodata=None, valid_mask=None):
    """Normalized difference red-edge index: (NIR - red-edge)/(NIR + red-edge)."""
    return _ratio_index(nir, red_edge, nodata=nodata, valid_mask=valid_mask)


def ndmi(nir, swir1, *, nodata=None, valid_mask=None):
    """Normalized difference moisture index: (NIR - SWIR1)/(NIR + SWIR1)."""
    return _ratio_index(nir, swir1, nodata=nodata, valid_mask=valid_mask)


def lswi(nir, swir1, *, nodata=None, valid_mask=None):
    """Land surface water index, using the common NIR/SWIR1 formulation."""
    return _ratio_index(nir, swir1, nodata=nodata, valid_mask=valid_mask)


def ndwi(green, nir, *, nodata=None, valid_mask=None):
    """McFeeters open-water NDWI: (green - NIR)/(green + NIR)."""
    return _ratio_index(green, nir, nodata=nodata, valid_mask=valid_mask)


def mndwi(green, swir1, *, nodata=None, valid_mask=None):
    """Xu modified NDWI: (green - SWIR1)/(green + SWIR1)."""
    return _ratio_index(green, swir1, nodata=nodata, valid_mask=valid_mask)


def ndbi(swir1, nir, *, nodata=None, valid_mask=None):
    """Normalized difference built-up index: (SWIR1 - NIR)/(SWIR1 + NIR)."""
    return _ratio_index(swir1, nir, nodata=nodata, valid_mask=valid_mask)


def nbr(nir, swir2, *, nodata=None, valid_mask=None):
    """Normalized burn ratio: (NIR - SWIR2)/(NIR + SWIR2)."""
    return _ratio_index(nir, swir2, nodata=nodata, valid_mask=valid_mask)


def ndsi(green, swir1, *, nodata=None, valid_mask=None):
    """Common snow NDSI formulation: (green - SWIR1)/(green + SWIR1)."""
    return _ratio_index(green, swir1, nodata=nodata, valid_mask=valid_mask)


def savi(nir, red, *, soil_factor=0.5, nodata=None, valid_mask=None):
    """Soil-adjusted vegetation index with caller-selected L (default 0.5)."""
    nir, red = np.asarray(nir, dtype=float), np.asarray(red, dtype=float)
    if nir.shape != red.shape:
        raise ValueError("band arrays must have the same shape")
    if not np.isfinite(soil_factor) or soil_factor < 0:
        raise ValueError("soil_factor must be finite and non-negative")
    valid = np.isfinite(nir) & np.isfinite(red)
    if valid_mask is not None:
        mask = np.asarray(valid_mask)
        if mask.shape != nir.shape:
            raise ValueError("valid_mask must have the same shape as bands")
        if mask.dtype != np.bool_:
            raise TypeError("valid_mask must be boolean")
        valid &= mask
    if nodata is not None:
        valid &= (nir != nodata) & (red != nodata)
    denominator = nir + red + soil_factor
    valid &= denominator != 0
    out = np.full(nir.shape, np.nan)
    np.divide((1 + soil_factor) * (nir - red), denominator, out=out, where=valid)
    return out


def evi(nir, red, blue, *, nodata=None, valid_mask=None):
    """Enhanced vegetation index: 2.5*(NIR-red)/(NIR+6red-7.5blue+1)."""
    nir, red, blue = (np.asarray(x, dtype=float) for x in (nir, red, blue))
    if nir.shape != red.shape or nir.shape != blue.shape:
        raise ValueError("band arrays must have the same shape")
    valid = np.isfinite(nir) & np.isfinite(red) & np.isfinite(blue)
    if valid_mask is not None:
        mask = np.asarray(valid_mask)
        if mask.shape != nir.shape:
            raise ValueError("valid_mask must have the same shape as bands")
        if mask.dtype != np.bool_:
            raise TypeError("valid_mask must be boolean")
        valid &= mask
    if nodata is not None:
        valid &= (nir != nodata) & (red != nodata) & (blue != nodata)
    denominator = nir + 6 * red - 7.5 * blue + 1
    valid &= denominator != 0
    out = np.full(nir.shape, np.nan)
    np.divide(2.5 * (nir - red), denominator, out=out, where=valid)
    return out


def dnbr(pre_fire_nbr, post_fire_nbr):
    """Differenced NBR = pre-fire NBR minus post-fire NBR."""
    pre, post = np.asarray(pre_fire_nbr, dtype=float), np.asarray(post_fire_nbr, dtype=float)
    if pre.shape != post.shape:
        raise ValueError("NBR arrays must have the same shape")
    return np.where(np.isfinite(pre) & np.isfinite(post), pre - post, np.nan)


def awei_sh(blue, green, nir, swir1, swir2, *, nodata=None, valid_mask=None):
    """AWEI shadow variant: B + 2.5G - 1.5(NIR+SWIR1) - 0.25SWIR2."""
    bands = [np.asarray(x, dtype=float) for x in (blue, green, nir, swir1, swir2)]
    if any(x.shape != bands[0].shape for x in bands[1:]):
        raise ValueError("band arrays must have the same shape")
    valid = np.logical_and.reduce([np.isfinite(x) for x in bands])
    if valid_mask is not None:
        mask = np.asarray(valid_mask)
        if mask.shape != bands[0].shape:
            raise ValueError("valid_mask must have the same shape as bands")
        if mask.dtype != np.bool_:
            raise TypeError("valid_mask must be boolean")
        valid &= mask
    if nodata is not None:
        valid &= np.logical_and.reduce([x != nodata for x in bands])
    b, g, n, s1, s2 = bands
    result = b + 2.5*g - 1.5*(n+s1) - 0.25*s2
    return np.where(valid, result, np.nan)


def awei_nsh(green, nir, swir1, swir2, *, nodata=None, valid_mask=None):
    """AWEI non-shadow variant: 4(G-SWIR1) - (0.25NIR + 2.75SWIR2)."""
    bands = [np.asarray(x, dtype=float) for x in (green, nir, swir1, swir2)]
    if any(x.shape != bands[0].shape for x in bands[1:]):
        raise ValueError("band arrays must have the same shape")
    valid = np.logical_and.reduce([np.isfinite(x) for x in bands])
    if valid_mask is not None:
        mask = np.asarray(valid_mask)
        if mask.shape != bands[0].shape:
            raise ValueError("valid_mask must have the same shape as bands")
        if mask.dtype != np.bool_:
            raise TypeError("valid_mask must be boolean")
        valid &= mask
    if nodata is not None:
        valid &= np.logical_and.reduce([x != nodata for x in bands])
    g, n, s1, s2 = bands
    result = 4*(g-s1) - (0.25*n + 2.75*s2)
    return np.where(valid, result, np.nan)

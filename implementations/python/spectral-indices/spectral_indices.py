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


def _prepare_index_bands(*bands, nodata=None, valid_mask=None):
    """Validate same-shaped bands and build a shared validity mask."""
    arrays = tuple(np.asarray(band, dtype=np.float64) for band in bands)
    if not arrays or any(array.shape != arrays[0].shape for array in arrays[1:]):
        raise ValueError("band arrays must have the same shape")
    valid = np.logical_and.reduce([np.isfinite(array) for array in arrays])
    if valid_mask is not None:
        mask = np.asarray(valid_mask)
        if mask.shape != arrays[0].shape:
            raise ValueError("valid_mask must have the same shape as bands")
        if mask.dtype != np.bool_:
            raise TypeError("valid_mask must be boolean")
        valid &= mask
    if nodata is not None:
        for array in arrays:
            valid &= array != nodata
    return arrays, valid


def _finish_index(values, valid):
    values = np.asarray(values, dtype=np.float64)
    output = np.full(values.shape, np.nan, dtype=np.float64)
    valid = valid & np.isfinite(values)
    np.copyto(output, values, where=valid)
    return output


def _safe_ratio(numerator, denominator, valid):
    output = np.full(np.shape(numerator), np.nan, dtype=np.float64)
    valid = valid & (denominator != 0) & np.isfinite(numerator) & np.isfinite(denominator)
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        np.divide(numerator, denominator, out=output, where=valid)
    return _finish_index(output, valid)


def gndvi(nir, green, *, nodata=None, valid_mask=None):
    """Green NDVI: (NIR-Green)/(NIR+Green)."""
    (n, g), valid = _prepare_index_bands(nir, green, nodata=nodata, valid_mask=valid_mask)
    return _safe_ratio(n-g, n+g, valid)


def arvi(nir, red, blue, *, gamma=1.0, nodata=None, valid_mask=None):
    """Atmospherically resistant VI; gamma=1 gives red*=2*Red-Blue."""
    if not np.isfinite(gamma) or gamma < 0:
        raise ValueError("gamma must be finite and non-negative")
    (n, r, b), valid = _prepare_index_bands(nir, red, blue, nodata=nodata, valid_mask=valid_mask)
    corrected_red = r - gamma * (b-r)
    return _safe_ratio(n-corrected_red, n+corrected_red, valid)


def gci(nir, green, *, nodata=None, valid_mask=None):
    """Green chlorophyll index: NIR/Green - 1."""
    (n, g), valid = _prepare_index_bands(nir, green, nodata=nodata, valid_mask=valid_mask)
    return _safe_ratio(n, g, valid) - 1.0


def ci_green(nir, green, *, nodata=None, valid_mask=None):
    """Alias for the green chlorophyll index (GCI/CIgreen)."""
    return gci(nir, green, nodata=nodata, valid_mask=valid_mask)


def ci_rededge(nir, red_edge, *, nodata=None, valid_mask=None):
    """Red-edge chlorophyll index: NIR/RedEdge - 1."""
    (n, re), valid = _prepare_index_bands(nir, red_edge, nodata=nodata, valid_mask=valid_mask)
    return _safe_ratio(n, re, valid) - 1.0


def msavi(nir, red, *, nodata=None, valid_mask=None):
    """MSAVI-2: [2*NIR+1-sqrt((2*NIR+1)^2-8*(NIR-Red))]/2."""
    (n, r), valid = _prepare_index_bands(nir, red, nodata=nodata, valid_mask=valid_mask)
    with np.errstate(over="ignore", invalid="ignore"):
        discriminant = (2*n+1)**2 - 8*(n-r)
        valid &= discriminant >= 0
        return _finish_index((2*n+1-np.sqrt(np.maximum(discriminant, 0)))/2, valid)


def osavi(nir, red, *, nodata=None, valid_mask=None):
    """OSAVI using the Rondeaux 1.16 scale factor and L=0.16."""
    (n, r), valid = _prepare_index_bands(nir, red, nodata=nodata, valid_mask=valid_mask)
    return _safe_ratio(1.16*(n-r), n+r+0.16, valid)


def wdrvi(nir, red, *, alpha=0.1, nodata=None, valid_mask=None):
    """Wide-dynamic-range VI; alpha is sensor/study-selected (often 0.1-0.2)."""
    if not np.isfinite(alpha) or alpha <= 0:
        raise ValueError("alpha must be finite and positive")
    (n, r), valid = _prepare_index_bands(nir, red, nodata=nodata, valid_mask=valid_mask)
    return _safe_ratio(alpha*n-r, alpha*n+r, valid)


def nirv(nir, red, *, nodata=None, valid_mask=None):
    """NIRv = NDVI * NIR reflectance."""
    (n, r), valid = _prepare_index_bands(nir, red, nodata=nodata, valid_mask=valid_mask)
    nd = _safe_ratio(n-r, n+r, valid)
    return _finish_index(nd*n, valid)


def kndvi(nir, red, *, nodata=None, valid_mask=None):
    """Kernel NDVI approximation: tanh(NDVI squared)."""
    (n, r), valid = _prepare_index_bands(nir, red, nodata=nodata, valid_mask=valid_mask)
    nd = _safe_ratio(n-r, n+r, valid)
    return _finish_index(np.tanh(nd**2), valid)


def mtci(red, red_edge1, red_edge2, *, nodata=None, valid_mask=None):
    """MERIS terrestrial chlorophyll index: (RE2-RE1)/(RE1-Red)."""
    (r, re1, re2), valid = _prepare_index_bands(red, red_edge1, red_edge2, nodata=nodata, valid_mask=valid_mask)
    return _safe_ratio(re2-re1, re1-r, valid)


def reip(red, red_edge1, red_edge2, nir_780, *, nodata=None, valid_mask=None):
    """Four-band red-edge inflection point interpolation (bands near 670/700/740/780 nm)."""
    (r, re1, re2, n780), valid = _prepare_index_bands(
        red, red_edge1, red_edge2, nir_780, nodata=nodata, valid_mask=valid_mask
    )
    return _safe_ratio(40*((r+n780)/2-re1), re2-re1, valid) + 700.0


def tcari(red, green, red_edge, *, nodata=None, valid_mask=None):
    """Transformed chlorophyll absorption index using Red, Green and RE705-like bands."""
    (r, g, re), valid = _prepare_index_bands(red, green, red_edge, nodata=nodata, valid_mask=valid_mask)
    ratio = _safe_ratio(re, r, valid)
    return _finish_index(3*((re-r)-0.2*(re-g)*ratio), valid)


def psri(red, green, red_edge, *, nodata=None, valid_mask=None):
    """Plant senescence reflectance index: (Red680-Green500)/RedEdge750."""
    (r, g, re), valid = _prepare_index_bands(red, green, red_edge, nodata=nodata, valid_mask=valid_mask)
    return _safe_ratio(r-g, re, valid)


def ari(green, red_edge, *, nodata=None, valid_mask=None):
    """Anthocyanin reflectance index: 1/Green - 1/RedEdge."""
    (g, re), valid = _prepare_index_bands(green, red_edge, nodata=nodata, valid_mask=valid_mask)
    return _finish_index(_safe_ratio(np.ones_like(g), g, valid)-_safe_ratio(np.ones_like(re), re, valid), valid)


def cri1(blue, green, *, nodata=None, valid_mask=None):
    """Carotenoid reflectance index 1: 1/Blue510 - 1/Green550."""
    (b, g), valid = _prepare_index_bands(blue, green, nodata=nodata, valid_mask=valid_mask)
    return _finish_index(_safe_ratio(np.ones_like(b), b, valid)-_safe_ratio(np.ones_like(g), g, valid), valid)


def cri2(blue, red_edge, *, nodata=None, valid_mask=None):
    """Carotenoid reflectance index 2: 1/Blue510 - 1/RedEdge700."""
    (b, re), valid = _prepare_index_bands(blue, red_edge, nodata=nodata, valid_mask=valid_mask)
    return _finish_index(_safe_ratio(np.ones_like(b), b, valid)-_safe_ratio(np.ones_like(re), re, valid), valid)


def sipi(nir, blue, red, *, nodata=None, valid_mask=None):
    """Structure-insensitive pigment index variant: (NIR-Blue)/(NIR-Red)."""
    (n, b, r), valid = _prepare_index_bands(nir, blue, red, nodata=nodata, valid_mask=valid_mask)
    return _safe_ratio(n-b, n-r, valid)


def pri(green531, green570, *, nodata=None, valid_mask=None):
    """Photochemical reflectance index: (R531-R570)/(R531+R570)."""
    (a, b), valid = _prepare_index_bands(green531, green570, nodata=nodata, valid_mask=valid_mask)
    return _safe_ratio(a-b, a+b, valid)


def ndii(nir, swir1, *, nodata=None, valid_mask=None):
    """Normalized difference infrared index; common NIR/SWIR1 form."""
    return _ratio_index(nir, swir1, nodata=nodata, valid_mask=valid_mask)


def nmdi(nir, swir1, swir2, *, nodata=None, valid_mask=None):
    """Normalized multi-band drought index: [NIR-(SWIR1-SWIR2)]/[NIR+(SWIR1-SWIR2)]."""
    (n, s1, s2), valid = _prepare_index_bands(nir, swir1, swir2, nodata=nodata, valid_mask=valid_mask)
    difference = s1-s2
    return _safe_ratio(n-difference, n+difference, valid)


def bsi(blue, red, nir, swir1, *, nodata=None, valid_mask=None):
    """Bare soil index: [(SWIR1+Red)-(NIR+Blue)]/[(SWIR1+Red)+(NIR+Blue)]."""
    (b, r, n, s1), valid = _prepare_index_bands(blue, red, nir, swir1, nodata=nodata, valid_mask=valid_mask)
    return _safe_ratio((s1+r)-(n+b), (s1+r)+(n+b), valid)


def ndti(swir1, swir2, *, nodata=None, valid_mask=None):
    """Normalized difference tillage index: (SWIR1-SWIR2)/(SWIR1+SWIR2)."""
    return _ratio_index(swir1, swir2, nodata=nodata, valid_mask=valid_mask)


def sti(swir1, swir2, *, nodata=None, valid_mask=None):
    """Simple tillage index ratio: SWIR1/SWIR2 (band mapping is sensor-specific)."""
    (s1, s2), valid = _prepare_index_bands(swir1, swir2, nodata=nodata, valid_mask=valid_mask)
    return _safe_ratio(s1, s2, valid)


def cai(r2030, r2100, r2210, *, nodata=None, valid_mask=None):
    """Crop-residue cellulose absorption index: 0.5*(R2030+R2210)-R2100."""
    (a, b, c), valid = _prepare_index_bands(r2030, r2100, r2210, nodata=nodata, valid_mask=valid_mask)
    return _finish_index(0.5*(a+c)-b, valid)

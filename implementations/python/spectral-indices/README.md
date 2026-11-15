# Spectral indices

NumPy implementations of common optical remote-sensing indices with explicit
validity handling. Functions return NaN for non-finite, masked, NoData or
undefined (zero-denominator) pixels where applicable.

## Implemented indices

- NDVI: vegetation contrast, NIR and red.
- EVI: enhanced vegetation index, NIR/red/blue, standard coefficients.
- SAVI: soil-adjusted vegetation index, caller-selectable soil factor L (default 0.5).
- NDRE: red-edge vegetation contrast.
- NDMI and LSWI: common NIR/SWIR1 moisture formulations.
- NDWI (McFeeters): green/NIR open-water contrast.
- MNDWI: green/SWIR1 modified water index.
- NDBI: SWIR1/NIR built-up contrast.
- NBR and dNBR: NIR/SWIR2 burn ratio and pre-minus-post differenced NBR.
- NDSI: common green/SWIR1 snow index.
- AWEI_sh and AWEI_nsh: shadow and non-shadow automated water extraction indices.

## Run

    python -m pip install -r requirements.txt
    python -m pytest -q

Supply same-shaped, comparable reflectance arrays after sensor/product
calibration and quality masking. Select bands by spectral response, not by
assuming identical band numbers across sensors. Indices are proxies, not
universal class labels. Soil, atmosphere, canopy, water, illumination,
phenology and sensor response influence values.

The dNBR convention here is pre-fire minus post-fire; document alternatives.
NDMI and LSWI overlap in common formulations. Common MNDWI and NDSI formulas
also use the same bands but serve different interpretation goals. Do not treat
different names as independent measurements without checking definitions.

EVI's additive denominator constant assumes reflectance-scale inputs
consistent with its conventional formulation; do not apply it blindly to
unscaled digital numbers.

Read the [NDVI lesson](../../../algorithms/remote-sensing/ndvi.md) and
[extended index family lesson](../../../algorithms/remote-sensing/spectral-index-family.md).

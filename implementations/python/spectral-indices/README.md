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
- GNDVI, ARVI, GCI/CIgreen and CIrededge.
- MSAVI-2, OSAVI, WDRVI, NIRv and kNDVI.
- MTCI, four-band REIP and TCARI.
- PSRI, ARI, CRI1/CRI2, SIPI and PRI.
- NDII, NMDI, BSI, NDTI, STI and hyperspectral CAI.

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


## Band and formula variants

The added indices are explicit reflectance formulae, not sensor-independent band-number recipes. Map bands by wavelength and spectral response. OSAVI uses the 1.16 scale factor with L=0.16; WDRVI exposes alpha (default 0.1); ARVI exposes its blue-band correction gamma (default 1). REIP expects bands near 670, 700, 740 and 780 nm; MTCI and TCARI also require red-edge bands. CAI requires hyperspectral reflectance near 2030, 2100 and 2210 nm and should not be approximated with broad multispectral bands. Several published indices have variants; the lesson records the selected formula and assumptions.


## Band and formula variants

The added indices are explicit reflectance formulae, not sensor-independent band-number recipes. Map bands by wavelength and spectral response. OSAVI uses the 1.16 scale factor with L=0.16; WDRVI exposes alpha (default 0.1); ARVI exposes its blue-band correction gamma (default 1). REIP expects bands near 670, 700, 740 and 780 nm; MTCI and TCARI also require red-edge bands. CAI requires hyperspectral reflectance near 2030, 2100 and 2210 nm and should not be approximated with broad multispectral bands. Several published indices have variants; the lesson records the selected formula and assumptions.

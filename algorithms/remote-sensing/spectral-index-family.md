# Optical spectral-index family

Stable ID: `SA-RS-SPECTRAL-INDEX-FAMILY` · Draft 0.1 · Source compendium section 5, page 8

This family converts calibrated multispectral reflectance into band-ratio or
band-combination indicators. The implementation package covers a useful
subset of the source inventory: EVI, SAVI, NDRE, NDMI, LSWI, NDWI, MNDWI,
NDBI, NBR, dNBR and NDSI, alongside NDVI. AWEI_sh and AWEI_nsh are also included for shadow-aware water extraction.

| Index | Formula | Typical use |
|---|---|---|
| EVI | (2.5(NIR-Red)/(NIR+6Red-7.5Blue+1)) | Vegetation signal with atmospheric/background adjustment |
| SAVI | ((1+L)(NIR-Red)/(NIR+Red+L)) | Vegetation with soil-background adjustment |
| NDRE | ((NIR-RedEdge)/(NIR+RedEdge)) | Red-edge vegetation response |
| NDMI | ((NIR-SWIR1)/(NIR+SWIR1)) | Vegetation/land-surface moisture proxy |
| LSWI | Commonly ((NIR-SWIR1)/(NIR+SWIR1)) | Land-surface water response |
| NDWI | ((Green-NIR)/(Green+NIR)) | Open-water delineation (McFeeters) |
| MNDWI | ((Green-SWIR1)/(Green+SWIR1)) | Modified water extraction (Xu) |
| NDBI | ((SWIR1-NIR)/(SWIR1+NIR)) | Built-up surface contrast |
| NBR | ((NIR-SWIR2)/(NIR+SWIR2)) | Burn-sensitive contrast |
| dNBR | (NBR_{pre}-NBR_{post}) | Change in burn-sensitive response |
| NDSI | Commonly ((Green-SWIR1)/(Green+SWIR1)) | Snow-sensitive contrast |

The [implementation](../../implementations/python/spectral-indices/README.md)
returns NaN for invalid or undefined pixels. SAVI defaults to (L=0.5);
choose and report the factor. EVI's conventional coefficients and denominator
offset assume reflectance-scale inputs consistent with that formulation.

These indices are proxies, not direct measurements of biomass, water depth,
built-up fraction, burn severity or snow cover. Thresholds are scene-, sensor-,
season- and objective-dependent. Validate classifications against reference
data and confirm sensor-specific band mappings. Apply cloud, cloud-shadow,
snow and saturation masks as appropriate.

NDMI and LSWI overlap in common formulations. Common MNDWI and NDSI formulas
also use the same bands but serve different interpretation goals. Keep such
distinctions explicit in metadata; names alone do not imply independent signals.

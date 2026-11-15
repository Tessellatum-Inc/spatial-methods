# Verification record: optical spectral-index family

## Source identity
- Compendium: *Spatial Analysis Algorithms: Complete Compendium*
- Original location: Section 5, page 8
- Source entries: vegetation/soil, water/burn/snow indices

## Implemented scope
NDVI, EVI, SAVI, NDRE, NDMI, LSWI, McFeeters NDWI, MNDWI, NDBI, NBR,
dNBR and the common green/SWIR1 NDSI formulation.

## Verification
- Formula-level fixtures compare outputs with independently written scalar
  equations.
- Invalid denominators, masks and non-finite values are tested.
- EVI/SAVI coefficient handling and dNBR sign convention are tested.
- Shape and parameter validation are tested.

## Not implemented in this package
Tasseled-cap transforms, AWEI variants, atmospheric corrections, band
harmonisation, cloud masking, and index compositing remain separate methods.
Tests have been authored; execution is pending.

# Verification record: optical spectral-index family

## Source identity
- Compendium: *Spatial Analysis Algorithms: Complete Compendium*
- Original location: Section 5, page 8
- Source entries: vegetation/soil, water/burn/snow indices

## Implemented scope
NDVI, EVI, SAVI, NDRE, NDMI, LSWI, McFeeters NDWI, MNDWI, NDBI, NBR,
dNBR, the common green/SWIR1 NDSI formulation, and AWEI shadow/non-shadow variants.

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


## Section 20 extension

Added and formula-tested: GNDVI, ARVI (gamma exposed), GCI/CIgreen, CIrededge, MSAVI-2, OSAVI (1.16 scale form), WDRVI (alpha exposed), NIRv, kNDVI, MTCI, four-band REIP, TCARI, PSRI, ARI, CRI1/2, SIPI (documented variant), PRI, NDII, NMDI, BSI, NDTI, STI and hyperspectral CAI. Tests cover scalar formula agreement, mask/NoData propagation, zero denominators and parameter validation.

The work does not include sensor-specific band selection, atmospheric correction, classification thresholds, field validation, mineral-ratio families or full microwave/thermal retrieval.

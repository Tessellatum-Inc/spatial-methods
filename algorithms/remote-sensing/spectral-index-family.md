# Optical spectral-index family

This family transforms calibrated reflectance bands into vegetation, pigment, moisture, soil, burn, water and residue indicators. Formula names are not sufficient band specifications: each index must be mapped to bands with suitable central wavelengths and spectral response for the sensor.

## Added vegetation and chlorophyll indices

| Index | Formula used here | Required bands |
|---|---|---|
| GNDVI | (NIR-Green)/(NIR+Green) | NIR, Green |
| ARVI | (NIR-R*)/(NIR+R*), R*=Red-gamma(Blue-Red) | NIR, Red, Blue |
| GCI / CIgreen | NIR/Green - 1 | NIR, Green |
| CIrededge | NIR/RedEdge - 1 | NIR, RedEdge |
| MSAVI-2 | [2NIR+1-sqrt((2NIR+1)^2-8(NIR-Red))]/2 | NIR, Red |
| OSAVI | 1.16(NIR-Red)/(NIR+Red+0.16) | NIR, Red |
| WDRVI | (alpha*NIR-Red)/(alpha*NIR+Red) | NIR, Red |
| NIRv | NDVI*NIR | NIR, Red |
| kNDVI | tanh(NDVI^2) | NIR, Red |

ARVI exposes gamma because atmospheric correction variants differ. WDRVI exposes alpha; values around 0.1–0.2 are common, but the choice should be reported. OSAVI conventions sometimes omit the 1.16 multiplier; this package uses the Rondeaux form.

## Red-edge and pigment indices

| Index | Formula used here | Required bands |
|---|---|---|
| MTCI | (RE2-RE1)/(RE1-Red) | Red, RE1, RE2 |
| REIP | 700+40[((Red+R780)/2-RE700)/(RE740-RE700)] | Red, RE700, RE740, R780 |
| TCARI | 3[(RE-Red)-0.2(RE-Green)(RE/Red)] | Red, Green, RedEdge |
| PSRI | (Red680-Green500)/RedEdge750 | Red680, Green500, RedEdge750 |
| ARI | 1/Green-1/RedEdge | Green, RedEdge |
| CRI1 / CRI2 | 1/Blue510-1/Green550; 1/Blue510-1/RedEdge700 | Blue, Green or RedEdge |
| SIPI | (NIR-Blue)/(NIR-Red) | NIR, Blue, Red |
| PRI | (R531-R570)/(R531+R570) | narrow green bands at 531 and 570 nm |

SIPI has published variants; this implementation uses the NIR-blue over NIR-red form and records that choice explicitly. REIP is a four-band interpolation and is sensitive to band placement and spectral resolution. These narrow-band indices should not be computed from arbitrary broad bands without validation.

## Moisture, soil, tillage and residue indices

| Index | Formula used here | Required bands |
|---|---|---|
| NDII | (NIR-SWIR1)/(NIR+SWIR1) | NIR, SWIR1 |
| NMDI | [NIR-(SWIR1-SWIR2)]/[NIR+(SWIR1-SWIR2)] | NIR, SWIR1, SWIR2 |
| BSI | [(SWIR1+Red)-(NIR+Blue)]/[(SWIR1+Red)+(NIR+Blue)] | Blue, Red, NIR, SWIR1 |
| NDTI | (SWIR1-SWIR2)/(SWIR1+SWIR2) | SWIR1, SWIR2 |
| STI | SWIR1/SWIR2 | SWIR1, SWIR2 |
| CAI | 0.5(R2030+R2210)-R2100 | hyperspectral bands near 2030, 2100, 2210 nm |

NDII and NDMI overlap in common NIR/SWIR formulations. NDTI and STI are not interchangeable: one is a normalised difference, the other a simple ratio. CAI is a narrow-band hyperspectral residue index; broad multispectral substitutions require separate validation.

## Validity and preprocessing

All new functions share the package's NoData and boolean validity-mask contract. Undefined ratios, zero denominators, non-finite inputs and masked pixels return NaN. MSAVI returns NaN where its square-root discriminant is negative. Inputs should be calibrated reflectance with documented scale factors, atmospheric correction, cloud/shadow/saturation masks and sensor-specific wavelength mapping.

Indices are proxies, not direct measurements of biomass, chlorophyll, crop residue, water content or soil condition. Thresholds require calibration and validation for the sensor, scene, season and application.

## Verification and sources

Tests compare each implemented formula with an independently written scalar expression and exercise NoData, masks, zero denominators and invalid parameters. Formulae were cross-checked against [ESA EO for Agriculture training material](https://eo4society.esa.int/wp-content/uploads/2025/12/Introduction%20to%20EO%20for%20Agriculture_Dash.pdf), [RStoolbox spectral-index reference](https://search.r-project.org/CRAN/refmans/RStoolbox/html/spectralIndices.html), [pliman index reference](https://rdrr.io/github/TiagoOlivoto/pliman/f/vignettes/indexes.Rmd), and published crop-residue index comparisons (Remote Sensing, 2020).

See the [NumPy implementation](../../implementations/python/spectral-indices/README.md).

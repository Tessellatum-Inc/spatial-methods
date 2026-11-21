# Electromagnetic observations and radiometric quantities

**Subject:** SM-FND-012 — Remote sensing physics and radiometry  
**Status:** Initial foundation module; technical review and learner testing pending  
**Scope:** Establish the physical language needed to interpret passive optical and active microwave Earth-observation measurements. This is an introductory foundation, not a complete treatment of radiative transfer, atmospheric correction, radar signal processing or sensor calibration.

## 1. Why this foundation matters

A remotely sensed pixel is not a direct label for a place. It is a recorded response produced by a measurement system observing electromagnetic energy under a particular geometry, wavelength range, atmosphere, surface condition and processing chain.

Before calculating an index, classifying a pixel or comparing two images, ask:

- What physical quantity did the instrument detect or estimate?
- Over what wavelength or frequency range?
- Was the sensor passive or active?
- What geometry connects the source, surface and sensor?
- Which calibration and corrections have already been applied?
- What units, scale factors, masks and uncertainties accompany the product?

The central distinction in this module is between **optical measurements of reflected solar radiation** and **radar measurements of returned transmitted microwave energy**. Both involve electromagnetic radiation, but their observation models and product semantics differ.

## 2. Electromagnetic radiation: wavelength, frequency and energy

Electromagnetic radiation can be described by wavelength \(\lambda\), frequency \(\nu\), and photon energy \(E\). In vacuum:

\[
c = \lambda \nu
\]

where \(c\) is the speed of light (approximately \(2.998\times10^8\;\mathrm{m\,s^{-1}}\)).

Photon energy is:

\[
E = h\nu = \frac{hc}{\lambda}
\]

where \(h\) is Planck's constant. Shorter wavelengths correspond to higher photon energies. For remote sensing, wavelength matters because electromagnetic interactions with matter depend on wavelength, material properties, structure, moisture and geometry.

The broad electromagnetic spectrum includes radio, microwave, infrared, visible, ultraviolet, X-ray and gamma radiation. Earth-observation systems use selected wavelength intervals rather than measuring the entire spectrum.

### Spectral bands are finite intervals

A sensor band does not normally measure one mathematically exact wavelength. Its detector and optical system have a **spectral response function** describing sensitivity across a wavelength interval. The band measurement is therefore a weighted response over that interval.

Consequences:

- Two sensors with bands carrying the same informal name may have different spectral response functions.
- Band numbers are sensor-specific; “Band 4” is not a universal wavelength.
- Spectral indices and thresholds may not transfer unchanged between sensors.
- Hyperspectral measurements sample narrower and more numerous intervals than typical multispectral systems, but still have finite bandwidth and calibration limits.

Always record the sensor, product, band identifier, wavelength range and relevant response information when quantitative comparability matters.

## 3. Passive and active observation

### Passive optical observation

A passive optical sensor detects naturally available radiation. For many land-imaging applications, the dominant illumination source is the Sun. The measured signal is influenced by:

1. solar irradiance and solar geometry;
2. atmospheric absorption and scattering on the downward path;
3. surface reflection, transmission and absorption;
4. atmospheric effects on the upward path;
5. sensor spectral response, viewing geometry and calibration.

A simplified conceptual chain is:

\[
\text{Sun} \rightarrow \text{atmosphere} \rightarrow \text{surface}
\rightarrow \text{atmosphere} \rightarrow \text{sensor}
\]

This is a conceptual chain, not a complete radiative-transfer equation. Thermal infrared and passive microwave observations may have different dominant energy sources and require their own measurement models.

### Active radar observation

An active radar sensor transmits electromagnetic energy and measures returned signal energy. A simplified chain is:

\[
\text{transmitter} \rightarrow \text{surface / volume scatterers}
\rightarrow \text{receiver}
\]

The return depends on transmitted waveform and frequency, antenna pattern, range, incidence geometry, polarisation, target scattering, propagation losses, processing and calibration.

Synthetic aperture radar (SAR) uses platform motion and coherent signal processing to obtain an effective antenna aperture larger than the physical antenna. SAR image formation and phase-sensitive processing are therefore not equivalent to simply taking a photograph with a microwave camera.

**Do not transfer optical vocabulary uncritically to radar.** Optical surface reflectance and radar backscatter are different physical quantities.

## 4. Radiometric quantities: what is being measured?

Radiometry describes electromagnetic radiation quantitatively. Several quantities are related, but they are not interchangeable.

| Quantity | Symbol | Meaning | SI unit |
|---|---|---|---|
| Radiant energy | \(Q\) | Energy carried by radiation | joule (J) |
| Radiant flux / power | \(\Phi\) | Energy transferred per unit time | watt (W) |
| Irradiance | \(E_e\) | Incident radiant power per unit area | W m⁻² |
| Radiant exitance | \(M_e\) | Outgoing radiant power per unit surface area | W m⁻² |
| Radiance | \(L\) | Power per projected area per solid angle | W m⁻² sr⁻¹ |
| Spectral radiance | \(L_\lambda\) | Radiance per wavelength interval | W m⁻² sr⁻¹ µm⁻¹ (when per µm) |

The subscript \(e\) distinguishes radiometric quantities from similarly named photometric quantities based on human visual response.

### Radiance

Radiance describes how much radiant power travels in a specified direction per unit projected area and solid angle. In differential form:

\[
L = \frac{d^2\Phi}{dA\cos\theta\,d\Omega}
\]

where \(dA\) is the surface area, \(\theta\) is the angle between the surface normal and the direction of propagation, and \(d\Omega\) is a differential solid angle.

Radiance is central to many imaging sensor measurements because the sensor receives energy from a field of view and spectral response. Real sensor products may apply calibration and rescaling to encode radiance or related quantities.

### Irradiance

Irradiance is radiant power incident on a surface per unit area. For a collimated beam on a flat surface, the projected-area relationship gives:

\[
E_e = F\cos\theta
\]

where \(F\) is the beam irradiance measured on a plane perpendicular to the beam and \(\theta\) is the angle between the beam and the surface normal. This simple cosine relation assumes a collimated beam and planar surface; diffuse sky radiation and complex terrain require more complete treatment.

### Spectral quantities

A spectral quantity is expressed per unit wavelength or frequency. Its numerical value depends on the spectral interval and units. For example, radiance per micrometre and radiance per nanometre differ by a factor of 1000. Never compare spectral values without checking the wavelength unit and whether the product is integrated over a band or expressed as a spectral density.

## 5. Reflectance: a ratio, not a raw pixel value

Reflectance describes the fraction or ratio of incident radiant energy reflected by a surface under a specified geometry and wavelength convention. For a real surface, reflection is generally directional: the reflected energy depends on illumination direction, viewing direction, wavelength, surface structure and material properties.

A simple hemispherical reflectance concept is:

\[
\rho = \frac{M_{e,\mathrm{reflected}}}{E_{e,\mathrm{incident}}}
\]

where the numerator is reflected radiant exitance and the denominator is incident irradiance, defined over compatible spectral ranges and conditions. The ratio is dimensionless.

This expression is useful conceptually, but operational remote-sensing reflectance products may represent particular directional or hemispherical conventions. A product labelled “surface reflectance” is not automatically a complete description of the surface's bidirectional reflectance distribution function (BRDF).

### Bidirectional reflectance

For many land surfaces, the reflected signal varies with both illumination and viewing direction. The bidirectional reflectance distribution function (BRDF) describes this angular dependence. A surface can appear different in two images even when its material properties have not changed, simply because the Sun-sensor geometry differs.

This is one reason why multi-date comparison may require geometric, atmospheric, illumination and BRDF considerations.

### Top-of-atmosphere and surface reflectance

- **Top-of-atmosphere (TOA) reflectance** is derived at the sensor/atmosphere boundary and still includes atmospheric effects.
- **Surface reflectance** is an atmospherically corrected estimate intended to better represent surface reflection under a defined product convention.

Surface reflectance is not raw detector output. It is a derived product whose quality depends on atmospheric inputs, algorithms, assumptions, masks and product generation. The USGS explains that Landsat Collection 2 surface-reflectance products correct for atmospheric scattering and absorption and require product-specific scaling factors.

For Landsat Collection 2 Level-2 surface reflectance, the documented conversion is:

\[
\rho = DN\times0.0000275 - 0.2
\]

This is a product-specific example, not a universal scale factor. It must not be applied to Sentinel-2 or arbitrary imagery. Check the exact product guide and metadata for the collection and processing version.

## 6. Radar backscatter: normalised return, not optical reflectance

A calibrated SAR product commonly expresses returned radar power using a normalised backscatter coefficient. Common conventions include:

- \(\beta^0\) (beta nought): normalisation to a reference area in slant-range geometry;
- \(\sigma^0\) (sigma nought): normalisation to a reference ground area tangent to the reference ellipsoid;
- \(\gamma^0\) (gamma nought): normalisation to an area perpendicular to the radar line of sight.

These coefficients are dimensionless area-normalised quantities under their respective definitions. Their values depend on the product convention and processing. Terrain, incidence angle, polarisation, wavelength, surface roughness, moisture, vegetation structure and scattering mechanisms influence the return.

Terrain correction and radiometric terrain normalisation are not synonyms. Geometric terrain correction places pixels in a map coordinate system; radiometric terrain correction attempts to account for illuminated area and terrain-related radiometric effects. A map-projected image is not necessarily radiometrically terrain-normalised.

### Linear power and decibels

Radar backscatter is often displayed in decibels:

\[
\sigma^0_{dB}=10\log_{10}(\sigma^0)
\]

The inverse conversion is:

\[
\sigma^0=10^{\sigma^0_{dB}/10}
\]

This logarithmic conversion applies to power-like quantities. For an amplitude ratio, the corresponding decibel expression uses \(20\log_{10}(A)\). Do not apply the amplitude formula to a calibrated power coefficient.

Example: a linear backscatter coefficient of 0.1 corresponds to -10 dB. A coefficient of 1 corresponds to 0 dB. Negative decibel values do not mean negative physical power; they represent positive linear values below one under the chosen normalisation.

Averaging in decibels is generally not equivalent to averaging in linear power. State the domain in which filtering, averaging, ratios and statistics were calculated.

## 7. From sensor response to a usable raster

A raster pixel is a spatially sampled and processed representation. Its numeric value may be:

- a raw or quantised detector count;
- a calibrated radiance;
- a TOA reflectance estimate;
- a surface-reflectance estimate;
- a calibrated SAR backscatter coefficient;
- a logarithmic representation of a physical quantity;
- a classification, index or model output.

A numeric array alone does not tell you which of these it is.

Before analysis, record at minimum:

| Metadata | Why it matters |
|---|---|
| Sensor and platform | Defines the measurement system |
| Product name, level and version | Identifies processing and semantics |
| Acquisition date/time | Supports temporal interpretation |
| Band/polarisation and spectral interval | Defines what was observed |
| Numeric type, scale and offset | Converts stored values to physical/product values |
| Units and coefficient convention | Prevents invalid comparisons |
| CRS, grid, pixel spacing and resampling | Defines spatial support |
| No-data and quality masks | Distinguishes missing/invalid observations |
| Calibration and correction history | Establishes what transformations have occurred |
| Geometry and ancillary data | Explains illumination, view and terrain effects |
| Licence and provenance | Supports traceability and lawful reuse |

A scale factor must be applied exactly as specified. A fill value must be masked before scaling unless the product documentation explicitly states otherwise. Resampling changes the representation and can affect statistics; upsampling does not create new physical detail.

## 8. Worked reasoning examples

### Example A — stored optical values

Suppose a Landsat Collection 2 Level-2 surface-reflectance pixel has stored value \(DN=18{,}639\). Using the documented collection scale and offset:

\[
\rho=18{,}639\times0.0000275-0.2=0.3125725
\]

The approximate reflectance value is 0.313. This calculation is only valid after confirming that the pixel is not fill or otherwise invalid and that the product is the specified Landsat Collection 2 Level-2 surface-reflectance product.

### Example B — radar decibels

Suppose a calibrated linear backscatter coefficient is \(\sigma^0=0.01\):

\[
10\log_{10}(0.01)=-20\;\mathrm{dB}
\]

Converting back:

\[
10^{-20/10}=0.01
\]

The logarithmic representation changes scale, not the underlying physical quantity.

### Example C — why optical and radar values cannot be compared directly

An optical surface-reflectance value of 0.2 and a SAR backscatter value of -10 dB are not two measurements on one shared “brightness” scale. The first is a reflectance estimate under an optical product convention; the second is a logarithmic representation of a radar backscatter coefficient. Their physical definitions, sensor interactions and processing histories differ.

## 9. Common reasoning errors

1. **Treating digital numbers as physical measurements.** Apply the product's documented calibration, scale and offset.
2. **Treating TOA reflectance as surface reflectance.** Atmospheric effects remain in TOA products.
3. **Assuming reflectance is independent of geometry.** Real surfaces are often anisotropic.
4. **Treating every pixel as an independent ground sample.** Spatial resolution, point-spread functions, resampling and autocorrelation complicate spatial support.
5. **Comparing band names across sensors without checking response functions.** Spectral overlap may be imperfect.
6. **Treating SAR backscatter as optical reflectance.** They are different measurement quantities.
7. **Assuming dB values are linear.** Logarithmic operations and averages require care.
8. **Assuming terrain correction solves every terrain effect.** Geometric and radiometric corrections address different problems.
9. **Assuming a corrected product is error-free.** Atmospheric, calibration, ancillary-data and model errors remain.
10. **Interpreting an index as a direct physical property.** An index is a transformation of input measurements; its interpretation requires context and validation.

## 10. Questions and exercises

Use these to test whether the measurement concepts are clear. They are conceptual and hand-computable; no real imagery is required.

1. A sensor band is reported in W m⁻² sr⁻¹ µm⁻¹. Identify the physical quantity and explain the role of the per-micrometre term.
2. Explain why two sensors with bands both called “near infrared” may produce different values over the same target.
3. A product has stored value 10,000 and metadata gives scale 0.0001 with no offset. What value results? What metadata would you still need before interpreting it?
4. Explain why surface reflectance is a derived estimate rather than a raw measurement of the surface.
5. Convert \(\sigma^0=0.1\) to decibels and convert -15 dB back to linear power.
6. Explain why averaging -5 dB and -15 dB directly may not represent the arithmetic mean backscatter power.
7. Give two reasons why a surface may appear different in two optical images even when its material properties are unchanged.
8. Explain the difference between geometric terrain correction and radiometric terrain normalisation.
9. List the metadata you would require before calculating NDVI from a downloaded raster.
10. State why an optical reflectance value and a SAR backscatter coefficient cannot be compared as if they were measurements of the same quantity.

### Answers / discussion prompts

1. Spectral radiance; the denominator includes a wavelength interval, so the value is expressed per micrometre.
2. Their spectral response functions and calibration can differ; nominal band names do not guarantee equivalent spectral weighting.
3. The scaled value is 1.0. You still need product identity, valid range, fill value, units, band identity and processing convention.
4. It requires calibration and often atmospheric correction/model assumptions to estimate surface reflection from the signal reaching the sensor.
5. \(10\log_{10}(0.1)=-10\) dB; \(10^{-15/10}\approx0.0316\).
6. Decibels are logarithmic. Convert to linear power, perform the intended averaging, then convert back if a dB summary is required.
7. Illumination/view geometry, atmospheric conditions, phenology, moisture, shadow or surface change.
8. Geometric correction addresses where pixels are placed; radiometric terrain normalisation addresses how terrain changes the effective illuminated area and measured return.
9. Sensor/product, red and NIR band mapping, scale/offset, units, masks, CRS/grid, acquisition date and processing level.
10. They arise from different sensor interactions and have different definitions.

## 11. Connections to the four pillars

- **Spatial Data Collection:** the instrument, platform, acquisition geometry, spectral response, calibration and metadata determine what observations are available.
- **Spatial Algorithms:** indices, corrections, filters, classification and change detection operate on inputs whose physical meaning and numeric representation must be understood.
- **Spatial Recipes:** a reproducible workflow records product selection, preprocessing, parameters, masks, validation and delivery.
- **Applications:** land-cover, vegetation, water, agriculture, urban and hazard claims require evidence appropriate to the decision and its consequences.

Next in this foundation domain: develop the optical radiative-transfer and surface-reflection model in more depth, then a separate radar measurement and SAR signal-formation foundation. They must remain distinct modules connected through shared electromagnetic principles.

## 12. References and further reading

- NASA, [Remote Sensing](https://science.nasa.gov/earth/earth-observatory/remote-sensing/) — introductory overview of passive sensors, radiometers and spectral measurement.
- USGS, [Landsat Surface Reflectance](https://www.usgs.gov/landsat-missions/landsat-surface-reflectance) — product meaning, atmospheric correction and collection-specific documentation.
- USGS, [Landsat Collection 2 Level-2 Science Products](https://www.usgs.gov/landsat-missions/landsat-collection-2-level-2-science-products) — units, scale factors, offsets and quality bands.
- USGS, [Using the USGS Landsat Level-1 Data Product](https://www.usgs.gov/landsat-missions/using-usgs-landsat-level-1-data-product) — conversion from stored values to TOA radiance and reflectance using product metadata.
- Copernicus / Digital Earth Africa, [Sentinel-1 Normalised Radar Backscatter](https://docs.digitalearthafrica.org/en/latest/data_specs/Sentinel-1_specs.html) — beta, sigma and gamma reference areas and terrain considerations.
- European Space Agency, [Sentinel-1 Level-1 Detailed Algorithm Definition](https://sentinels.copernicus.eu/documents/247904/1877131/Sentinel-1-Level-1-Detailed-Algorithm-Definition) — product calibration vectors and radar coefficient definitions.

The sources above support the specific product and measurement claims described. Product conventions evolve; consult the exact collection, platform, processing baseline and product guide used in any operational analysis.

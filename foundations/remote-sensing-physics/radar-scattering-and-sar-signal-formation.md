# Radar scattering and SAR signal formation

**Subject:** SM-FND-012 — Remote sensing physics and radiometry  
**Related subjects:** SM-FND-013 — Optics, electromagnetism and wave physics; SM-FND-014 — Signal processing and information theory; SM-COL-006 — Radar, SAR and interferometric sensing  
**Status:** Initial foundation module; technical review, numerical verification and learner testing pending  
**Scope:** Physical scattering, coherent radar observations, basic SAR image formation, speckle, geometry and interferometric phase. This is a conceptual and mathematical foundation, not a complete electromagnetic solver, raw-data focuser, mission-specific processor or operational InSAR procedure.

## 1. Why radar needs its own observation model

A SAR image is not a photograph with a different colour palette. It is the result of transmitting a known microwave signal, receiving a weak echo, preserving its timing and phase relationships, and processing a sequence of observations collected as the platform moves.

A pixel can encode complex-valued signal information, detected amplitude, intensity, calibrated backscatter or a later derivative. Those representations answer different questions.

This module develops the physical chain:

1. transmitted electromagnetic wave;
2. propagation to a distributed scene;
3. scattering by surface and volume structures;
4. propagation back to the antenna;
5. coherent reception and sampling;
6. range and azimuth processing;
7. focused complex image;
8. detected or calibrated products;
9. downstream interpretation, estimation and validation.

The companion [electromagnetic observations and radiometric quantities module](electromagnetic-observations-and-radiometric-quantities.md) introduces shared radiation and radiometric concepts. The [SAR acquisition and observation design method](../../collection/sar-acquisition-and-observation-design.md) turns these concepts into product and study-design requirements.

## 2. Electromagnetic wave quantities

A monochromatic plane wave in a homogeneous, lossless medium can be represented conceptually by an electric field:

\[
\mathbf{E}(\mathbf{r},t)=\Re\left\{\mathbf{E}_0 e^{j(\mathbf{k}\cdot\mathbf{r}-\omega t)}\right\}
\]

where:
- \(\mathbf{E}_0\) is a complex amplitude vector;
- \(\mathbf{k}\) is the wave vector;
- \(\omega=2\pi f\) is angular frequency;
- \(f\) is frequency;
- \(j=\sqrt{-1}\);
- \(\Re\{\cdot\}\) denotes the real part.

In free space:

\[
c=f\lambda,\qquad k=\frac{2\pi}{\lambda}
\]

where \(c\) is the speed of light, \(\lambda\) is wavelength and \(k=\|\mathbf{k}\|\) is the wavenumber.

The phase accumulated over propagation distance \(R\) is proportional to \(kR=2\pi R/\lambda\). This is why a small change in path length can create a measurable phase change when wavelength is centimetric.

A radar transmits a finite-duration waveform, not an infinitely long sinusoid. Real systems use shaped and often frequency-modulated pulses. The carrier frequency and the waveform bandwidth play different roles: carrier frequency sets the wavelength and strongly influences target interaction, while bandwidth is central to range resolution.

## 3. The radar observation geometry

Most spaceborne land-imaging SAR is side-looking. The platform travels approximately along the azimuth (along-track) direction while the antenna illuminates a swath to one side. Range is the across-track, radar line-of-sight direction.

Keep these geometries distinct:

- **Slant range:** distance along the radar line of sight.
- **Ground range:** horizontal/map-plane projection of slant range onto a reference surface.
- **Incidence angle:** angle between the incident ray and the local or reference surface normal, depending on the stated convention.
- **Look direction:** horizontal direction toward which the antenna points.
- **Azimuth:** along-track image coordinate.
- **Near range / far range:** portions of the swath nearer to or farther from the sensor.

Do not confuse incidence angle with off-nadir angle, look angle or local incidence angle. Product specifications may define these with different reference surfaces and conventions.

### Two-way travel time and range

For a point target at slant range \(R\), the approximate round-trip propagation time is:

\[
t_r=\frac{2R}{c}
\]

so that:

\[
R=\frac{ct_r}{2}
\]

The factor of two matters because the pulse travels to the target and back. Range is inferred from delay after accounting for system timing and processing conventions.

### Range resolution

For a pulse with effective bandwidth \(B\), the ideal slant-range resolution for a simple broadside geometry is approximately:

\[
\delta_r\approx\frac{c}{2B}
\]

This is a resolution relation, not a promise that two arbitrary ground objects will be separable by exactly this distance. Windowing, waveform design, signal-to-noise ratio, processing, incidence angle and product resampling affect realised performance.

For a flat reference surface and incidence angle \(\theta\) measured from the surface normal, the corresponding ground-range resolution is approximately:

\[
\delta_{gr}\approx\frac{\delta_r}{\sin\theta}
\]

This simplified relation assumes local flat geometry. Sloped terrain requires local geometry and may exhibit foreshortening or layover.

**Example:** with effective bandwidth \(B=20\;\mathrm{MHz}\),

\[
\delta_r\approx\frac{3.0\times10^8}{2(20\times10^6)}
=7.5\;\mathrm{m}
\]

This is a theoretical slant-range value under the simplified model. It is not a Sentinel-1 product specification or an estimate of final ground pixel size.

## 4. Why platform motion creates a synthetic aperture

A real antenna illuminates a target over a finite angular beamwidth. As the platform moves, the same target is observed from a sequence of positions. Its range and Doppler history change systematically.

The processor uses the coherent sequence of echoes to focus energy from the target into an image location. In effect, the platform's motion synthesises a much longer aperture than the physical antenna.

Two dimensions are formed through related but distinct information:

- **Range focusing** separates targets using echo delay and transmitted waveform bandwidth.
- **Azimuth focusing** separates targets using the phase/Doppler history observed along the platform trajectory.

A SAR processor must model the changing sensor-target geometry and phase history. Errors in trajectory, timing, waveform knowledge, synchronisation or processing can defocus the image or misplace targets.

For an ideal stripmap broadside SAR under simplified assumptions, azimuth resolution is often approximated by about half the real antenna length in azimuth. This counter-intuitive result depends on the imaging mode and processing assumptions; do not use it as a universal formula for spotlight, ScanSAR, TOPS or arbitrary acquisition configurations.

### Doppler and azimuth

The Doppler frequency shift is related to the rate of change of sensor-target range. A target's Doppler history changes as the platform approaches and passes it. SAR focusing exploits this history to locate energy in azimuth.

Doppler centroid and Doppler bandwidth are not the same quantity:
- Doppler centroid describes the centre of the observed Doppler spectrum and is affected by squint, geometry and acquisition conditions.
- Doppler bandwidth describes the span of Doppler frequencies contributing to the focused azimuth response.

Precise definitions and processing are mission- and mode-specific. The simplified intuition is that range delay distinguishes across-track positions while Doppler history helps distinguish along-track positions.

## 5. The complex SAR signal

A focused single-look complex (SLC) pixel is represented by:

\[
z=I+jQ
\]

where \(I\) and \(Q\) are in-phase and quadrature components. From this representation:

\[
A=|z|=\sqrt{I^2+Q^2}
\]

\[
P=|z|^2=I^2+Q^2
\]

\[
\phi=\arg(z)=\operatorname{atan2}(Q,I)
\]

Here \(A\) is amplitude, \(P\) is intensity/power-like magnitude and \(\phi\) is phase. Product conventions and calibration determine the exact physical interpretation and scaling.

These quantities must not be casually interchanged:
- amplitude is not intensity;
- intensity is not a calibrated normalised backscatter coefficient by itself;
- phase is not a direct displacement measurement;
- a detected product may discard the phase information needed for conventional interferometry.

For a simple complex sample, if \(I=3\) and \(Q=4\), then amplitude is 5, intensity is 25, and phase is \(\operatorname{atan2}(4,3)\), approximately 0.927 radians. This arithmetic illustrates the representation only; it is not a calibrated geophysical observation.

## 6. Scattering: why surfaces return different signals

The returned signal is produced by electromagnetic interactions with a scene. A resolution cell may contain many scatterers: soil aggregates, leaves, branches, trunks, walls, roofs, roads, rocks, water facets and other structures.

The observed return depends jointly on:
- wavelength and frequency;
- transmitted and received polarisation;
- incidence and local viewing geometry;
- dielectric properties and electrical conductivity;
- surface roughness relative to wavelength;
- object size, orientation and arrangement;
- moisture and material composition;
- canopy or volume structure;
- shadowing, occlusion and multiple interactions.

There is no universal one-to-one mapping from backscatter value to land-cover class.

### 6.1 Specular reflection

A sufficiently smooth surface relative to the radar wavelength can reflect energy predominantly away from the sensor under a given geometry. Calm open water is a common example and may appear dark in a side-looking image.

But dark does not mean water. Smooth roads, roofs, dry surfaces, radar shadow and low-return materials may also be dark. Wind-roughened water, emergent vegetation or double-bounce interactions can make water-related areas brighter.

### 6.2 Rough-surface scattering

A rough surface distributes returned energy across a wider range of directions. The amount returned to the antenna depends on roughness relative to wavelength, incidence angle, dielectric properties and the surface's statistical structure.

“Rough” is therefore not an absolute label. A surface can be smooth at one wavelength and rough at another. The relevant roughness scale must be considered relative to wavelength and the distribution of surface heights and slopes.

### 6.3 Volume scattering

A wave may interact with many scatterers within a volume, such as vegetation canopy, branches, stems, trunks or snow/firn structures. The returned signal depends on the density, orientation, size and dielectric properties of these scatterers, and on attenuation through the volume.

Cross-polarised returns can be sensitive to depolarising and volume-scattering processes, but VH or HV is not a pure vegetation channel. Surface scattering, multiple scattering, geometry and noise also contribute.

### 6.4 Double-bounce and multiple interactions

Energy may reflect between two surfaces or structures before returning to the antenna. A vertical wall next to a horizontal ground surface is a familiar idealised double-bounce geometry. Depending on orientation and look direction, this can produce a strong return.

Urban areas contain many orientations and complex interactions. A bright linear feature may reflect building geometry, corner-like structures, roads, infrastructure, terrain or other effects. Do not identify a specific object from brightness alone.

### 6.5 Dielectric properties and moisture

The dielectric response of a material influences how much radar energy is reflected, transmitted and absorbed. Water content can change the effective dielectric properties of soil and vegetation, often changing backscatter.

The relationship is not monotonic in every setting. Surface roughness, vegetation, incidence angle, texture, salinity, freeze/thaw state and wavelength may dominate or complicate the moisture response. Any soil-moisture retrieval needs an explicit physical/statistical model and independent validation.

## 7. Polarisation as a measurement dimension

An electromagnetic wave has an electric-field orientation. Radar systems may transmit and receive different polarisation states. A channel label describes both ends of the measurement:

- VV: vertical transmit, vertical receive;
- VH: vertical transmit, horizontal receive;
- HH: horizontal transmit, horizontal receive;
- HV: horizontal transmit, vertical receive.

The first letter is transmit polarisation; the second is receive polarisation. Confirm mission conventions and actual channels in metadata.

Co-polarised channels (VV, HH) and cross-polarised channels (VH, HV) respond differently to target structure and scattering. Cross-polarised returns may increase where scattering changes the polarisation state, but channel values also depend on calibration, noise floor, geometry, wavelength and scene composition.

A dual-polarisation product is not a full polarimetric measurement. Full polarimetry requires a suitable set of transmit/receive channels and consistent complex calibration. Do not infer a scattering matrix or polarimetric decomposition from two detected intensity bands.

## 8. Backscatter coefficients and radiometric meaning

A calibrated SAR product may provide a normalised radar backscatter coefficient, commonly expressed using \(\beta^0\), \(\sigma^0\) or \(\gamma^0\). The [electromagnetic observations module](electromagnetic-observations-and-radiometric-quantities.md#6-radar-backscatter-normalised-return-not-optical-reflectance) introduces their reference-area conventions.

The important distinction here is between the complex image sample and the calibrated backscatter product:
1. complex samples encode amplitude and phase under product scaling;
2. detected intensity is derived from magnitude squared;
3. calibration applies product-specific factors and corrections;
4. normalisation defines the reference area convention;
5. terrain correction/flattening may apply geometric and radiometric models;
6. conversion to decibels is a logarithmic representation of a power-like coefficient.

For a positive power coefficient \(\sigma^0\):

\[
\sigma^0_{dB}=10\log_{10}(\sigma^0)
\]

and:

\[
\sigma^0=10^{\sigma^0_{dB}/10}
\]

If \(\sigma^0=0.1\), then \(\sigma^0_{dB}=-10\;\mathrm{dB}\). The negative dB value does not mean negative power.

Averages, filters, ratios and thresholds can produce different results depending on whether they are applied in linear power or logarithmic units. State the domain explicitly. Never average dB values and silently describe the result as the mean linear power.

## 9. Speckle: coherent interference inside a resolution cell

A SAR resolution cell often contains many elementary scatterers. Their returned waves add as complex vectors. The phase relationships cause constructive and destructive interference. The resulting spatial variation is called speckle.

Speckle is not simply a camera sensor defect or an ordinary independent additive-noise layer. It is an inherent consequence of coherent imaging of distributed targets. The observed amplitude and intensity vary even across a statistically homogeneous surface.

### A simple statistical model

For an ideal fully developed speckle model, the complex return can be approximated by a zero-mean circular complex Gaussian random variable. The single-look intensity is then exponentially distributed under the homogeneous-target assumptions:

\[
p(I\mid\mu)=\frac{1}{\mu}\exp\left(-\frac{I}{\mu}\right),\quad I\geq0
\]

where \(\mu=E[I]\) is the mean intensity.

For this ideal single-look model:

\[
E[I]=\mu,\qquad \operatorname{Var}(I)=\mu^2
\]

so the intensity coefficient of variation is 1. Real data may depart from this model because of heterogeneous targets, multilooking, correlated samples, processing, noise and nonstationarity.

### Multilooking and filtering

Multilooking averages multiple looks to reduce speckle variance, generally at the cost of spatial resolution. Spatial and temporal filters can also reduce visible speckle but may smooth boundaries, remove small features, alter distributions or introduce bias.

A speckle filter is therefore a modelling decision, not an obligatory cosmetic step. Record:
- whether filtering occurred in amplitude or intensity/power;
- the filter family and parameters;
- the number of looks or effective equivalent number of looks where known;
- the spatial support and edge handling;
- the output resolution and grid;
- the effect on the target feature and downstream statistics.

The [Lee speckle filter algorithm record](../../algorithms/remote-sensing/lee-speckle-filter.md) is a later computational method. This foundation explains why such filters exist and what trade-offs they face.

## 10. Side-looking geometry and terrain distortion

SAR does not observe the ground from directly overhead. The side-looking geometry produces characteristic distortions:

- **Foreshortening:** slopes facing the sensor are compressed in range because their near and far portions have similar or compressed slant-range positions.
- **Layover:** elevated parts of a slope or structure may be imaged before lower parts, reversing their apparent range order.
- **Radar shadow:** terrain or structures block illumination of areas behind them, producing little or no return.
- **Incidence-angle variation:** the same target may return different energy across near and far range.
- **Local illuminated-area effects:** slope orientation changes the effective illuminated area and radiometric response.

These are not all solved by map projection. Geometric terrain correction can geocode observations, but it cannot recover information that was never illuminated or resolve all layover. Radiometric terrain normalisation attempts to address radiometric area effects under a model; it is not identical to geometric correction.

A DEM and viewing geometry can help identify or model terrain effects. DEM errors, resolution mismatch, vegetation height and inaccurate geometry can limit the correction.

## 11. Phase and interferometric SAR

The phase of a complex SAR pixel is related to the two-way propagation path and the scattering response of the resolution cell. A simplified point-scatterer relation is:

\[
\phi\approx-\frac{4\pi R}{\lambda}+\phi_s
\]

where \(R\) is sensor-to-target range and \(\phi_s\) represents target/scattering and system contributions under a chosen sign convention. The sign convention varies by processing convention; the relationship is the key point.

A path-length change \(\Delta R\) produces a phase change approximately:

\[
\Delta\phi\approx-\frac{4\pi}{\lambda}\Delta R
\]

This is a line-of-sight path relationship. It is not yet ground displacement: the radar observes only the line-of-sight component, and the phase also contains other contributions.

### 11.1 Interferogram

Given two co-registered complex images \(z_1\) and \(z_2\), a common interferogram convention is:

\[
I_{12}=z_1 z_2^*
\]

where \(^*\) denotes complex conjugation. The interferometric phase is:

\[
\phi_{12}=\arg(I_{12})
\]

The interferometric phase includes several terms, depending on the application and processing:
- flat-Earth / reference geometry contribution;
- topographic phase;
- deformation-related phase;
- atmospheric delay differences;
- orbit and processing residuals;
- noise and decorrelation.

The exact signs and decomposition depend on reference/secondary ordering and processor conventions. Never compare phase signs without checking the convention.

### 11.2 Coherence

Interferometric coherence measures the degree of complex similarity between two observations over a local estimation window. A common estimator is:

\[
\hat{\gamma}=\frac{\left|\sum_{k\in W} z_{1,k}z^*_{2,k}\right|}
{\sqrt{\left(\sum_{k\in W}|z_{1,k}|^2\right)
\left(\sum_{k\in W}|z_{2,k}|^2\right)}}
\]

Under this estimator, \(0\leq\hat{\gamma}\leq1\), subject to numerical and estimator details. Values nearer one indicate stronger local complex similarity; values nearer zero indicate weak similarity. Coherence is estimated over a window, so window size affects spatial resolution and estimator variance.

Coherence loss may result from:
- **temporal decorrelation:** scene changes between acquisitions;
- **geometric decorrelation:** different viewing geometry and spectral support;
- **volume decorrelation:** distributed scatterers at different heights or within vegetation;
- **Doppler/processing mismatch:** inconsistent acquisition or processing;
- **thermal noise and low signal-to-noise ratio.**

Low coherence does not identify one unique cause. High coherence does not prove the phase is deformation-only.

### 11.3 Baselines and phase interpretation

The spatial baseline describes the separation between acquisition trajectories, commonly decomposed into components relative to the line of sight. Perpendicular baseline influences the difference in viewing geometry and sensitivity to topography; temporal baseline is the time between acquisitions and relates to scene evolution.

A useful interferometric pair must balance:
- temporal decorrelation risk;
- geometric decorrelation and common-band limitations;
- topographic sensitivity;
- acquisition geometry and burst overlap;
- atmospheric and orbit errors;
- the target's expected stability and deformation.

A short temporal baseline is not a guarantee of high coherence. Vegetation, water, construction and other changing targets can decorrelate quickly.

### 11.4 From phase to displacement

After suitable corrections and phase unwrapping, a phase change can be related to line-of-sight displacement using a wavelength-dependent scale. Under one common convention:

\[
d_{LOS}=-\frac{\lambda}{4\pi}\Delta\phi
\]

The sign depends on phase and displacement conventions. The relation applies only to the deformation-related phase after other contributions have been modelled or removed and phase ambiguity resolved. It does not yield a full three-dimensional displacement vector from one viewing geometry.

Independent measurements, such as GNSS or other geodetic observations, are important for reference and validation where the claim requires them.

The [local InSAR coherence algorithm record](../../algorithms/remote-sensing/insar-local-coherence.md) covers a bounded computational estimator; it is not a complete InSAR workflow.

## 12. From physical model to acquisition and algorithm choices

The physics implies practical requirements:

| Physical or signal concept | Acquisition / processing implication |
|---|---|
| Carrier wavelength | Influences interaction with roughness, vegetation, moisture and penetration |
| Pulse bandwidth | Constrains ideal slant-range resolution |
| Platform motion and Doppler history | Requires accurate timing, orbit/trajectory and coherent focusing |
| Complex phase | Requires SLC-like complex products for conventional InSAR |
| Polarisation | Verify transmit/receive channels and calibration |
| Incidence/local geometry | Preserve orbit, look direction, angle and terrain metadata |
| Speckle | Choose multilooking/filtering with explicit resolution/statistical trade-offs |
| Terrain distortion | Inspect layover, foreshortening, shadow and DEM suitability |
| Temporal scene change | Design repeat acquisitions and coherence expectations |
| Radiometric normalisation | Record coefficient, scale, calibration and processing lineage |

The collection method defines how to choose and document the observation. Algorithms implement particular transformations or estimators. Recipes connect these components to an application with validation and acceptance criteria.

## 13. Worked reasoning examples

### Example A — wavelength and phase sensitivity

Suppose a radar wavelength is \(\lambda=0.056\;\mathrm{m}\). A line-of-sight path change of \(\Delta R=0.014\;\mathrm{m}\) corresponds in magnitude to:

\[
|\Delta\phi|=\frac{4\pi(0.014)}{0.056}=\pi\;\mathrm{rad}
\]

This is a half-cycle phase change under the simplified point-scatterer relation. It does not mean a displacement of 1.4 cm has been measured from a real interferogram: atmospheric, topographic, orbit, noise, reference and phase-unwrapping terms must be considered.

### Example B — what a coherence value means

A local coherence estimate of 0.9 indicates strong complex similarity under the chosen estimator and window. It does not establish that the phase is free of atmospheric delay or that the target did not move. A coherence estimate of 0.2 indicates weak local similarity, but cannot by itself distinguish vegetation change, temporal change, geometric mismatch, noise or processing problems.

### Example C — same target, different look

A building façade facing the radar may contribute a strong double-bounce return with adjacent ground. The same building observed from the opposite side may have a different response and shadow pattern. Therefore, an ascending and descending scene can differ even if the building has not changed.

## 14. Common conceptual errors

| Error | Correction |
|---|---|
| SAR is a microwave photograph | It is a coherently processed measurement system with geometry and product-specific representations |
| Range and azimuth resolution are the same mechanism | Range relies on waveform delay/bandwidth; azimuth uses platform motion and Doppler history |
| Pixel spacing equals resolution | Sampling interval and resolving power are different quantities |
| Bright means urban; dark means water | Multiple physical and geometric mechanisms can produce similar intensity |
| Cross-polarisation is a pure vegetation measure | Several scattering, geometry and noise contributions affect it |
| Speckle is ordinary additive sensor noise | Speckle arises from coherent summation of scatterers within resolution cells |
| Terrain correction removes all terrain effects | Geocoding cannot recover shadowed data or fully resolve layover |
| SLC phase directly measures displacement | Phase includes geometry, topography, atmosphere, scattering and noise |
| High coherence validates deformation | Coherence indicates local complex similarity, not the physical cause of phase |
| One SAR wavelength sees through all clouds and vegetation | Penetration and atmospheric interaction depend on wavelength, medium, structure and conditions |

## 15. Exercises

1. A sensor transmits at 5.4 GHz. Calculate the free-space wavelength using \(c=2.998\times10^8\;\mathrm{m/s}\). Explain why this does not by itself determine penetration into vegetation.
2. A waveform has effective bandwidth 40 MHz. Estimate ideal slant-range resolution using \(c/(2B)\). State at least three reasons a delivered product may have a different ground pixel spacing.
3. Explain why SAR uses platform motion to improve azimuth resolution.
4. A complex sample is \(z=6-j8\). Calculate amplitude, intensity and phase.
5. Describe how a smooth water surface can return a weak signal in one geometry and a stronger signal under wind-roughened or vegetation-covered conditions.
6. Explain why roughness must be considered relative to wavelength.
7. Give two plausible mechanisms for a strong cross-polarised return and explain why neither uniquely identifies vegetation.
8. Explain how coherent summation produces speckle in a homogeneous distributed target.
9. State the information lost when complex SLC data are detected into an intensity-only product.
10. A repeat-pass interferogram contains phase variation. List at least five contributions other than deformation that may be present.
11. Explain why high coherence does not prove that a displacement estimate is correct.
12. Describe one way terrain can cause geometric distortion and one reason map geocoding cannot fully repair it.

## 16. Discussion notes

1. \(\lambda=c/f\). At 5.4 GHz, \(\lambda\approx0.0555\;\mathrm{m}\), or about 5.6 cm. Penetration also depends on dielectric properties, vegetation structure, moisture and path geometry.
2. \(\delta_r\approx3.75\;\mathrm{m}\). Product spacing can differ due to ground projection, multilooking, resampling, processing mode and sampling design.
3. The moving platform observes each target across a sequence of positions. Coherent phase/Doppler history allows the processor to focus the echoes in along-track direction.
4. Amplitude is 10; intensity is 100; phase is \(\operatorname{atan2}(-8,6)\), approximately -0.927 radians.
5. Smooth water may reflect energy away from the antenna; wind roughens the surface and redistributes energy. Emergent vegetation and multiple scattering can also increase returns.
6. Electromagnetic interaction depends on the ratio and distribution of surface-height variation to wavelength, not an absolute roughness label.
7. Volume scattering and multiple/bounce interactions can depolarise the return; calibration, geometry, surface structure and noise also matter.
8. Individual echoes add as complex vectors. Their relative phases cause constructive and destructive interference, creating spatial variation in amplitude and intensity.
9. Detection discards the phase relationship in the complex samples, preventing conventional phase-based interferometry from the detected product.
10. Flat-Earth/reference geometry, topographic phase, atmosphere, orbit error, temporal decorrelation, geometric decorrelation, volume decorrelation, thermal noise and processing residuals.
11. Coherence describes local complex similarity. It does not separate deformation from atmospheric or topographic phase, nor validate the reference, unwrapping or displacement model.
12. Layover can superimpose returns from different terrain positions. Map geocoding changes coordinates but cannot separate unresolved or shadowed contributions.

## 17. Connections and limits

- [SAR acquisition and observation design](../../collection/sar-acquisition-and-observation-design.md) — turns physical requirements into product selection, geometry, metadata and quality gates.
- [Radar exploration](../../explorations/radar/README.md) — curiosity-led entry point for SAR and neighbouring radar domains.
- [Radar territory map](../../explorations/radar/territory-map.md) — shows which concepts are shared across SAR, weather radar and radar engineering.
- [Sentinel-1 backscatter investigation](../../explorations/radar/sentinel-1-backscatter-investigation.md) — guided interpretation, not a validated classification.
- [Nairobi Sentinel-1 scene record](../../explorations/radar/nairobi-sentinel-1-scene-record.md) — study specification; no scene-specific result is claimed.
- [Lee speckle filter](../../algorithms/remote-sensing/lee-speckle-filter.md), [SAR CFAR](../../algorithms/remote-sensing/sar-cfar.md) and [local InSAR coherence](../../algorithms/remote-sensing/insar-local-coherence.md) — algorithm records with narrower computational scopes.
- [Remote-sensing cross-pillar pathway](../../learning-paths/remote-sensing-cross-pillar-pathway.md) — links foundations, collection, algorithms and applications.

This module does not replace a full electromagnetics course, SAR raw-data processing text, mission product specification or advanced InSAR reference. Its purpose is to establish a defensible conceptual model and vocabulary so that acquisition and algorithm choices can be reasoned about rather than copied.

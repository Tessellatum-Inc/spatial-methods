# Radar: map of the territory

Radar is not one subject with one learning path. It is a family of sensing and engineering systems that share electromagnetic foundations but solve different problems.

This map is a navigation aid. Follow the branch that matches the question you actually have; move between branches when the connections become useful.

## 1. The shared foundation

Most radar branches draw on some combination of:

- **Electromagnetics:** wave propagation, frequency, wavelength, polarisation, reflection, scattering and dielectric properties.
- **Signals and systems:** pulses, bandwidth, sampling, filtering, Fourier transforms, matched filtering and noise.
- **Measurement and geometry:** range, Doppler, viewing geometry, calibration, coordinate systems and uncertainty.
- **Probability and estimation:** noise models, detection, estimation, statistical inference and classification.
- **Computing:** numerical methods, signal processing, image formation, data structures and visualisation.

These foundations overlap, but the mathematics and engineering depth required differ by branch.

## 2. Earth-observation radar

**Central question:** What can radar measurements tell us about the Earth's surface and how it changes?

### 2.1 Synthetic aperture radar (SAR) imaging

A moving platform collects coherent radar measurements. Processing uses the platform's motion and signal history to form an image with a synthetic aperture.

Investigate:
- range and azimuth resolution;
- pulse bandwidth and pulse compression;
- Doppler history and synthetic aperture formation;
- focusing and image formation;
- complex imagery versus detected amplitude or intensity;
- acquisition modes, swath and resolution trade-offs.

**Useful next question:** How do echoes collected along a moving satellite path become a focused two-dimensional image?

### 2.2 Backscatter and surface interaction

**Central question:** Why do different surfaces return different amounts of radar energy?

Investigate:
- wavelength and surface roughness;
- dielectric properties and moisture;
- incidence angle and local terrain;
- polarisation (for example VV and VH);
- surface, volume and double-bounce scattering;
- radiometric calibration and terrain effects.

**Useful next question:** Which physical and acquisition factors could explain a bright or dark patch in this scene?

### 2.3 Interferometric SAR (InSAR)

**Central question:** What can phase differences between radar acquisitions reveal about changes in the sensor-to-ground path?

Investigate:
- complex phase and interferograms;
- coherence and decorrelation;
- perpendicular and temporal baselines;
- orbital and topographic phase;
- atmospheric delay;
- phase unwrapping and reference points;
- displacement geometry and uncertainty.

Applications include ground deformation, subsidence, earthquakes, volcanoes, landslides and infrastructure monitoring.

**Useful next question:** What contributions besides ground motion can create a phase difference between two acquisitions?

### 2.4 Polarimetric SAR (PolSAR)

**Central question:** What additional information is available when the radar records multiple transmit/receive polarisations?

Investigate:
- scattering matrices and covariance/coherency representations;
- polarimetric decompositions;
- scattering mechanisms;
- calibration and channel consistency;
- classification and physical interpretation.

**Useful next question:** What can multiple polarisation channels distinguish that a single channel cannot?

### 2.5 Time series and change analysis

**Central question:** What changes across repeated observations, and how can real change be separated from acquisition or processing differences?

Investigate:
- temporal consistency and acquisition geometry;
- radiometric terrain correction;
- time-series statistics;
- change detection and anomaly detection;
- coherence time series;
- reference data and validation.

Applications include crop monitoring, forest change, flood extent, soil moisture proxies and infrastructure change.

**Useful next question:** How do we know an observed difference is a change on the ground rather than a difference in measurement conditions?

### 2.6 Applications are not methods

Flood mapping, agriculture, forestry, urban analysis, maritime monitoring and disaster response are application areas. Each may combine several methods above with domain-specific evidence and validation.

For example, flood mapping may use backscatter change, thresholding, temporal context, terrain, permanent-water masks and independent reference data. It is not synonymous with “dark pixels equal water”.

## 3. Weather radar

**Central question:** What is happening in the atmosphere, and how is precipitation distributed and moving?

Investigate:
- reflectivity and the radar equation;
- Doppler velocity and spectrum width;
- dual-polarisation variables;
- precipitation estimation and attenuation;
- beam blockage, range effects and clutter;
- volume scans, mosaics, nowcasting and data assimilation.

Weather radar observes atmospheric targets such as precipitation particles. Its measurement, scanning strategy and interpretation differ from satellite SAR imaging of the land surface.

**Useful next question:** What does reflectivity measure, and why is it not a direct measurement of rainfall at the ground?

## 4. Radar systems engineering

**Central question:** How do we design a radar system to detect, locate or characterise targets under real constraints?

Investigate:
- system requirements and link budgets;
- transmitters, receivers, antennas and waveforms;
- frequency bands and regulatory constraints;
- noise figure, dynamic range and sensitivity;
- range and Doppler resolution;
- clutter, interference and detection probability;
- hardware/software integration and testing.

**Useful next question:** Given a detection range and target requirement, what system parameters constrain the design?

## 5. Radar signal processing and detection

This is a cross-cutting technical branch rather than a single application.

Investigate:
- sampled signals and complex baseband representations;
- matched filtering and pulse compression;
- FFTs and spectral analysis;
- range-Doppler processing;
- clutter suppression and adaptive filtering;
- CFAR detection;
- tracking, estimation and classification;
- computational performance and numerical precision.

These methods appear in weather, maritime, defence, automotive and remote-sensing systems, but parameter choices and operational constraints are application-specific.

**Useful next question:** How does a detector distinguish a target return from noise and clutter while controlling false alarms?

## 6. Maritime, navigation and automotive radar

These are application-specific system families.

- **Maritime radar:** navigation, collision avoidance, target tracking, sea clutter, rain clutter and vessel traffic.
- **Navigation and surveillance radar:** detection and tracking in defined operational environments.
- **Automotive radar:** short-range sensing, range-Doppler estimation, angle estimation, multi-target tracking and sensor fusion.

Do not assume that a satellite SAR workflow or weather-radar interpretation transfers directly to these systems.

## 7. Choose a route by the question

| Your question | Start with | A useful first action |
|---|---|---|
| How does a satellite form a radar image? | SAR imaging | Trace the range and azimuth dimensions through a SAR formation explanation |
| Why is this surface bright or dark? | Backscatter | Inspect one Sentinel-1 scene and record competing explanations |
| Can I measure ground movement? | InSAR | Interpret an existing interferogram and list phase contributions |
| Can radar map a flood? | SAR applications and change analysis | Compare a documented event with an independent reference |
| How does weather radar estimate precipitation? | Weather radar | Distinguish reflectivity, velocity and rainfall-rate products |
| How is a radar system designed? | Systems engineering | Translate a detection requirement into a parameter and link-budget question |
| How does a radar detect targets? | Signal processing and detection | Work through matched filtering and a simple detection threshold |
| How do vehicle or vessel radars work? | Application-specific radar | Identify the sensing range, clutter, tracking and safety constraints |

## 8. Connections beyond radar

- **Remote sensing and GIS:** georeferencing, raster analysis, map projections and spatial validation.
- **Geodesy:** reference frames, precise orbits, deformation and measurement uncertainty.
- **Hydrology:** flood processes, terrain, water extent and independent event evidence.
- **Forestry and agriculture:** canopy structure, biomass proxies, crop phenology and field validation.
- **Computer vision:** image formation, feature extraction, classification and sensor fusion.
- **Physics and electrical engineering:** electromagnetic propagation, antennas, circuits and systems.
- **Statistics and machine learning:** estimation, detection, classification, time series and uncertainty.

## 9. Editorial boundary

This map is an orientation layer, not an exhaustive radar textbook or a claim that every branch is covered by the current Spatial Methods collection. Each branch needs its own source evaluation, methods, practical examples and limitations before it can be treated as a developed exploration.

**Current flagship scope:** Earth-observation SAR, beginning with image interpretation and Sentinel-1 data. Other branches are mapped to make the boundaries visible and to provide credible next directions, not to imply equivalent depth.

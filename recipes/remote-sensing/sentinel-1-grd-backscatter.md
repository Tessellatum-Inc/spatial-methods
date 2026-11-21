# Sentinel-1 IW GRD backscatter preparation

<text>
Status: workflow specification and validation plan. This recipe is not yet executed on the Nairobi products; its first execution depends on a downloaded SAFE archive and a recorded SNAP version.
</text>

## Purpose

Prepare comparable Sentinel-1 Interferometric Wide (IW) Ground Range Detected (GRD) VV/VH backscatter layers for mapping and temporal comparison. The Nairobi exercise uses four candidate Sentinel-1C acquisitions on descending relative orbit 79, each reported as slice 4 of 11 and each covering the complete rectangular study AOI.

This is a **detected-backscatter workflow**, not an interferometric workflow. GRD processing includes detection and multilooking, and phase information is lost. Do not use these GRD products to calculate InSAR displacement or interferometric coherence; those require suitable SLC products and a separate processing design.

## Cross-pillar connections

- **Foundations:** [Radar scattering and SAR signal formation](../../foundations/remote-sensing-physics/radar-scattering-and-sar-signal-formation.md)
- **Acquisition:** [SAR acquisition and observation design](../../collection/sar-acquisition-and-observation-design.md)
- **Algorithms:** [Lee speckle filter](../../algorithms/remote-sensing/lee-speckle-filter.md)
- **Investigation record:** [Nairobi Sentinel-1 scene record](../../explorations/radar/nairobi-sentinel-1-scene-record.md)
- **Download gate:** [Sentinel-1 download and validation](../../explorations/radar/sentinel-1-download-and-validation.md)

## Inputs and prerequisites

1. An intact Sentinel-1 IW GRD SAFE product archive, with a passing ZIP CRC and SAFE-structure check.
2. Product UUID, product name, acquisition time, platform, relative orbit, orbit direction, slice number and polarisation metadata.
3. A compatible ESA SNAP installation with Sentinel-1 Toolbox and Graph Processing Tool (GPT).
4. Orbit auxiliary data appropriate to the acquisition; use precise orbit information when available and record the orbit file actually applied.
5. A documented DEM choice for Range-Doppler terrain correction. Use the same DEM source and version for all dates in a comparison.
6. A target projected CRS and analysis grid. For the Nairobi exercise, use UTM zone 37S, EPSG:32737, subject to verifying the AOI and output coordinate metadata.

Do not proceed if the archive, product identity, acquisition metadata or VV/VH measurement availability cannot be verified.

## Processing design

The reference processing chain is:

1. Read SAFE and inspect metadata.
2. Apply an updated orbit file.
3. Remove thermal noise where appropriate for the product and operator version.
4. Remove GRD border noise.
5. Calibrate VV and VH to linear Sigma Nought (Sigma0).
6. Optionally filter speckle, only when justified by the analytical task.
7. Apply Range-Doppler terrain correction using the chosen DEM and target grid.
8. Convert calibrated power to decibels for display or analysis products that require dB.
9. Run spatial, radiometric and temporal quality checks.

This sequence follows the common SNAP GRD workflow, but operator availability and parameters must be checked against the installed SNAP/S1TBX version. Do not copy parameters from another software version without recording and testing them.

### 1. Read and inspect

Confirm from the SAFE manifest and annotation files:

- product type is IW GRD;
- actual measurement files exist for both VV and VH;
- swaths and polarisation channel names are consistent;
- acquisition start and stop times match the catalogue record;
- slice identity and total slice count are retained;
- processing baseline and product generation metadata are recorded;
- calibration and noise annotation references are present.

Record archive SHA-256, SNAP version, operating system, DEM source/version, and the full GPT graph or command line used.

### 2. Orbit update

Apply the best suitable orbit state vectors available at processing time. Prefer precise orbit files when available; if only restituted or predicted orbit information is available, record that fact and do not silently describe it as precise.

Record the orbit filename, type, publication date and whether SNAP actually applied it. A successful operator exit alone is not proof that the intended orbit file was used.

### 3. Noise and border handling

Inspect product annotations and SNAP operator documentation before applying thermal-noise removal. Use the operator only where it is applicable and supported by the product metadata. Avoid double correction or unexamined processing of noise profiles.

Apply GRD border-noise removal and retain the resulting valid-data mask. Do not replace removed edge pixels with zeros and then treat those zeros as valid backscatter.

### 4. Radiometric calibration

Calibrate VV and VH to Sigma0 in **linear power units**. Keep the linear calibrated output as the primary quantitative product. Record the calibration output bands and confirm the units and scaling from the SNAP product metadata.

For this baseline recipe, Sigma0 is the required output. Gamma0 or terrain-flattened backscatter may be produced as a separate, explicitly justified branch; do not label ordinary geometric terrain correction as radiometric terrain flattening.

### 5. Speckle treatment — optional branch

Do not make spatial despeckling mandatory for the baseline temporal stack. Spatial filters trade noise reduction against edge and small-object preservation. For change detection, independently filtering each date can also change the signal being compared.

Retain an unfiltered calibrated branch. If a filtered branch is needed, select the filter and window based on the target phenomenon, test edge preservation and small-target loss, and record the parameters. Link the selected method to the [Lee speckle filter algorithm record](../../algorithms/remote-sensing/lee-speckle-filter.md).

### 6. Geometric terrain correction

Use Range-Doppler terrain correction with one documented DEM and the same target CRS/grid across all acquisitions. For Nairobi, EPSG:32737 is the proposed projected output CRS.

Choose pixel spacing deliberately. A 10 m output grid is a sampling interval, not a claim that Sentinel-1 IW GRD has 10 m ground resolution. For a conservative comparison, evaluate a 20 m analysis grid against the native sampling and target scale; record any resampling. Use a continuous-data resampler for backscatter and nearest-neighbour resampling for categorical masks.

Geometric terrain correction addresses geolocation and terrain displacement. It does not, by itself, remove all radiometric terrain effects. If local relief materially affects the analysis, design and validate a separate radiometric terrain-flattening branch rather than assuming the geometric correction has done it.

### 7. Linear-to-decibel conversion

For positive linear backscatter power, convert to dB using:

\[
\sigma^0_{\mathrm{dB}} = 10\log_{10}(\sigma^0)
\]

Do not use the amplitude conversion factor of 20 for calibrated power. Preserve NoData and invalid masks; never evaluate the logarithm on zero or negative values. Keep linear Sigma0 available even when dB is the preferred display format.

For a temporal difference in dB:

\[
\Delta \sigma^0_{\mathrm{dB}} =
\sigma^0_{\mathrm{dB},t_2} - \sigma^0_{\mathrm{dB},t_1}
= 10\log_{10}\left(\frac{\sigma^0_{t_2}}{\sigma^0_{t_1}}\right)
\]

Interpret the difference only after confirming compatible acquisition geometry, masks, calibration, grid alignment and processing choices.

## Nairobi temporal-stack design

The four current full-AOI candidates are:

| Acquisition (UTC) | Platform | Orbit | Polarisation | Slice |
|---|---|---|---|---|
| 2026-10-09 03:11:12.665772 | Sentinel-1C | Descending, relative 79 | VV/VH | 4 of 11 |
| 2026-10-21 03:11:12.521298 | Sentinel-1C | Descending, relative 79 | VV/VH | 4 of 11 |
| 2026-11-02 03:11:12.222559 | Sentinel-1C | Descending, relative 79 | VV/VH | 4 of 11 |
| 2026-11-14 03:11:11.786734 | Sentinel-1C | Descending, relative 79 | VV/VH | 4 of 11 |

The catalogue dates are spaced by 12 days. This is a promising repeat-observation design, not proof that the four scenes are interchangeable. Before stacking, compare incidence-angle ranges, acquisition timing, processing baseline, noise annotations, valid-data masks and slice boundaries. A slice is not the complete datatake: determine whether adjacent slices are required for the study extent and preserve the slice context.

## Quality gates

A scene is not accepted as analysis-ready until all applicable checks pass:

| Gate | Evidence |
|---|---|
| Archive integrity | ZIP CRC test and SHA-256 recorded |
| SAFE structure | Manifest, measurement and annotation files present |
| Channel completeness | VV and VH measurement files verified |
| Metadata consistency | UUID, product name, time, platform, orbit, slice and baseline reconciled |
| Orbit correction | Applied orbit type and filename recorded |
| Noise handling | Operator applicability and valid-data mask inspected |
| Calibration | Sigma0 bands and units confirmed from metadata |
| Geometry | CRS, transform, pixel spacing, extent and DEM recorded |
| NoData | Border and invalid pixels masked, not treated as measurements |
| Temporal comparability | Same orbit direction/relative orbit, compatible geometry and processing |
| Visual inspection | VV/VH quicklooks and edge/noise artefacts reviewed |
| Reproducibility | SNAP version, graph, parameters, logs and output checksums retained |

Failure at any critical gate means the scene remains a candidate or intermediate, not an analysis-ready layer.

## Expected outputs

Keep each processing stage distinct and preserve immutable raw inputs:

- original downloaded SAFE archive and download provenance sidecar;
- SNAP processing log and version record;
- calibrated linear Sigma0 VV/VH product;
- terrain-corrected linear Sigma0 VV/VH GeoTIFFs;
- optional dB derivatives;
- valid-data / border-noise masks;
- per-scene QA report and quicklook;
- temporal-stack manifest with input checksums, acquisition metadata and common-grid specification.

Never overwrite the source archive. Do not commit large satellite archives or generated rasters to the source repository; use an appropriate data store and retain stable references and checksums.

## Current limitations and next execution

This recipe is a documented processing design, not an executed workflow. No Nairobi SAFE archive has yet passed the download gate in this repository, no SNAP graph has been run, and no backscatter values or change interpretations are reported.

The next execution is deliberately one-scene-at-a-time: download and inspect the 2 November candidate, validate its SAFE content and measurement channels, run the baseline SNAP graph, inspect outputs and QA, then repeat for the other three dates only after the first scene passes.

## References

- [Copernicus Data Space — Sentinel-1 product characteristics](https://documentation.dataspace.copernicus.eu/Data/SentinelMissions/Sentinel1.html)
- [Copernicus Data Space — OData product and download documentation](https://documentation.dataspace.copernicus.eu/APIs/OData.html)
- [ESA SNAP Toolbox](https://step.esa.int/main/toolboxes/snap/)
- [Sentinel-1 GRD processing overview](https://developers.google.com/earth-engine/guides/sentinel1)

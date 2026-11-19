# Radar source notes and evidence register

**Review date:** 19 November 2026  
**Scope:** First release of the Earth-observation SAR pathway, with radar branches mapped for orientation.  
**Editorial status:** Sources checked for relevance and technical role. No claim is made that every branch in the territory map has a complete literature review.

## How to use this register

A resource is included because it performs a defined job in the exploration. Primary mission/product documentation should control product definitions and processing assumptions. Training resources help readers build intuition and practical skill. Derived-product guides are useful only when the reader understands which processing choices produced the data.

A source being authoritative for one task does not make it authoritative for every claim. For example, an RTC product guide describes that provider's processing choices; it is not a universal prescription for all SAR applications.

## Core sources

| Source | Authority and best use | Important caveat |
|---|---|---|
| [Sentinel-1 Product Definition, issue 2/8 (2025)](https://sentiwiki.copernicus.eu/__attachments/1673968/S1-RS-MDA-52-7440-Sentinel-1-Product-Definition-2025-2.8.pdf) | Mission/product-level reference. Use for SLC/GRD definitions, product structure, acquisition modes and product characteristics. | Technical specification, not a beginner tutorial or a processing recipe. Check for a newer issue before relying on version-specific details. |
| [ASF HyP3 Sentinel-1 RTC Product Guide](https://hyp3-docs.asf.alaska.edu/guides/rtc_product_guide/) | Detailed description of ASF RTC products, radiometry, output scale, pixel spacing, DEM and optional speckle filtering. | Describes ASF's product and options. Other RTC pipelines may make different choices. Record product metadata. |
| [ESA Sentinel-1 Toolbox features](https://step.esa.int/main/toolboxes/sentinel-1-toolbox/s1tbx-features/) | Confirms SNAP/S1TBX capabilities including calibration, orbit handling, filtering, terrain correction and InSAR tools. | Feature list, not a complete operator guide. Use current operator documentation for parameters and version behaviour. |
| [Copernicus Data Space — Sentinel-1 GRD documentation](https://documentation.dataspace.copernicus.eu/APIs/SentinelHub/Data/S1GRD.html) | Documents the processing chain and coefficient options exposed by Sentinel Hub. Useful for understanding prepared GRD backscatter products. | Service-specific. Do not assume every Copernicus or third-party product uses the same defaults. |
| [NASA / ASF Introduction to SAR](https://asf.alaska.edu/trainings/arset-an-introduction-to-synthetic-aperture-radar-sar-and-its-applications/) | Accessible introduction to SAR and Earth-observation applications. | Introductory material; follow primary technical sources for detailed processing or quantitative claims. |
| [ASF SAR learning resources](https://asf.alaska.edu/learn/) | Conceptual and practical SAR learning material, including interpretation and applications. | Individual resources may have different dates and product assumptions. Check the specific lesson. |
| [ESA SNAP SAR training resource](https://knowledge-hub-gda.esa.int/training_resource/working-with-sar-data-snap/) | Practical orientation to processing SAR data in SNAP. | Interface and operator details can change. Match the lesson to the exact product and installed SNAP version. |
| [ASF Vertex](https://search.asf.alaska.edu/) | Data discovery and access to Sentinel-1 scenes and available derived products. | A portal is a discovery/access tool, not independent validation of the scientific interpretation. |

## Claims checked for the first practical investigation

### 1. GRD and SLC are not interchangeable

The Sentinel-1 Product Definition distinguishes Slant Range Single-Look Complex (SLC) products from Ground Range Multi-Look Detected (GRD) products. GRD is detected and multi-looked; SLC retains complex information needed for phase-based applications such as conventional interferometry. The first backscatter exercise therefore uses GRD or an RTC derivative, not SLC as if all product types were equivalent.

### 2. Calibration and terrain correction answer different questions

Radiometric calibration relates image values to a defined backscatter coefficient. Terrain correction / radiometric terrain correction addresses geometric and terrain-related effects and produces map-oriented products. Product providers may combine these operations with noise removal and other steps. The reader must record the coefficient, scaling, DEM and processing provenance rather than merely write “processed”.

### 3. Backscatter coefficient and scale must be recorded

The ASF RTC guide documents gamma-nought and sigma-nought options, and power, amplitude and decibel output scales. The Copernicus Sentinel Hub documentation describes its own coefficient options and notes that the returned values are linear power for the selected coefficient. These conventions are not interchangeable without conversion and context.

### 4. Speckle filtering is an analytical choice

ASF explains that its optional Enhanced Lee filter can smooth the product but reduces spatial resolution. Whether to filter depends on the application; temporal aggregation or no filtering may be preferable in some workflows. The lab therefore does not make despeckling a mandatory default.

### 5. Visual brightness is not a land-cover label

Backscatter depends on the surface and acquisition geometry, including roughness, moisture, vegetation structure, polarisation and incidence angle. Bright/dark heuristics are useful prompts only. A defensible application needs domain context and independent reference evidence.

## What is not yet established

- No scene-specific Sentinel-1 data have been downloaded and processed as part of this documentation pass.
- No backscatter values, classification accuracy, flood extent or deformation result is claimed.
- The weather radar, radar engineering, maritime, automotive and advanced PolSAR/InSAR branches are mapped at orientation level only; each needs its own curated evidence set and practical test before being presented as a developed pathway.
- The initial exercise does not establish a validated operational method for flood mapping, land-cover classification or change detection.

## Review triggers

Recheck this register when:
- ESA updates Sentinel-1 product specifications or SNAP/S1TBX behaviour;
- ASF changes RTC product options or processing methodology;
- a new practical exercise relies on a different product type, coefficient, sensor or derived dataset;
- a source link or training interface becomes unavailable;
- a publication makes a new quantitative or application-specific claim.

## Publication gate

Before publishing a scene-specific practical result, archive the exact input product ID, acquisition metadata, product type, processing software/version, parameters, DEM and reference data. Include the processing graph or script where possible. Have a second reviewer inspect the interpretation and limitations.

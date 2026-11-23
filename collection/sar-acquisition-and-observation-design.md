# SAR acquisition and observation design

**Record type:** Canonical collection method  
**Scope:** Earth-observation synthetic aperture radar (SAR), with Sentinel-1 as the first bounded reference case  
**Status:** Initial method published; technical review, scene execution and application testing pending  
**Method boundary:** Defines how to specify, discover, acquire, screen and document SAR observations. It is not a SAR processing recipe, algorithm specification or validated application workflow.

## 1. Purpose: acquire an observation that can answer a defined question

SAR acquisition should begin with the intended measurand and decision, not with whichever image is easiest to download.

A SAR product is the output of an active microwave measurement system. The recorded signal depends on transmitted waveform and frequency, antenna and platform geometry, target scattering, polarisation, system calibration, processing and product representation. A map-ready raster is not a neutral photograph of the ground.

Before searching, write a short observation brief:

| Design question | Required record |
|---|---|
| What phenomenon or quantity is being investigated? | For example, calibrated backscatter, coherence, line-of-sight displacement, inundation evidence or wave/ocean parameters |
| What decision or scientific claim could the observation support? | State the intended claim and its spatial and temporal scope |
| What is the target area? | AOI geometry, CRS, boundary source/version and buffer rationale |
| What spatial detail is needed? | Minimum feature size, required resolution and acceptable pixel spacing |
| What temporal design is needed? | Single date, repeated observations, event window, seasonal series or interferometric pair/stack |
| What observation geometry is acceptable? | Pass direction, relative orbit/track, incidence-angle range, look direction and coverage |
| What polarisation is needed? | Single or dual/multiple channels, with a physical reason |
| What product information must be retained? | Product type, mode, processing level, calibration, orbit and provenance |
| What independent evidence will test the interpretation? | Field data, event records, reference maps, corner reflectors, GNSS or other appropriate observations |

A requirement that is not tied to the question should not become an arbitrary filter. Conversely, a convenient scene should not redefine the scientific question after the fact without documenting the change.

## 2. Identify the measurement family

This method concerns Earth-observation SAR: an active microwave instrument transmits a signal and records returned echoes while the platform moves. Synthetic aperture processing combines observations along the platform trajectory to form an image.

Do not collapse the following into one generic “radar image” category:

- **Satellite/airborne SAR:** coherent imaging of the Earth's surface, with product families for amplitude/backscatter, interferometry and polarimetry.
- **Weather radar:** observes atmospheric targets using scanning strategies and variables such as reflectivity and radial velocity.
- **Maritime, automotive and surveillance radar:** application-specific sensing and detection systems with different geometry, clutter, temporal and operational requirements.

These domains share electromagnetic and signal-processing foundations but not interchangeable acquisition procedures.

For a SAR observation brief, identify the sensor and mission, operating frequency/wavelength, acquisition mode, polarisation, platform and product family. Sentinel-1 is a C-band mission; do not transfer its mode names, product structure or acquisition characteristics to another SAR mission without checking that mission's documentation.

## 3. Choose the product family to match the measurand

### 3.1 Detected products for amplitude/backscatter analysis

A Level-1 Ground Range Detected (GRD) product is detected and multilooked, with samples represented in ground-range geometry. It is appropriate for many amplitude/backscatter investigations after the product's calibration, noise treatment, geometry and processing history have been checked.

GRD does **not** preserve the complex phase needed for conventional interferometric processing. A GRD scene cannot be substituted for an SLC merely because both depict the same area and date.

### 3.2 Complex products for phase-sensitive analysis

A Level-1 Single Look Complex (SLC) product retains complex in-phase and quadrature information, carrying amplitude and phase in slant-range/azimuth geometry. SLC is the normal starting product family for conventional repeat-pass InSAR and many polarimetric workflows, subject to the mission and application requirements.

SLC is not automatically analysis-ready. Interferometric work additionally requires compatible acquisitions, precise geometry/orbit information, co-registration and suitable temporal/spatial coherence.

### 3.3 Derived products

Products such as radiometrically terrain-corrected (RTC) backscatter are processed derivatives. They can reduce the burden of preparing amplitude data for GIS analysis, but their radiometric convention, DEM, geocoding, pixel spacing, filtering and processing provenance must be recorded.

A derived product is not interchangeable with the original Level-1 product or with another provider's derivative. Compare the actual processing specifications, not just product names.

### 3.4 Sentinel-1 acquisition modes

Sentinel-1 documentation distinguishes Stripmap (SM), Interferometric Wide swath (IW), Extra Wide swath (EW) and Wave (WV) modes. Mode choice controls coverage, resolution, sampling and acquisition design; it is not a cosmetic metadata field.

- **IW:** a common land-observation mode and the starting mode in the Nairobi study specification.
- **EW:** wider-swath observations used in particular coverage/application contexts, including some coastal and maritime contexts.
- **SM:** narrower, higher-detail acquisition configurations for selected targets.
- **WV:** vignette-based wave observations, not a general substitute for a contiguous land-imaging scene.

The available mode, resolution class and polarisation combinations depend on the product and mission acquisition. Confirm them in the current mission specification and actual product metadata.

## 4. Select polarisation deliberately

Polarisation describes the orientation of the transmitted and received electric-field components. Sentinel-1 product labels commonly distinguish channels such as VV, VH, HH and HV.

Select channels because they contribute to the observation question, not because “dual polarisation is always better”. Channel availability varies by mode, acquisition and product. A product labelled with a dual-polarisation configuration may be incomplete or distributed with only one channel in a particular derivative.

Record:
- transmit/receive polarisation channels actually present;
- whether channels are co-polarised or cross-polarised;
- channel naming convention and product metadata;
- any channel-specific calibration, noise or missing-data condition.

Polarisation differences can help investigate scattering mechanisms, but no channel uniquely identifies a land-cover class or physical state. Interpretation requires wavelength, geometry, target structure, moisture and reference evidence.

## 5. Design acquisition geometry and temporal compatibility

SAR is side-looking. Acquisition geometry is part of the measurement and can materially change the observed return.

Record and assess:

- **Orbit/pass direction:** ascending or descending.
- **Relative orbit / track:** preserve the mission's orbit identifiers exactly.
- **Incidence angle:** distinguish the product's reported angle from local incidence angle where terrain is involved.
- **Look direction and viewing geometry:** retain the metadata needed to understand which side of the platform illuminated the target.
- **Swath and burst coverage:** especially for burst-mode products and partial-area acquisitions.
- **Acquisition time:** UTC timestamp and local event/field context.
- **Platform and instrument identity:** mission/platform and sensor.
- **Orbit state and auxiliary data:** orbit-file type, version and whether a precise orbit was available/applied.

For repeated amplitude observations, comparable orbit direction, relative orbit, mode, polarisation, incidence-angle behaviour, processing and radiometric convention generally improve interpretability. They do not guarantee perfect equivalence.

For interferometry, use compatible SLC acquisitions and assess:
- same sensor/mode and compatible sub-swath/burst coverage;
- acquisition geometry and orbit relationship;
- temporal separation and perpendicular baseline;
- common burst overlap and valid common footprint;
- precise orbit availability and processing compatibility;
- temporal, geometric and volume decorrelation risks.

Do not assume that two scenes are compatible merely because they intersect the same AOI, share an orbit label, or were acquired on nearby dates. Verify the actual identifiers, footprint, geometry and product metadata.

### Temporal design depends on the phenomenon

- **Flooding:** choose pre-event baseline(s), event/post-event observations and a time window that reflects flood dynamics. Consider rainfall, river levels, acquisition timing, wind, vegetation and permanent water.
- **Ground deformation:** define a time series or pair/stack with appropriate SLC data, temporal sampling and baseline constraints; establish an independent deformation reference where possible.
- **Agriculture/vegetation:** consider crop calendar, seasonal moisture and canopy development, and maintain acquisition consistency.
- **Urban/built environment:** account for geometry, building orientation, shadow/layover and temporal construction/change.
- **Coastal/ocean applications:** ensure the mode and product family are suitable for the actual oceanographic measurand.

A pre/post pair is not automatically a valid change design. Document event timing, expected persistence and alternative explanations.

## 6. Discover candidate observations

Use a mission archive or catalogue that exposes product metadata and stable identifiers. For Sentinel-1, practical discovery routes include:

- [Copernicus Data Space Ecosystem — Sentinel-1](https://dataspace.copernicus.eu/data-collections/copernicus-sentinel-missions/sentinel-1)
- [Copernicus Data Space Sentinel-1 documentation](https://documentation.dataspace.copernicus.eu/Data/Sentinel1.html)
- [Copernicus Data Space OData catalogue documentation](https://documentation.dataspace.copernicus.eu/APIs/OData.html)
- [Copernicus Browser](https://browser.dataspace.copernicus.eu/)
- [Alaska Satellite Facility Vertex](https://search.asf.alaska.edu/)
- [ASF HyP3 product documentation](https://hyp3-docs.asf.alaska.edu/products/)

Catalogue search should use:
1. AOI geometry or a clearly described spatial query;
2. acquisition time window;
3. mission/platform and instrument;
4. acquisition mode;
5. product type/processing level;
6. polarisation;
7. pass direction and relative orbit where relevant;
8. coverage/footprint and product availability.

Treat search results as candidates, not accepted observations. Inspect the full metadata and product footprint. Confirm whether the data asset can actually be accessed, downloaded or processed under the required terms.

For reproducible discovery, preserve the query, catalogue/provider, query timestamp, result identifiers and selection rationale. If a provider returns a derived RTC product, preserve its link to the source acquisition and its processing metadata.

## 7. Inspect the product before accepting it

Create a product manifest before processing. At minimum, record the fields below where available.

| Metadata group | Required fields |
|---|---|
| Identity | Mission, platform, instrument, product identifier, provider, product URI, acquisition start/end time |
| Acquisition | Mode, swath/sub-swath, burst identifiers where relevant, pass direction, relative orbit/track, incidence-angle information |
| Signal | Frequency/wavelength, polarisation channels, product type, resolution class |
| Processing | Processing level, processing baseline/software where exposed, product generation time, source product, provider workflow |
| Radiometry | Calibration state, coefficient (β⁰, σ⁰ or γ⁰), value scale (linear power, amplitude or dB), units, noise treatment |
| Geometry | Footprint, native geometry, map projection/grid if derived, pixel spacing, DEM and geocoding/terrain-correction method |
| Auxiliary data | Orbit file type/version, calibration/noise annotations, DEM source/version and relevant auxiliary datasets |
| Quality | Coverage, missing bursts/swaths, border/thermal noise checks, saturation or invalid values, layover/shadow indicators, known artefacts |
| Provenance | Catalogue query, access time, checksum if available, licence/terms, retrieval method, processing history and retained files |

### Radiometric conventions

Do not write only “backscatter”. Record the actual coefficient and scale.

- **β⁰ (beta nought):** normalised with respect to a slant-range reference area.
- **σ⁰ (sigma nought):** normalised with respect to a ground-area reference.
- **γ⁰ (gamma nought):** normalised with respect to an area perpendicular to the line of sight.

The exact definition and implementation must be checked for the product/provider. These quantities are not interchangeable labels. If converting power to decibels, record the conversion and use the correct power convention; amplitude and power conversions differ.

A display stretch, byte-scaled quicklook or arbitrary image export is not a quantitative backscatter dataset. Preserve the source numeric values and metadata.

## 8. Quality screening and acceptance gates

A scene can be present in a catalogue and still be unsuitable. Apply gates before analysis.

### Gate A — question and product fit
- Does the product family preserve the information required by the measurand?
- Is the acquisition mode and polarisation suitable?
- Is the spatial and temporal sampling adequate?
- Is the product level and provider processing understood?

**Reject or redesign** if, for example, GRD is selected for conventional phase-based InSAR.

### Gate B — spatial and temporal coverage
- Does the product footprint cover the AOI and required buffer?
- Are required sub-swaths/bursts present and usable?
- Is the acquisition time inside the event/season window?
- Are there gaps, partial coverage or edge effects that affect the intended output?

### Gate C — geometry compatibility
- Are pass direction, relative orbit, incidence angle and look geometry suitable?
- For time series, are acquisitions sufficiently comparable?
- For InSAR, are common coverage, burst alignment, baseline and co-registration feasibility established?

### Gate D — radiometric and signal quality
- Is the calibration state understood?
- Have thermal/border noise and relevant product artefacts been assessed?
- Are the selected channels present and valid?
- Are coefficient, scale and units known?
- Is the DEM/terrain treatment appropriate to the terrain and application?
- Are layover, foreshortening and radar shadow mapped or otherwise considered?

### Gate E — provenance and access
- Is the original product identifier retained?
- Can the actual assets be read and verified?
- Are checksums or equivalent integrity checks available?
- Are licence, terms and provider attribution recorded?
- Is the full processing lineage recoverable?

A successful download passes only an access check. It does not establish calibration correctness, scientific suitability or fitness for purpose.

## 9. Branch-specific acquisition requirements

### 9.1 Amplitude/backscatter

For a single-date or multi-date backscatter analysis, decide whether original GRD or a documented RTC derivative is appropriate. Preserve coefficient, scale, calibration/noise handling, DEM, terrain correction, speckle treatment and grid.

Do not automatically apply a speckle filter. Filtering can change spatial detail and statistics. Justify it for the target scale and analysis, compare filtered/unfiltered data where appropriate, and record the method and parameters.

### 9.2 Interferometric SAR

For conventional repeat-pass InSAR, acquire SLC data rather than detected GRD. Establish a compatible pair/stack and retain precise orbit and acquisition metadata. The acquisition record must include the temporal and perpendicular baseline information used in pair selection, common burst coverage and the plan for co-registration.

The later processing chain may include co-registration, interferogram formation, coherence estimation, removal/modelling of topographic phase, filtering, phase unwrapping, atmospheric treatment, reference selection and displacement conversion. Those are downstream processing and algorithm decisions, not steps completed by acquisition alone.

Phase can include deformation, topography, atmosphere, orbit error, noise and decorrelation contributions. An interferogram is not a direct deformation map. Require an explicit geometry model and independent evidence appropriate to the displacement claim.

### 9.3 Polarimetric SAR

For polarimetric analysis, verify that the required channels and calibration information are present and mutually consistent. Determine whether the task requires dual-pol or full-pol data and whether the mission/mode actually supplies them. Do not infer full polarimetric capability from a dual-polarisation VV/VH or HH/HV product.

## 10. Acquisition record template

Copy and complete this record for each accepted observation or acquisition set.

### Study design
- **Study/application question:**
- **Measurand / intended claim:**
- **AOI and boundary source/version:**
- **Spatial detail and temporal requirements:**
- **Independent reference / validation plan:**

### Candidate and selected product
- **Catalogue/provider and query timestamp:**
- **Search query / AOI:**
- **Mission/platform/instrument:**
- **Product identifier and URI:**
- **Product type and processing level:**
- **Acquisition mode / swath / burst:**
- **Acquisition start/end (UTC):**
- **Pass direction / relative orbit:**
- **Incidence-angle information:**
- **Polarisation channels present:**
- **Footprint and coverage assessment:**

### Processing and measurement metadata
- **Calibration state and coefficient:**
- **Value scale and units:**
- **Thermal/border noise treatment:**
- **Orbit auxiliary file and version:**
- **DEM source/version:**
- **Terrain correction / RTC method:**
- **Pixel spacing, CRS and grid:**
- **Speckle filtering (if any):**
- **Provider/software/version and parameters:**
- **Source product and processing lineage:**

### Quality and decision
- **Coverage and data integrity checks:**
- **Geometry suitability:**
- **Radiometric/signal quality checks:**
- **Known distortions/limitations:**
- **Licence and attribution:**
- **Decision:** accepted / accepted with limitations / rejected / pending
- **Reason and reviewer:**
- **Next evidence gate:**

For an InSAR pair or stack, attach one record per acquisition plus a pair table containing temporal baseline, perpendicular baseline, common burst coverage, orbit source and pair-selection rationale.

## 11. Common failure modes

| Failure | Why it matters | Better practice |
|---|---|---|
| Choosing GRD for conventional InSAR | Detected GRD has lost complex phase | Select compatible SLC acquisitions |
| Comparing arbitrary scenes | Geometry, season, moisture and processing may differ | Control and document orbit, mode, polarisation, timing and processing |
| Treating all RTC products as equivalent | Providers use different DEMs, grids, radiometry and processing choices | Record the exact provider product specification and metadata |
| Confusing pixel spacing with spatial resolution | Sampling interval is not the same as resolving power | Record both where available and use mission specifications |
| Interpreting dB values as linear power | Statistics and thresholds become wrong | Preserve scale and convert explicitly |
| Assuming dual-pol is full-pol | Required polarimetric information may be absent | Check actual channels and product family |
| Ignoring terrain geometry | Layover, foreshortening and shadow can mimic or obscure surface patterns | Inspect incidence/local geometry and DEM-derived quality layers |
| Filtering by default | Spatial detail and statistical behaviour can change | Justify, compare and record filtering |
| Treating scene discovery as acquisition | Metadata may exist while assets are inaccessible or incomplete | Verify asset access, integrity and licence |
| Treating acquisition as validation | A suitable image does not prove the application claim | Define independent evidence and acceptance criteria |

## 12. Links to the wider Spatial Methods system

- [Remote-sensing cross-pillar pathway](../learning-paths/remote-sensing-cross-pillar-pathway.md) — connects foundations, collection, algorithms and practical evidence.
- [Radar exploration](../explorations/radar/README.md) — curiosity-led entry to Earth-observation SAR and other radar branches.
- [Radar territory map](../explorations/radar/territory-map.md) — distinguishes SAR, weather radar, systems engineering and signal processing.
- [Nairobi Sentinel-1 scene record](../explorations/radar/nairobi-sentinel-1-scene-record.md) — a study specification only; no scene is selected or processed by this method publication.
- [Sentinel-1 backscatter investigation](../explorations/radar/sentinel-1-backscatter-investigation.md) — a guided interpretation exercise, not a validated recipe.
- [Lee speckle filter](../algorithms/remote-sensing/lee-speckle-filter.md), [SAR CFAR](../algorithms/remote-sensing/sar-cfar.md) and [local InSAR coherence](../algorithms/remote-sensing/insar-local-coherence.md) — scoped algorithm records, not acquisition substitutes.
- [Electromagnetic observations and radiometric quantities](../foundations/remote-sensing-physics/electromagnetic-observations-and-radiometric-quantities.md) — shared radiometric foundation; radar-specific scattering and signal formation remain to be developed.

## 13. Evidence status and review requirements

This is an initial canonical method record based on mission/product documentation and provider-specific processing guidance. It has not yet been independently technically reviewed or tested end to end against a selected Sentinel-1 scene.

The existing Nairobi scene record remains a specification: product identifier, acquisition date, orbit, polarisation, coefficient, processing metadata and observations are pending. No Nairobi scene acquisition, processing result, flood extent, land-cover classification, deformation measurement or accuracy statistic is claimed here.

Before this method is promoted:
1. Review the product-family and geometry guidance against the current Sentinel-1 specification.
2. Test discovery and asset retrieval for a specific, documented scene.
3. Complete the acquisition manifest from actual product metadata.
4. Have a second reviewer inspect product suitability and processing provenance.
5. Link a tested application recipe only after its processing and validation gates have been executed.

## Sources and technical references

- [Sentinel-1 Product Specification, issue 3/16 (2025)](https://sentiwiki.copernicus.eu/__attachments/1673968/S1-RS-MDA-52-7441%20-%20Sentinel-1%20Product%20Specification%202025%20-%203.16.1.pdf) — product family, acquisition modes, product types and product characteristics.
- [Sentinel-1 Product Definition, issue 2/8 (2025)](https://sentiwiki.copernicus.eu/__attachments/1673968/S1-RS-MDA-52-7440-Sentinel-1-Product-Definition-2025-2.8.pdf) — SLC/GRD definitions and product structure.
- [Copernicus Data Space Sentinel-1 documentation](https://documentation.dataspace.copernicus.eu/Data/Sentinel1.html) — product access, product families and auxiliary orbit products.
- [ASF Sentinel-1 RTC Product Guide](https://hyp3-docs.asf.alaska.edu/guides/rtc_product_guide/) — ASF-specific RTC processing, radiometry, DEM, geocoding and output metadata.
- [Digital Earth Africa Sentinel-1 backscatter specifications](https://docs.digitalearthafrica.org/en/latest/data_specs/Sentinel-1_specs.html) — backscatter normalisation conventions and terrain-related considerations.
- [ASF Vertex](https://search.asf.alaska.edu/) — scene discovery and access.

Mission specifications define the sensor product; provider guides define the processing of that provider's derivative. Neither replaces study-specific design, independent review or validation.

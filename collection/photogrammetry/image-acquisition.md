# Photogrammetric image acquisition: designing observations before processing

> **Subject:** SM-COL-007 — Photogrammetry and structure from motion  
> **Connected subjects:** SM-COL-004, SM-COL-009, SM-COL-001, SM-FND-011, SM-FND-012, SM-REC-007  
> **Status:** Initial technical synthesis; independent specialist review and field testing pending  
> **Audience:** Intermediate undergraduate to postgraduate learners, practitioners and researchers

## 1. The problem begins before the software

A photogrammetric model is constrained by the images that were acquired. Processing software cannot reliably reconstruct detail that was never imaged, infer stable geometry from weak image overlap, or turn poorly controlled observations into independently verified survey measurements.

The acquisition problem is therefore not simply “choose a drone and fly a grid.” It is to design a set of images whose image scale, overlap, viewing geometry, sharpness, radiometric quality, control and metadata are appropriate for a stated measurement or mapping objective.

This applies to aerial cameras on crewed aircraft, uncrewed aircraft systems (UAS), close-range cameras and suitable historical image archives. UAS examples are common, but the principles are not drone-specific.

## 2. What is actually measured?

A frame camera records image-plane measurements of incoming light. A pixel value is a sampled sensor response, not a direct measurement of ground position or elevation. Photogrammetric reconstruction uses image correspondences, camera geometry, calibration and control to infer object-space coordinates.

A simplified central-perspective model is:

[
x' = -f\frac{X_c}{Z_c},\qquad
y' = -f\frac{Y_c}{Z_c}
]

where ((X_c,Y_c,Z_c)) are object coordinates expressed in the camera coordinate system, (f) is focal length, and ((x',y')) are ideal image-plane coordinates under the chosen sign convention. Real camera models also account for principal point, lens distortion, sensor geometry and other effects.

The practical chain is:

1. Light from the scene passes through the optical system.
2. The sensor integrates a signal during exposure.
3. Pixels sample that signal in a camera coordinate system.
4. Corresponding image features are identified across views.
5. Camera interior and exterior orientation are estimated or supplied.
6. Multi-view geometry is used to infer three-dimensional structure.
7. Ground control and reference information connect the reconstruction to a real-world frame.
8. Independent check observations assess the resulting product.

Each stage introduces assumptions and potential error. The output is an estimate, not an unmediated copy of the ground.

## 3. Ground sample distance is not positional accuracy

For a near-nadir pinhole camera over locally planar ground, approximate ground sample distance is:

[
GSD = \frac{H p}{f}
]

where:

- (H) is camera height above the local ground;
- (p) is physical pixel pitch;
- (f) is focal length;
- all lengths use consistent units.

GSD approximates the ground distance represented by one image pixel near the assumed geometry. It is not a statement of horizontal or vertical positional accuracy, object-detection certainty, or final product resolution.

A smaller GSD can make targets easier to identify, but accuracy also depends on camera calibration, image geometry, control quality, surface texture, matching, processing, terrain and independent validation. The USGS UAS calibration report explicitly cautions against inferring product accuracy from GSD alone and discusses the importance of control-point quality and tie-point distribution.

## 4. Image footprint and overlap

For a rectangular sensor with physical width (W) and height (L), a near-nadir camera at height (H) above a flat surface has approximate ground footprint dimensions:

[
F_W = \frac{H W}{f},\qquad F_L = \frac{H L}{f}
]

If forward overlap is (o_f) and side overlap is (o_s), expressed as fractions between zero and one, approximate maximum image-centre spacings are:

[
d_f = F_L(1-o_f),\qquad
d_s = F_W(1-o_s)
]

The mapping between sensor width/height and flight/side direction depends on camera orientation. Confirm the actual sensor orientation and flight direction rather than assuming the labels.

These equations are planning approximations. They assume a near-nadir camera, locally planar terrain, constant height above ground, negligible attitude variation and a simple rectangular footprint. Terrain relief, camera tilt, rolling shutter, variable speed, turns and irregular boundaries change effective overlap.

### Why overlap matters

A point visible in several images can be observed from multiple camera positions. The intersecting viewing rays provide geometric constraints. More overlap can increase redundancy and the number of image observations, but overlap percentage alone does not guarantee strong geometry.

The quality of the intersection geometry matters. Images captured from nearly identical positions may add less depth information than images with useful baseline and convergence. A block with parallel nadir images can be weak in some directions, particularly for camera self-calibration and height determination. Oblique and cross-strip imagery can add geometric diversity, but should be designed for the project rather than added mechanically.

There is no universal overlap percentage suitable for every sensor, terrain, surface and deliverable. Published guidance differs by platform and task. USGS guidance describes orthogonal cross-flight patterns as a way to strengthen camera calibration in its stated UAS context; it should not be treated as a universal flight prescription.

## 5. The acquisition design

### 5.1 Start with the deliverable and acceptance requirement

Specify the product and intended use before choosing flight settings:

- orthomosaic, surface model, terrain model, point cloud, mesh or feature extraction;
- required spatial extent, coordinate reference and vertical reference;
- minimum feature size or target visibility;
- horizontal and vertical accuracy requirements, if applicable;
- required temporal consistency and radiometric comparability;
- independent validation method and acceptance criteria.

A centimetre-scale GSD is not a substitute for a defensible accuracy requirement.

### 5.2 Camera and sensor behaviour

Record the camera model, sensor dimensions, pixel pitch where known, focal length, lens configuration, focus, shutter type, exposure settings and calibration information.

Fixed focal length and stable focus simplify some acquisition designs. A global shutter exposes the sensor at approximately one instant; a rolling shutter exposes rows at different times and can interact with platform motion. Neither label alone establishes product quality: actual sensor behaviour, motion, exposure and processing model matter.

### 5.3 Motion and image sharpness

Image motion during exposure can blur features and weaken image matching. Exposure time, ground speed, image scale, platform vibration and camera stabilisation all contribute.

A first-order ground-motion distance during exposure is:

[
b_g \approx v_g t_e
]

where (v_g) is ground-relative speed and (t_e) is exposure duration. This is a simplified estimate, not a complete blur model; camera rotation, image scale, shutter readout and motion direction also matter.

Do not rely on overlap to compensate for blurred images.

### 5.4 Lighting and scene properties

Image matching needs identifiable, sufficiently stable features. Consider:

- illumination and shadow length;
- changing cloud and illumination conditions;
- repetitive or texture-poor surfaces;
- water, specular surfaces and transparent materials;
- moving vegetation, vehicles, people and water;
- wind-driven movement between exposures;
- seasonal or temporal changes in the scene.

A surface can be visible but unsuitable for reliable correspondence. A dense point cloud can represent canopy tops rather than bare earth where vegetation obscures the ground.

### 5.5 Flight or camera geometry

A simple parallel strip pattern may be adequate for some flat, open mapping tasks. More complex scenes can require cross-strips, oblique images, convergent views, multiple heights or ground-based images.

The purpose of additional views is to improve visibility, ray intersection geometry, tie-point distribution or calibration observability. They increase acquisition time, data volume and processing burden. Design them to address a specific geometric weakness.

## 6. Ground control, tie points and check points are different

- **Tie points** are image features matched across photographs. They connect images and support relative orientation and reconstruction. They are not automatically known ground coordinates.
- **Ground control points (GCPs)** have independently determined object-space coordinates and are used to constrain georeferencing or adjustment.
- **Check points** are independent reference observations withheld from model fitting and used to assess product accuracy.

Using a point as control and then reporting its fit residual as an independent accuracy check is circular. Keep validation observations independent of the adjustment to the extent required by the project.

Control should be distributed across the project area and, where relevant, across elevation. A cluster of accurate control points in one corner cannot necessarily constrain a large block uniformly. Control survey method, datum, coordinate epoch where relevant, uncertainty and traceability must be documented.

The USGS report gives context-specific recommendations for control quality and discusses orthogonal image acquisition and tie-point distribution. Its recommendations should be read in the context of its UAS programme and project assumptions, not converted into universal legal or engineering requirements.

## 7. Acquisition quality assurance

Before acquisition:

- confirm permissions, airspace, site access, safety plan and environmental constraints;
- inspect camera, lens, storage, batteries and platform condition;
- check calibration status and required control/check-point plan;
- verify coordinate and vertical reference requirements;
- review weather, illumination, wind and surface conditions;
- confirm coverage, overlap, image interval and geometry;
- define naming, metadata and backup procedures.

During acquisition:

- monitor actual height above ground, speed, exposure and image sharpness;
- check that planned strips and image intervals are being achieved;
- monitor gaps, turns, changing illumination and unexpected motion;
- record deviations, interruptions and operational events;
- verify control targets are visible and not obscured.

After acquisition:

- inspect image completeness, blur, exposure and overlap;
- confirm metadata, time, camera settings and trajectory records are preserved;
- inspect image coverage and tie-point distribution during initial processing;
- record exclusions and processing decisions;
- preserve independent check points for accuracy assessment;
- retain raw imagery and provenance alongside derived products.

## 8. A worked planning example

Suppose a hypothetical camera has:

- focal length (f=24\,mm);
- sensor width (W=13.2\,mm);
- sensor height (L=8.8\,mm);
- pixel pitch (p=2.4\,\mu m);
- height above local ground (H=120\,m).

Convert pixel pitch to metres: (p=0.0000024\,m), and focal length to metres: (f=0.024\,m).

Then:

[
GSD = \frac{120\times0.0000024}{0.024}=0.012\,m=1.2\,cm
]

The approximate footprint is:

[
F_W=\frac{120\times0.0132}{0.024}=66\,m
]

[
F_L=\frac{120\times0.0088}{0.024}=44\,m
]

For an illustrative 80% forward overlap and 70% side overlap:

[
d_f=44(1-0.80)=8.8\,m
]

[
d_s=66(1-0.70)=19.8\,m
]

These are idealised image-centre spacings, not a complete mission plan. They omit terrain relief, safety margins, turns, image timing, camera attitude, wind, speed limits, boundary coverage and regulatory requirements.

The [photogrammetric flight-design implementation](../../implementations/python/photogrammetric-flight-design/README.md) provides reproducible calculations for GSD, footprint and overlap-constrained spacing. It is a planning calculator, not a flight controller or complete mission planner.

## 9. What the model cannot repair

Processing cannot reliably compensate for:

- missing coverage or inadequate overlap;
- severe blur or unusable exposure;
- weak or repetitive image texture;
- insufficient viewing-angle diversity;
- poor camera calibration or unstable camera configuration;
- inaccurate or poorly distributed control;
- control/check-point leakage;
- unrecorded datum or coordinate-reference mistakes;
- scene movement between image captures;
- missing independent validation.

A visually convincing orthomosaic or dense point cloud is not, by itself, evidence of positional accuracy.

## 10. Spatial context and operational transfer

The same acquisition principles apply to infrastructure inspection, corridor mapping, construction monitoring, archaeology, agricultural plots, environmental monitoring and terrain surveys. The design differs with object scale, surface properties, access, required detail, viewing geometry, temporal frequency and consequence of error.

For example, mapping a roof façade requires views that see the façade; a nadir-only block may not observe it adequately. Monitoring vegetation requires attention to canopy movement, illumination and whether the target is the canopy surface or underlying terrain. A repeat survey requires consistent geometry and documented changes in sensor, calibration and processing.

Before an operational deployment, establish the local legal and safety requirements, competent personnel, independent survey control, validation design and client acceptance criteria. This educational unit does not provide flight authorisation or certify a survey.

## 11. References and further study

- Sampath, A., Shrestha, M., While, M. and Scholl, V. M. (2023). *Guidelines for Calibration of Uncrewed Aircraft Systems Imagery*. USGS Open-File Report 2023–1033. [Official report and landing page](https://pubs.usgs.gov/publication/ofr20231033/full). The report covers UAS data acquisition, geometric and radiometric calibration, control, tie points and quality assurance. Its recommendations are specific to the report's context.
- U.S. Geological Survey (2025). *Creating 3D Point Clouds, Digital Elevation Models, and Orthomosaics From Historical Aerial Imagery Through Structure From Motion Aided Photogrammetry*. USGS Techniques and Methods 11–C11. [Official publication](https://pubs.usgs.gov/publication/tm11C11).
- NOAA. *Best Practices for Incorporating UAS Image Collection into Wetland Monitoring Efforts: A Guide for Entry Level Users*. [Official repository record](https://repository.library.noaa.gov/view/noaa/47954). Useful as a domain-specific field guide; do not generalise wetland-specific choices to every survey.
- [Measurement principles and field verification](../../foundations/measurement-science/measurement-principles-and-field-verification.md) — measurement quality, traceability and verification.
- [Photogrammetric flight-design calculations](../../implementations/python/photogrammetric-flight-design/README.md) — runnable planning calculations.

## 12. Related Spatial Methods material

- [Spatial Data Collection pillar](../README.md)
- [Photogrammetry and 3D reconstruction workflow family](../../catalog/master-subject-index.md#8-spatial-recipes-rec)
- [Measurement science and survey adjustment](../../learning-paths/measurement-science-and-survey-adjustment.md)
- [Photogrammetric image-acquisition exercise](image-acquisition-exercise.md)

## 13. Scope and review status

This is an initial educational synthesis. It has not been independently reviewed by a photogrammetry specialist or tested in a field campaign. The numerical example is hypothetical. The planning equations are idealised and should not be used as a substitute for detailed mission planning, survey design, safety review, legal compliance or independent accuracy assessment.

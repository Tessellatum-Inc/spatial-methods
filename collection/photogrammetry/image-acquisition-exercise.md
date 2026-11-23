# Practical exercise: design a photogrammetric image-acquisition plan

> **Level:** Intermediate undergraduate to postgraduate  
> **Estimated time:** 2–3 hours  
> **Companion:** [Photogrammetric image acquisition](image-acquisition.md)  
> **Evidence status:** Hypothetical design exercise; no real flight or survey data

## Scenario

A research team needs to acquire imagery over a hypothetical 600 m by 400 m site. The team wants an orthomosaic and a surface model. The terrain is gently rolling, includes a mixture of hard surfaces and vegetation, and contains a building whose façades matter to the project.

A nadir camera has:

| Parameter | Value |
|---|---:|
| Focal length | 24 mm |
| Sensor width | 13.2 mm |
| Sensor height | 8.8 mm |
| Pixel pitch | 2.4 μm |
| Nominal height above local ground | 120 m |
| Illustrative forward overlap | 80% |
| Illustrative side overlap | 70% |

These overlap values are exercise inputs, not universal recommendations or flight instructions.

## Part A — Calculate the image scale

1. Convert focal length and pixel pitch to metres.
2. Calculate approximate GSD.
3. Calculate the near-nadir footprint width and height.
4. Calculate approximate forward and side image-centre spacing at the stated overlap.
5. Explain why these values are not product-accuracy estimates.

## Part B — Challenge the geometry

6. Explain why a large overlap percentage does not automatically imply strong three-dimensional geometry.
7. Propose an additional image configuration that could improve the building-façade coverage and explain its trade-offs.
8. Explain when cross-strips or convergent views might improve camera calibration or reconstruction.
9. Identify two scene conditions that may make image matching unreliable and propose mitigations.

## Part C — Control and validation

10. Distinguish tie points, GCPs and independent check points.
11. Propose a control and check-point distribution for the hypothetical site. Explain why a cluster of points in one corner is weak.
12. Explain why GCP residuals alone do not provide independent accuracy validation.
13. List the metadata and field records that should be retained for traceability.

## Part D — Design a defensible acquisition plan

14. Produce a one-page plan covering the deliverable, image geometry, camera settings, lighting and weather, control, field QA, data backup and independent validation.
15. State at least five conditions that would cause you to pause, reacquire imagery or qualify the final product.
16. Identify which project requirements cannot be decided from the supplied information and what evidence or stakeholder input is needed.

## Submission checklist

- [ ] Calculations with units and intermediate steps
- [ ] A sketch or description of the image geometry
- [ ] Control/check-point strategy and justification
- [ ] Acquisition and quality-assurance plan
- [ ] Limitations and unresolved requirements
- [ ] Clear statement that this is a hypothetical plan, not a flight authorisation

## Worked solution

### Part A

Convert (f=24\,mm=0.024\,m) and (p=2.4\,\mu m=0.0000024\,m).

[
GSD=\frac{120(0.0000024)}{0.024}=0.012\,m=1.2\,cm
]

[
F_W=\frac{120(0.0132)}{0.024}=66\,m
\qquad
F_L=\frac{120(0.0088)}{0.024}=44\,m
]

[
d_f=44(1-0.80)=8.8\,m
\qquad
d_s=66(1-0.70)=19.8\,m
]

These values assume a near-nadir pinhole camera over locally planar ground at constant height above ground. They do not include relief, attitude, turns, boundary margins or actual image timing. GSD describes approximate pixel spacing on the ground, not positional accuracy.

### Part B

Repeated near-parallel nadir views can produce high overlap but limited convergence and weak depth geometry. Oblique or convergent views and cross-strips can improve ray intersection diversity and expose façades, but add acquisition complexity, image volume and processing challenges. The exact design depends on the deliverable and acceptance criteria.

Moving vegetation, water, reflective surfaces, low-texture pavement, shadows and changing illumination can weaken matching. Possible mitigations include changing acquisition timing, adding suitable view geometry, controlling exposure, using complementary sensors or documenting areas where reliable reconstruction is not possible. No single mitigation solves every surface.

### Part C

Tie points are image correspondences; GCPs are independently surveyed coordinates used to constrain the model; check points are independent coordinates withheld for validation. Distribute control and check observations around the site and across relevant elevation and feature types. The exact count and spacing depend on area, terrain, required accuracy, standards and project risk; this exercise does not prescribe a universal count.

Retain camera and lens identity, calibration information, image timestamps, exposure settings, platform/trajectory records, coordinate reference and vertical datum, control/check-point coordinates and uncertainty, collection conditions, mission deviations, raw images, processing software/version and processing decisions.

### Part D

A defensible plan states the product and accuracy requirement first. It then chooses image scale and geometry, defines control and independent validation, establishes safety and permissions, sets camera and weather limits, and describes in-field checks and data custody. If a required accuracy, coordinate reference, site access, façade detail or legal permission is unknown, the plan must identify it as unresolved rather than invent a value.

## Marking guide (20 points)

| Criterion | Points | Strong work demonstrates |
|---|---:|---|
| Scale and footprint calculations | 4 | Correct unit conversion, equations and interpretation |
| Image geometry reasoning | 4 | Understands convergence, overlap, relief and façade visibility |
| Control and validation | 4 | Separates tie points, GCPs and independent check points |
| Acquisition QA and provenance | 4 | Covers sensor, environment, records, field checks and data custody |
| Critical judgement | 4 | Identifies assumptions, unresolved requirements and limits of the hypothetical plan |
| **Total** | **20** | |

## Instructor notes

Accept equivalent calculations within reasonable rounding tolerance. Reward explicit assumptions and defensible design reasoning over memorised overlap percentages. Do not accept GCP residuals as independent check-point validation. The scenario does not establish safe operating conditions, legal permission, survey accuracy or a real flight plan.

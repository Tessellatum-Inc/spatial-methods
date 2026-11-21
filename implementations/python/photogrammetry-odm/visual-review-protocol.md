# HEIG-VD visual-review protocol

## Purpose

Assess whether each publisher-supplied image observation plausibly identifies a visible, unambiguous physical target in the source image. This is a visual quality-control stage, not a coordinate-accuracy assessment.

## Review material

Use the two role-blind contact sheets for navigation, then inspect each relevant annotated image at full available resolution. The yellow circles and labels reproduce the publisher's Metashape image picks. They are overlays, not independently measured locations.

The annotated images intentionally do not disclose control/checkpoint roles. Keep the proposed split key separate until the visual decisions are recorded.

## Per-observation review

For every one of the 206 source observations, record:

- **Visibility:** Is the physical feature/target identifiable in the image?
- **Target identity:** Is there a discrete, stable target rather than a vague area or transient object?
- **Centring:** Does the overlay appear to fall on the intended target centre, not merely nearby?
- **Occlusion:** Is any part of the target obscured by vegetation, buildings, vehicles, shadows or other objects?
- **Sharpness:** Is the target sufficiently resolved to identify its centre?
- **Ambiguity:** Could the marker plausibly refer to another nearby feature?
- **Correspondence:** Is the same physical target recognisable across the images in which it is observed?

Use `review-decisions-template.csv` to record the assessment for every source observation. Use the lock utility's exact decision values: `accepted`, `questioned`, or `rejected`. Complete every required field, including reviewer identity and an ISO 8601 review timestamp with timezone. Provide a concise rationale for every row; explain all `questioned` and `rejected` decisions explicitly. The `target_visible`, `target_identity_clear`, and `marker_centred` fields must each be `yes`, `no`, or `uncertain`. The source pixel columns identify the publisher's pick being reviewed; they are not independent remeasurements. Do not infer a pass from the fact that a marker is visible.

## Point-level disposition

A point should not be accepted solely because one image looks good. Review all of its observations together. Record the point-level disposition and reasons, and flag any inconsistent image measurements. A point with insufficient, ambiguous or unstable observations should not be used as a control or checkpoint without a separately justified treatment.

## Independence rule

The source `gcp_obs.csv` observations were measured in Metashape. They may be visually reviewed, but they must **not** be reused as independent checkpoint measurements.

After the visual-review decisions are recorded and locked, independently remeasure checkpoint image coordinates from the unannotated source images, without consulting the Metashape pixel coordinates or annotated overlays. Preserve the measurement method, reviewer, image, point ID, new pixel coordinates and review date. The independent measurements must be stored separately from the source observations.

## Decision gate

The split remains `proposed_not_locked` until the visual review is complete, point-level dispositions are recorded, the control/checkpoint geometry and image coverage are reassessed, and independent checkpoint measurements are available. Do not run or report an accuracy assessment before those conditions are met.

## Scope limitations

This protocol does not establish the quality of the surveyed ground coordinates, the horizontal or vertical reference transformations, camera calibration, bundle-adjustment quality, dense reconstruction quality or final product accuracy. The source OPK solution was adjusted using ground points as control and is not independent truth.

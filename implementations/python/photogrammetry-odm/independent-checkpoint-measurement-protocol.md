# Independent checkpoint image-measurement record

## Purpose

Capture new image-coordinate measurements for points designated as checkpoints only after the role-blind visual review has been recorded and the control/checkpoint partition has been formally locked.

This is a blank record template. It intentionally contains no prefilled point IDs, image coordinates or claimed measurements.

## Independence requirements

- Use the original, unannotated source images.
- Do not consult `gcp_obs.csv`, the annotated images, the point-review crops, the supplied OPK solution or any prior Metashape project while measuring.
- Measure the same physical target identified by the point ID, not the location of the old source marker.
- Record the measurement method, reviewer, UTC timestamp and source image SHA-256.
- Preserve the original measurement record. Corrections should be new versioned records with a reason, not silent overwrites.
- If the target cannot be identified confidently, record the reason and leave pixel coordinates blank. Do not invent or interpolate a measurement.
- Use an independent reviewer or an explicitly documented independent measurement procedure. Merely retyping or copying source coordinates is not independent.

## Record format

Use `independent-checkpoint-measurements.template.csv`. One row represents one point observation in one source image. Pixel origin is top-left; x increases rightward and y downward. Coordinates are in source-image pixels, not resized preview pixels.

The image SHA-256 must refer to the original source image, not an annotated derivative or crop. The template does not define an accuracy threshold.

## Separation from model validation

These measurements establish image-coordinate observations only. They do not themselves establish surveyed ground-coordinate accuracy or product accuracy. The checkpoint reference coordinates, their horizontal/vertical reference systems, uncertainties and provenance must be separately documented before comparing a reconstructed product with them.

Do not pass a checkpoint into the ODM GCP file. Do not use the supplied source OPK orientations as independent truth.


## Validate the measurement register

After the partition has been formally approved/locked, validate the completed CSV against that approved split, the immutable acquisition manifest and the role-blind visual-review summary:

```bash
python validate_independent_checkpoint_measurements.py \\
  independent-checkpoint-measurements.csv \\
  approved-control-checkpoint-split.json \\
  acquisition-provenance.json \\
  visual-review-summary.json \\
  --json-out independent-measurement-validation.json
```

The approved split must declare `status` as `approved`, `locked` or `approved_locked`, with `dataset.resolved_revision`, `dataset.selected_path` and `selection.checkpoint_points` / `selection.control_points`. If present, `dataset.acquisition_manifest_sha256` must match the supplied manifest. The validator checks that every source point/image observation belonging to an approved checkpoint is represented exactly once as measured or explicitly unmeasurable, each image hash matches the immutable acquisition manifest, timestamps are UTC, coordinates are finite/non-negative, and each checkpoint has at least one measured view. An explicitly `unmeasurable` row may leave both coordinates blank but must state a reason; it does not satisfy the per-checkpoint measured-view requirement.

The validator does not read or copy publisher pixel coordinates. Source observation keys are used only to establish that a point/image pair belongs to the acquired dataset. A successful report means record structure and provenance checks passed; it does not prove reviewer independence, target identity, measurement quality, ground-coordinate accuracy or product acceptance.

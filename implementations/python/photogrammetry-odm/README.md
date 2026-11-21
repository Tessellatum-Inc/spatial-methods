# OpenDroneMap photogrammetry processing companion

A small, auditable companion for running [OpenDroneMap (ODM)](https://github.com/OpenDroneMap/ODM) in Docker and assessing independent 3D checkpoint residuals from a CSV export.

This is deliberately **not** a photogrammetry engine. ODM performs image alignment, bundle adjustment, reconstruction, georeferencing, orthorectification and product generation. The Python utilities here make the invocation reproducible and provide a transparent, separate checkpoint-statistics step.

## Scope and evidence status

- Open-source engine: OpenDroneMap, executed in a Docker container.
- Local utilities: Python standard library only.
- The runner validates a project folder and constructs a Docker command. It does not install Docker, fetch images, select processing parameters or interpret the resulting products.
- Checkpoint assessment expects coordinates independently extracted/measured for the same named points in the model and reference survey.
- The included tests use synthetic values. No imagery has been processed and no real-world positional accuracy has been established.
- This is a UAS/aerial imagery workflow. Terrestrial, close-range, multisensor and non-UAS use cases need their own acquisition and processing design.

## Project layout

ODM expects a project directory containing an `images/` directory. For example:

```text
datasets/
  campus_block/
    images/
      IMG_0001.JPG
      IMG_0002.JPG
    gcp_list.txt       # optional; only if used and correctly formatted
```

Keep the original acquisition media in a separate immutable raw archive. Process a verified working copy. The runner mounts the parent `datasets/` directory into the container and asks ODM to process `campus_block`.

## Requirements

- Python 3.10 or later (utilities use the standard library).
- Docker installed and running.
- A locally available or pullable, explicitly pinned ODM image.
- Sufficient disk space, memory and processing time for the image set.

Do not use an unpinned `latest` image for a reproducible project record. Record the exact image tag and, for high-assurance workflows, the resolved image digest.

## Run ODM

First inspect the project's image set and prepare any optional GCP file according to the official [ODM GCP format](https://docs.opendronemap.org/gcp/). GCP image measurements, coordinates, projection and units must be checked before processing. Do not include independent check points as GCPs.

From this directory:

```bash
python odm_runner.py /absolute/path/to/datasets/campus_block \
  --image opendronemap/odm:<PINNED_VERSION> \
  --dry-run
```

Review the printed command and project path. Then run without `--dry-run`:

```bash
python odm_runner.py /absolute/path/to/datasets/campus_block \
  --image opendronemap/odm:<PINNED_VERSION>
```

The runner requests a DSM by default. Add or remove ODM options explicitly, for example:

```bash
python odm_runner.py /absolute/path/to/datasets/campus_block \
  --image opendronemap/odm:<PINNED_VERSION> \
  --odm-arg=--orthophoto-resolution --odm-arg=5
```

ODM's available arguments and defaults are version-dependent. Consult the [official arguments reference](https://docs.opendronemap.org/arguments/) for the exact pinned version. The example value above is illustrative, not a recommended resolution.

The Docker image and project data are not bundled in this repository. The first execution may need to download the image. Processing can be computationally expensive.

## Expected products

Depending on options and successful processing, ODM can produce georeferenced orthophotos, elevation products, point clouds and 3D models. Common output locations include:

- `odm_orthophoto/odm_orthophoto.tif`
- `odm_dem/dsm.tif` and/or other DEM products, depending on version and options
- `odm_georeferencing/odm_georeferenced_model.laz`
- `odm_texturing/` and `odm_meshing/`

Do not assume every product exists. Confirm the actual output tree, inspect processing logs and open geospatial products in appropriate software such as QGIS or CloudCompare.

## Independent checkpoint assessment

Prepare a CSV containing **independent check points** measured in the reference survey and extracted from the final model. Required columns:

```csv
point_id,ref_x,ref_y,ref_z,model_x,model_y,model_z
CP01,500000.120,9900000.220,1640.500,500000.145,9900000.190,1640.540
CP02,500020.100,9900010.300,1641.100,500020.080,9900010.340,1641.060
```

The numbers above are fictitious and only illustrate the schema. All six coordinate columns must use the same projected coordinate system, axis order and units. Reference and model heights must use the same vertical reference and height type. Do not compare ellipsoidal heights with orthometric heights without a documented transformation.

Run:

```bash
python checkpoint_qa.py checkpoints.csv --json-out checkpoint-report.json
```

The script reports residuals as **model minus reference**, component bias, component RMSE, horizontal RMSE, vertical RMSE, horizontal radial median/95th percentile and maximum. The percentile is a descriptive statistic of the supplied sample; it is not automatically CE95, a standards-compliance result or a confidence bound.

The script does not transform coordinates, account for reference-survey uncertainty, choose a sampling design, test spatial independence, remove outliers, apply an accuracy standard or decide acceptance. Those are project responsibilities. Report sample size, point distribution, survey method, reference uncertainty, exclusions and the pre-agreed acceptance test alongside the output.

## Tests

```bash
python -m unittest -v
```

Tests cover project validation and command construction without running Docker, checkpoint metrics, validation and JSON output, image inventory/hash behaviour, acquisition-manifest hashing and metadata, and structural checks for GCP/observation/OPK records and rotation matrices. A successful unit test is not a test of ODM, image quality or a real photogrammetric project.

## Dataset inventory and image audit

Before preparing an ODM project, run the read-only dataset auditor against the extracted dataset directory:

```bash
python dataset_audit.py /path/to/drone_heig_2019 --expected-images 32 \\
  --json-out dataset-image-audit.json
```

The utility inventories supported image files recursively, records file sizes and SHA-256 hashes, and (when Pillow is installed) verifies image readability and reports dimensions, basic camera EXIF and whether GPS metadata is present. It does not expose GPS coordinates. A present GPS tag is not evidence of positional accuracy. Keep the JSON manifest with the processing record; do not commit source imagery or a manifest containing sensitive metadata.

Run the companion tests with `python -m unittest -v`.

## Dataset metadata and geometry audit

After acquiring the HEIG-VD dataset, run the structural auditor:

```bash
python dataset_metadata_audit.py /path/to/drone_heig_2019 \\
  --json-out dataset-metadata-audit.json
```

It checks the publisher's GCP coordinate, image-observation and OPK text exports; expected record counts; duplicate coordinate groups; observed point and image mappings; pixel-coordinate bounds against the README dimensions; and OPK rotation-matrix orthogonality/determinants. It is a structural consistency check, not a CRS transformation, survey validation or control/checkpoint design. It reports the known point 100/206 coordinate coincidence rather than treating it as an automatic file error. The README's stated 31 GCPs, 206 observations, 30 image-measured points and 32 orientations are defaults; inspect any count mismatch rather than suppressing it.

## End-to-end rehearsal

A candidate real-image rehearsal dataset and its processing/validation protocol are documented in [rehearsal-plan.md](rehearsal-plan.md). The dataset-specific README states that the subset contains 32 original 5472 × 3648 JPG images, 31 surveyed ground points, 206 image measurements for 30 points, and a Metashape OPK export. It explicitly identifies LV95 horizontal coordinates (EPSG:2056) and LN02 heights in metres. The GCP text renders 31 coordinate rows, consistent with the README; point 100 has no image measurement and duplicates point 206's coordinates. See [the source inspection record](dataset-inspection.md) for the detailed evidence boundary and remaining checks.

To download only this subset on a network-enabled machine, install the optional Hub client and run:

```bash
python -m pip install huggingface_hub
python acquire_rehearsal_dataset.py ./data/heig-vd-scop
```

The helper resolves the Hub repository's current commit first and downloads `datasets/drone_heig_2019/` at that exact revision. It writes into `snapshots/<commit-sha>/`, with `acquisition-provenance.json` in that revision-specific directory. Each immutable revision therefore has an isolated dataset tree and manifest; repeat downloads cannot silently mix files left by a different revision. Existing snapshots are not deleted. The manifest records the immutable repository revision, retrieval time, client/Python versions, and each downloaded file's size and SHA-256. Keep this manifest with the project record. Then run `dataset_audit.py` against the downloaded directory. The dataset's README and text exports have been inspected online, but the helper has not acquired the real files in this runtime; local image-byte and metadata auditing remain outstanding.

## Connected Spatial Methods material

- [End-to-end photogrammetric mapping recipe](../../../recipes/photogrammetric-mapping/README.md)
- [Photogrammetric acquisition theory and QA](../../../collection/photogrammetry/image-acquisition.md)
- [Image acquisition exercise](../../../collection/photogrammetry/image-acquisition-exercise.md)
- [Flight-design calculation companion](../photogrammetric-flight-design/README.md)
- [Measurement principles and field verification](../../../foundations/measurement-science/measurement-principles-and-field-verification.md)
- [Existing accuracy-assessment methods](../accuracy-assessment/README.md)

## References

- OpenDroneMap Authors. [OpenDroneMap repository and Docker quickstart](https://github.com/OpenDroneMap/ODM).
- OpenDroneMap documentation. [Ground Control Points](https://docs.opendronemap.org/gcp/).
- OpenDroneMap documentation. [Command-line arguments](https://docs.opendronemap.org/arguments/).

Verify documentation and options against the exact software release used. This implementation has not yet been run against a live Docker engine or real imagery.

## Project manifest and preflight

Use [project-manifest.template.json](project-manifest.template.json) as a starting point for a new project. Copy it into the project record, replace every placeholder, and keep site-sensitive values or credentials out of the public repository.

The manifest makes intended use, data sources, local project directory, processing engine/configuration, coordinate and vertical references, independent-checkpoint status, reference uncertainty, acceptance criteria and deliverables explicit.

Run a read-only preflight:

```bash
python project_manifest.py /path/to/project-manifest.json \\\
  --json-out preflight-report.json
```

The report distinguishes:
- **blocked:** required local project structure or imagery is missing;
- **review_required:** the local structure exists, but configuration or validation details need attention;
- **ready_for_operator_review:** no configured checks raised a blocker or warning.

“Ready” is not an approval to fly, survey, process or deliver. The utility does not assess image quality, site safety, legal permissions, CRS correctness, coverage, camera calibration, control quality or product accuracy. It does not invoke Docker or modify data. An operator must review the report and project specification before proceeding.

The manifest and preflight utility establish a common handoff contract that can later be reused by other Spatial Recipes, while domain-specific checks remain separate.


## Integrated read-only preflight

The manifest-only check validates the project record:

```bash
python project_manifest.py /path/to/project-manifest.json --json-out manifest-preflight.json
```

For the integrated check, run:

```bash
python project_preflight.py /path/to/project-manifest.json --json-out preflight-report.json
```

The integrated report combines manifest checks, project and image-directory checks, image inventory and SHA-256 hashes, image decoding/dimensions when Pillow is installed, expected-versus-observed image counts, and a constructed ODM Docker command for operator review.

The report distinguishes `blocked`, `review_required` and `ready_for_operator_review`. Missing or unreadable images block the handoff; incomplete validation configuration and count mismatches require review. If Pillow is unavailable, inventory is still produced but decoding checks are explicitly marked unavailable.

The command is a dry-run handoff only. It does not invoke Docker, alter source images, assess image sharpness or overlap, validate CRS or control, assess product accuracy, or authorise flight, survey, processing or delivery. The HEIG-VD-specific metadata auditor remains separate because its GCP/observation/OPK assumptions are not generic to all photogrammetry projects.

The integrated preflight is a first domain-level orchestration pattern. Its manifest, severity model and report structure are candidates for reuse in other Spatial Recipes; image and ODM checks remain domain adapters. Tests are in `test_project_preflight.py`.


## Processing-run provenance

The integrated preflight prepares a command but does not execute it. When an operator is ready to run ODM, use the run recorder to capture input identity, container metadata (when inspectable), execution details, logs and output inventory.

Prepare a provenance record without invoking Docker:

```bash
python processing_run.py /absolute/path/to/datasets/campus_block \
  --image opendronemap/odm:<PINNED_VERSION> \
  --run-directory /absolute/path/to/run-records/campus-block-run-001
```

Actual processing requires the explicit `--execute` switch:

```bash
python processing_run.py /absolute/path/to/datasets/campus_block \
  --image opendronemap/odm:<PINNED_VERSION> \
  --run-directory /absolute/path/to/run-records/campus-block-run-001 \
  --execute
```

The run directory must be outside the ODM project directory. The recorder hashes supported source images before execution, captures stdout/stderr, records the process exit code and inventories project files after execution. It also attempts to record the local Docker image ID, repository digests, OS and architecture. Dry-run does not invoke Docker at all.

The record is evidence of what the wrapper observed, not a complete execution attestation. It does not yet capture all host hardware/runtime details, guarantee bit-for-bit deterministic reconstruction, validate output CRS or raster contents, or establish product accuracy. A zero exit code is not an acceptance decision. Preserve the run directory alongside (but separately from) the raw source archive.


## Output inventory and geospatial inspection

After a processing run, inspect the resulting project tree:

```bash
python output_inspection.py /absolute/path/to/datasets/campus_block \
  --expect odm_orthophoto/odm_orthophoto.tif \
  --expect odm_dem/dsm.tif \
  --json-out output-inspection.json
```

Expected paths are project-relative and may be repeated. Missing declared files are blockers. The utility inventories all project files and, when Rasterio is installed, checks GeoTIFF readability and records dimensions, band count, data types, CRS, affine transform, bounds, pixel size and nodata. It attempts a small read from the first band. If Rasterio is unavailable, the file remains inventoried but structural raster inspection is explicitly marked unavailable. LAS/LAZ point clouds are streamed in chunks when `laspy` (and a compatible LAZ backend for compressed files) is installed; the report records declared/observed point counts, point format, version, scales, offsets, header bounds, parsed CRS, classification counts, intensity range, finite-coordinate checks, observed extents, point-count reconciliation, header-bound checks with scale-derived tolerance and a five-point sample. Missing `laspy` is a warning, not a silent pass.

For optional inspection support, install `rasterio` for GeoTIFF structure and `laspy` for streamed LAS/LAZ point-record inspection. LAZ compression additionally needs a compatible backend such as `lazrs` (for example, `python -m pip install rasterio laspy lazrs`). These are optional inspection dependencies; the scripts report unavailable checks rather than silently treating them as passed.

This is a structural inspection stage, not an accuracy assessment. A present CRS may still be wrong; plausible bounds and pixel sizes do not establish georeferencing correctness. LAS/LAZ point-record structural inspection is included when `laspy` is available, including classification counts, observed extents and reconciliation of streamed coordinates against header bounds. The comparison tolerance is derived from LAS coordinate scales. It does not assess classification correctness, point density suitability or positional accuracy. Wavefront OBJ files receive basic syntax and vertex-index inspection; topology/manifoldness, self-intersections, texture/normal quality and geometric accuracy remain unverified. Compare products with independent reference data and project acceptance criteria before delivery.


## Independent checkpoint validation evidence

The statistics-only utility is useful for transparent residual summaries. To turn those summaries into a project-level evidence record, use `validation_evidence.py` with a context JSON file. The CSV must contain the seven fields documented by `checkpoint_qa.py`: `point_id,ref_x,ref_y,ref_z,model_x,model_y,model_z`.

Start from [validation-context.template.json](validation-context.template.json), then replace every placeholder with project facts. The template deliberately leaves checkpoint independence unconfirmed and acceptance pending. Required context includes the project-specific acceptance criteria reference.

```json
{
  "project_id": "replace-with-project-id",
  "processing_run_id": "replace-with-run-id",
  "horizontal_crs": "EPSG:XXXX",
  "vertical_reference": "declare the vertical datum/reference",
  "coordinate_units": "metres",
  "reference_uncertainty": "describe source, method and uncertainty",
  "sample_design": "describe selection frame, design and exclusions",
  "checkpoint_independence": false,
  "acceptance_criteria": "cite project-specific acceptance specification and version",
  "acceptance_decision": "pending"
}
```

Generate the report and link the run/output records where available:

```bash
python validation_evidence.py checkpoints.csv validation-context.json \\
  --run-record /path/to/processing-run.json \\
  --output-inspection /path/to/output-inspection.json \\
  --json-out validation-evidence.json
```

The adapter hashes the checkpoint CSV and linked JSON evidence, checks the processing-run identifier when present, and reports residual statistics alongside declared CRS, vertical reference, units, reference uncertainty and sample design. Missing context or unconfirmed checkpoint independence yields `not_assessable`; it is not converted into a pass or a failed product.

Acceptance is deliberately separate. The default decision is `pending`. A human may supply `accepted`, `rejected` or `not_assessable`, but a non-pending decision requires both a named reviewer and a written rationale. The tool does not invent generic thresholds, infer compliance, or automatically accept based on RMSE/P95.

This is an evidence adapter, not a full survey-design auditor. It records rather than independently proves checkpoint independence, sample representativeness, CRS compatibility or reference uncertainty. It does not propagate reference uncertainty, transform coordinates, calculate confidence intervals, or establish CE95. A single reviewer decision is not independent multi-reviewer validation. GCPs, training points and AI-assisted interpretations must not be represented as independent checkpoints.


## Reproducible evidence delivery dossier

Once the five evidence records exist, assemble them into a reviewable ZIP dossier:

```bash
python delivery_dossier.py \
  --acquisition-manifest /path/to/acquisition-provenance.json \\
  --acquisition-verification /path/to/acquisition-verification.json \\
  --manifest /path/to/project-manifest.json \
  --preflight /path/to/preflight-report.json \
  --run-record /path/to/processing-run.json \
  --output-inspection /path/to/output-inspection.json \
  --validation-evidence /path/to/validation-evidence.json \
  --output /path/to/delivery-dossier.zip
```

The archive contains the acquisition provenance manifest and its verification report, project manifest, preflight report, processing-run record, output-inspection report, checkpoint-validation evidence and a `delivery-dossier.json` index. The dossier cross-checks the verified revision, selected dataset path, declared file count and exact acquisition-manifest SHA-256 before it can be considered consistent. The index records SHA-256 hashes, byte sizes, observed statuses, project/run identity checks, warnings and consistency errors.

The dossier is `inconsistent` when declared project or run identities conflict, `review_required` when evidence is incomplete in quality or its recorded decisions remain unresolved, and `assembled` when the supplied records are internally consistent and report the expected positive statuses. Even an `assembled` dossier has `release_authorized: false`: packaging evidence never substitutes for project-specific professional, contractual, legal or safety release decisions.

The ZIP bundles evidence records, not raw imagery or the complete processing outputs. Preserve those source and product files separately, using the recorded hashes to identify the exact evidence versions. The archive's own SHA-256 is printed after creation.


## Reviewer guide

Before reviewing or reusing this pipeline, read [REVIEWER-GUIDE.md](REVIEWER-GUIDE.md). It defines the evidence handoff, status meanings, reviewer questions, known gaps and the distinction between an assembled dossier and release authorization.


## Verify an acquired source snapshot

Before image or metadata auditing, verify the acquired files against the saved provenance manifest:

```bash
python verify_acquisition.py ./data/heig-vd-scop/snapshots/<commit-sha>/acquisition-provenance.json --json-out ./data/heig-vd-scop/acquisition-verification.json
```

The verifier checks each declared file's size and SHA-256, rejects unsafe manifest paths, and reports missing, modified, symbolic-link and unmanifested files. Continue only when the report status is `verified`. This means local bytes match the saved acquisition manifest; it does not establish publisher authenticity, licence compliance, image readability or dataset suitability.


## Synthetic pipeline integration test

Run the package tests from this directory:

```bash
python -m pytest -q
```

`test_pipeline_integration.py` exercises the evidence handoff from a locally acquired snapshot through integrity verification, a separate working copy, read-only preflight, dry-run processing provenance, output inspection, checkpoint evidence and ZIP dossier assembly. It uses synthetic bytes and mocked image-audit output. It deliberately leaves ODM unexecuted, checkpoint independence unconfirmed, validation not assessable and dossier release authorization false. This is an integration test of evidence flow and gate preservation, not a real-data rehearsal, photogrammetric processing test or accuracy validation.

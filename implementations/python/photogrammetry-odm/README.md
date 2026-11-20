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

Tests cover project validation and command construction without running Docker, plus checkpoint metrics, validation and JSON output. A successful unit test is not a test of ODM, image quality or a real photogrammetric project.

## Dataset inventory and image audit

Before preparing an ODM project, run the read-only dataset auditor against the extracted dataset directory:

```bash
python dataset_audit.py /path/to/drone_heig_2019 --expected-images 32 \\
  --json-out dataset-image-audit.json
```

The utility inventories supported image files recursively, records file sizes and SHA-256 hashes, and (when Pillow is installed) verifies image readability and reports dimensions, basic camera EXIF and whether GPS metadata is present. It does not expose GPS coordinates. A present GPS tag is not evidence of positional accuracy. Keep the JSON manifest with the processing record; do not commit source imagery or a manifest containing sensitive metadata.

Run the companion tests with `python -m unittest -v`.

## End-to-end rehearsal

A candidate real-image rehearsal dataset and its processing/validation protocol are documented in [rehearsal-plan.md](rehearsal-plan.md). The collection catalogue describes the HEIG-VD subset as 32 geotagged images and 31 ground points with image measurements, under the collection's CC BY 4.0 licence. The catalogue labels the ground-point horizontal reference LV95; the vertical reference, height type and detailed file contents still require inspection. Do not assume LN02 or any other vertical datum until verified from the dataset files.\n\nTo download only this subset on a network-enabled machine, install the optional Hub client and run:\n\n```bash\npython -m pip install huggingface_hub\npython acquire_rehearsal_dataset.py ./data/heig-vd-scop\n```\n\nThe helper resolves the Hub repository's current commit first and downloads `datasets/drone_heig_2019/` at that exact revision. It prints the revision and local directory. Keep the printed revision with the project record. Then run `dataset_audit.py` against the downloaded directory. This helper has not been able to retrieve the dataset in the current network-restricted environment.

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

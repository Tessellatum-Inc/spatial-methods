# ODM end-to-end rehearsal plan

## Status

**Dataset selected; source files not yet acquired or inspected; processing not executed.** The public collection catalogue confirms the dataset name, 32 geotagged images, 31 ground points with image measurements, and the collection-level CC BY 4.0 licence. The dataset-specific README and raw files have not yet been retrieved in this environment. An attempted direct retrieval failed because outbound DNS/network access is unavailable. Therefore, detailed claims about individual file names, point counts, vertical datum, duplicate points and image-observation completeness remain provisional until checked against the actual dataset files. The current execution environment also has no Docker executable, so it cannot run ODM here. Do not describe this as a successful dataset inspection or processing test.

## Selected dataset

**HEIG-VD drone 2019 (Yverdon campus)**

- Dataset collection: https://huggingface.co/datasets/heig-vd-geo/scop-datasets
- Dataset directory: `datasets/drone_heig_2019/`
- Licence: Creative Commons Attribution 4.0 International (CC BY 4.0).
- Required attribution: HEIG-VD, Geomatics group (2026), “HEIG-VD drone 2019 (Yverdon campus)”.
- Dataset card states the collection's own datasets are CC BY 4.0; the dataset-specific README repeats this licence.
- Dataset-specific README: https://huggingface.co/datasets/heig-vd-geo/scop-datasets/blob/main/datasets/drone_heig_2019/README.md
- Download size: approximately 280 MB for the dataset directory.
- Contents confirmed by the collection catalogue: 32 geotagged drone images and 31 ground points (LV95) with image measurements. Exact image dimensions, total size, detailed observation counts, additional exports and vertical-height reference have not been confirmed from the dataset-specific README or files in this environment.
- Sensor and acquisition date in the collection catalogue: senseFly S.O.D.A. on an eBee; 16 July 2019.
- Coordinate caution: the catalogue labels ground points LV95. Do not assume that this alone fully specifies the vertical datum or that all image EXIF positions are suitable as control. Confirm these details from the dataset-specific README and raw metadata before preparing GCPs.

The images are a small, real aerial survey rather than synthetic placeholders. The catalogue description makes this a promising candidate for a controlled processing exercise, but suitability for a control/checkpoint split must be established from the actual observation files. It is not evidence that ODM will reproduce the original Metashape solution.

## Important coordinate and control cautions

1. Confirm the horizontal CRS, vertical datum, height type, axis order and units from the dataset-specific README and source files. Do not infer the vertical datum from the LV95 label alone. Record horizontal and vertical reference components separately.
2. Confirm how the selected ODM release interprets GCP Z values and how the resulting products encode vertical metadata before using any GCP file.
3. Inspect the actual ground-point and image-observation files. Resolve the point count, duplicate identifiers or coordinates, points without image measurements, and image filename mappings from the source data; do not rely on unverified secondary descriptions.
4. Partition only verified, image-measured points into adjustment controls and withheld independent checkpoints. Record the split and rationale. Never use a withheld checkpoint as an ODM GCP.
5. Treat any supplied Metashape exterior orientations or reference outputs as comparison material, not ODM inputs or independent validation.
6. Do not present image EXIF positions as survey control without evidence of their accuracy and reference system.
7. The dataset was acquired at the HEIG-VD campus in Switzerland. Its metadata and control conventions are specific to that site and survey.

## Rehearsal sequence

### A. Preserve and inspect

- Run `dataset_audit.py` on the extracted dataset and retain its JSON report outside the source archive.
- Confirm the expected 32-image count, valid image decoding, image dimensions, EXIF coverage and SHA-256 manifest. Investigate any mismatch before processing.
- Download only `datasets/drone_heig_2019/`; do not mirror the entire 10 GB collection.
- Preserve the downloaded archive and record its retrieval date, source revision, file manifest and checksums.
- Verify the 32 image files, dimensions, EXIF metadata and image labels.
- Read the dataset-specific README and inventory the actual delivered ground-control and image-observation files. Previously anticipated filenames such as `GCP_MN95.txt` and `gcp_obs.csv` must be confirmed from the repository tree, not assumed.
- Confirm the image labels in the observation file map unambiguously to the delivered filenames.
- Record the source revision and exact file paths before any coordinate interpretation or point split.

### B. Baseline image-only processing

- Select and record an explicit ODM release tag and resolved image digest.
- Run the Python runner in dry-run mode and inspect the mounted path and exact command.
- Process the image set without GCPs as a baseline; retain logs and the complete output tree.
- Inspect image alignment, camera solution, orthophoto, DSM and point cloud where generated.
- Record failed or unaligned images and any processing warnings. Do not infer accuracy from visual appearance.

### C. Controlled processing

- Resolve the horizontal and vertical coordinate treatment with authoritative CRS definitions.
- Define and document a spatially distributed control/checkpoint split before processing.
- Prepare an ODM GCP file using only the adjustment control subset and verified image measurements.
- Run a second processing variant with the documented control subset.
- Keep withheld checkpoints out of all adjustment and parameter-tuning steps.

### D. Independent evaluation

- Extract model coordinates at the withheld checkpoint locations using a documented method.
- Transform reference and model coordinates into a common horizontal CRS and common vertical reference before calculating residuals.
- Record reference uncertainty, point distribution, extraction method and any exclusions.
- Run `checkpoint_qa.py` on the resulting CSV.
- Interpret bias, component RMSE, horizontal/vertical error and radial statistics in the context of sample size and spatial distribution. Do not label a descriptive P95 as CE95 or a confidence bound.

## Acceptance gates

The rehearsal is complete only when all of the following are evidenced:

- dataset attribution and licence are retained;
- all source images and metadata are accounted for;
- the exact ODM image tag and digest, command-line arguments and host environment are recorded;
- processing completes and the expected output files are inspected;
- the GCP coordinate and height-reference treatment is documented;
- control and independent checkpoint roles remain separate;
- checkpoint residuals are computed in a common coordinate reference;
- failures, exclusions and limitations are reported.

A successful run validates only this software/data combination and documented workflow. It does not establish universal accuracy, validate the acquisition design, certify survey quality or replace a project-specific acceptance specification.

## Reproduction

Download the dataset from the linked collection and follow the dataset-specific README. Keep imagery outside this repository; store only the provenance, processing record, non-sensitive logs and concise result summaries needed to reproduce the exercise.

## Current access limitation

The dataset catalogue and licence are discoverable online, but direct download and dataset-specific file inspection could not be completed in the current execution environment because outbound DNS/network access is unavailable. The Python audit utility's four unit tests were executed against local test fixtures and passed; the actual dataset has not been audited. No control/checkpoint partition has been created. To continue on a network-enabled machine, run `acquire_rehearsal_dataset.py`, retain its resolved commit SHA, then run the image audit and inspect the original ground-point and image-observation files before deciding any split.

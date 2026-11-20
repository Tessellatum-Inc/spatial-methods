# ODM end-to-end rehearsal plan

## Status

**Dataset selected; processing not yet executed.** This record defines the next reproducible rehearsal. The current execution environment has no Docker executable, so it cannot run ODM here. Do not describe this as a successful processing test.

## Selected dataset

**HEIG-VD drone 2019 (Yverdon campus)**

- Dataset collection: https://huggingface.co/datasets/heig-vd-geo/scop-datasets
- Dataset directory: `datasets/drone_heig_2019/`
- Licence: Creative Commons Attribution 4.0 International (CC BY 4.0).
- Required attribution: HEIG-VD, Geomatics group (2026), “HEIG-VD drone 2019 (Yverdon campus)”.
- Dataset card states the collection's own datasets are CC BY 4.0; the dataset-specific README repeats this licence.
- Dataset-specific README: https://huggingface.co/datasets/heig-vd-geo/scop-datasets/blob/main/datasets/drone_heig_2019/README.md
- Download size: approximately 280 MB for the dataset directory.
- Contents: 32 original geotagged JPG images (5472 × 3648; approximately 268 MB), 31 surveyed ground points, 206 image measurements for 30 points, and a Metashape exterior-orientation export.
- Sensor: senseFly S.O.D.A. on an eBee; survey date 16 July 2019.
- Reference coordinates: horizontal LV95 (EPSG:2056), heights LN02; image EXIF positions are WGS84 with consumer-grade GNSS accuracy.

The images are a small, real aerial survey rather than synthetic placeholders. The dataset has sufficient image observations and ground-control metadata to design a controlled processing exercise. It is not evidence that ODM will reproduce the original Metashape solution.

## Important coordinate and control cautions

1. Treat the supplied coordinates as a compound reference specification: LV95 horizontal coordinates plus LN02 heights. EPSG:2056 identifies the projected horizontal CRS; it does not, by itself, document the LN02 vertical datum. Record both components explicitly in every processing and evaluation record. Confirm exactly how the selected ODM release interprets GCP Z values and writes output vertical metadata before using the GCP file.
2. LN02 remains Switzerland's official height reference. LHN95 is a distinct, rigorous orthometric height system. Swisstopo states that an exact LN02–LHN95 transformation is not possible; available approximations can be at decimetric level because the systems differ in nature and LN02 contains distortions. Do not transform LN02 checkpoints to LHN95 and claim centimetric equivalence. If a conversion is necessary, use the official swisstopo REFRAME/HTRANS workflow, record its method and limitations, and retain the original LN02 values.
3. Keep horizontal and vertical transformations separate and explicit. The swisstopo REFRAME services support Swiss horizontal frames and height systems, but the service cannot verify that the input frame label supplied by the operator is correct.
2. The source says point 100 has no image measurement and shares coordinates with point 206. Do not treat these as two independent points.
3. The 30 measured ground points must be partitioned before processing into adjustment control points and withheld independent checkpoints. Record the split and rationale. Never use a withheld checkpoint as an ODM GCP.
4. The published Metashape exterior orientations and reference outputs are comparison material, not ODM inputs or independent validation.
5. EXIF positions are consumer-grade GNSS and should not be presented as survey control.
6. The dataset was acquired at the HEIG-VD campus in Switzerland. Its metadata and control conventions are specific to that site and survey.

## Rehearsal sequence

### A. Preserve and inspect

- Download only `datasets/drone_heig_2019/`; do not mirror the entire 10 GB collection.
- Preserve the downloaded archive and record its retrieval date, source revision, file manifest and checksums.
- Verify the 32 image files, dimensions, EXIF metadata and image labels.
- Read the dataset README and inspect `gcp/GCP_MN95.txt` and `gcp/gcp_obs.csv`.
- Confirm the image labels in the observation file map unambiguously to the delivered filenames.

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

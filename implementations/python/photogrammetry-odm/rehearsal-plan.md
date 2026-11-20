# ODM end-to-end rehearsal plan

## Status

**Dataset documentation and text exports inspected online; local acquisition, image-byte audit and processing not completed.** The dataset-specific README, folder listings, GCP coordinate text, image-observation CSV and OPK text export are now accessible through the publisher's Hugging Face pages. Their stated metadata and visible text have been reviewed and summarised in [dataset-inspection.md](dataset-inspection.md). No imagery has been downloaded, hashed or visually inspected locally, and the local audit utilities have not been run on the real files. The current execution environment still has no Docker executable, so ODM cannot be run here. Do not describe this as a completed local dataset audit or processing test.

## Selected dataset

**HEIG-VD drone 2019 (Yverdon campus)**

- Dataset collection: https://huggingface.co/datasets/heig-vd-geo/scop-datasets
- Dataset directory: `datasets/drone_heig_2019/`
- Licence: Creative Commons Attribution 4.0 International (CC BY 4.0).
- Required attribution: HEIG-VD, Geomatics group (2026), “HEIG-VD drone 2019 (Yverdon campus)”.
- The dataset-specific README also states CC BY 4.0 and gives the dataset citation. Retain the publisher's required attribution when reusing the data.
- Dataset-specific README: https://huggingface.co/datasets/heig-vd-geo/scop-datasets/blob/main/datasets/drone_heig_2019/README.md
- Dataset README: 32 original JPG images at 5472 × 3648 px; 31 surveyed ground points, 206 image measurements for 30 points, and a Metashape OPK export. It explicitly identifies LV95 horizontal coordinates (EPSG:2056) and LN02 heights in metres. The GCP text currently renders 30 coordinate rows, so reconcile this with the README's 31-point description during local parsing.
- Sensor and acquisition date in the collection catalogue: senseFly S.O.D.A. on an eBee; 16 July 2019.
- Coordinate caution: the dataset README explicitly states LV95 horizontal coordinates and LN02 heights. Preserve these as separate horizontal and vertical reference metadata; do not treat EPSG:2056 alone as a complete 3D CRS. The README describes EXIF GPS as metre-level consumer GNSS, not survey control.

The dataset-specific README and online text exports establish that the observation CSV has 206 image measurements for 30 point labels, and that the OPK file contains Metashape exterior orientations from an adjustment that used the ground points as control. The README says point 100 has no image measurement and shares coordinates with point 206. The rendered GCP coordinate file lists 30 labelled rows despite the README's 31 surveyed-point statement. These are now documented source-level findings; reconcile them against the downloaded files before splitting points. The OPK file is comparison material only, not independent validation.

## Important coordinate and control cautions

1. Confirm the horizontal CRS, vertical datum, height type, axis order and units from the dataset-specific README and source files. Do not infer the vertical datum from the LV95 label alone. Record horizontal and vertical reference components separately.
2. Confirm how the selected ODM release interprets GCP Z values and how the resulting products encode vertical metadata before using any GCP file.
3. Locally parse the downloaded ground-point and image-observation files. Reconcile the README's 31 surveyed points with the 30 coordinate rows visible in GCP_MN95.txt; verify the stated 206 observations, 30 observed point labels, duplicate point 100/206 coordinate note, finite pixel values and image filename mappings.
4. Partition only verified, image-measured points into adjustment controls and withheld independent checkpoints. Record the split and rationale. Never use a withheld checkpoint as an ODM GCP.
5. Treat the supplied Metashape OPK exterior orientations as comparison material only: the README states they came from a Metashape adjustment using the ground points as control, so they are not independent validation.
6. Do not present image EXIF positions as survey control without evidence of their accuracy and reference system.
7. The dataset was acquired at the HEIG-VD campus in Switzerland. Its metadata and control conventions are specific to that site and survey. The README describes EXIF GPS as consumer-grade, metre-level positioning; do not elevate it to survey control.

## Rehearsal sequence

### A. Preserve and inspect

- Run `dataset_audit.py` on the extracted dataset and retain its JSON report outside the source archive.
- Confirm the expected 32-image count, valid image decoding, image dimensions, EXIF coverage and SHA-256 manifest. Investigate any mismatch before processing.
- Download only `datasets/drone_heig_2019/`; do not mirror the entire 10 GB collection.
- Preserve the downloaded archive and record its retrieval date, source revision, file manifest and checksums.
- Verify the 32 image files, dimensions, EXIF metadata and image labels.
- Use the publisher-confirmed files `gcp/GCP_MN95.txt`, `gcp/gcp_obs.csv` and `opk.txt`; the online README identifies their schemas and reference frames.
- Locally reconcile the 31-point README statement against the 30 coordinate rows visible in the GCP text; verify 206 observation rows and 30 distinct measured point labels.
- Confirm observation image labels (with `EB-02-00761_` prefix and no extension) map unambiguously to the full JPG filenames; confirm OPK short photo IDs map to the same image set.
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

On a network-enabled machine, install the optional download dependency and retrieve only the selected subset:

```bash
python -m pip install huggingface_hub
python acquire_rehearsal_dataset.py ./data/heig-vd-scop
```

The helper resolves the repository's current commit SHA and downloads `datasets/drone_heig_2019/` into `./data/heig-vd-scop/snapshots/<commit-sha>/` at that immutable revision. It writes `acquisition-provenance.json` in the same revision-specific directory, with the revision, retrieval timestamp, client/Python versions, and per-file sizes and SHA-256 checksums. Separate revision directories prevent stale files from a previous snapshot being mixed into a new manifest; existing snapshots are retained. Preserve this manifest. Then inspect the dataset-specific README and run `dataset_audit.py` against `./data/heig-vd-scop/snapshots/<commit-sha>/datasets/drone_heig_2019`. Keep imagery outside this repository; store only provenance, processing records, non-sensitive logs and concise result summaries.

## Current access limitation

The dataset-specific README, repository listings and rendered GCP/observation/OPK text exports have now been inspected online. The real image bytes have not been acquired or audited locally; no local checksums, EXIF audit, OPK matrix validation or control/checkpoint partition exist yet. The image-audit and acquisition-helper tests were run only against local fixtures/mirrored source. The next gate is to run `acquire_rehearsal_dataset.py` on a network-enabled machine, retain its resolved commit SHA, then perform the local byte-level and structural checks specified in [dataset-inspection.md](dataset-inspection.md).

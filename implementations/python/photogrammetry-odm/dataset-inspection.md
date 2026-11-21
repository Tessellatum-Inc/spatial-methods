# HEIG-VD drone 2019 — source inspection record

## Review status

**Publisher-source inspection and CI acquisition/structural audit completed; human visual review is in progress; no ODM processing has been performed.** The immutable dataset snapshot was acquired and audited in GitHub Actions run [44899272147](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44899272147), resolved to publisher revision `e0dfeba2b6ed94ea1ae2bf773e742c39fb437b71`. All 36 manifest files passed size/SHA-256 verification; all 32 source images decoded at 5472 × 3648 px. The metadata audit reconciled 31 GCP records, 206 observations across 30 points, and 32 OPK records, with no missing image references or out-of-bounds observations. The workflow generated 32 annotated image derivatives, two contact sheets, 30 point-level review sheets and a blank 206-row observation review register. The original imagery is retained in the CI acquisition snapshot, not copied into this repository or artifact. Selected point sheets have received preliminary visual triage, but no full point-level approval register has been completed. No ODM processing or positional-accuracy assessment has been performed.

- Dataset: [HEIG-VD drone 2019 (Yverdon campus)](https://huggingface.co/datasets/heig-vd-geo/scop-datasets/tree/main/datasets/drone_heig_2019)
- Publisher: HEIG-VD, Geomatics group.
- Licence stated in the dataset README: CC BY 4.0.
- Required citation: HEIG-VD, Geomatics group (2026), “HEIG-VD drone 2019 (Yverdon campus)”.
- Acquisition: 16 July 2019, HEIG-VD campus, Yverdon-les-Bains (Cheseaux).
- Platform/sensor: senseFly eBee with S.O.D.A. camera; README states 10.6 mm focal length.
- Image set: 32 original JPG images, 5472 × 3648 pixels; README reports 268 MB. The online folder listing exposes 32 image entries.

## Local acquisition and structural audit

The completed audit artifact is attached to [workflow run 44899272147](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44899272147). Its acquisition manifest records 36 files; all 36 passed byte-size and SHA-256 comparison against the acquired manifest. The image audit decoded all 32 JPEGs and confirmed 5472 × 3648 dimensions. The structural audit found 31 coordinate records, 206 image observations, 30 observed point IDs, 32 OPK records, no missing observation-to-image mappings, no missing OPK-to-image mappings, and no pixel observations outside the declared image bounds.

The visual-review output contains role-blind annotated derivatives, point-level 640 × 640 review sheets, two contact sheets and a blank observation-level CSV register. The register is a review instrument, not a completed assessment. The publisher's Metashape image picks are shown only to guide inspection; they are not independent remeasurements. The proposed control/checkpoint split remains unlocked.

## Publisher-described files and observations

| File | Publisher description / online inspection |
|---|---|
| `images/*.JPG` | 32 original images, 5472 × 3648 px |
| `gcp/GCP_MN95.txt` | Space-delimited `label E N H` coordinates; README identifies horizontal coordinates as CH1903+/LV95 (EPSG:2056), heights as LN02, metres |
| `gcp/gcp_obs.csv` | Header/comment identifies `gcp_label image_label x y`; pixel picks have top-left origin and are stated to come from a Metashape project |
| `opk.txt` | Exterior orientations from a Metashape adjustment that used the ground points as control; fields include photo ID, XYZ, Omega/Phi/Kappa and a 3×3 rotation matrix |

The dataset README states 31 surveyed ground points, 206 image measurements for 30 of those points, and that point 100 has no image measurement and shares coordinates with point 206. The rendered GCP coordinate text lists 31 labelled coordinate rows, including point 100. This is internally consistent with the README's 31-point statement. The image-observation text visibly contains 206 measurement rows and 30 distinct point labels, as expected because point 100 has no image measurement. Counts and structural mappings have now been reconciled programmatically against the acquired snapshot; see the audit run linked above.

The online images folder lists 32 JPG filenames. The observation labels include the prefix `EB-02-00761_` and omit the `.JPG` suffix; OPK photo IDs use the shorter `0101_00xx.JPG` form. A deterministic filename-normalisation/matching check is therefore required. The local structural audit confirms the deterministic filename mapping for the acquired snapshot; do not assume raw string equality between these identifiers.

The OPK README description says its rotations are world-to-camera and specifies the Metashape angle convention. The file header begins `Cameras (105)`, while the README describes 32 image exterior orientations. Do not interpret the header's 105 as the number of image records. Parse the actual records and validate 32 unique photo IDs, finite values and rotation-matrix properties after local acquisition.

## Coordinate and independence implications

1. The dataset-specific README explicitly identifies LV95 horizontal coordinates and LN02 heights. This is materially more specific than the collection card's LV95 label. Keep the 2D horizontal CRS and vertical height reference separate in project metadata.
2. Do not silently treat `EPSG:2056` as a complete 3D CRS. Confirm how the chosen ODM release accepts the horizontal projection and height values, and how output products encode Z.
3. The README describes image EXIF GPS as WGS84 and consumer-grade GNSS with metre-level accuracy. These positions are not survey control and should not be treated as independent checkpoints.
4. The supplied OPK orientations originate from a Metashape adjustment that used the ground points as control. They are useful comparison material but are not independent truth and must not be used as an independent accuracy check.
5. Point 100 is explicitly described as having no image measurement and duplicate coordinates with point 206. It cannot serve as a separately measured image checkpoint. Avoid counting coincident records as independent spatial evidence.
6. A future control/checkpoint split must be defined from verified coordinate geometry, observation coverage and project objectives. Do not assign points by ID alone or use the supplied Metashape OPK as a validation reference.

## Remaining local verification gates

- Acquire the exact dataset revision with `acquire_rehearsal_dataset.py`; preserve the commit SHA and provenance manifest.
- Verify all 32 image files by SHA-256, dimensions, decoding and EXIF inventory.
- Parse the complete GCP file and observation CSV; reconcile the 31-versus-30 coordinate-row issue and check unique IDs, coordinate duplicates, observation counts, finite pixel values and image-name mapping.
- Parse the OPK export; check record count, photo-ID mapping, finite camera centres/angles/matrix values, and approximate rotation orthonormality and determinant.
- Only then assess control/checkpoint geometry and create a documented split.
- Run ODM only after the reference-system handling, GCP formatting and split are reviewed.

## Evidence boundary

The statements above are source-document and online text-export findings, not a local byte-level dataset audit. The dataset's declared CC BY 4.0 licence and citation must be retained. No imagery, control coordinates, OPK values or observation rows have been copied into the Spatial Methods repository.
# HEIG-VD drone 2019 — source inspection record

## Review status

**Publisher-source inspection, acquisition/integrity audit, metadata audit and EXIF-only ODM baseline completed; role-blind human visual review remains in progress; no positional-accuracy assessment has been performed.** The immutable dataset snapshot was acquired and audited in GitHub Actions run [44900854170](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44900854170), resolved to publisher revision `e0dfeba2b6ed94ea1ae2bf773e742c39fb437b71`. All 36 manifest files passed size/SHA-256 verification; all 32 source images decoded at 5472 × 3648 px. The metadata audit reconciled 31 GCP records, 206 observations across 30 points, and 32 OPK records, with no missing image references or out-of-bounds observations. The workflow generated 32 annotated image derivatives, two contact sheets, 30 point-level review sheets and a blank 206-row review-decision template. The role-blind packet includes the acquisition manifest and verification report but not the split key or full source imagery. Selected point sheets have received preliminary visual triage, but no full point-level approval register has been completed. A real EXIF-only ODM baseline has since been processed and structurally inspected; no GCP-controlled run or positional-accuracy assessment has been performed.

- Dataset: [HEIG-VD drone 2019 (Yverdon campus)](https://huggingface.co/datasets/heig-vd-geo/scop-datasets/tree/main/datasets/drone_heig_2019)
- Publisher: HEIG-VD, Geomatics group.
- Licence stated in the dataset README: CC BY 4.0.
- Required citation: HEIG-VD, Geomatics group (2026), “HEIG-VD drone 2019 (Yverdon campus)”.
- Acquisition: 16 July 2019, HEIG-VD campus, Yverdon-les-Bains (Cheseaux).
- Platform/sensor: senseFly eBee with S.O.D.A. camera; README states 10.6 mm focal length.
- Image set: 32 original JPG images, 5472 × 3648 pixels; README reports 268 MB. The online folder listing exposes 32 image entries.

## Local acquisition and structural audit

The completed acquisition/metadata audit and role-blind review packet are attached to [workflow run 44900854170](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44900854170). The real EXIF-only processing run is [44899855412](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44899855412), and the successful post-run output inspection is [44901305912](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44901305912). Its acquisition manifest records 36 files; all 36 passed byte-size and SHA-256 comparison against the acquired manifest. The image audit decoded all 32 JPEGs and confirmed 5472 × 3648 dimensions. The structural audit found 31 coordinate records, 206 image observations, 30 observed point IDs, 32 OPK records, no missing observation-to-image mappings, no missing OPK-to-image mappings, and no pixel observations outside the declared image bounds.

The visual-review output contains role-blind annotated derivatives, point-level 640 × 640 review sheets, two contact sheets and a blank observation-level review-decision CSV template. The register is a review instrument, not a completed assessment. The publisher's Metashape image picks are shown only to guide inspection; they are not independent remeasurements. The proposed control/checkpoint split remains unlocked.

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



## EXIF-only ODM baseline and structural output inspection

The first real ODM run used the verified 32-image working copy, without a GCP file, OPK adjustment or checkpoint observations. Processing completed with exit code 0 using ODM 3.6.2 at digest `sha256:a96f56dbc4f775e352fb2b3acc472bb59f456c0948a699eb1c433659dccfbdf7`. The processing run is [44899855412](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44899855412).

The separate post-run output inspection completed with status `inspected`, no blockers and no warnings: [run 44901305912](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44901305912). The evidence and selected products are in [artifact 14706410333](https://github.com/Tessellatum-Inc/spatial-methods/actions/runs/44901305912/artifacts/14706410333).

- Orthophoto: 9172 × 7801 pixels, 0.05 m pixel size, EPSG:32632.
- DSM: 9172 × 7801 pixels, 0.05 m pixel size, EPSG:32632.
- LAZ: 1,963,721 points, LAS 1.4 / point format 7; all coordinates finite; observed count matches header; no points outside header bounds.
- LAZ classification counts contain only class 0 and intensity range is 0–0.
- The LAZ WKT parses but has no explicit EPSG authority identifier; its Transverse Mercator parameters are consistent with UTM zone 32N. Raster products explicitly declare EPSG:32632. Reconcile this before treating the point-cloud CRS as authoritative.

This is a structural processing baseline, not positional-accuracy validation. EXIF GPS is not independent survey control, camera altitude reference is unresolved, and no checkpoint residuals or acceptance decision exist. The initial inspection attempt lacked `pyproj`; the products were preserved and inspected successfully in a separate workflow with `pyproj` installed. Future manual baseline runs include the dependency.

## Remaining verification gates

- Complete the role-blind 206-row observation review and lock it with `lock_visual_review.py` before consulting the split key.
- Confirm the proposed control/checkpoint partition and the separate LV95 horizontal / LN02 vertical reference handling.
- Run the approved control-GCP ODM variant; keep all checkpoints out of adjustment and parameter tuning.
- Independently establish checkpoint image positions or document the limitations of reusing source Metashape picks.
- Compare model coordinates with independent checkpoints using predeclared project-specific criteria and uncertainty treatment.
- Assemble the acquisition-bound evidence dossier and record a human acceptance decision. The EXIF-only baseline is not accuracy validation.

## Evidence boundary

The record combines publisher documentation with a local immutable snapshot and structural audit. The acquisition manifest verifies 36/36 files; all 32 JPGs decoded; the metadata audit reconciled 31 surveyed-point records, 206 observations and 32 OPK rows. The EXIF-only ODM baseline and output inspection are documented above. The dataset's declared CC BY 4.0 licence and citation must be retained. Full source imagery and raw GCP/OPK source files are not committed to the repository; the separate role-blind review artifact contains derived crops and the observation decision template.
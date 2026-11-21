# HEIG-VD coordinate-reference handling decision record

## Purpose

Define the reference-system questions that must be resolved before the HEIG-VD coordinates are passed to ODM or before any reconstructed height is compared with a reference height.

This is a decision record and implementation gate, not a coordinate transformation. No source coordinate values are transformed by this document.

## Source coordinate semantics

The HEIG-VD dataset README identifies:

- horizontal coordinates: CH1903+ / LV95, EPSG:2056, in metres;
- heights: LN02, in metres.

These are distinct horizontal and vertical reference declarations. Do not describe the source tuple as if a single two-dimensional EPSG code fully describes all three ordinates.

## What ODM's GCP format establishes

The ODM GCP format accepts a projection declaration on the first line, followed by rows containing `geo_x geo_y geo_z im_x im_y image_name` and optional point labels. The documentation describes the first-line projection as the projection used for the geographic coordinates.

That file format alone does not prove that a vertical datum is encoded, transformed or preserved in the generated product metadata. In particular, a header of `EPSG:2056` should be treated as the horizontal CRS declaration unless the exact pinned ODM/OpenSfM/PROJ processing path has been demonstrated to carry the LN02 vertical reference explicitly.

Official ODM documentation: https://docs.opendronemap.org/gcp/

## Swiss vertical reference facts

swisstopo identifies LN02 as Switzerland's official height reference and distinguishes it from LHN95. LN02 is based on historical precise levelling and has distortions relative to the newer potential-theoretic LHN95 system. swisstopo states that an exact LN02/LHN95 transformation is not possible because the systems differ in nature and LN02 has distortions; approximate transformation methods are available for practical use.

Relevant official sources:

- Local Swiss reference frames (LV95, LN02 and LHN95): https://www.swisstopo.admin.ch/en/local-swiss-reference-frames
- Height transformations LHN95/LN02: https://www.swisstopo.admin.ch/en/transformations-in-height
- REFRAME web services and supported reference frames: https://www.swisstopo.admin.ch/en/rest-api-geoservices-reframe-web
- Swiss national levelling network LN02: https://www.swisstopo.admin.ch/en/swiss-national-levelling-network-ln02

Do not substitute LHN95 values for LN02 values, or vice versa, without an explicitly selected and documented transformation method and its uncertainty/limitations. Do not treat ellipsoidal GNSS heights as LN02 heights.

## Current decision

**No vertical transformation is authorised for this rehearsal at this stage.**

For the initial control-constrained ODM experiment, the source GCP Z values may only be used unchanged as LN02-valued numeric heights if all of the following are made explicit in the run record:

1. the horizontal coordinates are LV95 (EPSG:2056);
2. the numeric Z values originate in LN02;
3. the ODM first-line projection is only being used to declare the horizontal projected coordinate system;
4. the processing stack's handling of Z and output CRS metadata is verified for the exact pinned ODM image;
5. no claim is made that the output carries a formally encoded LN02 vertical CRS unless that is independently demonstrated.

If ODM or downstream software requires a 3D/compound CRS, select a suitable representation only after verifying support in the pinned versions. Do not invent a compound EPSG code or assign a modern vertical reference to LN02 heights.

## Required implementation checks

Before a real processing run:

- Pin the ODM image by version and record its resolved digest.
- Record ODM, OpenSfM, GDAL and PROJ versions where available.
- Inspect the GCP parser and coordinate transformation path used by that release.
- Use a small, controlled test with known LV95/LN02 values to establish whether horizontal coordinates and Z are passed through as intended.
- Inspect output GeoTIFF, point-cloud and sidecar metadata; verify horizontal CRS, axis order, units and Z semantics separately.
- Preserve source LN02 coordinates and any transformed coordinates as separate immutable records, with transformation tool/version, grid/model, method and provenance.
- If transforming heights, record the method, transformation grid/model, software version and expected accuracy/limitations; do not silently overwrite source heights.
- Confirm that independent checkpoint reference heights and model heights use the same vertical reference and height type before computing vertical residuals.

## Implications for this repository

The current `prepare_odm_gcp.py` writes `EPSG:2056` as the first GCP-list line and copies the source numeric height values unchanged. That is a provisional horizontal-CRS declaration plus numeric Z handoff; it is not proof of an end-to-end 3D reference-system transformation or vertical CRS encoding.

The GCP-preparation report and processing-run record should preserve this distinction. The proposed split is not locked, and no ODM processing or checkpoint accuracy assessment is authorised yet.

## Review status

Pending specialist review of the pinned ODM/OpenSfM/PROJ behaviour and an explicit project decision on output vertical-reference semantics.


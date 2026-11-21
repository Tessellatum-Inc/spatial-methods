# Fiji review contact sheets

`build_fiji_review_contact_sheets.py` creates one label-blind contact sheet per sample. Each distinct acquisition is shown as a two-scale panel:

- **Context:** the complete 256 × 256 RGB chip, with a centre crosshair. At 10 m pixels this is approximately 2.56 km across.
- **Close-up:** a centre crop sized to approximately 320 m using the source RGB pixel resolution, enlarged with nearest-neighbour display interpolation. At 10 m this is 32 × 32 source pixels. The crop remains pixel-faithful; enlargement does not add spatial detail.

The 320 m close-up matches the nominal ground dimensions used by the multispectral extraction (32 × 32 at 10 m and 16 × 16 at 20 m). It is not guaranteed to have identical pixel-grid alignment or exact map bounds: the RGB and multispectral assets are read from independent native grids. Treat it as a same-scale visual comparison aid, not a co-registered overlay or a new raster measurement. The actual source grid and derived crop extent are recorded in the worksheet inventory. If source resolution metadata is absent or inconsistent, the script labels the crop extent as unverified rather than asserting a ground scale.

The script consolidates duplicate catalogue representations of the same Sentinel-2 platform/acquisition within two seconds for display. It keeps all original catalogue rows in the separate provenance CSV and records all item IDs/collections in the worksheet inventory. Different acquisition dates remain separate panels.

Run:

```bash
python build_fiji_review_contact_sheets.py \
  --worksheet /tmp/fiji-blind-review/fiji-blind-review-worksheet.csv \
  --rgb-provenance /tmp/fiji-rgb/stac-imagery-provenance.csv \
  --chips-dir /tmp/fiji-blind-review/chips \
  --output-dir /tmp/fiji-blind-review/review-chips
```

The crosshair marks the sampled coordinate in the chip; it is not a positional-accuracy statement. RGB bands retain their independent per-band 2nd–98th percentile stretch and are not radiometric products. Scene cloud percentage is metadata for the whole scene, not a point-local cloud estimate; use the multispectral SCL summary for local QA and human judgement for interpretation.

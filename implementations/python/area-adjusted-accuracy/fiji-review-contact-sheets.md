# Fiji review contact sheets

`build_fiji_review_contact_sheets.py` creates one image contact sheet per blind sample. It overlays a small centre crosshair at the sample coordinate; the source RGB chips remain unchanged. The imagery extraction code centres each 256-pixel window on the sample point.

The script consolidates duplicate catalogue representations of the same Sentinel-2 platform/acquisition within two seconds for display. It keeps all original catalogue rows in the separate provenance CSV and records all item IDs/collections in the worksheet inventory. Different acquisition dates remain separate panels.

Run:
    python build_fiji_review_contact_sheets.py --worksheet /tmp/fiji-blind-review/fiji-blind-review-worksheet.csv --rgb-provenance /tmp/fiji-rgb/stac-imagery-provenance.csv --chips-dir /tmp/fiji-blind-review/chips --output-dir /tmp/fiji-blind-review/review-chips

The contact sheet is a visual navigation aid. The crosshair is not a positional-accuracy statement. RGB bands retain their independent per-band 2nd–98th percentile stretch and are not radiometric products.

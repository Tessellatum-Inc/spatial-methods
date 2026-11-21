# Fiji blind-review evidence preparation

## Purpose
Prepare a reproducible, label-blind evidence packet for human interpretation of the 25 purposively selected disagreement points. Candidate acquisitions are ranked by evidence availability and local quality. RGB provenance is joined by exact STAC item ID or, when catalogue item IDs differ, by the same point, platform and acquisition timestamp within two seconds. The worksheet separately lists every available RGB chip with its own date and provenance. The workflow never reads, copies, infers or exposes either map's class labels or transition field.

## Candidate ordering
1. Complete co-registered 10 m core bands (B02, B03, B04, B08).
2. Availability of native 20 m SCL quality assessment.
3. Higher local SCL analysis-valid fraction.
4. Lower local SCL cloud/shadow/cirrus fraction.
5. Fewer missing requested bands.
6. Lower scene-wide cloud metadata, only as a tie-breaker.
7. Acquisition date and item ID for deterministic ordering.

This is a review aid, not a classifier. An RGB chip is attached to a multispectral candidate only when item ID or same-platform acquisition time matches. Other RGB chips remain in the per-point inventory with their own dates; do not mistake them for the ranked candidate acquisition.

## Outputs
- `fiji-review-candidate-ranking.csv`: one row per candidate with local QA, rank, RGB match method, matched RGB date/delta and chip path/hash.
- `fiji-blind-review-worksheet.csv`: one row per blind point, primary and alternate candidates, same-acquisition RGB links, complete RGB inventory, and blank reviewer fields for interpretation, confidence, ambiguity, temporal consistency, evidence and limitations.

No map labels, transitions, original accuracy results or automated class predictions are written.

## Run
    python prepare_fiji_blind_review.py --multispectral /path/to/fiji-multispectral-pilot.csv --blind-points data/fiji-worldcover-legend-adjudication-blind-review.csv --rgb-provenance /path/to/stac-imagery-provenance.csv --output-dir /tmp/fiji-blind-review

The RGB provenance file is optional. Keep generated chips and worksheets outside Git unless a deliberately selected review record is approved for version control.

## Review protocol
- Review independently before discussing candidate labels.
- Do not reveal either map's class or transition until independent interpretation is locked.
- Record reviewer and role. If only one person reviews, describe it as single-reviewer adjudication, not independent validation.
- Confidence is ordinal, not a probability. Record ambiguity and plausible alternatives rather than forcing a class.
- Record evidence source, acquisition date, visible cues, spectral context and limitations.
- AI output is not an independent human reference label.
- Preserve the original 834-point baseline and reference labels unchanged. Adjudicated labels belong in a separately versioned dataset with provenance.
- The 25-point sample is purposive and cannot revise the design-based accuracy estimate.

## Quality limitations
SCL is a 20 m scene-classification layer, not a perfect cloud mask or field observation. High local valid fraction does not guarantee interpretability; shadows, haze, mixed pixels, seasonal change and geolocation uncertainty still require human judgement. RGB chips use independent per-band display stretches and are for visual context, not quantitative radiometry.

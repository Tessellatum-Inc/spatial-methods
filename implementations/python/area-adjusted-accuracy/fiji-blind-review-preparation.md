# Fiji blind-review evidence preparation

## Purpose
Prepare a reproducible, label-blind evidence packet for human interpretation of the 25 purposively selected disagreement points. This workflow ranks candidate acquisitions by evidence availability and local quality, joins RGB chip provenance where exact sample/item IDs match, and creates a separate reviewer worksheet. It must never read, copy, infer, or expose either map's class labels or the transition field.

## Candidate ordering
The script uses a transparent lexicographic ordering, not an opaque weighted score:
1. Complete co-registered 10 m core bands (B02, B03, B04, B08).
2. Availability of native 20 m SCL quality assessment.
3. Higher local SCL analysis-valid fraction.
4. Lower local SCL cloud/shadow/cirrus fraction.
5. Fewer missing requested bands.
6. Lower scene-wide cloud metadata, only as a tie-breaker.
7. Acquisition date and item ID for deterministic ordering.

This is a review aid, not a classifier. Inspect alternate dates because seasonality, crop cycles, land management and real change can make temporal context decisive. No assumed reference-image date is privileged.

## Outputs
- `fiji-review-candidate-ranking.csv`: one row per candidate scene-point, with rank, bands, local SCL QA, scene cloud metadata and RGB chip path/hash when an exact item-ID match exists.
- `fiji-blind-review-worksheet.csv`: one row per blind point, top candidate and up to two alternates, plus blank reviewer fields for identity/role, review date, class, confidence, ambiguity, alternative class, temporal consistency, visible evidence, spectral context, limitations and adjudication notes.

No map labels, transitions, original accuracy results or automated class predictions are written.

## Run
From this directory:
    python prepare_fiji_blind_review.py --multispectral /path/to/fiji-multispectral-pilot.csv --blind-points data/fiji-worldcover-legend-adjudication-blind-review.csv --rgb-provenance /path/to/stac-imagery-provenance.csv --output-dir /tmp/fiji-blind-review

The RGB provenance file is optional. The multispectral CSV and blind-point input are required. Keep generated chips and worksheets outside Git unless a small, deliberately selected review record is approved for version control.

## Review protocol
- Review independently before discussing candidate labels.
- Do not reveal either map's class or the transition until the independent interpretation is locked.
- Record reviewer and role. If only one person reviews, describe it as single-reviewer adjudication, not independent validation.
- Confidence is ordinal, not a probability. Record ambiguity and plausible alternatives rather than forcing a class.
- Record evidence source, acquisition date, visible cues, spectral context and limitations.
- AI may help describe evidence or check workflow consistency, but AI output is not an independent human reference label.
- Preserve the original 834-point baseline and reference labels unchanged. Any adjudicated labels belong in a separately versioned dataset with provenance.
- The 25-point sample is purposive and cannot revise the design-based accuracy estimate.

## Quality limitations
SCL is a 20 m scene-classification layer, not a perfect cloud mask or field observation. High local valid fraction does not guarantee interpretability; shadows, haze, mixed pixels, seasonal change and geolocation uncertainty still require human judgement. RGB chips use independent per-band display stretches and are for visual context, not quantitative radiometry.

# Fiji–WorldCover point-level legend adjudication pilot

## Purpose
This 25-point pilot moves the Fiji–WorldCover comparison from documentary legend review to point-level visual review. It tests the adjudication procedure; it is **not** a probability sample and must not be used to estimate accuracy or the prevalence of error causes.

## Pilot selection
Five geographically dispersed points were selected from each major disagreement group: tree → shrubland (5 of 89), tree → grassland (5 of 52), grassland → agriculture (5 of 38), tree → agriculture (5 of 25), and herbaceous wetland → tree (5 of 7). Selection used a deterministic maximin procedure in longitude/latitude space, scaling longitude by the cosine of each group's mean latitude. The first point was the lexicographically smallest sample ID; each subsequent point maximised its minimum distance to the selected points. This is a practical coverage strategy, not a formal spatial sampling design.

## Review sequence
1. Obtain imagery as close as possible to the 2021 reference period and suitable to the point's spatial context.
2. Record provider, product, acquisition date/composite period, access date, resolution/scale, scene or URL, display stretch and review-window dimensions.
3. Where practical, first interpret without showing either map label. Record visible evidence, independent class and confidence.
4. Reveal the Fiji reference label and WorldCover prediction; adjudicate without forcing a conclusion.
5. Preserve alternatives and reasons. Send ambiguous or consequential cases for independent second review where feasible.

## Primary adjudication categories
- `ontology_or_crosswalk`: legend definitions differ.
- `likely_worldcover_classification_error`: imagery supports the Fiji label more strongly.
- `likely_reference_interpretation_uncertainty`: imagery does not clearly support the supplied Fiji label.
- `temporal_difference`: evidence of change between relevant image dates.
- `spatial_support_or_mixed_pixel`: boundary or heterogeneous cover at pixel support.
- `insufficient_imagery`: imagery unavailable, obscured, unsuitable or too coarse.
- `unresolved`: evidence does not support a defensible conclusion.

These are review judgements, not ground truth. Record secondary factors in notes.

## Safeguards
- Both products target 2021, but acquisition dates, seasons, sensors, compositing and spatial support may differ.
- The related Fiji class-definition document is context, not a confirmed operational manual for all 834 points.
- Apply WorldCover definitions from the 2021 v200 Product User Manual.
- InputQuality is an observation diagnostic, not a per-pixel class probability.
- Do not infer causes from transitions alone.
- Do not redistribute Planet NICFI or Google basemap imagery/screenshots unless the applicable terms permit it. Prefer source identifiers and access metadata.
- Keep the design-based accuracy estimates separate from this purposive visual review.

## Completion criteria
Before scaling up, confirm imagery access and licence constraints, traceable imagery metadata, blind first-pass interpretations, consistent adjudication, and second review of ambiguous cases. If imagery cannot be accessed or used lawfully, record that limitation rather than substituting an unverified source.

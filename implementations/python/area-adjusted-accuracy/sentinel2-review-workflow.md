# Sentinel-2 imagery workflow for the Fiji blind-review pilot

## Purpose

This workflow supplies independent visual context for the 25 purposively selected Fiji–WorldCover disagreement points. It uses Sentinel-2 Level-2A surface reflectance in Google Earth Engine (GEE), with a joined per-pixel cloud-probability mask.

The script is deliberately blind: it contains point IDs and coordinates only. It does not expose the Fiji reference class, the WorldCover prediction, or the transition group.

This is an imagery-review aid, not a new accuracy assessment and not a substitute for field reference data.

## Open and run the script

1. Sign in to the [Google Earth Engine Code Editor](https://code.earthengine.google.com/).
2. Create a new script.
3. Copy the complete contents of [gee-sentinel2-blind-review.js](./gee-sentinel2-blind-review.js) into the editor.
4. Click **Run** and authorize access if prompted.
5. In the map layer list, begin with **2021 annual median RGB**. Turn on the quarterly layers to inspect seasonal differences.
6. Click a point with the map Inspector to confirm its sample ID. To centre the map on another point, change `FOCUS_SAMPLE_ID` near the top of the script and run it again.
7. Record observations in the blind first-pass sheet before revealing either land-cover label.

## Imagery and processing choices

- Collection: `COPERNICUS/S2_SR_HARMONIZED` (Level-2A surface reflectance).
- Period: 1 January–31 December 2021.
- Cloud masking: join `COPERNICUS/S2_CLOUD_PROBABILITY` by `system:index`; mask pixels with cloud probability of 40 or higher.
- Edge masking: apply the B8A and B9 masks to reduce unreliable scene-edge pixels.
- Composites: annual median and four calendar-quarter medians.
- Display: B4/B3/B2 true colour; annual NDVI is provided as optional contextual evidence.
- Pilot locations: 25 points, displayed without reference or predicted classes.

Sentinel-2's visible and near-infrared bands used here are 10 m. Some other bands, including SWIR bands, are 20 m; do not describe every Sentinel-2 band as 10 m.

## Review protocol

For each point:

1. Confirm the sample ID and inspect the point and its 150 m context.
2. Start with the annual median, then inspect all available quarterly composites.
3. Check the printed scene IDs, acquisition dates and scene-level cloudiness for the focus point. A composite is not a single acquisition; record the contributing date range and the relevant scene identifiers where possible.
4. Record the imagery source, product, date or composite period, access date, resolution, review window, visible evidence, independent first-pass class and confidence in the blind sheet.
5. If the point is obscured, mixed, near a boundary or unsupported by usable imagery, record that limitation rather than forcing a class.
6. Only after the blind first pass, reveal the Fiji reference and WorldCover labels and complete adjudication.

Use the existing adjudication categories in the pilot protocol. Keep the design-adjusted accuracy estimates separate from these purposive visual judgements.

## Important limitations

- Sentinel-2 at 10 m is substantially coarser than Planet NICFI imagery and some Google basemap imagery. Small fields, narrow features, settlements and mixed pixels may be difficult to interpret.
- Quarterly and annual medians can suppress short-lived events and can combine observations from different dates. Inspect individual scene metadata where temporal change is suspected.
- Cloud probability is an imperfect mask; bright surfaces can also receive high probabilities. The threshold of 40 is a working choice, not a validated optimum. For uncertain points, rerun at 30 and 50 and note whether the interpretation changes.
- The Fiji reference labels were visually interpreted from multiple sources. Sentinel-2 is an additional evidence source, not fully independent field truth.
- Do not infer the accuracy of either map from this 25-point purposive pilot.
- Follow the applicable Copernicus data terms and Earth Engine terms. Do not redistribute third-party basemap imagery or screenshots unless their terms permit it.

## Official dataset documentation

- [Sentinel-2 Level-2A Harmonized — Earth Engine Data Catalog](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED)
- [Sentinel-2 Cloud Probability — Earth Engine Data Catalog](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_CLOUD_PROBABILITY)

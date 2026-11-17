# Canopy-height local maxima and watershed crown segmentation

A canopy height model (CHM) expresses canopy elevation above a ground surface.
A common individual-tree workflow detects local treetop maxima, uses them as
markers, and segments the canopy surface into crown regions.

## Marker-controlled watershed

The reference workflow:
1. masks cells below a canopy-height threshold;
2. finds local maxima in a configurable neighbourhood;
3. merges connected maximum plateaus and chooses one deterministic seed per
   plateau;
4. runs watershed on the negative CHM, so regions grow outward from treetops.

## Implementation and limits

See [the Python implementation](../../implementations/python/chm-watershed-crowns/README.md).
This is a basic CHM watershed baseline, not a reproduction of Dalponte's
method or a point-cloud-native segmentation system. Seed-window size,
canopy threshold, CHM resolution and forest structure influence crown
boundaries. Validate against reference delineations.

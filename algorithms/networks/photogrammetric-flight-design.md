# Photogrammetric flight-design calculations

For a nadir pinhole camera at height H above local ground, pixel pitch p and
focal length f, the ground sample distance is GSD = H p / f.

For physical sensor width W and height L, the approximate nadir ground
footprint is (H W/f, H L/f). Required side overlap o_s and forward overlap
o_f imply maximum adjacent-line and exposure spacings:

    line spacing = footprint width (1 - o_s)
    exposure spacing = footprint height (1 - o_f)

All quantities must use consistent length units. The model assumes a nadir
camera, a locally planar ground surface and negligible lens distortion.

The reference package does not solve terrain-following paths, camera-footprint
polygon coverage, aircraft dynamics, battery constraints or multi-UAV
scheduling.

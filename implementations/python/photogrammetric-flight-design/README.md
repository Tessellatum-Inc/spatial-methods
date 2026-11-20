# Photogrammetric flight-design calculations

Pure-Python nadir-camera calculations for ground sample distance, image
footprint, and maximum image-center spacing under specified forward and side
overlap fractions.

## Equations

For flying height H above local ground, pixel pitch p and focal length f,
the nadir ground sample distance is GSD = H p / f.

For sensor width W and height L, the approximate nadir footprint is
(H W / f, H L / f). Given side overlap o_s and forward overlap o_f, the
maximum line and exposure spacings are footprint_width(1-o_s) and
footprint_height(1-o_f), respectively.

All lengths must use consistent units. Height is above local ground, not
necessarily above mean sea level. The pinhole approximation assumes a
near-nadir camera and locally planar terrain.

## Connected learning material

See [Photogrammetric image acquisition](../../../collection/photogrammetry/image-acquisition.md) for the measurement and acquisition principles behind these calculations, including the distinction between GSD and positional accuracy, image geometry, control and quality assurance.

## Limitations

The package does not design terrain-following paths, account for relief
displacement, camera tilt, lens distortion, rolling shutter, wind, aircraft
dynamics, battery limits, turn geometry, multi-UAV assignment or camera
footprint polygon coverage. It provides planning calculations, not a flight
controller or complete photogrammetric mission planner.

## Run

    python -m pytest -q

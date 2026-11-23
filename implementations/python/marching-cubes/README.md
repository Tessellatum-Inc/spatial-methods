# Marching-cubes isosurface extraction

A validated wrapper around scikit-image's Lewiner marching-cubes algorithm.
It extracts a triangle mesh from a finite 3-D scalar volume at a requested
isosurface level.

## Coordinate convention

Volume axes are ordered (axis0, axis1, axis2). The wrapper transforms voxel
vertices using the supplied three-axis spacing and origin. It returns
vertices, triangular faces, vertex normals and sampled scalar values.

## Run

Install with python -m pip install -r requirements.txt, then run
python -m pytest -q.

## Limits

This deliberately delegates the lookup/configuration details to the maintained
scikit-image implementation; it is not a new implementation of the
marching-cubes lookup tables. It does not perform Poisson surface
reconstruction, mesh repair, decimation, texturing or point-cloud registration.
Check axis conventions, handedness, spacing and units when connecting a mesh
to geospatial or photogrammetric coordinate frames.

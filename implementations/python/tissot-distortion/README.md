# Tissot indicatrix and projection distortion

A NumPy-free finite-difference implementation of local map-projection distortion diagnostics. Supply a callable that maps longitude/latitude degrees to projected x/y in the same linear units as the spherical Earth radius.

The local Jacobian is expressed against east/north ground distances. Its singular values are the major and minor Tissot scale factors; the absolute determinant is the local area scale; maximum angular deformation is computed from the ratio of the principal scales.

## Run

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Assumptions and limitations

This is a local numerical diagnostic on a spherical Earth. It uses central finite differences and assumes the projection is smooth over the selected step. It is not a projection implementation or projection-selection optimizer. It does not model ellipsoidal geodesics, projection discontinuities, pole singularities, global distortion extrema, or datum transformations. Longitude/latitude are degrees; projected output and earth_radius must share linear units. Avoid evaluating across projection seams and document the step-size sensitivity.

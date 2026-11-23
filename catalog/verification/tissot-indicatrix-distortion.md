# Verification dossier: Tissot indicatrix diagnostics

## Implemented
- Central finite-difference projection Jacobian relative to local spherical east/north ground distances.
- Principal major/minor scale factors from singular values.
- Local area scale and maximum angular distortion.

## Independent tests
- Spherical Mercator is tested for conformality and expected sec(latitude) scale.
- Equirectangular projection is tested for its latitude-dependent parallel scale and area factor.
- Unit local scale, polar/non-finite inputs, invalid finite-difference settings and non-finite projection output are tested.

## Exclusions
Ellipsoidal reference surfaces, projection families, discontinuity/seam handling, global distortion optimisation and uncertainty bounds remain outside scope. The broad projection-distortion source entry is Partial.

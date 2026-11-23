# Verification dossier: spherical polygon area

## Implemented scope

Spherical area from latitude/longitude rings using unit-vector signed spherical excesses, with optional hole subtraction and caller-supplied sphere radius.

## Independent tests

Tests compare a spherical right triangle with its analytic spherical excess, check orientation invariance, exercise an antimeridian-crossing rectangle, accept a repeated closing coordinate, verify hole subtraction, and reject malformed, non-finite, out-of-range, duplicate/ambiguous rings and invalid radii.

## Exclusions

The implementation is spherical rather than ellipsoidal and assumes simple, unambiguous rings. Other spherical geometry structures and grids remain open; the source row is Partial.
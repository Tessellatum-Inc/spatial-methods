# Source verification — Nicholl–Lee–Nicholl line clipping

## Identity and bibliography
- Nicholl, T. M., Lee, D. T., & Nicholl, R. A. (1987). “An efficient new algorithm for 2-D line clipping: Its development and analysis.” *Computer Graphics*, 21(4), 253–262. DOI 10.1145/37401.37432.

## Technical claims
- NLN is a rectangular 2D segment-clipping method.
- It uses endpoint-region classification and slope sectors to select boundary intersections.
- The repository implementation reduces endpoints to canonical regions through rotations/reflections and explicit branch cases.

## Implementation and tests
- Implemented in the shared line-clipping package.
- Tests include hand-constructed intersections, horizontal/vertical and boundary cases, degenerate windows, zero-length segments, and 2,000 seeded random differential cases against Liang–Barsky.

## Limits and rights
Floating-point rectangular clipping only. No polygon clipping, arbitrary convex windows or exact arithmetic. Original implementation and explanatory text; bibliographic metadata only.

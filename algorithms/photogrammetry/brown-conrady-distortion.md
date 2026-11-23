# Brown-Conrady lens distortion

The Brown-Conrady model represents radial and decentering/tangential lens
distortion in normalized camera-plane coordinates. It is commonly used as one
component of a camera model, not as a complete photogrammetric calibration.

## Forward model

For normalized coordinates (x,y), let r²=x²+y². With radial coefficients
k1,k2,k3 and tangential coefficients p1,p2:

    radial = 1 + k1*r² + k2*r⁴ + k3*r⁶
    xd = x*radial + 2*p1*x*y + p2*(r² + 2*x²)
    yd = y*radial + p1*(r² + 2*y²) + 2*p2*x*y

Pixel coordinates are related through camera intrinsics; apply the intrinsic
normalization before distortion and the inverse mapping afterward.

## Inversion

The inverse solves the two-coordinate nonlinear system using Newton iterations
and the analytic Jacobian. The reference implementation checks for singular
Jacobians and verifies the final residual. Strong distortion or poor initial
conditions may cause non-convergence; the implementation reports this rather
than silently returning an inaccurate point.

## Implementation and limits

See [the Python implementation](../../implementations/python/brown-conrady/README.md).
It implements forward and inverse distortion only. It does not estimate camera
intrinsics or coefficients, perform boresight calibration, or replace bundle
adjustment. Those are separate source methods and workflows.

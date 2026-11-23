# Brown-Conrady lens distortion

A NumPy reference for radial (k1, k2, k3) and tangential (p1, p2) lens
distortion in normalized camera-plane coordinates, plus Newton inversion.

## Coordinate contract

Input points end in an (x, y) dimension and may have arbitrary leading
dimensions. Coordinates are normalized camera-plane coordinates, not pixel
coordinates. Convert pixels using the camera intrinsics before applying this
model, and convert back afterward.

The forward model is

    r2 = x*x + y*y
    radial = 1 + k1*r2 + k2*r2*r2 + k3*r2*r2*r2
    xd = x*radial + 2*p1*x*y + p2*(r2 + 2*x*x)
    yd = y*radial + p1*(r2 + 2*y*y) + 2*p2*x*y

The inverse uses Newton steps with the analytic 2x2 Jacobian. It raises if
the Jacobian is singular or the requested residual tolerance is not achieved.

## Run

Install with python -m pip install -r requirements.txt and run python -m pytest -q.

## Limits

This is a forward/inverse distortion model, not a camera-calibration optimiser.
It does not estimate intrinsics, distortion coefficients, focal length,
principal point, boresight alignment, rolling-shutter effects or a complete
bundle adjustment. Calibrate coefficients from an appropriate target and
validate residuals across the image field before metric photogrammetric use.

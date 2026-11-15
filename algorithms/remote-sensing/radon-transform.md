# Radon transform

## Purpose

The Radon transform maps an image into a sinogram of line integrals indexed by angle and perpendicular offset. It underpins tomographic reconstruction and provides a continuous-line-integral counterpart to discrete voting methods such as the Hough transform.

## Implemented scope

The reference implementation samples parallel lines using bilinear interpolation and approximates each line integral by unit-spaced summation. It supports user-supplied angles, rho spacing and an optional inscribed-circle mask for square images. See [implementation](../../implementations/python/radon-transform/README.md).

## Distinction from Hough

The Radon transform accumulates image intensity along lines; the standard Hough transform accumulates votes from edge points in parameter space. They are related geometrically but are not interchangeable algorithms.

## Limitations

This direct method is computationally expensive and discretisation-dependent. It does not implement filtered back-projection or inverse reconstruction.

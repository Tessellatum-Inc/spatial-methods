# Hough transform for straight-line detection

## Purpose

The line Hough transform maps edge pixels into a parameter space and accumulates votes for candidate lines. It is useful for detecting approximately straight structures despite gaps or local edge noise.

## Line parameterisation

Use rho = x cos(theta) + y sin(theta), where rho is the signed perpendicular distance from the origin and theta is the normal angle. This avoids the infinite-slope singularity of y = mx + b.

## Implemented scope

The NumPy implementation builds a dense rho-theta accumulator from nonzero edge pixels and extracts peaks with rectangular non-maximum suppression. It does not estimate segment endpoints or implement probabilistic Hough sampling. See [implementation](../../implementations/python/hough-lines/README.md).

## Practical cautions

The result depends on theta and rho quantisation, edge quality, accumulator peak suppression and image coordinate conventions. A line and its equivalent representation (-rho, theta + pi) describe the same geometric line; the default theta range avoids a full redundant period.

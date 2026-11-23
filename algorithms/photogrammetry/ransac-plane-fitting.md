# RANSAC plane fitting

RANSAC estimates a geometric model despite outliers by repeatedly drawing a
minimal sample, fitting a candidate and scoring observations against a
distance threshold. For a 3D plane the model is

    a*x + b*y + c*z + d = 0,

with orthogonal residual

    |a*x + b*y + c*z + d| / sqrt(a*a + b*b + c*c).

The reference implementation samples three points, skips collinear triples,
selects the largest consensus set with residual-sum tie breaking, and refits
the selected points by total least squares (SVD). It returns the unit normal,
offset, inlier mask and residuals.

See [the Python implementation](../../implementations/python/ransac-plane-fitting/README.md).
This is a single-plane baseline; it is not a general shape-fitting suite or a
guaranteed ground classifier. A dominant fitted plane need not represent the
terrain surface.

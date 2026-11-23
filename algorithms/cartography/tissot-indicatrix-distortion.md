# Tissot indicatrix projection-distortion diagnostics

The local projection Jacobian maps differential east/north ground distances to projected coordinate changes. Its singular values are the principal linear scale factors of the Tissot indicatrix. The absolute Jacobian determinant is the local areal scale. The maximum angular deformation is 2 asin((a-b)/(a+b)), where a and b are the major and minor principal scales.

This implementation estimates the Jacobian by central finite differences of a caller-supplied projection. It assumes a spherical Earth, smooth projection behaviour in the finite-difference neighbourhood, and consistent linear units for projected coordinates and Earth radius. It excludes ellipsoidal geodesy, projection formulae, seam handling, global projection selection and numerical uncertainty analysis.

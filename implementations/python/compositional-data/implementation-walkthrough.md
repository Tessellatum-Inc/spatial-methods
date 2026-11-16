# Compositional data analysis — implementation walkthrough

## 1. Why closure matters

Parts of a whole carry relative information. If a composition is multiplied by a positive constant, its ratios do not change. Closure divides each part by the row total to put the composition on the unit simplex.

## 2. CLR coordinates

The centered log-ratio transform subtracts the mean log part (the log geometric mean) from each log part. CLR coordinates sum to zero, so the full D-dimensional coordinate covariance is singular.

## 3. ILR coordinates

The isometric log-ratio transform projects log parts onto an orthonormal basis orthogonal to the all-ones vector. This implementation uses the Helmert basis and returns D−1 coordinates. The inverse multiplies by the transposed basis and closes the exponentiated values.

## 4. ALR coordinates

The additive log-ratio transform uses one part as a denominator and returns D−1 log ratios. Its interpretation depends on that denominator, unlike the Aitchison distance.

## 5. Zero values

A zero cannot be logged. Do not replace every zero with an arbitrary tiny constant. First determine whether it is structural, rounded or censored, then choose a replacement or model consistent with the measurement process. This implementation rejects zeros in log-ratio methods and does not automate replacement.

## 6. Tests and scope

Tests check closure, scale invariance, CLR centring, ILR/ALR round trips, Helmert orthonormality, Aitchison-distance isometry and invalid inputs. Compositional kriging and spatial regression remain separate, unimplemented methods.

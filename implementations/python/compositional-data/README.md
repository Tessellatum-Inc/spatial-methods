# Compositional data analysis

NumPy implementation of the closure, centered log-ratio (CLR), additive log-ratio (ALR), and isometric log-ratio (ILR) transforms, plus Aitchison distance.

## Quick start

~~~python
from logratio import closure, clr, ilr, ilr_inverse, aitchison_distance

parts = [12, 25, 63]
print(closure(parts))
print(clr(parts))
coordinates = ilr(parts)
print(coordinates)
print(ilr_inverse(coordinates))
print(aitchison_distance([12, 25, 63], [20, 20, 60]))
~~~

## Important conventions

- A composition represents relative parts of a whole; multiplying every part by the same positive constant does not change its information.
- CLR coordinates sum to zero and therefore have a singular covariance matrix in the full D-dimensional representation.
- ILR uses one fixed orthonormal Helmert basis to represent a D-part composition in D−1 Euclidean coordinates. Other orthonormal balances are possible; individual coordinates depend on the chosen basis, while Aitchison distance does not.
- ALR coordinates depend on the selected denominator part.
- Log-ratio transforms require strictly positive parts. This package does not silently replace zeros. Structural zeros, rounded zeros and below-detection-limit values need different domain-specific treatment.
- Closure accepts nonnegative parts but requires a positive finite total. CLR, ALR, ILR and Aitchison distance reject zero parts.

## Scope and limitations

This package implements compositional geometry and coordinate transforms only. It does not implement zero replacement, missing-part imputation, compositional regression, compositional kriging, Bayesian models, spatial dependence or uncertainty propagation. It is not appropriate to apply ordinary Euclidean methods directly to raw proportions without considering the simplex geometry.

## Run

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q --import-mode=importlib
~~~

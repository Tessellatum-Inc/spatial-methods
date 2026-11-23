# Radial-basis-function interpolation (2D)

A NumPy-based global interpolator for finite planar point samples. The
reference implementation supports three radial kernels:

- Thin plate: `phi(r) = r² log(r)`, with `phi(0) = 0`.
- Cubic: `phi(r) = r³`.
- Gaussian: `phi(r) = exp(-(epsilon r)²)`.

An affine polynomial tail is included in the augmented saddle-point system,
so affine fields are reproduced when the system is nonsingular. Coordinates
are centered and scaled before fitting. A non-negative diagonal smoothing
parameter trades exact interpolation for regularization. The helper
select_rbf_smoothing chooses among caller-supplied positive smoothing values
using exact leave-one-out refits, with one held-out observation per fit.

## Use

```python
from rbf_interpolation import rbf_interpolate

predicted = rbf_interpolate(
    points=[(0, 0), (1, 0), (0, 1), (1, 1)],
    values=[1, 2, 3, 4],
    queries=[(0.25, 0.25), (0.75, 0.5)],
    kernel="thin_plate",
)
```

Install dependencies and run tests:

```bash
python -m pip install -r requirements.txt
python -m pytest -q
```

## Limits

This is a dense global 2D teaching baseline. Fitting requires a dense solve
and scales cubically in the number of observations; prediction costs
O(mn) for m queries and n samples. It is not a local RBF, a geostatistical
kriging estimator, or a complete spline toolbox. It does not estimate
kernel shape or epsilon, search a continuous smoothing range, model anisotropy,
barriers, measurement uncertainty or spatially varying trends, or provide
prediction intervals. The Gaussian shape parameter is user supplied.
Collinear points and duplicate coordinates are rejected. Use projected
coordinates with meaningful planar units.

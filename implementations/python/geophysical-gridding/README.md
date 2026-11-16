# Geophysical gridding baselines

Seven scattered-point gridding methods for regular output grids:
- nearest-neighbour assignment using a spatial k-d tree, optionally masking nodes beyond a maximum distance;
- piecewise-linear interpolation over a Delaunay triangulation using barycentric coordinates, with an explicit outside-convex-hull fill value;
- thin-plate-spline radial-basis interpolation, the minimum-bending-energy surface with an affine polynomial tail and optional smoothing;
- ordinary kriging with an explicitly supplied exponential covariance model, returning both prediction and kriging variance;\n- Cressman successive-correction objective analysis with decreasing influence radii;\n- Barnes Gaussian successive-correction objective analysis with explicit kappa and relaxation parameters;\n- weighted or unweighted polynomial trend surfaces of total degree one through three.

The thin-plate spline is a minimum-bending-energy (thin-plate) surface and a minimum-curvature-style interpolant. It is not the classic Briggs iterative minimum-curvature gridding algorithm; exact algorithm equivalence is not claimed. All methods assume planar coordinates in consistent units. Nearest-neighbour creates Voronoi regions; Delaunay interpolation is limited to the convex hull and has piecewise-constant gradients within each triangle; thin-plate splines and covariance-based kriging can return values beyond the convex hull, where model assumptions dominate. Sparse or uneven sampling can create artefacts.

A separate [discrete biharmonic fixed-boundary solver](discrete_biharmonic.py) fills unknown interior nodes on an already defined regular grid by minimizing squared five-point Laplacian curvature. It requires a fixed finite perimeter and is a small-grid teaching baseline, not the full Briggs scattered-data program. See its [tests](test_discrete_biharmonic.py), [walkthrough](discrete-biharmonic-walkthrough.md) and [lab](../../../notebooks/discrete-biharmonic-gridding-lab.ipynb).

Run python -m pip install -r requirements.txt and python -m pytest -q.


See the [gridding methods lesson](../../../methods/geophysical-gridding.md) and [implementation walkthrough](implementation-walkthrough.md).

Ordinary kriging does not estimate its own variogram: range, sill and nugget are supplied by the caller. The dense solver is intended for small teaching examples, not large surveys.


Cressman and Barnes are objective-analysis methods: they start from an explicit first-guess grid (zero by default), interpolate that field to observation locations, and iteratively spread residual corrections back to grid nodes. Both require observations inside the rectangular analysis domain and strictly decreasing radii in the same planar units as the coordinates. The Cressman weight is $(R^2-d^2)/(R^2+d^2)$ for $d<R$; the Barnes baseline uses $\exp(-d^2/(\kappa R^2))$ and a per-pass relaxation factor $\gamma$. These parameterized educational implementations make the successive-correction contract explicit; they are not a claim of bit-for-bit equivalence with every operational Barnes/Cressman variant.


Polynomial trend surfaces fit a global least-squares polynomial in centred/scaled coordinates. Degrees 1–3 are supported, with optional positive observation precision weights. The method is global and extrapolates beyond the sample footprint; weights are not a robust-regression procedure, and high-degree surfaces can oscillate or overfit. Use spatially blocked validation and inspect residual structure before interpreting the trend.

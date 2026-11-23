# Verification record: Voronoi point-process intensity

## Identity
- Canonical record: inverse-area Voronoi intensity estimator in a bounded planar window.
- Implementation: implementations/python/spatial-intensity/voronoi_intensity.py.
- Classification: clipped rectangular-window Voronoi tessellation and piecewise-constant inverse-cell-area estimate.

## Bibliographic verification
- Barr & Schoenberg (2010), Biometrika 97(4), 977–984, DOI 10.1093/biomet/asq047, defines and studies the Voronoi estimator for inhomogeneous planar Poisson intensity.
- Moradi et al. (2019), Statistics and Computing 29, 995–1010, DOI 10.1007/s11222-018-09850-0, studies resample-smoothing as a separate variance-reduction extension.

## Technical checks
- Cell inequalities are derived from squared Euclidean distances and represented as linear half-planes.
- Each site cell is clipped against the rectangular study window.
- Areas are computed by the polygon shoelace formula.
- The sum of cell areas is checked against the window area.
- Intensity is the reciprocal of clipped cell area.
- Boundary bias and estimator variability are explicitly documented.

## Reproduction and rights
- Original NumPy implementation and tests.
- Tests cover single-site, bisector split, regular grid partition, asymmetric sites and invalid inputs.
- No third-party source code, figures or data are reproduced.
- Repository CI pending.

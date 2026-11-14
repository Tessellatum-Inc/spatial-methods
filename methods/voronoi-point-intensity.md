# Voronoi tessellation intensity estimation

## Definition

Given observed sites \(x_1,\ldots,x_n\) in a bounded study window \(W\), the Voronoi cell associated with site \(x_i\) is the subset of \(W\) closer to \(x_i\) than to any other observed site:

\[
V_i=\{u\in W:\|u-x_i\|\leq\|u-x_j\|,\ \forall j\ne i\}.
\]

The classical Voronoi intensity estimate is piecewise constant on each cell, with value

\[
\widehat\lambda(u)=\frac{1}{|V_i|},\qquad u\in V_i.
\]

Small cells indicate high local point concentration; large cells indicate lower concentration. Barr and Schoenberg (2010) study the statistical properties of this estimator for inhomogeneous planar Poisson processes.

## Implemented baseline

The companion NumPy function constructs each cell by starting with a rectangular study window and clipping it against the perpendicular-bisector half-plane for every other site. It returns cell polygons, clipped areas and reciprocal-area intensity values. The implementation verifies that the cells partition the full rectangle.

## Boundary and statistical caveats

The implementation uses only observed sites inside the supplied window and clips their cells to the window. It does not correct for unobserved points outside the boundary; edge effects can therefore distort cell areas and local estimates near the boundary. Guard points, larger observation windows, border corrections or model-based edge treatment may be needed. The raw Voronoi estimator is adaptive but can be highly variable and sensitive to point locations; resample-smoothing is a distinct extension not implemented here.

This is not a Delaunay tessellation field estimator, network Voronoi estimator, centroidal Voronoi estimator, kernel estimator or a complete spatial point-process inference workflow. Complexity is dense and intended for small point sets.

## Reproduction

Run from implementations/python/spatial-intensity:

~~~bash
python -m pytest -q --import-mode=importlib
~~~

## References

- Barr, C. D., & Schoenberg, F. P. (2010). On the Voronoi estimator for the intensity of an inhomogeneous planar Poisson process. *Biometrika*, 97(4), 977–984. DOI: 10.1093/biomet/asq047.
- Moradi, M. M., Cronie, O., Rubak, E., Lachieze-Rey, R., Mateu, J., & Baddeley, A. (2019). Resample-smoothing of Voronoi intensity estimators. *Statistics and Computing*, 29, 995–1010. DOI: 10.1007/s11222-018-09850-0.

This lesson paraphrases the published estimator and does not reproduce source code, figures or data.

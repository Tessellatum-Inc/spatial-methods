# OD flow clustering, line KDE and hotspots

## Flow clustering

An OD record is represented by ((x_o,y_o,x_d,y_d)). The reference implementation applies DBSCAN after independent origin and destination coordinate scaling. This makes the clustering metric explicit: a unit of origin separation need not have the same weight as a unit of destination separation. Noise records receive label -1.

## Line-integrated flow KDE

For flow segment (L_i(t)=o_i+t(d_i-o_i)), (t\in[0,1]), the density at grid location (x) is

\[
\hat f(x)=\sum_i w_i\int_0^1
\frac{1}{2\pi h^2}
\exp\left(-\frac{\|x-L_i(t)\|^2}{2h^2}\right)dt.
\]

The integral is approximated by Gauss–Legendre quadrature. This treats each flow's weight as uniformly distributed along its straight segment. It is not a network-constrained kernel and does not preserve route geometry.

## Hotspot extraction

A hotspot cell is a finite grid value that is a local maximum in a caller-defined odd-sized neighbourhood and is at or above a caller-selected quantile of all finite grid values. This is descriptive peak extraction, not a Getis–Ord or permutation significance test.

## Verification and limitations

Tests cover DBSCAN corridor separation and noise, symmetry of a horizontal segment density, weight linearity, the zero-length point-kernel limit and a synthetic single hotspot. Projected coordinate units and bandwidth must be consistent.

See the [implementation package](../../implementations/python/flow-analysis/README.md).

# Cross-type point-pattern summary functions

Stable ID: SA-STAT-CROSS-POINT-SUMMARIES · Supplementary companion to source compendium section 2, page 3

## The question

A marked point pattern contains event locations and a categorical type (for example, two tree species, service types or incident categories). Cross-type summaries ask how events of type j are arranged around a typical event of type i. They describe interaction between component patterns, rather than the within-type structure of either pattern alone.

The functions below assume two distinct mark types, a planar rectangular observation window and coordinates in consistent projected linear units.

## Cross-type nearest-neighbour G

For every type-i event, find its nearest type-j event. The empirical cross-G function is the proportion of type-i events whose nearest type-j distance is no greater than r:

\[
\widehat G_{ij}(r)=\frac{1}{n_i}\sum_{x\in X_i}
\mathbf{1}\{d(x,X_j)\leq r\}.
\]

This is directional: G_ij need not equal G_ji because the source populations and nearest-neighbour distances differ. The simple empirical estimator in the companion package does not apply an advanced edge correction.

## Cross-type K and L

The cross-K function scales the expected number of type-j events within radius r of a typical type-i event by the type-j intensity. Under stationarity and independence of the two component processes:

\[
K_{ij}(r)=\pi r^2,\qquad L_{ij}(r)=\sqrt{K_{ij}(r)/\pi}=r.
\]

For a rectangular window W, the teaching estimator uses translation correction:

\[
\widehat K_{ij}(r)=\frac{|W|}{n_i n_j}
\sum_{x\in X_i}\sum_{y\in X_j}
\frac{\mathbf{1}\{\|x-y\|\leq r\}}
{|W\cap(W-(y-x))|/|W|}.
\]

The translation weight compensates for the fraction of the window that overlaps after shifting by the pair displacement. It assumes stationarity; it is not a universal correction for inhomogeneity, anisotropy or arbitrary observation windows.

## Cross pair correlation

The cross pair-correlation function is related to the derivative of cross-K:

\[
g_{ij}(r)=\frac{K'_{ij}(r)}{2\pi r}.
\]

Under independence of stationary component processes, its theoretical reference is one. The package estimates it by finite differences of supplied K values. Differentiation amplifies noise, so radius spacing and smoothing matter; this finite-difference result is exploratory, not a high-precision estimator.

## Cross-type J

Let F_j(r) be the empty-space distribution for type j, estimated from random locations in the observation window, and let G_ij(r) be the nearest type-j distance distribution from type-i events. Then:

\[
J_{ij}(r)=\frac{1-G_{ij}(r)}{1-F_j(r)}.
\]

For independent component processes, the theoretical cross-J reference is one. The implementation estimates F_j by seeded uniform Monte Carlo probes and returns NaN where the estimated denominator is zero. Its F and J estimates are uncorrected and subject to finite-window and Monte Carlo error.

## Interpretation

- These are descriptive functions across a continuum of distances, not single p-values.
- Under stationary independent component processes, cross-K follows the Poisson benchmark πr², cross-L follows r, cross-pair-correlation follows 1 and cross-J follows 1.
- A cross-G comparison with F_j is more meaningful than comparing G_ij to a homogeneous Poisson formula unless type j itself is homogeneous Poisson.
- Direction matters for G_ij; K_ij and g_ij also use the intensity of the target type in their definition.
- A departure from the independence benchmark does not by itself identify causation or a biological/social interaction mechanism.
- Inhomogeneous intensity, nonstationarity, barriers, anisotropy, missing events and mark-assignment mechanisms can all affect interpretation.

## Implementation scope

The existing point-process package adds:
- cross-nearest-neighbour G_ij;
- rectangular translation-corrected cross-K_ij;
- finite-difference cross pair-correlation from K_ij;
- cross-J_ij using seeded uniform Monte Carlo estimates of F_j.

It does not implement advanced border/isotropic corrections, arbitrary polygon windows, inhomogeneous cross-K, simulation envelopes, mark permutation tests or model fitting. Complexity is O(n_i n_j) for the direct pair-based summaries and O(S n_j) for S empty-space probes.

## References

- Baddeley, A. (2010). Multivariate and Marked Point Processes. In Gelfand, Diggle, Fuentes and Guttorp (eds.), Handbook of Spatial Statistics, Chapter 21, pp. 371–402. CRC Press.
- van Lieshout, M. N. M., & Baddeley, A. J. (1999). Indices of dependence between types in multivariate point patterns. Scandinavian Journal of Statistics, 26, 511–532.
- Baddeley, A., Rubak, E., & Turner, R. (2015). Spatial Point Patterns: Methodology and Applications with R. CRC Press.
- spatstat.explore documentation: Kcross, Gcross, pcfcross and Jcross.

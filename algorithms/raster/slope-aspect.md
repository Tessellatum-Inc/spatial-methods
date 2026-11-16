# Terrain slope and aspect with Horn's 3×3 operator

Stable ID: SA-RASTER-HORN-SLOPE-ASPECT · Draft 0.1 · Source compendium section 4, page 6

## What the derivatives describe

A DEM is a sampled elevation surface. Slope describes steepness; aspect describes the direction of steepest descent. Both are local derivatives, so estimates depend on neighbourhood, cell spacing, elevation units and missing-value policy.

This lesson covers two local estimators: Horn's weighted 3×3 finite-difference operator and the Zevenbergen–Thorne central-difference stencil. They agree on planar surfaces but can differ on curved or noisy terrain.

## The 3×3 neighbourhood

Label elevations:

$$
\begin{matrix}a&b&c\\d&e&f\\g&h&i\end{matrix}
$$

Let Δx and Δy be horizontal cell spacing. The east-positive and north-positive derivatives are:

$$z_x=\frac{(c+2f+i)-(a+2d+g)}{8\Delta x}$$

$$z_y=\frac{(a+2b+c)-(g+2h+i)}{8\Delta y}$$

The sign of zy accounts for raster rows increasing southward. If elevation units differ from horizontal units, multiply both derivatives by a declared vertical conversion factor.

## Slope

$$p=\sqrt{z_x^2+z_y^2}$$

$$\theta=\tan^{-1}(p)\frac{180}{\pi},\qquad S_{\%}=100p$$

A 100% grade is a 45° slope. Degrees and percent rise are different units.


## Zevenbergen–Thorne central differences

The Zevenbergen–Thorne first-derivative stencil uses the west/east and north/south cardinal neighbours:

$z_x=\frac{f-e}{2\Delta x},\qquad z_y=\frac{b-h}{2\Delta y}$

Here (e) and (f) are the west and east neighbours in the centre row, while (b) and (h) are the north and south neighbours in the centre column. The same slope and downslope-aspect equations above then apply. The implementation is exposed as `zevenbergen_thorne_slope_aspect` beside `horn_slope_aspect`.

Both use the same strict 3×3 validity and border policy. On a planar surface their first derivatives agree; on curved terrain the stencils have different smoothing and noise responses. This addition implements first derivatives only, not the full family of profile and plan curvature measures.

## Downslope aspect

Aspect is measured clockwise from north:

$$\alpha=\operatorname{atan2}(-z_x,-z_y)\pmod{360^\circ}$$

A plane rising eastward faces westward downslope (270°). A plane rising northward faces southward (180°). A perfectly flat cell has no unique aspect.

## Grid, units and NoData

The [Python baseline](../../implementations/python/terrain-derivatives/README.md) requires positive cell spacing and a positive vertical conversion factor. It expects a regular grid in a suitable projected coordinate system. A geographic longitude/latitude grid has spatially varying ground distances and should not be treated as metres.

The implementation uses a strict 3×3 validity rule: borders and any window containing NoData return NaN. Other software may interpolate gaps or use another edge rule; comparisons must align these choices.

## Interpretation cautions

Slope and curvature are sensitive to DEM resolution and noise. Aspect and directional curvature become unstable on nearly flat terrain. Horizontal and vertical units must be compatible. Resampling changes the sampled surface and therefore its derivatives. These local derivatives do not calculate visibility, solar radiation or flow direction.

## Exercises

1. Derive slope and aspect for a plane rising one metre per metre eastward.
2. Repeat with a north-rising plane. Explain the aspect sign.
3. Change horizontal spacing while holding elevation differences fixed.
4. Insert one NoData cell. Which output neighbourhoods become invalid?
5. Compare Horn with central-difference or Zevenbergen–Thorne estimators, matching units and edge policy.

## References

- Horn, B. K. P. (1981), *Hill shading and the reflectance map*, Proceedings of the IEEE, 69(1), 14–47.
- Burrough, P. A. and McDonnell, R. A. (1998), *Principles of Geographical Information Systems*, Oxford University Press.

**Scope:** local Horn and Zevenbergen–Thorne slope/aspect plus central-difference profile/plan curvature; multiscale curvature is provided as a separate Gaussian scale-space baseline; no geographic-grid correction, geomorphon classification or DEM conditioning.


## Profile and plan curvature

Curvature describes how the surface bends, rather than only how steep it is. With east-positive (z_x), north-positive (z_y), second derivatives (z_{xx},z_{yy},z_{xy}), and (p^2=z_x^2+z_y^2), this implementation uses:

$$k_{profile}=-\frac{z_{xx}z_x^2+2z_{xy}z_xz_y+z_{yy}z_y^2}{p^2(1+p^2)^{3/2}}$$

$$k_{plan}=-\frac{z_{xx}z_y^2-2z_{xy}z_xz_y+z_{yy}z_x^2}{p^2\sqrt{1+p^2}}$$

The numerators project the Hessian onto the downslope direction and its perpendicular, respectively. These are signed curvatures under the convention shown; software packages may use different signs or scaled variants. The companion `terrain_curvature` function estimates derivatives with central differences and returns inverse-horizontal-unit values. Flat cells are undefined because the directional axes cannot be selected. It uses a strict 3×3 NoData and border rule.

A useful check is a plane, whose two curvatures are zero, and a cylindrical parabola (z=x^2), whose profile curvature is nonzero while plan curvature is zero. These local estimates are resolution- and noise-sensitive; they are not substitutes for multiscale terrain classification.


## Multiscale Gaussian curvature

The companion `multiscale_terrain_curvature` evaluates profile and plan curvature after separable Gaussian smoothing. Each requested scale is a Gaussian standard deviation in horizontal map units; the implementation converts it independently to row and column pixel units, applies reflective padding, and then calls the same central-difference curvature estimator. The result is a mapping from scale to the two curvature rasters.

This separates terrain form at different spatial scales: small scales retain more local variation, while larger scales suppress short-wavelength roughness. The current reference implementation requires a fully finite DEM rather than silently allowing NoData to contaminate the Gaussian convolution. It is computationally direct and intended for teaching and moderate grids, not as a replacement for optimized large-raster filtering. Scale values, cell size, vertical conversion and boundary handling should accompany any derived map.

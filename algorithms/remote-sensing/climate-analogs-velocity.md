# Climate analogs and climate velocity

## Mahalanobis analog ranking

Given historical climate vectors (x_i), future vector (y), and a reference covariance matrix (Sigma), the Mahalanobis distance is

\[
d_M(x_i,y)=\sqrt{(x_i-y)^T\Sigma^{-1}(x_i-y)}.
\]

The implementation estimates (Sigma) from historical samples or accepts a declared covariance, adds a scale-relative diagonal ridge, and ranks historical samples for each future vector. The distance accounts for variable scale and covariance under the selected reference model. It is not a probability of ecological suitability or a measure of dispersal feasibility.

## Climate velocity

Let (T(x,y,t)) be a climate variable, (partial T/\partial t) its temporal trend and (
abla T) its spatial gradient. The local isocline displacement vector is

\[
\mathbf v=-\frac{\partial T/\partial t}{\|\nabla T\|^2}\nabla T,
\qquad
\|\mathbf v\|=\frac{|\partial T/\partial t|}{\|\nabla T\|}.
\]

The minus sign expresses the direction in which one would move to encounter the former climate as the climate changes. Units follow from the supplied derivatives. Where the spatial gradient approaches zero, velocity magnitude diverges and direction is undefined.

## Scope

The package implements the metric and vector equations, not a complete climate-analogue mapping workflow. Derivative estimation, ensemble uncertainty, coastline and terrain constraints, novel-climate thresholds, species range models and climate-refugia optimisation remain open.

## Verification

Tests compare analog ranking against an independent quadratic-form oracle, exercise collinear-variable regularisation, verify an analytic linear climate field, check broadcasting and zero-gradient handling, and reject invalid controls.

See the [implementation package](../../implementations/python/climate-velocity/README.md).

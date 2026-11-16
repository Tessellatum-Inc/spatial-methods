# Circular and directional statistics

## Why circular data need circular methods

Directions wrap around: 1° and 359° are close, not 358° apart. Arithmetic means and ordinary linear differences therefore fail near the wrap boundary. This lesson uses radians counterclockwise from the positive x-axis; bearings clockwise from north must be converted before use.

## Circular mean and resultant length

For angles \(\theta_i\), calculate the mean sine and cosine,

\[
\bar C=\frac1n\sum_i\cos\theta_i,\qquad
\bar S=\frac1n\sum_i\sin\theta_i.
\]

The mean direction is \(\operatorname{atan2}(\bar S,\bar C)\), normalized to \([0,2\pi)\). The mean resultant length is \(\bar R=\sqrt{\bar C^2+\bar S^2}\). It ranges from zero (balanced directions) to one (identical directions). When the resultant is numerically zero, a mean direction is undefined.

## Rayleigh test

The Rayleigh statistic is \(Z=n\bar R^2\). Its null is circular uniformity; its alternative is concentrated, approximately unimodal directions. The implementation uses a commonly used finite-sample tail approximation. It is not a general-purpose detector of every multimodal departure: opposing clusters can cancel and produce a small resultant.

## Kuiper test

Normalize sorted angles to \(u_i\in[0,1)\). Define

\[
D^+=\max_i(i/n-u_i),\qquad
D^-=\max_i(u_i-(i-1)/n),\qquad
V=D^++D^-.
\]

Unlike a one-sided linear empirical-CDF statistic, the sum is invariant to rotation of the circle. The implementation reports a Stephens-corrected asymptotic p-value. Treat it cautiously for very small samples, ties and discrete directional data.

## von Mises density

The von Mises distribution is the circular analogue of a symmetric normal-like distribution:

\[
f(\theta\mid\mu,\kappa)=
\frac{\exp\{\kappa\cos(\theta-\mu)\}}
{2\pi I_0(\kappa)}.
\]

Here \(\mu\) is the mean direction, \(\kappa\geq0\) controls concentration, and \(I_0\) is the modified Bessel function of the first kind. At \(\kappa=0\), the density is uniform.

## Rose histograms

A rose histogram bins normalized directions around the circle. Weighted counts are supported. Bin origin and width should be reported because changing the origin can change the apparent shape.

## Reproducible implementation

The dependency-light Python baseline is in [spatial-distribution-summaries](../../implementations/python/spatial-distribution-summaries/README.md). It includes tests for wraparound, undefined means, rotation invariance, density normalization, histogram boundaries and invalid inputs.

## Interpretation and limitations

- The tests assume angular observations are measured on a common, meaningful reference frame.
- A direction is not a compass bearing until its origin and rotation convention are specified.
- Rayleigh is most useful for a unimodal concentration alternative; use Kuiper or a suitable model-based test for other departures.
- The Kuiper p-value is asymptotic, not an exact finite-sample distribution.
- Neither test corrects for spatial dependence, temporal dependence, sampling bias or measurement uncertainty.
- These planar circular methods are not substitutes for spherical statistics on global locations or 3D orientations.

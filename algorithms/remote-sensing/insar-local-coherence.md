# Local interferometric coherence

**Physical context:** The [radar scattering and SAR signal-formation foundation](../../foundations/remote-sensing-physics/radar-scattering-and-sar-signal-formation.md) explains complex observations, interferometric phase, coherence and decorrelation. The [SAR acquisition and observation design method](../../collection/sar-acquisition-and-observation-design.md) defines why conventional interferometry requires phase-preserving SLC observations with compatible acquisition geometry.

## Definition

For coregistered complex master and slave SLC images, local magnitude coherence over a window W is

\[
\hat\gamma =
\frac{|\sum_{k\in W} z_{1,k}z^*_{2,k}|}
{\sqrt{(\sum_{k\in W}|z_{1,k}|^2)(\sum_{k\in W}|z_{2,k}|^2)}}.
\]

The estimator is bounded in [0, 1] up to floating-point error. It measures local complex similarity (often interpreted as phase consistency), not displacement by itself. The package also provides a signed after-minus-before difference for aligned coherence maps.

## Assumptions and interpretation

- Inputs are complex SLC arrays, accurately coregistered and on the same grid.
- The estimator uses a square odd-sized moving window with no padding; therefore the output is smaller than the input.
- The window defines a spatial averaging support. Larger windows can reduce estimator variance but blur boundaries and reduce spatial detail; the nominal window size is not an independent-look count.
- Windows with insufficient mean power return NaN.
- Low coherence can arise from temporal, geometric or volume decorrelation, thermal noise, low signal-to-noise ratio or processing mismatch. It does not identify a unique cause.
- High coherence does not prove that phase is deformation-only, nor does it validate orbit, atmospheric, topographic, reference or unwrapping corrections.
- The signed coherence difference is a descriptive map comparison; it is not a significance test or a physical change attribution.

## Scope limits

This is only a local coherence estimator. It is not a complete InSAR processor and does not implement orbit refinement, TOPS handling, precise co-registration, flattening, phase filtering, unwrapping, atmospheric correction, geocoding, PS/SBAS time series, offset tracking, tomography or autofocus.

See the [NumPy implementation](../../implementations/python/insar-coherence/README.md) and [verification dossier](../../catalog/verification/insar-local-coherence.md).

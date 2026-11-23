# InSAR local coherence

NumPy reference implementation of local magnitude interferometric coherence from two coregistered complex single-look complex (SLC) images, plus a signed difference between two aligned coherence maps.

The local estimator is |sum(master * conj(slave))| / sqrt(sum(|master|²) sum(|slave|²)) over valid odd-sized square windows. No edge padding is applied; output dimensions are reduced by window_size - 1. A zero- or low-power window returns NaN.

## Assumptions and limitations

Inputs must be finite, coregistered, same-grid complex arrays. This is a local estimator baseline, not a complete InSAR processing chain. It does not perform orbit refinement, TOPS debursting, precise co-registration, interferogram flattening, filtering, phase unwrapping, atmospheric correction, terrain correction, PS/SBAS time-series estimation or uncertainty modelling. The transparent nested-window implementation is intended for small teaching examples; use blockwise/vectorized or specialized SAR software for large scenes.

Run python -m pip install -r requirements.txt and python -m pytest -q.
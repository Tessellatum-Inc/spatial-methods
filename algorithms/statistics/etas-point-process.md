# Epidemic-type aftershock sequence (ETAS) simulation

ETAS models earthquake occurrence as a background process plus triggered descendants. In a branching representation, event magnitudes affect offspring productivity, offspring delays follow an Omori-type temporal kernel, and spatial offsets follow a heavy-tailed kernel.

This bounded simulator uses homogeneous Poisson background events, exponential magnitude excesses above a threshold, a normalized infinite-horizon Omori density with parameters c and p>1, and an isotropic radial power-law spatial kernel with exponent q>1. Magnitude-dependent productivity is calibrated so the expected offspring count under the magnitude distribution equals the supplied branching ratio n<1.

The implementation returns time, planar coordinates, magnitude, parent index, generation and immigrant flag. It uses a toroidal spatial window, finite horizon, seeded NumPy generator and maximum-event guard.

## Limits

No pre-window history is simulated; the beginning of the time window has a startup transient. Toroidal wrapping is not a substitute for geographic boundary correction. The implementation does not estimate parameters, evaluate likelihoods, model spatially varying background intensity, handle catalogue incompleteness or implement the full suite of ETAS variants and diagnostics. It is an educational marked branching simulator, not an operational seismic hazard model.

## Sources

- Ogata, Y. (1988). Statistical models for earthquake occurrences and residual analysis for point processes. *Journal of the American Statistical Association*, 83(401), 9–27. https://doi.org/10.1080/01621459.1988.10478560.
- Hawkes, A. G., & Oakes, D. (1974). A cluster process representation of a self-exciting process. *Journal of Applied Probability*, 11(3), 493–503. https://doi.org/10.2307/3212693.

No source figures, code or datasets are reproduced.

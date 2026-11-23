# Spatial Hawkes process simulation

A linear Hawkes process has conditional intensity equal to a baseline plus the accumulated triggering contribution of prior events. The Hawkes–Oakes branching representation expresses a subcritical process as Poisson immigrants whose descendants form Poisson offspring clusters. The mean number of direct offspring is the branching ratio \(n\), constrained here to \(0\le n<1\).

This spatial teaching baseline uses homogeneous immigrants at rate \(\mu\) per area per time, exponential offspring delays with rate \(\beta\), and isotropic Gaussian spatial displacements with scale \(\sigma\). Each event independently produces \(\operatorname{Poisson}(n)\) children. Child coordinates wrap on a rectangular torus, avoiding spatial edge loss by imposing periodic geography.

The implementation returns event times, coordinates, parent indexes, generation numbers and immigrant flags. It is seeded, finite-horizon and protected by a maximum-event cap.

## Limits

No pre-window temporal history is simulated, so the start of the interval has a startup transient rather than a stationary temporal distribution. Toroidal wrapping is not appropriate for ordinary bounded geographic study areas without a deliberate periodic-domain interpretation. The implementation does not estimate parameters, evaluate likelihoods, model marks or magnitudes, or implement ETAS/Omori triggering. It is a simulator, not a full inference workflow.

## Sources

- Hawkes, A. G. (1971). Spectra of some self-exciting and mutually exciting point processes. *Biometrika*, 58(1), 83–90. https://doi.org/10.1093/biomet/58.1.83.
- Hawkes, A. G., & Oakes, D. (1974). A cluster process representation of a self-exciting process. *Journal of Applied Probability*, 11(3), 493–503. https://doi.org/10.2307/3212693.

No source figures, code or datasets are reproduced.

# Source verification — planar point-process model simulators

## Scope and identity

The Section 2 source entry groups Poisson, Cox, Neyman–Scott, Gibbs and Strauss processes, log-Gaussian Cox processes and marked patterns. It is not one model. The repository now has separate canonical records for the following simulation families:

| Model | Canonical record | Implemented treatment | Important boundary |
|---|---|---|---|
| Homogeneous Poisson | [Homogeneous Poisson and Thomas](../../algorithms/statistics/poisson-and-thomas-processes.md) | Exact Poisson event count and uniform conditional locations in a rectangle | Homogeneous intensity only |\n| Piecewise-constant inhomogeneous Poisson | [Inhomogeneous Poisson process](../../algorithms/statistics/inhomogeneous-poisson-process.md) | Independent cell Poisson counts with uniform within-cell locations | Exact for supplied piecewise-constant intensity grid; no intensity estimation |
| Thomas / Gaussian Neyman–Scott | [Homogeneous Poisson and Thomas](../../algorithms/statistics/poisson-and-thomas-processes.md) | Poisson parents and offspring, isotropic Gaussian displacement | Finite Gaussian-tail buffer truncation |
| Matérn disc-cluster / Neyman–Scott | [Matérn cluster process](../../algorithms/statistics/matern-cluster-process.md) | Poisson parents, Poisson offspring and uniform disc displacement | Compact-support parent buffer; no fitting |
| Log-Gaussian Cox | [Log-Gaussian Cox process](../../algorithms/statistics/log-gaussian-cox-process.md) | Dense Gaussian-field simulation at cell centres, piecewise-constant cell intensity | Small-grid approximation, capped at 225 cells |
| Strauss repulsive Gibbs | [Strauss point process](../../algorithms/statistics/strauss-point-process.md) | Finite-window birth-death Metropolis–Hastings sampler | Finite-run approximate MCMC; no convergence diagnostics or fitting |

The package also implements a piecewise-constant inhomogeneous Poisson simulator. It is exact for the supplied grid intensity, but does not estimate a continuous intensity surface or provide inference. Marked cross-type G/K/J summaries are documented separately in [cross-type point-pattern summaries](../../algorithms/statistics/cross-type-point-pattern-summaries.md). Marked-process simulation, general Gibbs interaction potentials, inhomogeneous Cox families beyond the stated LGCP approximation, and parameter fitting/inference are not covered by these simulators.

## Technical claims and implementation

The Strauss record states the finite-window density proportional to \(\beta^n\gamma^{s_R}\), with \(s_R\) counting unordered pairs within the interaction radius. The birth and death acceptance ratios are documented with the proposal and reverse-move probabilities included. The code uses strict distance comparison \(d<R\); the hard-core tests assert that no returned pair is closer than the radius.

The LGCP record states the mean correction \(-\sigma^2/2\) in the log intensity so that the marginal expected intensity is preserved. Its dense covariance and Cholesky limitations are explicit. The Thomas and Matérn records distinguish unbounded Gaussian displacement from compact-support disc displacement and describe their different finite-window buffers.

The implementation and test suite are in [point-process](../../implementations/python/point-process/README.md). Tests cover seeded reproducibility, window containment, zero-activity/zero-intensity cases, hard-core pair separation, parameter validation and the bounded LGCP grid. These are implementation-contract tests; they do not prove MCMC convergence, estimator validity under arbitrary observation processes, or parameter-recovery performance. The package is included in the Python CI manifest; repository CI is still required to establish that the tests pass on the release commit.

## Bibliography and rights

The canonical records cite the primary or authoritative sources used for model definitions and simulation conventions, including Thomas (1949), Neyman and Scott (1958), Møller, Syversveen and Waagepetersen (1998), Geyer and Møller (1994), and maintained spatstat documentation for the Matérn construction. Bibliographic metadata should be checked against publisher or authoritative records during the full source-entry review; this note does not claim that every grouped source label has been resolved.

Only mathematical definitions and bibliographic metadata are paraphrased here; no source prose, figures, code or datasets are reproduced. Rights to redistribute the supplied compendium and transcription remain a separate unresolved project-level decision.

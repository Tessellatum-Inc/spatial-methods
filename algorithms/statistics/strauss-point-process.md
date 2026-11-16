# Strauss point process

## Purpose

The Strauss process models spatial inhibition: adding an event is penalised when other events already lie within a specified interaction distance. It is a finite-window Gibbs point process, not a Poisson cluster process.

## Density and interaction

For a finite configuration \(x\) in window \(W\), its density relative to a unit-rate Poisson process is proportional to

\[
f(x)\propto \beta^{n(x)}\gamma^{s_R(x)},
\]

where \(n(x)\) is the number of points, \(s_R(x)\) is the number of unordered pairs separated by less than \(R\), \(\beta\ge0\) is the activity parameter and \(0\le\gamma\le1\) controls interaction. The normalising constant is generally intractable.

The Papangelou conditional intensity for inserting \(u\notin x\) is

\[
\lambda(u\mid x)=\beta\gamma^{t_R(u,x)},
\qquad
t_R(u,x)=\sum_{v\in x}\mathbf 1\{\lVert u-v\rVert<R\}.
\]

Thus:
- \(\gamma=1\) removes interaction and gives a homogeneous Poisson process of intensity \(\beta\).
- \(0<\gamma<1\) penalises close pairs; smaller values mean stronger inhibition.
- \(\gamma=0\) gives the hard-core limit: configurations containing a pair closer than \(R\) have zero density.

The model is sometimes called a Strauss interaction process; do not confuse it with the Matérn cluster process, which creates attraction/clustering around latent parents.

## Birth-death Metropolis–Hastings sampler

The package implementation uses a finite-window birth-death Metropolis–Hastings chain:

1. Choose birth or death with probability one half.
2. For a birth, propose a location uniformly in \(W\). If it has \(k\) neighbours within \(R\), accept with probability
   \[
   \min\left(1,\frac{\beta |W|\gamma^k}{n+1}\right).
   \]
3. For a death, choose one of the \(n\) current points uniformly. If it has \(k\) neighbours within \(R\), accept with probability
   \[
   \min\left(1,\frac{n}{\beta |W|\gamma^k}\right).
   \]
4. Run burn-in iterations, then continue the chain and return its final configuration.

The acceptance ratios include the proposal probabilities and reverse move probabilities; the intractable partition function cancels. The function `simulate_strauss_process(window, beta, gamma, interaction_radius, burn_in=5000, n_steps=5000, seed=0)` exposes the iteration counts and seed.

## Interpretation and limitations

This is a basic finite-run MCMC simulator. A returned configuration is an approximate draw whose quality depends on burn-in, chain length, parameter regime and mixing. Reproducibility with a fixed seed is not evidence of convergence. Strong inhibition, large windows or high activity can require substantially longer runs. The implementation does not report acceptance rates, effective sample sizes, convergence diagnostics, parameter estimates or uncertainty. It uses a rectangular planar window, isotropic Euclidean distance and a constant activity parameter; it does not implement inhomogeneous Strauss, multitype interactions or general Gibbs potentials.

For \(\gamma=0\), the sampler enforces the hard-core constraint through zero-probability births that violate it. This is a hard-core Strauss limit, not a general-purpose hard-core model estimator.

## References

- Geyer, C. J. and Møller, J. (1994). “Simulation procedures and likelihood inference for spatial point processes.” *Scandinavian Journal of Statistics*, 21(4), 359–373. [JSTOR stable record](https://www.jstor.org/stable/4616323).
- Baddeley, A., Rubak, E. and Turner, R. *Spatial Point Patterns: Methodology and Applications with R*. See the Gibbs/ Strauss process and Metropolis–Hastings simulation material in the spatstat documentation.
- [Handbook of Spatial Statistics](https://bpb-us-w2.wpmucdn.com/sites.umassd.edu/dist/8/406/files/2024/03/Handbook-of-Spatial-Statistics-fc3c1b00119b3c0a.pdf), discussion of Strauss and Gibbs point processes.

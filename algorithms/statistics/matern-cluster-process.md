# Matérn cluster process

## Question

How can a spatial point pattern represent compact clusters around unobserved centres, with a finite maximum cluster radius?

## Model

The stationary Matérn cluster process is a Neyman–Scott Poisson cluster process:

1. Parent centres form a homogeneous Poisson process with intensity \(\kappa\) per unit area.
2. Each parent independently generates \(M\sim\operatorname{Poisson}(\mu)\) offspring.
3. Conditional on a parent, each offspring is independently uniform in the disc of radius \(R\) centred on that parent.

The stationary offspring intensity is

\[
\lambda=\kappa\mu.
\]

The offspring displacement density is uniform over the disc, \(f(u)=1/(\pi R^2)\) for \(\lVert u\rVert\le R\), and zero otherwise. This compact support distinguishes the Matérn disc kernel from the Gaussian displacement kernel of the Thomas process.

## Simulation on a finite rectangle

For a target rectangle \(W\), simulate parent centres in the rectangle expanded outward by \(R\) on all four sides. This is sufficient: a parent farther away than \(R\) cannot produce an offspring inside \(W\). Draw each offspring radius as \(R\sqrt{U}\) and angle as \(2\pi V\), for independent uniform \(U,V\in[0,1)\). Retain only offspring inside \(W\).

The package implementation is a dependency-free teaching simulator: `simulate_matern_cluster_process(window, parent_intensity, mean_offspring, radius, seed=0)`. It returns offspring coordinates only; latent parents and parent identifiers are not retained.

## Interpretation and limitations

- Increasing \(\kappa\) creates more cluster centres; increasing \(\mu\) increases expected offspring per centre. Their product fixes the stationary first-order intensity, but not the clustering scale or second-order structure.
- Increasing \(R\) spreads offspring farther from each parent and changes the spatial scale of clustering.
- This is a generative model, not a fitted model, parameter estimator, hypothesis test or goodness-of-fit envelope.
- The simulator assumes a homogeneous parent process, constant Poisson offspring mean, Euclidean planar coordinates and a rectangular observation window. It does not implement inhomogeneous parents/offspring or conditional simulation.
- A stationary process on the infinite plane is represented by simulating parents only in the radius-expanded rectangle; this is exact for the compact-support offspring kernel, apart from floating-point boundary comparisons.

## Relationship to related models

- **Homogeneous Poisson:** independent events without parent-offspring clustering.
- **Thomas process:** the same Poisson-parent/Poisson-offspring construction, but with isotropic Gaussian displacements. Gaussian support is unbounded, so finite-window simulation uses a buffer approximation.
- **General Neyman–Scott:** permits other offspring-count and displacement mechanisms.

## References

- Baddeley, A., Rubak, E. and Turner, R. *Spatial Point Patterns: Methodology and Applications with R*. See the Matérn cluster process and `rMatClust` documentation in the spatstat ecosystem: [CRAN documentation](https://search.r-project.org/CRAN/refmans/spatstat.random/html/rMatClust.html).
- Diggle, P. J. *Statistical Analysis of Spatial and Spatio-Temporal Point Patterns* (3rd ed.). CRC Press, 2013.

The cited software documentation is used here to verify the model construction and simulation convention; this page does not claim that the repository implementation reproduces all spatstat options.

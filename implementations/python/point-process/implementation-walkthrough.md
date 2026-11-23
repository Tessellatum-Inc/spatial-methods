# Point-pattern summaries and areal cluster-detection — implementation walkthrough

## 1. Establish the observation window

The point-pattern routines use a rectangular planar observation window. Coordinates and radii must share a consistent linear unit. Duplicate coordinates are rejected. The homogeneous K estimator uses ordered point pairs and a rectangular translation edge correction.

## 2. Separate homogeneous and inhomogeneous K

The homogeneous estimator weights each ordered pair by the reciprocal overlap fraction after translation. The inhomogeneous estimator instead uses supplied positive intensity values at both points and the translated overlap area. It does not fit an intensity surface or select a bandwidth; its interpretation depends on second-order intensity-reweighted stationarity.

## 3. Estimate pair correlation cautiously

The pair-correlation function is approximated by finite differences of K(r), divided by 2πr. Numerical differentiation is sensitive to radius spacing and noise, so inspect the radii and the underlying K curve rather than treating the estimate as a noise-free diagnostic.

## 4. Test quadrat counts conditionally

The quadrat test partitions a rectangle into equal-area cells and conditions on the observed point count. Under homogeneous CSR, simulated counts follow a uniform multinomial distribution. The test uses an upper-tail Pearson statistic and the plus-one Monte Carlo p-value. Grid origin and dimensions are analyst choices; the test is scale-dependent and cannot distinguish interaction from first-order intensity variation.

## 5. Scan areal case counts

The Poisson scan uses one projected centroid, integer case count and positive population value per areal unit. For each centroid it expands candidate circles through distinct distances, including ties. The expected count is the total case count multiplied by the candidate zone's population share. Only elevated-rate candidates under the selected maximum population fraction and minimum case count are eligible.

## 6. Calibrate the maximum scan statistic

Each Monte Carlo replication preserves the total number of cases and draws areal counts from a multinomial distribution proportional to population. It recomputes the maximum over the same candidate circles. The plus-one p-value accounts for the finite simulation count; more replications are needed for finer p-value resolution.

## 7. Validation and scope

Tests cover nearest-neighbour summaries, translation correction, supplied-intensity K, pair-correlation calculation, quadrat boundaries and reproducibility, elevated clusters, population offsets, tied radii and invalid inputs. The scan is not a full SaTScan implementation: covariates, temporal scans, unrestricted arbitrary zones, secondary clusters and polygon-boundary geometry remain outside scope. A finite-grid elliptical teaching scan is now covered in section 10.

## Cross-type marked summaries

The marked-pattern extension partitions events by two distinct labels. Cross-G measures nearest target-type distances from source-type events. Cross-K loops over source-target pairs and applies the rectangular translation overlap weight before scaling by window area and both sample counts. Cross pair correlation differentiates cross-K numerically. Cross-J combines cross-G with Monte Carlo empty-space distances to the target type. These are exploratory estimators; G and J do not use advanced edge correction, and the cross-K stationarity assumptions remain essential.

## Point-process model simulation

The homogeneous Poisson simulator draws an exact Poisson event count with mean intensity times window area, then samples independent uniform locations. The Thomas simulator draws latent Poisson parents in a buffer-expanded rectangle, a Poisson offspring count per parent, and independent Gaussian x/y displacements. It retains only offspring inside the requested window; the finite buffer truncates Gaussian tails. The Thomas stationary intensity is parent intensity multiplied by mean offspring count. Neither simulator estimates parameters or performs a goodness-of-fit test.
\n\n## Matérn disc-cluster model\n\nThe Matérn simulator draws homogeneous Poisson parent centres in the observation rectangle expanded by the cluster radius. Each parent generates a Poisson number of offspring; each offspring radius is sampled as R√U and its angle uniformly on [0, 2π), giving a uniform disc displacement. Only offspring in the requested rectangle are retained. Unlike the Gaussian Thomas kernel, the Matérn disc kernel has compact support, so the radius-sized buffer is sufficient without a tail approximation. The stationary intensity is κμ. The implementation does not retain parent identities or fit model parameters.\n\n## Log-Gaussian Cox process\n\nThe LGCP simulator samples a zero-mean Gaussian field at regular cell centres using an exponential covariance, then exponentiates it with a -σ²/2 correction so the requested mean intensity is preserved. Conditional on that field, each cell receives an independent Poisson count and event locations are uniform within the cell. This is a piecewise-constant grid approximation; dense Cholesky factorisation is O(m³), so the implementation rejects grids above 225 cells. It is not a continuous-field simulator, parameter-fitting routine or inferential test.\n
## Strauss repulsive process

The Strauss sampler targets a finite-window Gibbs density proportional to βⁿγˢ, where s counts close unordered pairs. At each iteration it proposes a uniform-location birth or a uniformly selected death with equal probability. The birth acceptance ratio is β|W|γᵏ/(n+1); the death ratio is n/(β|W|γᵏ), with k the number of neighbours within the interaction radius. The partition function cancels from these Metropolis–Hastings ratios. Burn-in and retained chain length are user-controlled. This is approximate MCMC: fixed-seed reproducibility and a hard-core constraint check do not establish convergence or effective sample size.


## 8. Detect fixed-case-count neighbourhoods

The Besag–Newell routine orders each centre's areas by centroid distance and accumulates complete distance-tie groups until at least k cases are reached. It evaluates the selected neighbourhood's upper-tail hypergeometric probability conditional on the total population and case count. The global routine simulates case allocations proportional to population, repeats all local tests and compares the number of significant centres with the observed count. This is explicitly area-centred; case-centred historical variants and adjustments for multiple choices of k are not silently conflated with it.


## 9. Test global spatial concentration with Tango

Tango's statistic forms the residual vector between observed case proportions and population-proportional expected proportions, then evaluates its quadratic form under an exponential centroid-distance closeness matrix. The distance scale phi controls how quickly influence decays. The Monte Carlo test reallocates the fixed total cases according to population shares and recomputes the statistic for every replicate. Select phi before inspecting the p-value; searching across scales requires a separate multiplicity-aware design.


## 10. Extend the scan window to ellipses

The elliptical scan evaluates a finite grid of major/minor axis ratios and orientations at each areal centroid. Rotated coordinates are ranked by normalized elliptical radius, and tied prefixes define candidate zones. Each candidate is scored with the same elevated Poisson likelihood ratio as the circular scan. The Monte Carlo routine re-runs the full candidate grid for every population-proportional allocation of the fixed total cases. The finite grid is a transparent teaching approximation; it is not a full SaTScan reproduction and has no eccentricity penalty.


## 11. Enumerate connected irregular scan zones

The flexible scan uses a supplied symmetric areal adjacency graph. For each root centroid, it restricts candidates to the root plus its K-1 nearest other centroids, then exhaustively enumerates all connected subsets containing that root up to K areas. The same population-offset Poisson LLR scores each zone. Conditional Monte Carlo inference reallocates the fixed total cases by population and repeats the full enumeration. This implementation caps K at 15 because the candidate count grows combinatorially; it is a bounded teaching baseline, not an optimized production FleXScan engine.


## Spatial Hawkes branching simulation

The Hawkes routine uses the immigration-birth representation: homogeneous Poisson immigrants arrive over the finite time-space window, and each event independently generates a Poisson number of direct offspring. Offspring delays are exponential and spatial offsets are Gaussian wrapped onto a rectangular torus. The branching ratio must be below one. Returned parent indexes and generation numbers expose the cluster genealogy. No pre-window history is simulated, so early-time intensity has a startup transient; toroidal boundaries are a mathematical convenience, not a substitute for geographic edge correction. This is a simulator only, not ETAS, a likelihood or a parameter estimator.

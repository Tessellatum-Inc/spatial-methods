# Point-pattern summaries and circular Poisson scan — implementation walkthrough

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

Tests cover nearest-neighbour summaries, translation correction, supplied-intensity K, pair-correlation calculation, quadrat boundaries and reproducibility, elevated clusters, population offsets, tied radii and invalid inputs. The scan is not a full SaTScan implementation: covariates, temporal scans, elliptical zones, secondary clusters and polygon-boundary geometry remain outside scope.

## Cross-type marked summaries

The marked-pattern extension partitions events by two distinct labels. Cross-G measures nearest target-type distances from source-type events. Cross-K loops over source-target pairs and applies the rectangular translation overlap weight before scaling by window area and both sample counts. Cross pair correlation differentiates cross-K numerically. Cross-J combines cross-G with Monte Carlo empty-space distances to the target type. These are exploratory estimators; G and J do not use advanced edge correction, and the cross-K stationarity assumptions remain essential.

## Point-process model simulation

The homogeneous Poisson simulator draws an exact Poisson event count with mean intensity times window area, then samples independent uniform locations. The Thomas simulator draws latent Poisson parents in a buffer-expanded rectangle, a Poisson offspring count per parent, and independent Gaussian x/y displacements. It retains only offspring inside the requested window; the finite buffer truncates Gaussian tails. The Thomas stationary intensity is parent intensity multiplied by mean offspring count. Neither simulator estimates parameters or performs a goodness-of-fit test.

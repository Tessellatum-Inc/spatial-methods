# Source verification — point-pattern second-order summaries

## Identity and bibliography
Ripley's 1976 paper introduces second-order analysis of stationary point processes; Ripley (1977) develops modelling of spatial patterns. Baddeley, Møller and Waagepetersen (2000) introduce nonparametric interaction summaries for inhomogeneous point patterns. DOI metadata and the estimator/translation-correction structure were cross-checked against the published article and maintained spatstat documentation. The implementation uses the unnormalised p=0 form of the translation-corrected estimator with externally supplied pointwise intensities; it does not fit the intensity surface or apply the optional spatstat normalisation factors.

## Technical scope
The K estimator uses ordered point pairs and rectangular translation edge correction. It assumes stationarity/homogeneity and isotropy. The Poisson reference is K(r)=pi*r^2. The pair-correlation estimate differentiates the estimated K curve numerically, so it is bandwidth/radius-grid sensitive.

## Implementation and reproduction
Tests cover square nearest-neighbor distances and G CDF, Monte Carlo empty-space F and combined J, homogeneous K, a hand-calculated homogeneous translation correction, the Poisson reference curve, direct inhomogeneous pair-weight calculations, ordered-pair counting, intensity validation, quadrat cell assignment, Monte Carlo reproducibility, plus-one p-values and invalid inputs. The package now implements inhomogeneous K for a rectangular window using externally supplied positive intensity values and translation edge correction. It does not fit the intensity model, offer border/isotropic corrections or renormalisation, or implement Palm distributions, polygonal windows or simulation envelopes. Run repository tests/CI independently.

## Quadrat count test

The implementation partitions a rectangular window into equal-area quadrats, counts points with explicit upper/right boundary assignment, computes the Pearson statistic and obtains a conditional multinomial Monte Carlo p-value. The null conditioning on the observed point count follows the standard CSR formulation. The implementation does not use the asymptotic chi-square reference, does not estimate a trend or fitted inhomogeneous null, and is grid-configuration dependent.

## G, F and J functions

G is the empirical distribution of event-to-nearest-other-event distances. F is estimated by sampling uniform locations in the rectangular window and measuring distance to the nearest event. J is computed as (1-G)/(1-F), with NaN when F=1. The implementation uses a reproducible random seed and exposes sample count. This is an uncorrected rectangular-window Monte Carlo baseline; it does not implement advanced edge correction or inferential envelopes.

## Rights
Only metadata and paraphrased mathematical definitions are used; no source text or figures are copied.

# Source verification — point-pattern second-order summaries

## Identity and bibliography
Ripley's 1976 paper introduces second-order analysis of stationary point processes; Ripley (1977) develops modelling of spatial patterns. Baddeley, Møller and Waagepetersen (2000) introduce nonparametric interaction summaries for inhomogeneous point patterns. DOI metadata and the estimator/translation-correction structure were cross-checked against the published article and maintained spatstat documentation. The implementation uses the unnormalised p=0 form of the translation-corrected estimator with externally supplied pointwise intensities; it does not fit the intensity surface or apply the optional spatstat normalisation factors.

## Technical scope
The K estimator uses ordered point pairs and rectangular translation edge correction. It assumes stationarity/homogeneity and isotropy. The Poisson reference is K(r)=pi*r^2. The pair-correlation estimate differentiates the estimated K curve numerically, so it is bandwidth/radius-grid sensitive.

## Implementation and reproduction
Tests cover square nearest-neighbor distances, empirical CDF, homogeneous K, a hand-calculated homogeneous translation correction, the Poisson reference curve, direct inhomogeneous pair-weight calculations, ordered-pair counting, intensity validation and invalid inputs. The package now implements inhomogeneous K for a rectangular window using externally supplied positive intensity values and translation edge correction. It does not fit the intensity model, offer border/isotropic corrections or renormalisation, or implement Palm distributions, polygonal windows or simulation envelopes. Run repository tests/CI independently.

## Rights
Only metadata and paraphrased mathematical definitions are used; no source text or figures are copied.

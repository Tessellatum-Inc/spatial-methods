# Source verification — point-pattern second-order summaries

## Identity and bibliography
Ripley's 1976 paper introduces second-order analysis of stationary point processes; Ripley (1977) develops modelling of spatial patterns. Bibliographic identity and DOI metadata were checked. The K-function and pair-correlation relation are corroborated by point-process references and maintained spatstat documentation.

## Technical scope
The K estimator uses ordered point pairs and rectangular translation edge correction. It assumes stationarity/homogeneity and isotropy. The Poisson reference is K(r)=pi*r^2. The pair-correlation estimate differentiates the estimated K curve numerically, so it is bandwidth/radius-grid sensitive.

## Implementation and reproduction
Tests cover square nearest-neighbor distances, empirical CDF, monotone K estimates, a hand-calculated translation correction, the Poisson reference curve and invalid inputs. The package does not implement inhomogeneous K, intensity estimation, Palm distributions, polygonal windows or simulation envelopes. Run repository tests/CI independently.

## Rights
Only metadata and paraphrased mathematical definitions are used; no source text or figures are copied.

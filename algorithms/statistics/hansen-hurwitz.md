# Hansen–Hurwitz estimator

For independent draws with replacement, let p_i be the per-draw probability of selecting population unit i. For observed draw values y_j and corresponding selection probabilities p_j, the Hansen–Hurwitz total estimator is

\[
\widehat{Y}_{HH}=\frac{1}{n}\sum_{j=1}^{n}\frac{y_j}{p_j}.
\]

An unbiased variance estimator for n>1 is the sample variance of the weighted draw values divided by n:

\[
\widehat{V}(\widehat{Y}_{HH})=
\frac{1}{n(n-1)}\sum_{j=1}^{n}
\left(\frac{y_j}{p_j}-\widehat{Y}_{HH}\right)^2.
\]

The implementation accepts sampled values and their per-draw selection probabilities. Duplicate population units are allowed because the design is with replacement. For one draw, the variance estimate is unavailable. A population mean is returned when the population size is supplied.

## Source
- Hansen, M. H., & Hurwitz, W. N. (1943). On the theory of sampling from finite populations. *The Annals of Mathematical Statistics*, 14(4), 333–362. https://doi.org/10.1214/aoms/1177731356.

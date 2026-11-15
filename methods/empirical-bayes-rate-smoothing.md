# Empirical Bayes smoothing of area rates

For area i, let y_i be an event count and e_i a population or person-time exposure. The sampling model is Poisson with mean e_i times the unknown area rate theta_i. Crude rates x_i = y_i/e_i are less reliable when exposure is small.

## Global moment shrinkage
Marshall (1991) derives a best-linear-Bayes estimator using a common prior mean m and between-area variance A. The weighted moment estimates are

\[
\hat m=\frac{\sum_i y_i}{\sum_i e_i},\qquad
S^2=\frac{\sum_i e_i(x_i-\hat m)^2}{\sum_i e_i},
\]

\[
\hat A=\max\left(0,S^2-\frac{\hat m}{\bar e}\right),
\qquad \bar e=\frac{1}{N}\sum_i e_i.
\]

Then

\[
C_i=\frac{\hat A}{\hat A+\hat m/e_i},\qquad
\hat\theta_i=\hat m+C_i(x_i-\hat m).
\]

If the estimated between-area variance is zero, every estimate is the pooled rate. Shrinkage is stronger for smaller exposure.

## Local moment shrinkage
A local version repeats the same moment calculation within each analyst-defined neighbourhood N_i, including area i. The focal area's crude rate is shrunk toward the local pooled mean. The neighbourhood graph is part of the model: different contiguity or distance rules can change the result.

## Scope
The implementation is a bounded Poisson-rate smoothing baseline. It does not fit CAR/BYM priors, covariate effects, age-standardised expected counts, posterior intervals or a full hierarchical disease-mapping model. Global shrinkage ignores map geometry; local shrinkage depends on the supplied neighbourhoods. Smoothed rates are not cluster significance tests.

## References
- Marshall, R. J. (1991). “Mapping Disease and Mortality Rates Using Empirical Bayes Estimators.” *Journal of the Royal Statistical Society: Series C*, 40(2), 283–294. DOI [10.2307/2347593](https://doi.org/10.2307/2347593).
- Bivand et al., spdep documentation, [Global Empirical Bayes estimator](https://r-spatial.github.io/spdep/reference/EBest.html).

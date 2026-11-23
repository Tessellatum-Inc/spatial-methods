# Verification record — PPML gravity baseline

- **Method identity:** Poisson pseudo-maximum likelihood for a log-link conditional mean.
- **Primary source checked:** Santos Silva and Tenreyro (2006), The Log of Gravity, DOI 10.1162/rest.88.4.641; publisher-hosted article and authors' LSE resource page.
- **Follow-up:** Santos Silva and Tenreyro (2022), The Log of Gravity at 15, DOI 10.1007/S10258-021-00203-w.
- **Core claim:** log-linear OLS can produce inconsistent elasticity estimates under heteroskedasticity; PPML estimates the multiplicative conditional mean and accommodates zero outcomes.
- **Implementation:** Newton/IRLS, line search, known offset and HC0 sandwich covariance; tests cover synthetic coefficient recovery, offsets, zero outcomes, invalid shapes, negative outcomes and rank deficiency.
- **Not reproduced:** published data/tables; no fixed effects, clustering, high-dimensional absorption, separation algorithm or structural-gravity workflow.
- **Status:** primary method identity verified; implementation scope reviewed; empirical reproduction not performed.
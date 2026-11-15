# GNSS integer ambiguity resolution with LAMBDA reduction

## Integer least-squares problem

Given float ambiguities a_hat and their positive-definite covariance Q, integer least squares seeks

\`a_fixed = argmin_{z in Z^n} (a_hat - z)^T Q^{-1} (a_hat - z)\`.

Independent rounding is generally not optimal when ambiguity estimates are correlated.

## LAMBDA decorrelation

The implementation factors Q as \`Q = L^T diag(D) L\`, then applies integer Gauss transformations and permutations to construct an integer-unimodular matrix Z. The transformed problem is \`z_hat = Z^T a_hat\`, \`Q_z = Z^T Q Z\`.

Because Z is integer-unimodular, the transformed integer lattice is in one-to-one correspondence with the original lattice. The quadratic objective is preserved. Reduction seeks a more favourable conditional-variance structure for the subsequent search; it does not change the statistical estimator.

## Search and output

A depth-first conditional search explores integer candidates in the reduced domain, retaining the requested number of best candidates. Candidates are mapped back with \`a = Z^{-T} z\`; objective values are recomputed in the original covariance metric.

The default output includes the best and second-best candidates, their squared Mahalanobis objectives, the reduction matrix, transformed float ambiguities and visited search-node count. The objective ratio is descriptive only. It is not a universal ambiguity acceptance threshold and must not be interpreted as a validated ratio test without a model-specific success-rate or failure-rate analysis.

## Scope and limitations

- This is a stand-alone integer least-squares solver: the user supplies float ambiguities and their covariance. It does not estimate them from carrier-phase observations.
- The implementation includes classical LAMBDA reduction and depth-first conditional search in the MLAMBDA family. It does not implement all MLAMBDA search accelerations, partial ambiguity resolution, integer aperture estimation or bootstrapped success probability.
- The search has a configurable node limit and can be expensive for high-dimensional or poorly conditioned problems.
- It is not a complete RTK, PPP, PPP-AR or network adjustment engine.
- The existing Cholesky sphere-enumeration solver remains available as a transparent low-dimensional baseline without decorrelation.

## References

- Teunissen, P. J. G. (1995). The least-squares ambiguity decorrelation adjustment: a method for fast GPS integer ambiguity estimation. *Journal of Geodesy*, 70, 65–82. DOI: 10.1007/BF00863419.
- Chang, X.-W., Yang, X., & Zhou, T. (2005). MLAMBDA: a modified LAMBDA method for integer least-squares estimation. *Journal of Geodesy*, 79, 552–565. DOI: 10.1007/s00190-005-0004-x.

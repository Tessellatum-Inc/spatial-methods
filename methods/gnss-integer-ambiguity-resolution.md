# GNSS integer ambiguity resolution

Carrier-phase GNSS observations contain unknown integer-cycle ambiguities. After estimating a real-valued *float* ambiguity vector \(\hat a\) and its covariance \(Q_{\hat a}\), integer least squares (ILS) seeks
\[
\check a=\arg\min_{z\in\mathbb Z^n}(\hat a-z)^TQ_{\hat a}^{-1}(\hat a-z).
\]
The covariance matters: correlated ambiguities define a tilted search ellipsoid, so component-wise rounding is not generally the ILS solution.

## Search baseline in this compendium

The [Python implementation](../implementations/python/gnss-ambiguity/README.md) uses Cholesky-based sphere enumeration to find the two best integer candidates for small problems. It is a reference ILS solver, **not LAMBDA**. LAMBDA applies an integer decorrelation transformation before conditional search, improving efficiency for correlated ambiguity vectors. That decorrelation stage is not implemented here.

The returned best/second-best objective ratio is descriptive only. It is not a universal fix-acceptance threshold. Real ambiguity fixing requires a valid float solution, stochastic model, quality control, validation, and integrity monitoring. A wrong fix can corrupt the coordinate solution.

## Sources

- Teunissen, P. J. G. (1993). “Least-squares estimation of the integer GPS ambiguities.” IAG General Meeting, invited lecture.
- Teunissen, P. J. G. (1995). “The least-squares ambiguity decorrelation adjustment: a method for fast GPS integer ambiguity estimation.” *Journal of Geodesy*, 70, 65–82. [DOI](https://doi.org/10.1007/BF00863419).
- Teunissen, P. J. G., de Jonge, P. J., & Tiberius, C. C. J. M. (1997). “Performance of the LAMBDA method for fast GPS ambiguity resolution.” *Navigation*, 44(3), 373–383. [DOI](https://doi.org/10.1002/j.2161-4296.1997.tb02355.x).

No source text or figures are reproduced.

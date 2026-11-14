# Source verification — GNSS integer ambiguity resolution

## Identity and bibliography
Teunissen's 1993 IAG contribution introduces integer least-squares estimation of GPS ambiguities. Teunissen (1995), *Journal of Geodesy* 70, 65–82, DOI 10.1007/BF00863419, describes LAMBDA decorrelation and search. Teunissen, de Jonge & Tiberius (1997), *Navigation* 44(3), 373–383, DOI 10.1002/j.2161-4296.1997.tb02355.x, evaluates LAMBDA performance.

## Technical scope
The implementation solves the integer least-squares objective with Cholesky sphere enumeration. It is not LAMBDA and contains no integer decorrelation transformation. It assumes a correctly specified positive-definite covariance for float ambiguities; it does not derive that covariance from carrier-phase data.

## Implementation and reproduction
Tests compare diagonal and correlated two-dimensional cases against analytical/brute-force references, check distinct best/second candidates and reject invalid covariance inputs. The ratio is not an operational acceptance rule. Run repository tests/CI independently.

## Rights
Only bibliographic metadata and paraphrased mathematical definitions are included; no source text or figures are copied.

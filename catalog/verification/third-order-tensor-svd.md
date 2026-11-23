# Verification record — third-order t-SVD

- **Primary source:** Kilmer & Martin (2011), Factorization strategies for third-order tensors, DOI 10.1016/j.laa.2010.09.020.
- **Supporting theory:** Kilmer et al. (2013), SIAM Journal on Matrix Analysis and Applications 34(1), 148–172, DOI 10.1137/110837711.
- **Method identity:** FFT along mode three, matrix SVD of each frontal frequency slice, inverse FFT under the circular-convolution t-product.
- **Implementation:** reduced matrix SVD per Fourier slice, frequency-domain factors, inverse-FFT reconstruction and common tubal-rank truncation.
- **Tests:** full reconstruction, truncated approximation, rank-one synthetic recovery, invalid rank and input validation.
- **Not reproduced:** published imaging experiments; no missing-data solver, non-Fourier transform or production-scale algorithm.
- **Status:** method and algebra verified against primary publications; teaching implementation reviewed; empirical paper reproduction not performed.
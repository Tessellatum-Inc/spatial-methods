# Least-squares collocation

## Mixed observation model

Least-squares collocation combines fixed-parameter adjustment with prediction of a spatially correlated random signal. A useful teaching model is

\[
y=H\beta+s+e,\qquad \operatorname{Cov}(s)=C,\quad
\operatorname{Cov}(e)=R,\quad \operatorname{Cov}(s,e)=0.
\]

Here \(H\beta\) is the deterministic trend, \(s\) is the spatial signal and \(e\) is measurement noise. The observation covariance is \(\Sigma=C+R\). Generalized least squares estimates the trend:

\[
\hat\beta=(H^T\Sigma^{-1}H)^{-1}H^T\Sigma^{-1}y.
\]

For target-site signal cross-covariance \(C_{0s}\), target signal covariance \(C_{00}\), and target design matrix \(H_0\), the signal prediction and combined prediction are

\[
\hat s_0=C_{0s}\Sigma^{-1}(y-H\hat\beta),\qquad
\hat y_0=H_0\hat\beta+\hat s_0.
\]

The prediction-error covariance is

\[
C_{\hat y_0-y_0}=
C_{00}-C_{0s}\Sigma^{-1}C_{s0}
+B(H^T\Sigma^{-1}H)^{-1}B^T,
\quad B=H_0-C_{0s}\Sigma^{-1}H.
\]

## Implemented baseline

The companion NumPy function accepts the observation vector, trend design, signal covariance, noise covariance, target-to-observation signal cross-covariance, target signal covariance and (when needed) target trend design. It returns the estimated trend, predicted signal, combined prediction, prediction covariance and standard deviations. The matrices are supplied by the caller; no covariance model is fitted automatically.

This is the linear finite-dimensional LSC/universal-kriging form. The code checks dimensions, full trend rank and positive-definiteness of the combined observation covariance. The caller remains responsible for supplying mutually consistent covariance blocks and scientifically defensible covariance parameters.

## Scope and caveats

This is not a physical-geodesy gravity-field package. It does not construct covariance functions from spherical harmonic degree variances, handle heterogeneous observation functionals, estimate covariance hyperparameters, perform robust collocation, support large sparse systems, or account for correlated signal and measurement noise. It is algebraically related to universal kriging under the same covariance and trend assumptions; ordinary kriging is a special case with a constant unknown trend. The dense implementation is for small examples.

## Reproduction

Run from implementations/python/geostatistics:

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## References

- Moritz, H. (1978). Least-squares collocation. *Reviews of Geophysics*, 16(3), 421–430. DOI: 10.1029/RG016i003p00421.
- Moritz, H. (1973). *Least-squares collocation*. Publications on Geodesy, New Series, 75.
- Kok, J. J. (1982). *On Data Snooping and Multiple Outlier Testing*. NOAA Technical Report NOS NGS 30 (background on geodetic network quality control; not an LSC source).

This lesson is an original explanatory implementation and does not reproduce source code, figures or data.

# Potential-field matched bandpass filtering: walkthrough

## 1. Equivalent-layer spectral model

A horizontal source ensemble represented by an equivalent layer at depth z has an idealised radial Fourier-amplitude model:

\[
A(k)=B k^n e^{-kz},
\]

where k is radial angular wavenumber, B is an amplitude coefficient, and n depends on the idealised source type. The teaching implementation permits n = -1, 0 or 1, corresponding to commonly used density half-space, density thin-layer/magnetic half-space, and magnetic dipole-layer forms in the Phillips formulation.

For multiple source ensembles, the model spectrum is the sum:

\[
A_{\mathrm{total}}(k)=\sum_j B_j k^{n_j}e^{-kz_j}.
\]

## 2. Matched-bandpass transfer functions

The amplitude filter assigned to layer j is:

\[
W_j(k)=\frac{B_j k^{n_j}e^{-kz_j}}
{\sum_i B_i k^{n_i}e^{-kz_i}}.
\]

Multiply the 2D Fourier transform of the observed grid by W_j(k), then inverse transform to obtain the component associated with that equivalent layer. Since the weights sum to one at nonzero frequencies, the components sum back to the input field (apart from floating-point error).

## 3. DC and model inputs

The radial model is evaluated at positive radial wavenumbers. The zero-frequency coefficient is special, particularly when n is negative. This implementation explicitly assigns the DC mean to a caller-selected layer (dc_layer, default 0). This convention preserves the total mean but is a bookkeeping choice, not a physical inference about which source depth generated the regional mean.

The matched-bandpass decomposition caller supplies B, z and n for each equivalent layer. A separate bounded radial-spectrum utility now computes annular mean Fourier amplitude and fits a *single* spectral segment by testing n in {-1, 0, 1} and solving log(A)=log(B)+n log(k)-zk by least squares. It returns B, z, n, log-RMSE and log-space R-squared, and supports a caller-selected wavenumber band. It is a diagnostic single-segment fit: it does not estimate the number of layers, jointly fit multiple overlapping segments, design azimuthal filters or perform the nonlinear iterative multi-layer fitting described in the USGS workflow.

## 4. Radial spectrum and bounded single-layer fit

`radial_average_amplitude` bins the positive radial wavenumbers from a regular-grid FFT and returns the mean Fourier amplitude and number of coefficients per annulus. `fit_single_layer_spectrum` fits the log-linear single-layer model for each allowed discrete exponent and selects the smallest log-space residual. Restrict the wavenumber range to a visually defensible approximately straight segment; the selected segment and exponent are assumptions to inspect, not automatic geological classifications. The log-linear fit does not account for correlated Fourier coefficients, anisotropy, spectral leakage or uncertainty in choosing the fitting band.

- [Radial-spectrum implementation](radial_spectrum.py)
- [Radial-spectrum tests](test_radial_spectrum.py)
- [Radial-spectrum lab](../../../notebooks/potential-field-radial-spectrum-lab.ipynb)

## 5. Interpretation and limitations

- Equivalent-layer depths represent average/maximal depth interpretations under the assumed statistical source model, not exact depths of individual geological bodies.
- The method assumes a regular grid and uses a 2D FFT, so periodic boundary effects and edge treatment matter.
- Radial filters discard directional structure; azimuthal matched filters are not implemented.
- Spectral overlap between layers makes separation approximate.
- The supplied model can be wrong; inspect radial spectra and residuals before interpreting component grids.
- The output is a decomposition, not a unique inversion of geology.

## References

- Spector, A. & Grant, F. S. (1970). Statistical models for interpreting aeromagnetic data. Geophysics, 35(2), 293–302. https://doi.org/10.1190/1.1440092
- Phillips, J. D. (2001). Designing matched bandpass and azimuthal filters for the separation of potential-field anomalies by source region and source type. ASEG 15th Geophysical Conference and Exhibition, Expanded Abstracts.
- Nabighian, M. N., et al. (2005). The historical development of the magnetic method in exploration. Geophysics, 70(6), 33ND–61ND. https://doi.org/10.1190/1.2133784

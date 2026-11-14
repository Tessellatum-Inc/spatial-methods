# Third-order tensor singular value decomposition (t-SVD)

## Algebraic setting

t-SVD extends matrix SVD to third-order tensors through the t-product algebra. Under the standard circular-convolution t-product, the discrete Fourier transform along the third mode block-diagonalizes the operation. The tensor is therefore decomposed by taking an ordinary matrix SVD of each frontal slice in the Fourier domain.

\[ \widehat{\mathcal X}^{(k)}=U^{(k)}S^{(k)}V^{(k)*},\qquad k=1,\ldots,n_3. \]

The inverse FFT of the frequency-wise products gives the reconstructed tensor. The number of retained singular directions in each frequency slice defines a tubal-rank truncation.

## Implemented baseline

The NumPy implementation accepts a finite real or complex third-order array, performs FFT along mode three, applies a reduced matrix SVD to each frontal slice, and returns frequency-domain factors. Reconstruction multiplies the factors slice-wise and applies inverse FFT. A truncated helper retains a common rank k across frequency slices.

## Scope and assumptions

This is the classical FFT-based t-SVD for the standard circular-convolution t-product. It is not CP rank, Tucker multilinear rank or tensor-train rank; tubal rank is a different notion. The code is dense and performs one matrix SVD per frequency slice. It does not implement missing-data completion, robust losses, randomized/fast SVD, non-Fourier transforms, weighted boundary conditions or large-scale out-of-core processing. Circular wrap-around is part of the algebra and may not suit every time or spatial boundary condition.

## Reproducibility

Run `python -m pytest -q --import-mode=importlib` in `implementations/python/tensor-decomposition`. The lab uses a synthetic low-tubal-rank tensor.

## Primary references

- Kilmer, M. E., & Martin, C. D. (2011). Factorization strategies for third-order tensors. Linear Algebra and its Applications, 435(3), 641–658. DOI: 10.1016/j.laa.2010.09.020.
- Kilmer, M. E., Braman, K., Hao, N., & Hoover, R. C. (2013). Third-order tensors as operators on matrices: A theoretical and computational framework with applications in imaging. SIAM Journal on Matrix Analysis and Applications, 34(1), 148–172. DOI: 10.1137/110837711.
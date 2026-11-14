# Lucas–Kanade optical flow

For two nearby image frames, brightness constancy gives the first-order optical-flow constraint
\[
I_x u + I_y v + I_t = 0,
\]
where \(u\) and \(v\) are column and row displacement per frame. A single equation cannot determine two unknowns at one pixel. Lucas–Kanade assumes locally constant flow and solves a weighted least-squares system over a neighborhood:
\[
\begin{bmatrix}\sum I_x^2&\sum I_xI_y\\\sum I_xI_y&\sum I_y^2\end{bmatrix}
\begin{bmatrix}u\\v\end{bmatrix}
=-\begin{bmatrix}\sum I_xI_t\\\sum I_yI_t\end{bmatrix}.
\]
The eigenvalues of the local structure tensor indicate whether the neighborhood contains enough two-dimensional texture to constrain both motion components. Small minimum eigenvalues indicate an aperture/low-texture problem.

## Implemented baseline

The [Python package](../implementations/python/optical-flow/README.md) computes dense local least-squares flow with finite-difference gradients averaged across frames, clipped square windows and a minimum-eigenvalue validity mask. It assumes aligned grayscale images, small displacement and brightness constancy. It does not implement iterative feature tracking, pyramids, warping, Farneback, DIS or variational optical flow.

For Earth-observation advection, apparent image motion is not automatically physical transport: parallax, illumination, cloud evolution, changing view geometry and resampling can violate brightness constancy. Validate motion against independent tracking or physical observations.

## Source

- Lucas, B. D., & Kanade, T. (1981). “An Iterative Image Registration Technique with an Application to Stereo Vision.” Proceedings of the 7th International Joint Conference on Artificial Intelligence, 674–679. [IJCAI proceedings record and paper](https://ijcai.org/proceedings/1981/127).

No source text or figures are reproduced.

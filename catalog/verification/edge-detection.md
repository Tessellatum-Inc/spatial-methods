# Sobel and Canny — verification ledger

- Tests cover zero-gradient constant images, positive Sobel response to a horizontal ramp, a synthetic vertical step edge, boolean output and threshold validation.
- Canny uses Gaussian smoothing, bilinear non-maximum suppression and 8-connected hysteresis.
- Tests are authored but have not been run in this environment. No CI pass is claimed.
- Known compatibility differences: reflected convolution boundaries, clamped NMS interpolation and absolute thresholds.

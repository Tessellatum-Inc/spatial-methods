# Sobel and Canny edge detection

Sobel estimates image derivatives by convolving with separable 3×3 derivative/smoothing masks. Gradient magnitude and orientation support edge strength and direction analysis. Canny adds Gaussian smoothing, non-maximum suppression and hysteresis thresholding to produce thin connected edges.

## Implementation

See [Sobel and Canny implementation](../../implementations/python/edge-detection/README.md). The implementation uses bilinear interpolation along the gradient direction for non-maximum suppression and 8-connected hysteresis.

## Limitations

Thresholds are absolute post-smoothing gradient magnitudes. Boundary handling and interpolation differ from established libraries; this is a transparent reference implementation, not a bit-identical replacement. Noise scale and thresholds require calibration to the image's radiometry.

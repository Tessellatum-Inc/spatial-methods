# Sobel and Canny-style edge detection

Sobel returns horizontal/vertical derivatives, gradient magnitude and orientation. The Canny-style pipeline smooths with a separable Gaussian, computes Sobel gradients, suppresses non-maxima by interpolated sampling along the gradient direction, then retains weak responses connected to strong responses using 8-neighbour hysteresis.

Thresholds are absolute gradient-magnitude values after smoothing and suppression; they are not automatically normalized across images. This compact implementation favors transparency over speed. Boundary handling uses reflection for convolution and clamped interpolation for non-maximum suppression. It is not bit-for-bit equivalent to OpenCV or scikit-image Canny.

```python
from edge_detection import sobel, canny
gx, gy, magnitude, orientation = sobel(image)
edges = canny(image, low_threshold=0.08, high_threshold=0.2, sigma=1.2)
```

Run `pytest -q` in this directory.

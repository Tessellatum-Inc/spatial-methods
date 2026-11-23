# RANSAC plane fitting

A NumPy-only robust plane estimator for 3D point clouds. It samples triples,
scores absolute orthogonal distances, selects the largest consensus set (then
the lowest inlier residual sum), and refits with total least squares using SVD.

## Model

    a*x + b*y + c*z + d = 0
    distance = abs(a*x + b*y + c*z + d)

The normal is unit length and its largest-magnitude component is oriented
positive for deterministic presentation. The returned dictionary includes
normal, offset, point-aligned inlier mask, residuals and inlier count.

## Run

Install with python -m pip install -r requirements.txt, then run
python -m pytest -q.

## Limits

This implementation fits one plane. It is not a general primitive detector,
multi-model segmentation method, cylinder/sphere fitter or complete RANSAC
framework. It does not estimate an optimal trial count from a target
confidence, handle correlated sampling, or provide uncertainty intervals.
Thresholds must match coordinate units and expected noise. A dominant plane
may not be the ground surface; validate the model semantics and spatial
distribution of inliers.

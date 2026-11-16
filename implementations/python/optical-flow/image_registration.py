"""Translation and affine image-registration reference methods."""
from __future__ import annotations
import numpy as np


def phase_correlation(reference, moving, *, upsample_factor=1, window=True):
    """Estimate the pixel shift to apply to moving to align it to reference.

    Inputs are equal-shaped finite 2D arrays. The normalized cross-power
    spectrum gives a circular translation estimate. Optional parabolic peak
    interpolation provides subpixel offsets independently by axis.
    Returns (row_shift, column_shift), peak-to-mean response and peak value.
    Large shifts are subject to the periodic ambiguity of FFT correlation.
    """
    a, b = np.asarray(reference, float), np.asarray(moving, float)
    if a.ndim != 2 or a.shape != b.shape or min(a.shape) < 3:
        raise ValueError("reference and moving must be matching 2D arrays of at least 3x3")
    if np.any(~np.isfinite(a)) or np.any(~np.isfinite(b)):
        raise ValueError("images must be finite")
    if isinstance(upsample_factor, bool) or not isinstance(upsample_factor, int) or upsample_factor < 1:
        raise ValueError("upsample_factor must be a positive integer")
    a, b = a - a.mean(), b - b.mean()
    if window:
        wy, wx = np.hanning(a.shape[0]), np.hanning(a.shape[1])
        taper = wy[:, None] * wx[None, :]
        a, b = a * taper, b * taper
    cross = np.fft.fft2(a) * np.conj(np.fft.fft2(b))
    magnitude = np.abs(cross)
    cross /= np.maximum(magnitude, np.finfo(float).eps)
    correlation = np.fft.ifft2(cross).real
    peak = np.unravel_index(np.argmax(correlation), correlation.shape)
    shifts = []
    for axis, index in enumerate(peak):
        n = correlation.shape[axis]
        shift = float(index if index <= n // 2 else index - n)
        if upsample_factor > 1:
            before = list(peak)
            after = list(peak)
            before[axis] = (index - 1) % n
            after[axis] = (index + 1) % n
            fm, f0, fp = correlation[tuple(before)], correlation[peak], correlation[tuple(after)]
            denom = fm - 2.0 * f0 + fp
            if abs(denom) > np.finfo(float).eps:
                shift += float(0.5 * (fm - fp) / denom)
        shifts.append(shift)
    response = float(correlation[peak] / max(np.mean(np.abs(correlation)), np.finfo(float).eps))
    return {"shift_to_apply": tuple(shifts), "response": response, "peak": float(correlation[peak])}


def _fit_affine(source, target):
    design = np.column_stack((source, np.ones(source.shape[0])))
    coefficients, _, rank, _ = np.linalg.lstsq(design, target, rcond=None)
    if rank < 3:
        raise ValueError("affine correspondences are collinear or rank deficient")
    return coefficients[:2, :].T, coefficients[2, :]


def estimate_affine_ransac(source_points, target_points, *, residual_threshold=2.0,
                           max_trials=1000, min_inliers=3, random_state=0):
    """Estimate a 2D affine transform robustly from matched point coordinates.

    Returns matrix, offset, Boolean inlier mask and residuals. Coordinates
    are ordered (x, y), and target = source @ matrix.T + offset. Three
    non-collinear pairs define a candidate. This estimates a transform only;
    it does not detect or match image features.
    """
    src, dst = np.asarray(source_points, float), np.asarray(target_points, float)
    if src.ndim != 2 or src.shape[1:] != (2,) or dst.shape != src.shape or src.shape[0] < 3:
        raise ValueError("source_points and target_points must be matching (n, 2) arrays with n >= 3")
    if np.any(~np.isfinite(src)) or np.any(~np.isfinite(dst)):
        raise ValueError("point coordinates must be finite")
    try:
        threshold = float(residual_threshold)
    except (TypeError, ValueError):
        raise ValueError("residual_threshold must be finite and positive") from None
    if not np.isfinite(threshold) or threshold <= 0:
        raise ValueError("residual_threshold must be finite and positive")
    if isinstance(max_trials, bool) or not isinstance(max_trials, int) or max_trials < 1:
        raise ValueError("max_trials must be a positive integer")
    if isinstance(min_inliers, bool) or not isinstance(min_inliers, int) or min_inliers < 3 or min_inliers > src.shape[0]:
        raise ValueError("min_inliers must be between 3 and the number of matches")
    rng = np.random.default_rng(random_state)
    best = None
    for _ in range(max_trials):
        sample = rng.choice(src.shape[0], size=3, replace=False)
        try:
            matrix, offset = _fit_affine(src[sample], dst[sample])
        except ValueError:
            continue
        residuals = np.linalg.norm(src @ matrix.T + offset - dst, axis=1)
        inliers = residuals <= threshold
        count = int(inliers.sum())
        score = (count, -float(np.sum(residuals[inliers] ** 2)))
        if count >= min_inliers and (best is None or score > best[0]):
            best = (score, inliers)
    if best is None:
        raise ValueError("RANSAC could not find a model with the required inliers")
    inliers = best[1]
    matrix, offset = _fit_affine(src[inliers], dst[inliers])
    residuals = np.linalg.norm(src @ matrix.T + offset - dst, axis=1)
    inliers = residuals <= threshold
    if inliers.sum() < min_inliers:
        raise ValueError("refined affine model has too few inliers")
    matrix, offset = _fit_affine(src[inliers], dst[inliers])
    residuals = np.linalg.norm(src @ matrix.T + offset - dst, axis=1)
    return {"matrix": matrix, "offset": offset, "inliers": inliers,
            "residuals": residuals, "inlier_count": int(inliers.sum())}


def orb_feature_matches(reference, moving, *, max_features=2000,
                        fast_threshold=7, ratio=0.75):
    """Find ORB descriptor correspondences from moving-image to reference.

    Returned source_points are (x,y) coordinates in moving; target_points are
    corresponding (x,y) coordinates in reference. Pass them to
    estimate_affine_ransac to estimate a robust global affine transform.
    Inputs are finite single-channel arrays interpreted on an 8-bit 0..255
    intensity scale. ORB is rotation/scale tolerant within its operating
    range, but not invariant to arbitrary radiometry or cross-modal appearance.
    """
    import cv2

    ref, mov = np.asarray(reference), np.asarray(moving)
    if ref.ndim != 2 or mov.ndim != 2 or min(ref.shape) < 16 or min(mov.shape) < 16:
        raise ValueError("reference and moving must be 2D images at least 16x16")
    if not np.issubdtype(ref.dtype, np.number) or not np.issubdtype(mov.dtype, np.number):
        raise ValueError("images must be numeric")
    if np.any(~np.isfinite(ref)) or np.any(~np.isfinite(mov)):
        raise ValueError("images must contain only finite values")
    if isinstance(max_features, bool) or not isinstance(max_features, int) or max_features < 3:
        raise ValueError("max_features must be an integer of at least 3")
    if isinstance(fast_threshold, bool) or not isinstance(fast_threshold, int) or fast_threshold < 0:
        raise ValueError("fast_threshold must be a non-negative integer")
    try:
        ratio = float(ratio)
    except (TypeError, ValueError):
        raise ValueError("ratio must be in (0, 1)") from None
    if not np.isfinite(ratio) or not 0 < ratio < 1:
        raise ValueError("ratio must be in (0, 1)")

    ref8 = np.clip(ref, 0, 255).astype(np.uint8)
    mov8 = np.clip(mov, 0, 255).astype(np.uint8)
    detector = cv2.ORB_create(nfeatures=max_features, fastThreshold=fast_threshold)
    key_m, desc_m = detector.detectAndCompute(mov8, None)
    key_r, desc_r = detector.detectAndCompute(ref8, None)
    if desc_m is None or desc_r is None:
        raise ValueError("ORB found too few features in one or both images")
    pairs = cv2.BFMatcher(cv2.NORM_HAMMING).knnMatch(desc_m, desc_r, k=2)
    good = [pair[0] for pair in pairs if len(pair) == 2 and
            pair[0].distance < ratio * pair[1].distance]
    if len(good) < 3:
        raise ValueError("fewer than three ORB matches passed the ratio test")
    source = np.asarray([key_m[m.queryIdx].pt for m in good], dtype=float)
    target = np.asarray([key_r[m.trainIdx].pt for m in good], dtype=float)
    distances = np.asarray([m.distance for m in good], dtype=float)
    return {"source_points": source, "target_points": target,
            "descriptor_distances": distances, "match_count": len(good),
            "source_keypoint_count": len(key_m),
            "target_keypoint_count": len(key_r)}

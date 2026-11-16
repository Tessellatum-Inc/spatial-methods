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


def local_feature_matches(reference, moving, *, detector="ORB",
                            max_features=2000, fast_threshold=7, ratio=0.75):
    """Match ORB, SIFT or AKAZE local features from moving to reference.

    Returned source_points are (x,y) coordinates in moving; target_points are
    corresponding (x,y) coordinates in reference. Feed these to
    estimate_affine_ransac for a robust global affine estimate. Inputs are
    finite single-channel images interpreted on an 8-bit 0..255 scale.
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
    method = str(detector).upper()
    if method == "ORB":
        feature_detector = cv2.ORB_create(nfeatures=max_features,
                                          fastThreshold=fast_threshold)
        norm = cv2.NORM_HAMMING
    elif method == "SIFT":
        if not hasattr(cv2, "SIFT_create"):
            raise RuntimeError("this OpenCV build does not provide SIFT")
        feature_detector = cv2.SIFT_create(nfeatures=max_features)
        norm = cv2.NORM_L2
    elif method == "AKAZE":
        feature_detector = cv2.AKAZE_create()
        norm = cv2.NORM_HAMMING
    else:
        raise ValueError("detector must be ORB, SIFT or AKAZE")

    ref8 = np.clip(ref, 0, 255).astype(np.uint8)
    mov8 = np.clip(mov, 0, 255).astype(np.uint8)
    key_m, desc_m = feature_detector.detectAndCompute(mov8, None)
    key_r, desc_r = feature_detector.detectAndCompute(ref8, None)
    if desc_m is None or desc_r is None:
        raise ValueError(f"{method} found too few features in one or both images")
    pairs = cv2.BFMatcher(norm).knnMatch(desc_m, desc_r, k=2)
    good = [pair[0] for pair in pairs if len(pair) == 2 and
            pair[0].distance < ratio * pair[1].distance]
    if len(good) < 3:
        raise ValueError(f"fewer than three {method} matches passed the ratio test")
    source = np.asarray([key_m[m.queryIdx].pt for m in good], dtype=float)
    target = np.asarray([key_r[m.trainIdx].pt for m in good], dtype=float)
    distances = np.asarray([m.distance for m in good], dtype=float)
    return {"source_points": source, "target_points": target,
            "descriptor_distances": distances, "match_count": len(good),
            "source_keypoint_count": len(key_m),
            "target_keypoint_count": len(key_r), "detector": method}


def orb_feature_matches(reference, moving, *, max_features=2000,
                        fast_threshold=7, ratio=0.75):
    """Compatibility wrapper for ORB descriptor matching."""
    return local_feature_matches(reference, moving, detector="ORB",
        max_features=max_features, fast_threshold=fast_threshold, ratio=ratio)


def ecc_register(reference, moving, *, motion_model="affine",
                 max_iterations=500, epsilon=1e-7, gauss_filter_size=5,
                 initial_warp=None):
    """Register moving to reference by maximising enhanced correlation.

    Returns the OpenCV inverse-map warp matrix, aligned moving image in [0,1],
    and ECC correlation coefficient. The matrix is intended for
    warpAffine/warpPerspective with WARP_INVERSE_MAP. ECC is a local optimiser:
    use feature-based or phase-correlation initialisation for larger offsets.
    """
    import cv2

    ref, mov = np.asarray(reference), np.asarray(moving)
    if ref.ndim != 2 or ref.shape != mov.shape or min(ref.shape) < 8:
        raise ValueError("reference and moving must be matching 2D images of at least 8x8")
    if not np.issubdtype(ref.dtype, np.number) or not np.issubdtype(mov.dtype, np.number):
        raise ValueError("images must be numeric")
    if np.any(~np.isfinite(ref)) or np.any(~np.isfinite(mov)):
        raise ValueError("images must contain only finite values")
    models = {"translation": cv2.MOTION_TRANSLATION,
              "euclidean": cv2.MOTION_EUCLIDEAN,
              "affine": cv2.MOTION_AFFINE,
              "homography": cv2.MOTION_HOMOGRAPHY}
    model = str(motion_model).lower()
    if model not in models:
        raise ValueError("motion_model must be translation, euclidean, affine or homography")
    if isinstance(max_iterations, bool) or not isinstance(max_iterations, int) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    try:
        epsilon = float(epsilon)
    except (TypeError, ValueError):
        raise ValueError("epsilon must be positive") from None
    if not np.isfinite(epsilon) or epsilon <= 0:
        raise ValueError("epsilon must be positive")
    if isinstance(gauss_filter_size, bool) or not isinstance(gauss_filter_size, int) or gauss_filter_size < 1 or gauss_filter_size % 2 == 0:
        raise ValueError("gauss_filter_size must be a positive odd integer")
    shape = (3, 3) if model == "homography" else (2, 3)
    if initial_warp is None:
        warp = np.eye(3, dtype=np.float32) if model == "homography" else np.eye(2, 3, dtype=np.float32)
    else:
        warp = np.asarray(initial_warp, dtype=np.float32)
        if warp.shape != shape or np.any(~np.isfinite(warp)):
            raise ValueError(f"initial_warp must be finite with shape {shape}")
        warp = warp.copy()
    ref32 = np.clip(ref, 0, 255).astype(np.float32) / 255.0
    mov32 = np.clip(mov, 0, 255).astype(np.float32) / 255.0
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
                int(max_iterations), epsilon)
    correlation, warp = cv2.findTransformECC(
        ref32, mov32, warp, models[model], criteria, None, gauss_filter_size)
    height, width = ref.shape
    flags = cv2.INTER_LINEAR | cv2.WARP_INVERSE_MAP
    if model == "homography":
        aligned = cv2.warpPerspective(mov32, warp, (width, height), flags=flags)
    else:
        aligned = cv2.warpAffine(mov32, warp, (width, height), flags=flags)
    return {"warp_matrix": warp, "aligned": aligned,
            "correlation": float(correlation), "motion_model": model}


def local_phase_correlation_field(reference, moving, *, window_size=64,
                                   step=32, upsample_factor=10,
                                   min_response=0.0, min_texture_std=1e-6):
    """Estimate a tiled subpixel displacement field by local phase correlation.

    Each square window is correlated independently. Returned shifts are the
    row/column displacements to apply to moving to align it to reference;
    invalid or weak-texture windows are NaN. This is a transparent local
    correlation baseline, not a reproduction of COSI-Corr's full workflow.
    """
    a, b = np.asarray(reference, float), np.asarray(moving, float)
    if a.ndim != 2 or a.shape != b.shape:
        raise ValueError("reference and moving must be matching 2D arrays")
    if min(a.shape) < 8 or np.any(~np.isfinite(a)) or np.any(~np.isfinite(b)):
        raise ValueError("images must be finite and at least 8x8")
    if isinstance(window_size, bool) or not isinstance(window_size, int) or window_size < 8:
        raise ValueError("window_size must be an integer of at least 8")
    if isinstance(step, bool) or not isinstance(step, int) or step < 1:
        raise ValueError("step must be a positive integer")
    if window_size > min(a.shape):
        raise ValueError("window_size must fit inside both images")
    try:
        response_floor, texture_floor = float(min_response), float(min_texture_std)
    except (TypeError, ValueError):
        raise ValueError("response and texture thresholds must be numeric") from None
    if not np.isfinite(response_floor) or response_floor < 0:
        raise ValueError("min_response must be finite and non-negative")
    if not np.isfinite(texture_floor) or texture_floor < 0:
        raise ValueError("min_texture_std must be finite and non-negative")
    rows = np.arange(0, a.shape[0] - window_size + 1, step, dtype=int)
    cols = np.arange(0, a.shape[1] - window_size + 1, step, dtype=int)
    shape = (len(rows), len(cols))
    row_shift = np.full(shape, np.nan)
    col_shift = np.full(shape, np.nan)
    response = np.full(shape, np.nan)
    for i, row in enumerate(rows):
        for j, col in enumerate(cols):
            ref_window = a[row:row + window_size, col:col + window_size]
            mov_window = b[row:row + window_size, col:col + window_size]
            if min(ref_window.std(), mov_window.std()) < texture_floor:
                continue
            result = phase_correlation(ref_window, mov_window,
                                       upsample_factor=upsample_factor)
            response[i, j] = result["response"]
            if result["response"] >= response_floor:
                row_shift[i, j], col_shift[i, j] = result["shift_to_apply"]
    return {"row_centres": rows + (window_size - 1) / 2,
            "column_centres": cols + (window_size - 1) / 2,
            "row_shift": row_shift, "column_shift": col_shift,
            "response": response}


def mutual_information_translation(reference, moving, *, max_shift=12.0,
                                   initial_shift=(0.0, 0.0), bins=32,
                                   min_overlap_fraction=0.6,
                                   max_iterations=200, tolerance=0.01):
    """Estimate a translation by maximising joint-histogram mutual information.

    The returned row/column shift is applied to moving. Linear interpolation
    is used during optimisation. This is a translation-only multimodal
    registration baseline; it does not estimate rotation, scale or deformation.
    """
    from scipy.ndimage import shift as nd_shift
    from scipy.optimize import minimize

    ref, mov = np.asarray(reference, float), np.asarray(moving, float)
    if ref.ndim != 2 or ref.shape != mov.shape or min(ref.shape) < 8:
        raise ValueError("reference and moving must be matching 2D images of at least 8x8")
    if np.any(~np.isfinite(ref)) or np.any(~np.isfinite(mov)):
        raise ValueError("images must contain only finite values")
    if np.ptp(ref) <= 0 or np.ptp(mov) <= 0:
        raise ValueError("images must have non-zero intensity range")
    try:
        bound = float(max_shift)
        overlap_floor = float(min_overlap_fraction)
        tol = float(tolerance)
    except (TypeError, ValueError):
        raise ValueError("max_shift, overlap and tolerance must be numeric") from None
    if not np.isfinite(bound) or bound <= 0:
        raise ValueError("max_shift must be finite and positive")
    if not np.isfinite(overlap_floor) or not 0 < overlap_floor <= 1:
        raise ValueError("min_overlap_fraction must be in (0, 1]")
    if not np.isfinite(tol) or tol <= 0:
        raise ValueError("tolerance must be finite and positive")
    if isinstance(bins, bool) or not isinstance(bins, int) or bins < 8:
        raise ValueError("bins must be an integer of at least 8")
    if isinstance(max_iterations, bool) or not isinstance(max_iterations, int) or max_iterations < 1:
        raise ValueError("max_iterations must be a positive integer")
    start = np.asarray(initial_shift, dtype=float)
    if start.shape != (2,) or np.any(~np.isfinite(start)) or np.any(np.abs(start) > bound):
        raise ValueError("initial_shift must be a finite row/column pair within max_shift")
    histogram_range = [(float(ref.min()), float(ref.max())),
                       (float(mov.min()), float(mov.max()))]

    def objective(shift):
        aligned = nd_shift(mov, shift=shift, order=1, mode="constant",
                           cval=np.nan, prefilter=False)
        valid = np.isfinite(aligned)
        fraction = float(valid.mean())
        if fraction < overlap_floor:
            return 1e3 + (overlap_floor - fraction) * 1e3
        histogram, _, _ = np.histogram2d(
            ref[valid], aligned[valid], bins=bins, range=histogram_range)
        probability = histogram / histogram.sum()
        marginal_ref = probability.sum(axis=1)
        marginal_mov = probability.sum(axis=0)
        occupied = probability > 0
        denominator = marginal_ref[:, None] * marginal_mov[None, :]
        information = np.sum(probability[occupied] *
            np.log(probability[occupied] / denominator[occupied]))
        return -float(information)

    result = minimize(objective, start, method="Powell",
        bounds=[(-bound, bound), (-bound, bound)],
        options={"maxiter": int(max_iterations), "xtol": tol, "ftol": 1e-7})
    aligned = nd_shift(mov, shift=result.x, order=1, mode="constant",
                       cval=np.nan, prefilter=False)
    valid = np.isfinite(aligned)
    information = -objective(result.x)
    return {"shift_to_apply": tuple(float(v) for v in result.x),
            "mutual_information": float(information),
            "overlap_fraction": float(valid.mean()),
            "success": bool(result.success), "iterations": int(result.nit)}

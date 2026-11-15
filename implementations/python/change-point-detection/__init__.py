"""Teaching baselines for univariate change-point detection."""
if __package__:
    from .detectors import cusum, binary_segmentation, pelt
    from .online import bocpd_normal_mean
    __all__ = ["cusum", "binary_segmentation", "pelt", "bocpd_normal_mean"]
else:
    __all__ = []

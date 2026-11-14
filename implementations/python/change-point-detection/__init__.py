"""Teaching baselines for univariate change-point detection."""
from .detectors import cusum, binary_segmentation, pelt
from .online import bocpd_normal_mean
__all__ = ["cusum", "binary_segmentation", "pelt", "bocpd_normal_mean"]

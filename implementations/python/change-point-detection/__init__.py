"""Teaching baselines for univariate change-point detection."""
from .detectors import cusum, binary_segmentation, pelt
__all__ = ["cusum", "binary_segmentation", "pelt"]

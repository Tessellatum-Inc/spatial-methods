"""Spatially balanced active-sampling and UCB allocation baselines."""
from .sampling import select_spatial_batch, ucb1_arm
__all__ = ["select_spatial_batch", "ucb1_arm"]

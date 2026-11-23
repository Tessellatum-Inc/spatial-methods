"""Spatially balanced active-sampling and UCB allocation baselines."""
# Hyphenated source-directory names are loaded as direct modules in this repository.
# Guard package-relative exports for callers that load this directory under an alias.
if __package__:
    from .sampling import select_spatial_batch, ucb1_arm, gp_select_next
    __all__ = ["select_spatial_batch", "ucb1_arm", "gp_select_next"]
else:
    __all__ = []

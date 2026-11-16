# InSAR orbital-ramp removal and SBAS network inversion

Install and test with `python -m pip install -r requirements.txt && python -m pytest -q`.

- `remove_orbital_ramp` fits first-order planar or second-order polynomial spatial ramps to an unwrapped phase image using a valid-pixel mask.
- `sbas_network_inversion` solves per-pixel unwrapped interferogram differences for acquisition displacement relative to a reference date. Optional weights support per-interferogram or per-pixel weighting. Rank-deficient networks remain NaN.

The package does not unwrap phase, estimate coherence, remove atmospheric phase screens, correct DEM error, convert phase to LOS displacement, apply temporal regularization, or reproduce a complete SBAS/NSBAS/MintPy/LiCSBAS workflow. Input interferograms must be consistently unwrapped and referenced; their units carry through to the displacement solution.

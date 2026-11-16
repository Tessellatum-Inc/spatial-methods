# Adaptive thresholding

Install dependencies and run `pytest -q`. Supports local mean and Gaussian-weighted threshold surfaces with an explicit offset; pixels strictly above the local threshold are foreground. Odd window sizes are required. Reflection padding gives deterministic edge behaviour.

This is not Sauvola, Niblack or Phansalkar thresholding, and it does not automatically choose a window size. Select window size relative to the spatial scale of illumination variation and target objects. For remote-sensing imagery, apply per band or to a documented intensity/index layer; do not threshold raw multiband arrays implicitly.

# Lucas–Kanade optical-flow baseline

This dependency-free package implements dense local least-squares optical flow from two aligned grayscale images. It estimates horizontal (column, u) and vertical (row, v) displacement using averaged spatial gradients and a local brightness-constancy equation. A 2x2 normal system is solved per pixel; windows with a weak minimum structure-tensor eigenvalue are marked invalid.

Run with `python -m pytest -q` from this directory.

## Assumptions and limits

The implementation assumes small inter-frame motion, brightness constancy and locally constant motion within each window. It does not perform iterative patch tracking, image pyramids, warping, occlusion handling, robust outlier rejection, Farneback polynomial expansion, DIS optimization or variational regularization. Flat or edge-only regions can be ill-conditioned (the aperture problem) and are flagged invalid rather than assigned fabricated motion. It is a teaching baseline for regular image grids, not a production advection solver.

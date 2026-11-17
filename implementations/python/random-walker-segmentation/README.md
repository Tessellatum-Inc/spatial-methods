# Random-walker image segmentation

A SciPy sparse-Laplacian reference implementation of multi-label random-walker segmentation for 2D scalar or multichannel images. Positive integer seed labels are fixed boundary conditions; zero marks unknown pixels. Four-neighbour conductance is exp(-beta times squared feature difference), and the harmonic probabilities are obtained by solving the sparse Dirichlet system.

## Assumptions and limits

The image is a small finite regular grid. The method returns per-class probabilities and the maximum-probability label. It does not perform GrabCut, seeded region growing, superpixel acceleration, 8-neighbour graph construction, anisotropic physical pixel spacing, multiscale segmentation or uncertainty calibration. Sparse direct solving can be expensive for large rasters; this is an inspectable baseline, not a production gigapixel implementation.

Run python -m pip install -r requirements.txt and python -m pytest -q.
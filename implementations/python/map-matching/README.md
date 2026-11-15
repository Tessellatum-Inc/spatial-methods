# HMM road map matching

Dependency-free HMM/Viterbi map matching for observations and road-edge polylines in a projected metric CRS. Candidate generation projects each observation onto each road and retains its nearest point within a radius. Gaussian emission likelihoods penalise lateral offset; transition likelihoods penalise disagreement between observed displacement and a caller-supplied legal network distance. Viterbi selects a globally plausible sequence rather than snapping each point independently.

The caller must provide actual network shortest-path distances. Euclidean distance is not a substitute for legal road distance around barriers, one-way streets, turn restrictions or disconnected roads. This package does not construct topology, estimate HMM parameters, model heading/speed, or handle longitude/latitude directly. Candidate generation is a linear scan; use a spatial index for large networks.

Run `python -m pytest -q` in this directory. Runtime code uses only Python's standard library.

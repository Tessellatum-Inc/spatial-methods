# Inverse-distance weighting

For a query location q and sample locations x_i with observed values z_i,
inverse-distance weighting predicts

    z_hat(q) = sum(w_i z_i) / sum(w_i)
    w_i = d(q, x_i)^(-p)

The power p controls distance decay. Optional radius and maximum-neighbour
controls limit the support. Exact coordinate matches return the mean of
coincident observations; unsupported queries return None.

The reference implementation uses planar Euclidean coordinates. It does not
model anisotropy, barriers, spatial trends, variograms or prediction
uncertainty, and it is not kriging. Use projected coordinates in suitable
linear units. See the Python package for tests and usage.

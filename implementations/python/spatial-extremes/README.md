# Spatial extremes: empirical pairwise dependence

This package implements a rank-based empirical F-madogram and its pairwise extremal-coefficient transform for a matrix of block maxima.

Rows are temporal or replicate blocks; columns are spatial sites. NaN values are treated as missing. Each site pair is evaluated on pairwise-complete blocks, and average ranks are used for tied values. The function returns symmetric F-madogram, extremal-coefficient and pair-count matrices. Optional coordinates add Euclidean pairwise distances; coordinates are not used to fit a distance-decay model.

For pair i,j, the empirical estimate is nu_F = 0.5 mean(|F_i(X_i)-F_j(X_j)|), with empirical marginal CDF values given by average ranks divided by n+1. Under a max-stable model, theta = (1+2 nu_F)/(1-2 nu_F). Complete dependence corresponds to theta=1; independence corresponds to theta=2.

## Run

    python -m pytest -q

## Interpretation and limits

This is a descriptive pairwise dependence diagnostic, not a fitted spatial extreme-value process. Finite-sample estimates are not clipped to [1,2]; estimates outside that theoretical max-stable interval should prompt scrutiny of sample size, marginal ties, missingness and model suitability. The implementation does not fit marginal GEV/Gumbel distributions, Brown–Resnick or other max-stable processes, spatial copulas, variograms for extremes, confidence intervals, bootstrap uncertainty or spatial prediction. Input values should represent comparable block maxima formed with a defensible common block definition.

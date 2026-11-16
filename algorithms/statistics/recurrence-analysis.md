# Recurrence plots and quantification

A recurrence plot marks pairs of embedded observations whose distance is at most a fixed threshold. Delay-coordinate embedding uses dimension m and delay tau. The implementation supports Chebyshev and Euclidean distances and returns the full symmetric boolean matrix.

Recurrence quantification analysis reports recurrence rate (RR), determinism (DET), mean and maximum diagonal-line lengths (L and Lmax), divergence (1/Lmax), diagonal-line entropy (ENTR), laminarity (LAM), trapping time (TT) and maximum vertical-line length (Vmax). The Theiler window removes temporally adjacent pairs with |i-j| less than or equal to its width. Diagonal lines are counted once in the upper triangle; vertical lines are counted in the full symmetric matrix. ENTR is in nats.

The package also includes a Rosenstein largest-Lyapunov-exponent estimator. It embeds the scalar series, excludes temporally close neighbours with a Theiler window, follows nearest-neighbour trajectories and regresses mean log separation over a caller-selected fit interval. The reported exponent is per unit time after applying the sampling interval. Embedding dimension, delay, Theiler window, fit interval and sampling interval materially affect the estimate; inspect the divergence curve and report sensitivity. A positive estimate is not, by itself, proof of deterministic chaos.

Threshold, embedding dimension, delay, metric, Theiler window and minimum line lengths are analysis choices, not universal constants. Report sensitivity to them. These measures describe repeated states and temporal structure; they do not establish causality or prove deterministic dynamics.

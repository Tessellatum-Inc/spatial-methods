# Time-geography space-time prisms and potential path areas

For a constant-speed bound v and time budget T between fixed origin O and destination D, a location p is reachable when d(O,p) + d(p,D) <= vT. The spatial potential path area is an ellipse with foci O and D, semi-major axis vT/2 and semi-minor axis sqrt((vT/2)^2 - (d(O,D)/2)^2). If vT is shorter than the origin-destination distance, the feasible set is empty.

At time t between departure t0 and arrival t1, the prism cross-section is the intersection of two disks: radius v(t-t0) around O and radius v(t1-t) around D.

This implementation assumes a projected Euclidean plane and constant isotropic speed. Network-constrained prisms, obstacles, mode changes and empirically inferred activity spaces remain outside scope.

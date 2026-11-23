# Verification record: Kernighan–Lin bisection

- **Source:** Section 1, page 2, grouped entry “Community detection; partitioning”.
- **Method:** Greedy locked-pair swaps with D-values and best positive cumulative-gain prefix.
- **Implementation:** Dependency-free balanced two-way weighted/unweighted graph bisection.
- **Tests:** Two dense blocks joined by a weak bridge, path, isolates, deterministic repeat, odd/empty graph rejection, partition validation and invalid weights.
- **Boundary:** The implementation is a straightforward O(n^3)-per-pass teaching baseline; it is not METIS, multilevel partitioning, spectral partitioning or a multiway method. Grouped source entry remains partial.

# PAM k-medoids and CLARA

Dependency-light reference implementations for partitioning from a symmetric
precomputed dissimilarity matrix.

## Run

~~~bash
python -m pip install -r requirements.txt
python -m pytest -q
~~~

## Example

~~~python
import numpy as np
from k_medoids import euclidean_dissimilarity, pam, clara, clarans

points = np.array([(0, 0), (0, 1), (1, 0), (8, 8), (8, 9), (9, 8)])
D = euclidean_dissimilarity(points)
fit = pam(D, k=2)
large_fit = clara(D, k=2, n_samples=10, sample_size=6, random_state=7)
random_fit = clarans(D, k=2, max_neighbors=40, num_local=5, random_state=7)
print(fit["medoids"], fit["labels"], fit["cost"])
~~~

CLARANS samples medoid/non-medoid neighbours at random and accepts strict
improvements until a configured number of unsuccessful neighbour samples
identifies a local minimum. PAM uses a greedy BUILD initialization followed
by best-improving SWAP steps.
Every medoid is an observed object. CLARA fits PAM to several without-
replacement samples, then evaluates each candidate medoid set against the
entire dissimilarity matrix. Ties are resolved deterministically.

The implementation accepts general symmetric dissimilarities; the helper
constructs Euclidean distances from finite feature rows. It does not implement constrained/equal-size clustering, automatic selection
of k, or spatial contiguity. Dense storage is O(n²); PAM swaps are intended for modest
datasets. CLARA reduces fitting work through sampling but still requires the
full distance matrix for this reference implementation.

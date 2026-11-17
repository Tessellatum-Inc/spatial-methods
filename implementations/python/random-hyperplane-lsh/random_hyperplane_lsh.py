"""Random-hyperplane locality-sensitive hashing for cosine similarity."""
from collections import defaultdict
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class Neighbor:
    index: int
    similarity: float


class RandomHyperplaneLSH:
    """Static multi-table sign-random-projection index for cosine similarity."""

    def __init__(self, n_planes=12, n_tables=8, seed=0):
        if isinstance(n_planes, bool) or not isinstance(n_planes, int) or n_planes < 1:
            raise ValueError("n_planes must be a positive integer")
        if isinstance(n_tables, bool) or not isinstance(n_tables, int) or n_tables < 1:
            raise ValueError("n_tables must be a positive integer")
        self.n_planes, self.n_tables, self.seed = n_planes, n_tables, seed
        self._planes = None
        self._vectors = None
        self._tables = []

    @staticmethod
    def _normalise(matrix, name):
        values = np.asarray(matrix, dtype=float)
        if values.ndim != 2 or values.shape[1] < 1:
            raise ValueError(f"{name} must be a 2D array with at least one feature")
        if not np.isfinite(values).all():
            raise ValueError(f"{name} must contain only finite values")
        norms = np.linalg.norm(values, axis=1)
        if np.any(norms == 0):
            raise ValueError(f"{name} must not contain zero-length vectors")
        return values / norms[:, None]

    def fit(self, vectors):
        normalised = self._normalise(vectors, "vectors")
        if normalised.shape[0] == 0:
            raise ValueError("vectors must contain at least one row")
        rng = np.random.default_rng(self.seed)
        self._planes = rng.standard_normal((self.n_tables, self.n_planes, normalised.shape[1]))
        self._vectors = normalised
        self._tables = []
        for planes in self._planes:
            buckets = defaultdict(list)
            for index, bits in enumerate((normalised @ planes.T) >= 0):
                signature = 0
                for bit in bits:
                    signature = (signature << 1) | int(bit)
                buckets[signature].append(index)
            self._tables.append(buckets)
        return self

    @staticmethod
    def _signature(vector, planes):
        signature = 0
        for bit in (planes @ vector) >= 0:
            signature = (signature << 1) | int(bit)
        return signature

    def _query_vector(self, vector):
        if self._vectors is None or self._planes is None:
            raise RuntimeError("fit must be called before query")
        query = self._normalise(np.asarray(vector, dtype=float).reshape(1, -1), "query")[0]
        if query.shape[0] != self._vectors.shape[1]:
            raise ValueError("query feature count does not match fitted vectors")
        return query

    def query_candidates(self, vector):
        """Return sorted unique rows colliding in at least one hash table."""
        query = self._query_vector(vector)
        candidates = set()
        for planes, buckets in zip(self._planes, self._tables):
            candidates.update(buckets.get(self._signature(query, planes), ()))
        return sorted(candidates)

    def query(self, vector, top_k=10):
        """Return LSH candidates reranked by exact cosine similarity."""
        if isinstance(top_k, bool) or not isinstance(top_k, int) or top_k < 1:
            raise ValueError("top_k must be a positive integer")
        query = self._query_vector(vector)
        indices = self.query_candidates(query)
        scores = self._vectors[indices] @ query if indices else np.empty(0)
        ranked = [Neighbor(int(i), float(s)) for i, s in zip(indices, scores)]
        ranked.sort(key=lambda item: (-item.similarity, item.index))
        return ranked[:top_k]

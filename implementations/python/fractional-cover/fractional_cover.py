"""Small CART regression-tree baseline for fractional-cover estimation."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass
class _Node:
    value: float
    feature: int | None = None
    threshold: float | None = None
    left: "_Node | None" = None
    right: "_Node | None" = None

class FractionalCoverTree:
    """Fit squared-error CART to field-labelled fractional cover in [0, 1]."""
    def __init__(self, max_depth=8, min_samples_leaf=5, min_impurity_decrease=0.0):
        if not isinstance(max_depth, int) or isinstance(max_depth, bool) or max_depth < 1:
            raise ValueError("max_depth must be a positive integer")
        if not isinstance(min_samples_leaf, int) or isinstance(min_samples_leaf, bool) or min_samples_leaf < 1:
            raise ValueError("min_samples_leaf must be a positive integer")
        if not np.isfinite(min_impurity_decrease) or min_impurity_decrease < 0:
            raise ValueError("min_impurity_decrease must be finite and nonnegative")
        self.max_depth = max_depth
        self.min_samples_leaf = min_samples_leaf
        self.min_impurity_decrease = float(min_impurity_decrease)
        self.root_ = None
        self.n_features_in_ = None

    def fit(self, X, y):
        X, y = np.asarray(X, dtype=float), np.asarray(y, dtype=float)
        if X.ndim != 2 or y.ndim != 1 or X.shape[0] != y.size or X.shape[0] == 0:
            raise ValueError("X must be nonempty 2-D and y must be a matching 1-D array")
        if X.shape[1] == 0 or not np.all(np.isfinite(X)) or not np.all(np.isfinite(y)):
            raise ValueError("X and y must be finite and X must have at least one feature")
        if np.any((y < 0) | (y > 1)):
            raise ValueError("fractional-cover targets must lie in [0, 1]")
        self.n_features_in_ = X.shape[1]
        self.root_ = self._grow(X, y, 0)
        return self

    def _grow(self, X, y, depth):
        value = float(np.mean(y))
        node = _Node(value)
        if depth >= self.max_depth or len(y) < 2 * self.min_samples_leaf:
            return node
        parent_sse = float(np.sum((y - value) ** 2))
        best_gain, best = self.min_impurity_decrease, None
        for feature in range(X.shape[1]):
            values = np.unique(X[:, feature])
            for threshold in values[:-1] + (values[1:] - values[:-1]) / 2.0:
                mask = X[:, feature] <= threshold
                nl = int(np.count_nonzero(mask))
                if nl < self.min_samples_leaf or len(y) - nl < self.min_samples_leaf:
                    continue
                yl, yr = y[mask], y[~mask]
                gain = parent_sse - float(np.sum((yl-yl.mean())**2)) - float(np.sum((yr-yr.mean())**2))
                if gain > best_gain + 1e-14:
                    best_gain = gain
                    best = (feature, float(threshold), mask)
        if best is None:
            return node
        feature, threshold, mask = best
        node.feature, node.threshold = feature, threshold
        node.left = self._grow(X[mask], y[mask], depth + 1)
        node.right = self._grow(X[~mask], y[~mask], depth + 1)
        return node

    def predict(self, X):
        if self.root_ is None:
            raise RuntimeError("fit must be called before predict")
        X = np.asarray(X, dtype=float)
        if X.ndim != 2 or X.shape[1] != self.n_features_in_ or not np.all(np.isfinite(X)):
            raise ValueError("X must be finite and have the fitted feature count")
        pred = np.empty(X.shape[0], dtype=float)
        for i, row in enumerate(X):
            node = self.root_
            while node.feature is not None:
                node = node.left if row[node.feature] <= node.threshold else node.right
            pred[i] = node.value
        return np.clip(pred, 0.0, 1.0)

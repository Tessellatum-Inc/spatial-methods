"""Constrained intrinsic-CAR (ICAR) Gaussian field simulation.

For an undirected graph with adjacency A and degree matrix D, the intrinsic
precision is tau * (D - A). It is singular: each connected component has a
constant-vector null direction. This module samples on the component-wise
sum-to-zero subspace rather than pretending the precision is invertible.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np


@dataclass(frozen=True)
class ICARSample:
    field: tuple[float, ...]
    component_labels: tuple[int, ...]
    n_components: int
    precision: float
    log_pseudodeterminant: float


def _graph_components(adjacency: np.ndarray) -> tuple[np.ndarray, int]:
    n = adjacency.shape[0]
    labels = np.full(n, -1, dtype=int)
    component = 0
    for start in range(n):
        if labels[start] >= 0:
            continue
        labels[start] = component
        stack = [start]
        while stack:
            node = stack.pop()
            neighbours = np.flatnonzero(adjacency[node] > 0)
            for neighbour in neighbours:
                if labels[neighbour] < 0:
                    labels[neighbour] = component
                    stack.append(int(neighbour))
        component += 1
    return labels, component


def icar_sample(
    adjacency: Sequence[Sequence[float]],
    *,
    precision: float = 1.0,
    rng: np.random.Generator | int | None = None,
) -> ICARSample:
    """Draw a Gaussian ICAR field with one sum-to-zero constraint per component.

    The graph must be represented by a finite, symmetric, non-negative
    adjacency matrix with zero diagonal and no isolated vertices. For each
    connected component, the draw is a zero-mean Gaussian on the subspace
    orthogonal to its constant vector, with precision tau * (D - A).

    This is a dense spectral teaching implementation. It simulates a field;
    it does not fit hyperparameters or implement BYM/BYM2 or Leroux models.
    """
    a = np.asarray(adjacency, dtype=float)
    if a.ndim != 2 or a.shape[0] != a.shape[1] or a.shape[0] < 2:
        raise ValueError("adjacency must be a square matrix with at least two nodes")
    if not np.all(np.isfinite(a)):
        raise ValueError("adjacency must contain only finite values")
    if np.any(a < 0) or np.any(np.diag(a) != 0) or np.allclose(a, 0):
        raise ValueError("adjacency must be non-negative, nonzero and have a zero diagonal")
    if not np.allclose(a, a.T, rtol=1e-10, atol=1e-12):
        raise ValueError("ICAR adjacency must be symmetric")
    degree = a.sum(axis=1)
    if np.any(degree <= 0):
        raise ValueError("ICAR requires every node to have positive degree")
    if not np.isfinite(precision) or precision <= 0:
        raise ValueError("precision must be positive and finite")

    labels, n_components = _graph_components(a)
    generator = np.random.default_rng(rng)
    field = np.zeros(a.shape[0], dtype=float)
    log_pdet = 0.0
    laplacian = np.diag(degree) - a

    for component in range(n_components):
        indices = np.flatnonzero(labels == component)
        block = laplacian[np.ix_(indices, indices)]
        eigenvalues, eigenvectors = np.linalg.eigh(block)
        scale = max(1.0, float(np.max(np.abs(eigenvalues))))
        tolerance = np.finfo(float).eps * len(indices) * scale * 100.0
        positive = eigenvalues > tolerance
        if np.count_nonzero(positive) != len(indices) - 1:
            raise ValueError("graph component Laplacian does not have exactly one null direction")
        values = eigenvalues[positive]
        basis = eigenvectors[:, positive]
        coefficients = generator.normal(size=values.size) / np.sqrt(precision * values)
        field[indices] = basis @ coefficients
        log_pdet += float(np.log(values).sum())

    return ICARSample(
        field=tuple(float(value) for value in field),
        component_labels=tuple(int(value) for value in labels),
        n_components=n_components,
        precision=float(precision),
        log_pseudodeterminant=log_pdet,
    )


@dataclass(frozen=True)
class ICARLogDensity:
    """Log density on the component-wise constrained subspace."""
    log_density: float
    quadratic_energy: float
    constrained_dimension: int
    n_components: int
    log_pseudodeterminant_precision: float
    component_sums: tuple[float, ...]


def icar_log_density(
    adjacency: Sequence[Sequence[float]],
    field: Sequence[float],
    *,
    precision: float = 1.0,
    constraint_tolerance: float = 1e-8,
) -> ICARLogDensity:
    """Evaluate the normalized ICAR Gaussian density on its constrained subspace.

    The density is with respect to Euclidean (Hausdorff) measure on the
    orthogonal subspace satisfying one zero-sum constraint per connected
    component. It is not a density with respect to ordinary N-dimensional
    Lebesgue measure, for which the intrinsic Gaussian is improper.

    For Q0=D-A and constrained dimension d=n-c, this returns
    0.5*log|tau Q0|_+ - d/2*log(2*pi) - tau/2 * u'Q0u.
    """
    a = np.asarray(adjacency, dtype=float)
    u = np.asarray(field, dtype=float)
    if a.ndim != 2 or a.shape[0] != a.shape[1] or a.shape[0] < 2:
        raise ValueError("adjacency must be a square matrix with at least two nodes")
    if u.ndim != 1 or u.size != a.shape[0]:
        raise ValueError("field must have one value per adjacency row")
    if not np.all(np.isfinite(a)) or not np.all(np.isfinite(u)):
        raise ValueError("adjacency and field must contain only finite values")
    if np.any(a < 0) or np.any(np.diag(a) != 0) or np.allclose(a, 0):
        raise ValueError("adjacency must be non-negative, nonzero and have a zero diagonal")
    if not np.allclose(a, a.T, rtol=1e-10, atol=1e-12):
        raise ValueError("ICAR adjacency must be symmetric")
    degree = a.sum(axis=1)
    if np.any(degree <= 0):
        raise ValueError("ICAR requires every node to have positive degree")
    if not np.isfinite(precision) or precision <= 0:
        raise ValueError("precision must be positive and finite")
    if not np.isfinite(constraint_tolerance) or constraint_tolerance <= 0:
        raise ValueError("constraint_tolerance must be positive and finite")

    labels, n_components = _graph_components(a)
    component_sums = tuple(float(np.sum(u[labels == k])) for k in range(n_components))
    for k, total in enumerate(component_sums):
        component_scale = max(1.0, float(np.linalg.norm(u[labels == k], ord=1)))
        if abs(total) > constraint_tolerance * component_scale:
            raise ValueError(f"field violates the sum-to-zero constraint for component {k}")

    laplacian = np.diag(degree) - a
    quadratic = float(u @ laplacian @ u)
    if quadratic < -1e-10 * max(1.0, float(np.linalg.norm(u) ** 2)):
        raise ValueError("Laplacian quadratic energy is materially negative")
    quadratic = max(0.0, quadratic)
    log_pdet_laplacian = 0.0
    for k in range(n_components):
        indices = np.flatnonzero(labels == k)
        block = laplacian[np.ix_(indices, indices)]
        eigenvalues = np.linalg.eigvalsh(block)
        scale = max(1.0, float(np.max(np.abs(eigenvalues))))
        tolerance = np.finfo(float).eps * len(indices) * scale * 100.0
        positive = eigenvalues[eigenvalues > tolerance]
        if positive.size != len(indices) - 1:
            raise ValueError("graph component Laplacian does not have exactly one null direction")
        log_pdet_laplacian += float(np.log(positive).sum())

    dimension = a.shape[0] - n_components
    log_pdet_precision = dimension * float(np.log(precision)) + log_pdet_laplacian
    log_density = (
        0.5 * log_pdet_precision
        - 0.5 * dimension * float(np.log(2.0 * np.pi))
        - 0.5 * float(precision) * quadratic
    )
    return ICARLogDensity(
        log_density=float(log_density),
        quadratic_energy=quadratic,
        constrained_dimension=dimension,
        n_components=n_components,
        log_pseudodeterminant_precision=float(log_pdet_precision),
        component_sums=component_sums,
    )

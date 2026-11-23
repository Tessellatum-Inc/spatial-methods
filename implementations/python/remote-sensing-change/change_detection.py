"""Bitemporal multispectral and categorical change-detection baselines."""
from __future__ import annotations

import numpy as np


def change_vector_analysis(before, after, *, covariance=None, regularization=1e-6):
    """Return spectral change vectors, Euclidean magnitude and Mahalanobis magnitude.

    Inputs are matching (rows, columns, bands) numeric arrays. A pixel is valid
    only when every band in both dates is finite. The vector is after - before.
    If covariance is omitted, it is estimated from valid difference vectors
    using the sample covariance. A positive diagonal ridge stabilizes inversion.
    This is a bitemporal CVA baseline, not an automatic change/no-change
    classifier: callers choose thresholds and account for radiometric alignment.
    """
    a = np.asarray(before, dtype=float)
    b = np.asarray(after, dtype=float)
    if a.ndim != 3 or a.shape != b.shape or min(a.shape) < 1:
        raise ValueError("before and after must be matching (rows, columns, bands) arrays")
    if not np.isfinite(regularization) or regularization <= 0:
        raise ValueError("regularization must be finite and positive")

    valid = np.all(np.isfinite(a) & np.isfinite(b), axis=2)
    if np.count_nonzero(valid) < 2:
        raise ValueError("at least two valid pixels are required for covariance estimation")

    difference = b - a
    vectors = difference[valid]
    if covariance is None:
        cov = np.atleast_2d(np.cov(vectors, rowvar=False, ddof=1))
    else:
        cov = np.asarray(covariance, dtype=float)
        bands = a.shape[2]
        if cov.shape != (bands, bands) or not np.all(np.isfinite(cov)):
            raise ValueError("covariance must be a finite square matrix matching the band count")
        if not np.allclose(cov, cov.T, rtol=1e-10, atol=1e-12):
            raise ValueError("covariance must be symmetric")

    cov = cov + regularization * np.eye(a.shape[2])
    if np.min(np.linalg.eigvalsh(cov)) <= 0:
        raise ValueError("regularized covariance must be positive definite")

    magnitude = np.full(a.shape[:2], np.nan)
    mahalanobis = np.full(a.shape[:2], np.nan)
    magnitude[valid] = np.linalg.norm(vectors, axis=1)
    solved = np.linalg.solve(cov, vectors.T).T
    mahalanobis[valid] = np.sqrt(np.maximum(np.einsum("ij,ij->i", vectors, solved), 0.0))
    return {
        "difference": difference,
        "magnitude": magnitude,
        "mahalanobis_magnitude": mahalanobis,
        "valid_mask": valid,
        "covariance": cov,
    }


def post_classification_change(before, after, *, class_values=None):
    """Build an ordered from-class/to-class transition matrix and change mask.

    Inputs are matching 2D numeric class rasters; non-finite cells are NoData.
    By default class order is the sorted union of observed classes. Supplying
    class_values fixes the matrix order and requires every observed class to be
    included. Matrix rows are the earlier date and columns the later date.
    """
    a = np.asarray(before, dtype=float)
    b = np.asarray(after, dtype=float)
    if a.ndim != 2 or a.shape != b.shape:
        raise ValueError("before and after must be matching 2D class rasters")
    valid = np.isfinite(a) & np.isfinite(b)
    if class_values is None:
        classes = np.unique(np.concatenate((a[valid], b[valid])))
    else:
        classes = np.asarray(class_values, dtype=float)
        if classes.ndim != 1 or classes.size == 0 or not np.all(np.isfinite(classes)):
            raise ValueError("class_values must be a non-empty finite 1D sequence")
        if np.unique(classes).size != classes.size:
            raise ValueError("class_values must not contain duplicates")

    if classes.size == 0:
        raise ValueError("at least one valid class pair or explicit class value is required")
    lookup = {value: index for index, value in enumerate(classes.tolist())}
    transitions = np.zeros((classes.size, classes.size), dtype=np.int64)
    earlier = a[valid].tolist()
    later = b[valid].tolist()
    for old, new in zip(earlier, later):
        if old not in lookup or new not in lookup:
            raise ValueError("observed classes must all occur in class_values")
        transitions[lookup[old], lookup[new]] += 1

    changed = np.zeros(a.shape, dtype=bool)
    changed[valid] = a[valid] != b[valid]
    return {
        "class_values": classes,
        "transition_matrix": transitions,
        "changed_mask": changed,
        "valid_mask": valid,
    }

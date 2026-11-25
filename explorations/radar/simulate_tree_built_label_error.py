"""Synthetic sensitivity experiment for tree/built class-label error.

The target is the equal-stratum, then equal-block contrast in mean absolute
residual error (trees minus built) under latent true labels. The observed-label
estimator uses only noisy predicted labels. This isolates label contamination;
it is not a model of Dynamic World probabilities or the Nairobi R130 data.
"""
from __future__ import annotations
import json
import numpy as np


def apply_label_confusion(true_labels, rng, tree_to_built, built_to_tree,
                          ambiguity=None, ambiguity_multiplier=0.0):
    """Flip labels; optionally increase error odds for ambiguous pixels."""
    labels = np.asarray(true_labels)
    if labels.ndim != 1 or not np.isin(labels, ["T", "B"]).all():
        raise ValueError("true_labels must be a one-dimensional T/B vector")
    if not (0 <= tree_to_built <= 1 and 0 <= built_to_tree <= 1):
        raise ValueError("confusion probabilities must be in [0, 1]")
    if ambiguity is None:
        ambiguity = np.zeros(labels.size, dtype=float)
    ambiguity = np.asarray(ambiguity, dtype=float)
    if (ambiguity.shape != labels.shape or not np.isfinite(ambiguity).all()
            or np.any((ambiguity < 0) | (ambiguity > 1))):
        raise ValueError("ambiguity must match labels and lie in [0, 1]")
    if ambiguity_multiplier < 0:
        raise ValueError("ambiguity_multiplier must be non-negative")
    tree_probability = np.minimum(1.0, tree_to_built * (1 + ambiguity_multiplier * ambiguity))
    built_probability = np.minimum(1.0, built_to_tree * (1 + ambiguity_multiplier * ambiguity))
    observed = labels.copy()
    tree = labels == "T"
    built = ~tree
    observed[tree & (rng.random(labels.size) < tree_probability)] = "B"
    observed[built & (rng.random(labels.size) < built_probability)] = "T"
    return observed


def class_mae_contrast(labels, absolute_errors, min_class_pixels=5):
    """Return trees MAE minus built MAE, or None without both class supports."""
    labels = np.asarray(labels)
    errors = np.asarray(absolute_errors, dtype=float)
    if labels.ndim != 1 or errors.ndim != 1 or labels.size != errors.size:
        raise ValueError("labels and errors must be matching one-dimensional arrays")
    if not np.isin(labels, ["T", "B"]).all() or not np.isfinite(errors).all():
        raise ValueError("labels must be T/B and errors must be finite")
    tree = errors[labels == "T"]
    built = errors[labels == "B"]
    if tree.size < min_class_pixels or built.size < min_class_pixels:
        return None
    return float(tree.mean() - built.mean())


def equal_mean(values):
    values = np.asarray(values, dtype=float)
    if values.ndim != 1 or values.size == 0 or not np.isfinite(values).all():
        raise ValueError("values must be a non-empty finite vector")
    return float(values.mean())


def one_realization(rng, size=20, strata=3, pixels_per_stratum=80,
                    tree_to_built=0.0, built_to_tree=0.0,
                    spatially_varying=False, ambiguity_sensitive=False,
                    ambiguity_label_error=False, ambiguity_residual_effect=False):
    true_block, observed_block = [], []
    for block in range(size * size):
        row, col = divmod(block, size)
        block_true, block_observed = [], []
        for _ in range(strata):
            # Class prevalence varies over space; both classes remain represented.
            tree_share = np.clip(0.35 + 0.25 * row / max(1, size-1)
                                 + rng.normal(0, 0.04), 0.15, 0.75)
            true = np.where(rng.random(pixels_per_stratum) < tree_share, "T", "B")
            # A modest block-level effect plus distinct class means.
            block_effect = 0.05 * np.sin(row / 3) + 0.03 * np.cos(col / 4)
            means = np.where(true == "T", 0.82 + block_effect, 0.52 + block_effect)
            # Always draw the same ambiguity proxy, even in neutral scenarios.
            # This keeps latent labels, residuals and random streams paired across
            # the factorial cells for each Monte Carlo replicate.
            ambiguity = rng.beta(2, 5, pixels_per_stratum)
            errors = rng.exponential(means)
            if ambiguity_sensitive or ambiguity_residual_effect:
                # Isolate ambiguity-linked residual inflation when requested.
                errors = errors * (1.0 + 0.8 * ambiguity)
            t2b = tree_to_built
            b2t = built_to_tree
            if spatially_varying:
                gradient = row / max(1, size-1)
                t2b = min(0.95, tree_to_built * (0.5 + gradient))
                b2t = min(0.95, built_to_tree * (1.5 - gradient))
            observed = apply_label_confusion(
                true, rng, t2b, b2t, ambiguity=ambiguity,
                ambiguity_multiplier=3.0 if (ambiguity_sensitive or ambiguity_label_error) else 0.0)
            truth = class_mae_contrast(true, errors)
            estimate = class_mae_contrast(observed, errors)
            if truth is not None:
                block_true.append(truth)
            if estimate is not None and truth is not None:
                block_observed.append(estimate)
        if len(block_true) == strata and len(block_observed) == strata:
            true_block.append(equal_mean(block_true))
            observed_block.append(equal_mean(block_observed))
    if not true_block or not observed_block:
        raise RuntimeError("No blocks retained common true/observed stratum support")
    return equal_mean(true_block), equal_mean(observed_block), len(true_block)


def run(simulations=200, seed=20261205):
    scenarios = [
        ("perfect_labels", 0.00, 0.00, False, False, False, False),
        ("symmetric_5pct", 0.05, 0.05, False, False, False, False),
        ("asymmetric_15_5pct", 0.15, 0.05, False, False, False, False),
        ("spatially_varying_10pct", 0.10, 0.10, True, False, False, False),
        ("symmetric_20pct", 0.20, 0.20, False, False, False, False),
        ("ambiguity_neutral_10pct", 0.10, 0.10, False, False, False, False),
        ("ambiguous_high_residual_pixels", 0.10, 0.10, False, True, False, False),
        ("ambiguity_label_error_only", 0.10, 0.10, False, False, True, False),
        ("ambiguity_residual_inflation_only", 0.10, 0.10, False, False, False, True),
    ]
    results = []
    paired_shifts = {}
    for name, t2b, b2t, varying, ambiguity_sensitive, ambiguity_label_error, ambiguity_residual_effect in scenarios:
        rng = np.random.default_rng(seed)
        differences, true_values, observed_values, supports = [], [], [], []
        for _ in range(simulations):
            truth, observed, support = one_realization(
                rng, tree_to_built=t2b, built_to_tree=b2t,
                spatially_varying=varying,
                ambiguity_sensitive=ambiguity_sensitive,
                ambiguity_label_error=ambiguity_label_error,
                ambiguity_residual_effect=ambiguity_residual_effect)
            differences.append(observed - truth)
            true_values.append(truth)
            observed_values.append(observed)
            supports.append(support)
        paired_shifts[name] = np.asarray(differences, dtype=float)
        results.append({
            "scenario": name, "tree_to_built": t2b,
            "built_to_tree": b2t, "spatially_varying": varying,
            "ambiguity_sensitive": ambiguity_sensitive,
            "ambiguity_label_error": ambiguity_label_error,
            "ambiguity_residual_effect": ambiguity_residual_effect,
            "simulations": simulations,
            "mean_true_contrast": float(np.mean(true_values)),
            "mean_observed_label_contrast": float(np.mean(observed_values)),
            "mean_label_induced_shift": float(np.mean(differences)),
            "shift_q025_q975": [float(x) for x in np.quantile(differences,[.025,.975])],
            "mean_blocks_with_common_support": float(np.mean(supports)),
        })
    # Paired 2x2 contrast: (label + residual) - label-only - residual-only + neutral.
    interaction = (paired_shifts["ambiguous_high_residual_pixels"]
                   - paired_shifts["ambiguity_label_error_only"]
                   - paired_shifts["ambiguity_residual_inflation_only"]
                   + paired_shifts["ambiguity_neutral_10pct"])
    factorial = {
        "baseline": "ambiguity_neutral_10pct",
        "label_error_only": "ambiguity_label_error_only",
        "residual_inflation_only": "ambiguity_residual_inflation_only",
        "joint": "ambiguous_high_residual_pixels",
        "paired_interaction_mean": float(interaction.mean()),
        "paired_interaction_q025_q975": [float(x) for x in np.quantile(interaction, [.025, .975])],
        "interpretation": "Monte Carlo paired interaction contrast; not a confidence interval or real-world effect."
    }
    return {
        "schema": "tessellatum.tree-built-label-error-sensitivity.v2",
        "factorial_contrast": factorial,
        "target": "Equal-stratum trees-minus-built mean absolute residual error, then equal-block mean, under latent true labels.",
        "observed_estimator": "Same estimand form but computed using noisy T/B labels; blocks are retained only when all strata have both true and observed class support.",
        "design": "20x20 blocks; 3 strata per block; 80 pixels per stratum; class prevalence varies by row; exponential absolute errors with class-specific means. Ambiguity sensitivity includes a paired 2x2 factorial comparison (neutral, label-only, residual-only, joint) using the same latent draws and random streams within each replicate.",
        "limitations": [
            "Synthetic sensitivity analysis only; not Dynamic World validation or a Nairobi R130 result.",
            "No spatial confidence interval or coverage assessment is attempted.",
            "Confusion probabilities are assumed rather than estimated; real label errors may depend on season, class mixture, geometry and image conditions.",
            "Conditioning on common true/observed stratum support changes the retained block population; reported support counts must be read alongside bias.",
            "No probabilistic label calibration, abstention, or correction method is evaluated.",
            "Ambiguity is a synthetic proxy, not an observed boundary or mixed-pixel score."
        ],
        "results": results
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))

"""Reference confusion-matrix and thematic-map accuracy measures."""
from collections import Counter


def confusion_matrix(y_true, y_pred, labels=None):
    """Return (labels, matrix), with rows=reference and columns=prediction."""
    truth, predicted = list(y_true), list(y_pred)
    if not truth or len(truth) != len(predicted):
        raise ValueError("y_true and y_pred must have equal non-zero lengths")
    if labels is None:
        classes = sorted(set(truth) | set(predicted),
                         key=lambda value: (type(value).__name__, str(value)))
    else:
        classes = list(labels)
        if len(set(classes)) != len(classes):
            raise ValueError("labels must be unique")
        if not (set(truth) | set(predicted)).issubset(set(classes)):
            raise ValueError("all observed labels must be included")
    lookup = {value: i for i, value in enumerate(classes)}
    matrix = [[0 for _ in classes] for _ in classes]
    for actual, estimate in zip(truth, predicted):
        matrix[lookup[actual]][lookup[estimate]] += 1
    return classes, matrix


def accuracy_metrics(matrix):
    """Compute OA, class producer/user accuracies, kappa and disagreement.

    Matrix convention is reference rows and predicted columns. A zero class
    denominator yields None. Kappa is None when chance agreement is one.
    """
    rows = [list(row) for row in matrix]
    n_classes = len(rows)
    if n_classes == 0 or any(len(row) != n_classes for row in rows):
        raise ValueError("confusion matrix must be non-empty and square")
    if any(isinstance(v, bool) or not isinstance(v, int) or v < 0
           for row in rows for v in row):
        raise ValueError("confusion counts must be non-negative integers")
    n = sum(map(sum, rows))
    if n == 0:
        raise ValueError("confusion matrix must contain at least one observation")
    row_totals = [sum(row) for row in rows]
    col_totals = [sum(rows[i][j] for i in range(n_classes)) for j in range(n_classes)]
    correct = sum(rows[i][i] for i in range(n_classes))
    oa = correct/n
    producer = [rows[i][i]/row_totals[i] if row_totals[i] else None
                for i in range(n_classes)]
    user = [rows[i][i]/col_totals[i] if col_totals[i] else None
            for i in range(n_classes)]
    pe = sum(row_totals[i]*col_totals[i] for i in range(n_classes))/(n*n)
    kappa = (oa-pe)/(1-pe) if pe < 1 else None
    quantity = sum(abs(row_totals[i]-col_totals[i]) for i in range(n_classes))/(2*n)
    allocation = max(0.0, 1.0-oa-quantity)
    return {
        "n": n,
        "overall_accuracy": oa,
        "producer_accuracy": producer,
        "user_accuracy": user,
        "kappa": kappa,
        "quantity_disagreement": quantity,
        "allocation_disagreement": allocation,
    }


def figure_of_merit(reference_change, predicted_change):
    """Binary change FoM = hits / (hits + misses + false alarms)."""
    reference, predicted = list(reference_change), list(predicted_change)
    if not reference or len(reference) != len(predicted):
        raise ValueError("change arrays must have equal non-zero lengths")
    if any(value not in (0, 1, False, True) for value in reference+predicted):
        raise ValueError("change arrays must contain only binary values")
    hits = sum(bool(a) and bool(p) for a, p in zip(reference, predicted))
    misses = sum(bool(a) and not bool(p) for a, p in zip(reference, predicted))
    false_alarms = sum(not bool(a) and bool(p) for a, p in zip(reference, predicted))
    denominator = hits+misses+false_alarms
    return hits/denominator if denominator else None

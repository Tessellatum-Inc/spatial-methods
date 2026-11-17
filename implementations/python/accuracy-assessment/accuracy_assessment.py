"""Reference confusion-matrix and thematic-map accuracy measures."""
from collections import Counter
from math import isfinite, sqrt


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
    class_f1 = [
        (2 * rows[i][i] / (row_totals[i] + col_totals[i]))
        if row_totals[i] + col_totals[i] else None
        for i in range(n_classes)
    ]
    class_iou = [
        (rows[i][i] / (row_totals[i] + col_totals[i] - rows[i][i]))
        if row_totals[i] + col_totals[i] - rows[i][i] else None
        for i in range(n_classes)
    ]
    class_dice = class_f1.copy()
    valid_f1 = [value for value in class_f1 if value is not None]
    valid_iou = [value for value in class_iou if value is not None]
    return {
        "n": n,
        "overall_accuracy": oa,
        "producer_accuracy": producer,
        "user_accuracy": user,
        "class_f1": class_f1,
        "macro_f1": sum(valid_f1) / len(valid_f1) if valid_f1 else None,
        "class_iou": class_iou,
        "mean_iou": sum(valid_iou) / len(valid_iou) if valid_iou else None,
        "class_dice": class_dice,
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


def _regression_inputs(y_true, y_pred, sample_weight=None):
    truth, prediction = [float(x) for x in y_true], [float(x) for x in y_pred]
    if not truth or len(truth) != len(prediction):
        raise ValueError("y_true and y_pred must have equal non-zero lengths")
    if any(not isfinite(x) for x in truth + prediction):
        raise ValueError("regression values must be finite")
    if sample_weight is None:
        weights = [1.0] * len(truth)
    else:
        weights = [float(x) for x in sample_weight]
        if len(weights) != len(truth) or any(not isfinite(x) or x < 0 for x in weights):
            raise ValueError("sample_weight must be finite, non-negative and match the observations")
        if sum(weights) <= 0:
            raise ValueError("sample weights must have a positive sum")
    return truth, prediction, weights


def mean_absolute_error(y_true, y_pred, sample_weight=None):
    """Weighted or unweighted mean absolute prediction error."""
    truth, prediction, weights = _regression_inputs(y_true, y_pred, sample_weight)
    total = sum(weights)
    return sum(w * abs(a-b) for a, b, w in zip(truth, prediction, weights)) / total


def root_mean_squared_error(y_true, y_pred, sample_weight=None):
    """Weighted or unweighted root mean squared prediction error."""
    truth, prediction, weights = _regression_inputs(y_true, y_pred, sample_weight)
    total = sum(weights)
    return sqrt(sum(w * (a-b)**2 for a, b, w in zip(truth, prediction, weights)) / total)


def r2_score(y_true, y_pred, sample_weight=None):
    """Weighted coefficient of determination with finite constant-target policy.

    If the weighted target variance is zero, return 1.0 for a perfect
    prediction and 0.0 otherwise. This avoids undefined infinities while
    making the constant-target convention explicit.
    """
    truth, prediction, weights = _regression_inputs(y_true, y_pred, sample_weight)
    total = sum(weights)
    mean = sum(w*x for x, w in zip(truth, weights)) / total
    residual = sum(w*(a-b)**2 for a, b, w in zip(truth, prediction, weights))
    total_sum = sum(w*(a-mean)**2 for a, w in zip(truth, weights))
    if total_sum == 0:
        return 1.0 if residual == 0 else 0.0
    return 1.0 - residual / total_sum


def expected_calibration_error(probabilities, y_true, *, n_bins=15, sample_weight=None):
    """Top-label expected calibration error with equal-width confidence bins.

    probabilities is an n-by-k sequence of class probabilities; labels are
    integer class indices. The final bin includes confidence 1.0. ECE is the
    sample-weighted mean absolute gap between bin accuracy and confidence.
    """
    rows = [[float(value) for value in row] for row in probabilities]
    labels = list(y_true)
    if not rows or len(rows) != len(labels):
        raise ValueError("probabilities and labels must have equal non-zero lengths")
    n_classes = len(rows[0])
    if n_classes < 2 or any(len(row) != n_classes for row in rows):
        raise ValueError("probability rows must have the same class count of at least two")
    if any(not isfinite(value) or value < 0 or value > 1 for row in rows for value in row):
        raise ValueError("probabilities must be finite and lie in [0, 1]")
    if any(abs(sum(row)-1.0) > 1e-6 for row in rows):
        raise ValueError("each probability row must sum to one")
    if any(isinstance(label, bool) or not isinstance(label, int) or label < 0 or label >= n_classes
           for label in labels):
        raise ValueError("labels must be integer class indices in range")
    if isinstance(n_bins, bool) or not isinstance(n_bins, int) or n_bins < 1:
        raise ValueError("n_bins must be a positive integer")
    if sample_weight is None:
        weights = [1.0] * len(rows)
    else:
        weights = [float(value) for value in sample_weight]
        if len(weights) != len(rows) or any(not isfinite(w) or w < 0 for w in weights):
            raise ValueError("sample_weight must be finite, non-negative and match observations")
        if sum(weights) <= 0:
            raise ValueError("sample weights must have a positive sum")
    bins = [[] for _ in range(n_bins)]
    for row, label, weight in zip(rows, labels, weights):
        prediction = max(range(n_classes), key=lambda index: row[index])
        confidence = row[prediction]
        index = min(int(confidence * n_bins), n_bins - 1)
        bins[index].append((confidence, float(prediction == label), weight))
    total_weight = sum(weights)
    error = 0.0
    for bucket in bins:
        bucket_weight = sum(item[2] for item in bucket)
        if bucket_weight == 0:
            continue
        mean_confidence = sum(c*w for c, _, w in bucket) / bucket_weight
        mean_accuracy = sum(a*w for _, a, w in bucket) / bucket_weight
        error += bucket_weight / total_weight * abs(mean_accuracy - mean_confidence)
    return error


def recall_at_k(relevant_items, ranked_items, k):
    """Macro query-level recall@k; queries with no relevant items are skipped.

    Returns None when no query has a non-empty relevance set. Duplicate
    retrieved IDs count once, matching set-based retrieval evaluation.
    """
    relevant, ranked = list(relevant_items), list(ranked_items)
    if not relevant or len(relevant) != len(ranked):
        raise ValueError("relevance and ranking collections must have equal non-zero lengths")
    if isinstance(k, bool) or not isinstance(k, int) or k < 1:
        raise ValueError("k must be a positive integer")
    scores = []
    for truth, prediction in zip(relevant, ranked):
        truth_set = set(truth)
        if not truth_set:
            continue
        retrieved = set(list(prediction)[:k])
        scores.append(len(truth_set & retrieved) / len(truth_set))
    return sum(scores) / len(scores) if scores else None


def normalized_mutual_information(labels_true, labels_pred):
    """Arithmetic-normalised mutual information for two cluster labelings.

    NMI = 2 * mutual_information / (H(true) + H(predicted)). Label names are
    arbitrary hashable identifiers. Two constant partitions have NMI=1.
    """
    from math import log
    truth, predicted = list(labels_true), list(labels_pred)
    if not truth or len(truth) != len(predicted):
        raise ValueError("cluster labelings must have equal non-zero lengths")
    true_counts, pred_counts = Counter(truth), Counter(predicted)
    joint_counts = Counter(zip(truth, predicted))
    n = len(truth)
    h_true = -sum((count/n) * log(count/n) for count in true_counts.values())
    h_pred = -sum((count/n) * log(count/n) for count in pred_counts.values())
    if h_true + h_pred == 0:
        return 1.0
    mutual = 0.0
    for (a, b), count in joint_counts.items():
        p_ab = count / n
        mutual += p_ab * log((count*n) / (true_counts[a]*pred_counts[b]))
    return max(0.0, 2.0 * mutual / (h_true + h_pred))


def nash_sutcliffe_efficiency(observed, simulated, sample_weight=None):
    """Nash–Sutcliffe efficiency using the weighted observed mean.

    The constant-observation convention matches r2_score: 1 for a perfect
    prediction and 0 for an imperfect prediction.
    """
    return r2_score(observed, simulated, sample_weight)


def kling_gupta_efficiency(observed, simulated, sample_weight=None):
    """KGE 2009: correlation, standard-deviation ratio and mean ratio.

    Returns None when either series has zero variance or the observed mean is
    zero, because one or more KGE components are undefined.
    """
    truth, prediction, weights = _regression_inputs(observed, simulated, sample_weight)
    total = sum(weights)
    mean_obs = sum(w*x for x, w in zip(truth, weights)) / total
    mean_sim = sum(w*x for x, w in zip(prediction, weights)) / total
    var_obs = sum(w*(x-mean_obs)**2 for x, w in zip(truth, weights)) / total
    var_sim = sum(w*(x-mean_sim)**2 for x, w in zip(prediction, weights)) / total
    if var_obs <= 0 or var_sim <= 0 or mean_obs == 0:
        return None
    covariance = sum(w*(a-mean_obs)*(b-mean_sim)
                     for a, b, w in zip(truth, prediction, weights)) / total
    correlation = covariance / sqrt(var_obs*var_sim)
    variability_ratio = sqrt(var_sim/var_obs)
    bias_ratio = mean_sim/mean_obs
    return 1.0 - sqrt(
        (correlation-1.0)**2
        + (variability_ratio-1.0)**2
        + (bias_ratio-1.0)**2
    )


def ensemble_crps(observed, ensemble_members, sample_weight=None):
    """Mean empirical CRPS for finite ensemble forecasts.

    For each case, CRPS = mean(|member - observation|)
    - 0.5 * mean(|member_i - member_j|) over all ordered member pairs.
    Cases may have different positive ensemble sizes. Optional weights apply
    across cases, not within each ensemble.
    """
    truth = [float(value) for value in observed]
    ensembles = [[float(value) for value in row] for row in ensemble_members]
    if not truth or len(truth) != len(ensembles):
        raise ValueError("observed and ensemble_members must have equal non-zero lengths")
    if any(not row for row in ensembles):
        raise ValueError("each ensemble must contain at least one member")
    if any(not isfinite(value) for row in ensembles for value in row):
        raise ValueError("ensemble members must be finite")
    means = [sum(row)/len(row) for row in ensembles]
    truth, _, weights = _regression_inputs(truth, means, sample_weight)
    scores = []
    for observation, row in zip(truth, ensembles):
        m = len(row)
        first = sum(abs(member-observation) for member in row) / m
        pairwise = sum(abs(a-b) for a in row for b in row) / (2.0*m*m)
        scores.append(first-pairwise)
    return sum(w*score for w, score in zip(weights, scores)) / sum(weights)

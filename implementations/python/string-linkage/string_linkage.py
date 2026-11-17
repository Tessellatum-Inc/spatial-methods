"""Small dependency-free string comparison and record-linkage baselines."""
from collections import Counter
from math import log, sqrt
import re
import unicodedata


def normalize_text(value):
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    value = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(re.findall(r"\w+", value, flags=re.UNICODE))


def levenshtein(a, b):
    if not isinstance(a, str) or not isinstance(b, str):
        raise TypeError("inputs must be strings")
    if len(a) < len(b):
        a, b = b, a
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(cur[-1] + 1, prev[j] + 1, prev[j-1] + (ca != cb)))
        prev = cur
    return prev[-1]


def normalized_levenshtein(a, b):
    scale = max(len(a), len(b))
    return 1.0 if scale == 0 else 1.0 - levenshtein(a, b) / scale


def jaro_winkler(a, b, prefix_scale=0.1):
    if not 0 <= prefix_scale <= 0.25:
        raise ValueError("prefix_scale must be between 0 and 0.25")
    if a == b:
        return 1.0
    if not a or not b:
        return 0.0
    radius = max(0, max(len(a), len(b)) // 2 - 1)
    ma, mb = [False]*len(a), [False]*len(b)
    matches = 0
    for i, ch in enumerate(a):
        for j in range(max(0, i-radius), min(i+radius+1, len(b))):
            if not mb[j] and ch == b[j]:
                ma[i] = mb[j] = True
                matches += 1
                break
    if not matches:
        return 0.0
    xa = [a[i] for i in range(len(a)) if ma[i]]
    xb = [b[j] for j in range(len(b)) if mb[j]]
    trans = sum(x != y for x, y in zip(xa, xb)) / 2
    m = matches
    jaro = (m/len(a) + m/len(b) + (m-trans)/m) / 3
    prefix = 0
    for x, y in zip(a[:4], b[:4]):
        if x != y:
            break
        prefix += 1
    return jaro + prefix * prefix_scale * (1-jaro)


def character_ngram_cosine(a, b, n=3):
    if n < 1:
        raise ValueError("n must be positive")
    def grams(s):
        s = f" {s} "
        return Counter(s[i:i+n] for i in range(max(0, len(s)-n+1)))
    x, y = grams(a), grams(b)
    nx, ny = sqrt(sum(v*v for v in x.values())), sqrt(sum(v*v for v in y.values()))
    if not nx or not ny:
        return 1.0 if not nx and not ny else 0.0
    return sum(v*y.get(k, 0) for k, v in x.items()) / (nx*ny)


def soundex(value):
    letters = re.sub(r"[^A-Za-z]", "", value).upper()
    if not letters:
        return ""
    codes = dict.fromkeys("BFPV", "1") | dict.fromkeys("CGJKQSXZ", "2") | {"D":"3","T":"3","L":"4","M":"5","N":"5","R":"6"}
    first, result = letters[0], []
    previous = codes.get(letters[0], "")
    for ch in letters[1:]:
        code = codes.get(ch, "")
        if code and code != previous:
            result.append(code)
        previous = code
    return (first + "".join(result) + "000")[:4]


def exact_prefix_blocks(records, field, prefix_length=3):
    if prefix_length < 1:
        raise ValueError("prefix_length must be positive")
    blocks = {}
    for i, row in enumerate(records):
        key = normalize_text(str(row.get(field, "")))[:prefix_length]
        if key:
            blocks.setdefault(key, []).append(i)
    return blocks


def canopy_pairs(records, field, loose_threshold, tight_threshold):
    """O(n²) overlapping canopy candidate pairs; for small teaching datasets."""
    if not 0 <= tight_threshold <= loose_threshold <= 1:
        raise ValueError("require 0 <= tight_threshold <= loose_threshold <= 1")
    values = [normalize_text(str(r.get(field, ""))) for r in records]
    remaining, pairs = set(range(len(values))), set()
    while remaining:
        seed = min(remaining)
        remaining.remove(seed)
        for j, value in enumerate(values):
            if j == seed or not values[seed] or not value:
                continue
            score = jaro_winkler(values[seed], value)
            if score >= loose_threshold:
                pairs.add((min(seed, j), max(seed, j)))
                if score >= tight_threshold:
                    remaining.discard(j)
    return pairs


def fellegi_sunter_score(comparisons, probabilities):
    """Sum log(m/u) for agreements and log((1-m)/(1-u)) for disagreements."""
    unknown = set(comparisons) - set(probabilities)
    if unknown:
        raise KeyError(f"missing m/u probabilities: {sorted(unknown)}")
    score = 0.0
    for field, agrees in comparisons.items():
        m, u = probabilities[field]
        if not (0 < m < 1 and 0 < u < 1):
            raise ValueError(f"m and u for {field!r} must be strictly between 0 and 1")
        score += log(m/u) if agrees else log((1-m)/(1-u))
    return score

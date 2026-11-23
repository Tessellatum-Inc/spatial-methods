# Verification — string similarity and record linkage

- Source: Section 9, page 19, string-similarity/record-linkage row.
- Implementation: `implementations/python/string-linkage/string_linkage.py`.
- Tests: Unicode normalization, Levenshtein, normalized edge cases, published
  Jaro-Winkler examples, n-gram cosine, Soundex examples, prefix blocking,
  canopy candidates and Fellegi-Sunter log-weight arithmetic.
- Runtime: Python standard library; pytest for tests.
- Scope: reference baseline. m/u probabilities and thresholds are supplied,
  not estimated. Blocking recall and match quality require labelled evaluation.
- Open: Metaphone, full comparison levels, scalable indexing, automatic
  parameter estimation, geometry matching and production POI deduplication.
- Status: partial contribution to a grouped source entry, not full verification.

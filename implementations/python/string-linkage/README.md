# String similarity and record linkage

Dependency-free reference implementations of Levenshtein distance, normalized
edit similarity, Jaro-Winkler, character n-gram cosine, American Soundex,
normalized-prefix blocking, a small-data canopy candidate generator, and
Fellegi-Sunter log-likelihood-ratio scoring from supplied m/u probabilities.

Run `python -m pip install -r requirements.txt && python -m pytest -q`.

Similarity is evidence, not identity. Calibrate field probabilities and
thresholds on representative labelled pairs; measure candidate recall because
blocking can discard true matches. The canopy implementation is O(n²);
Soundex is English-oriented. Metaphone, automatic m/u estimation, scalable
indexing, address parsing, geometry matching and end-to-end POI deduplication
are not included.

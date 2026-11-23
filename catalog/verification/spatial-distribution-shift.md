# Verification record: spatial block MMD

## Identity
- Canonical record: block-level maximum mean discrepancy two-sample test.
- Implementation: implementations/python/distribution-shift/block_permutation.py.
- Classification: original teaching adaptation combining an unbiased block-kernel MMD statistic with whole-block label permutations.

## Bibliographic verification
- Gretton et al. (2012), JMLR 13, 723–773, is the primary source for MMD and kernel two-sample testing.
- The source does not prescribe the spatial-block permutation scheme implemented here; the lesson marks this distinction explicitly.

## Technical checks
- Gaussian RBF kernel; bandwidth supplied or median positive pairwise feature distance.
- Block similarity is the mean cross-observation kernel value between two blocks.
- Unbiased MMD statistic uses off-diagonal within-group block terms.
- Permutations shuffle block labels, preserving group block counts.
- Add-one Monte Carlo p-value avoids a zero p-value estimate.
- Validity requires exchangeable blocks under the null; code does not infer or establish this condition.

## Reproduction and rights
- Original NumPy implementation and tests.
- Tests cover separated groups, deterministic permutations, validation, block-label homogeneity and minimum block counts.
- No third-party code, figures or data are reproduced.
- Repository CI pending.

# Verification record: residual-based GNSS RAIM baseline

## Identity
- Implementation: `implementations/python/gnss-raim/raim.py`
- Classification: weighted linear least squares, global residual chi-square test and single-measurement leave-one-out exclusion baseline.

## Bibliographic and technical checks
- ESA Navipedia's RAIM Fundamentals describes fault detection as a statistical test on least-squares residuals and fault exclusion as a subsequent measurement/group rejection stage.
- Joerger, Chan & Pervan (2014), DOI 10.1002/navi.71, compare residual-based and solution-separation RAIM. This implementation is intentionally narrower than either complete integrity framework.
- Whitened residual statistic: `vᵀ R⁻¹ v`; under the stated null model it follows chi-square with `m - rank(H)` degrees of freedom.
- Leave-one-out candidate tests use a Bonferroni-adjusted alpha across the tested measurements. A unique passing candidate is reported; ambiguity and failure to isolate are explicit states.

## Reproduction and rights
- Original NumPy/SciPy implementation and synthetic tests.
- Tests cover exact GLS recovery, injected single outlier detection, unique exclusion, clean data and invalid inputs.
- No protection-level or integrity-risk claim is made.
- Full repository pytest and CI have not yet been confirmed for the new commit.

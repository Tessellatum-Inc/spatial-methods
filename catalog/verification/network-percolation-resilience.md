# Source verification — network percolation and resilience

## Identity and bibliography
Albert, Jeong & Barabási (2000), Nature 406, 378–382, DOI 10.1038/35019019. Nature's 2001 corrigendum (Nature 409, 542; DOI 10.1038/35054111) corrected part of the error-tolerance curves and is noted here.

## Technical and implementation scope
The package implements connected-component analysis and node-removal curves under static degree-targeted or seeded random orders. It does not reproduce all experiments in the source paper, model load redistribution/cascading failures or calculate service-level network performance.

## Reproduction
Tests cover disconnected components, star-network targeted attack, path fragmentation, deterministic random order and invalid removal sequences. Run repository tests/CI independently.

## Rights
Only metadata and paraphrased descriptions are included; no figures or source text are copied.

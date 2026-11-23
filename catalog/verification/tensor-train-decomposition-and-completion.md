# Verification record: tensor-train decomposition and completion

## Identity and scope
- Implementation: implementations/python/tensor-decomposition/tt_svd.py
- Tests: implementations/python/tensor-decomposition/test_tt_svd.py
- Classification: original dense TT-SVD implementation plus a simple data-consistent alternating-projection completion heuristic; not a reproduction of a named completion solver.

## Bibliographic checks
- Oseledets (2011), Tensor-train decomposition, SIAM Journal on Scientific Computing 33(5), 2295–2317, DOI 10.1137/090752286. This is the canonical TT-format reference used for the core representation and TT-SVD context.
- Grasedyck (2010), Hierarchical singular value decomposition of tensors, SIAM Journal on Matrix Analysis and Applications 31(4), 2029–2054, DOI 10.1137/090764189. Related hierarchical low-rank tensor context; not claimed as the implemented TT completion algorithm.

## Technical checks
- Core shapes are (r[k], n[k], r[k+1]) with boundary ranks one.
- TT-SVD uses sequential dense matrix SVDs; max_rank caps each internal rank.
- Relative tolerance is split across N-1 SVD truncations. A hard rank cap may prevent the requested error budget from being met.
- Completion alternates TT projection and exact restoration of observed entries.
- Observed RMSE is zero by construction; it is not evidence of predictive performance.
- Missing-value accuracy must be assessed with held-out observations. No global optimality or convergence guarantee is claimed.

## Reproduction and rights
- Original implementation and tests; no source code, text, figures or datasets copied.
- Tests cover exact reconstruction, rank-one tensors, rank caps, invalid core shapes, zero tensors and exact preservation of observed entries.
- Full repository pytest and CI have not been run in this authoring session.

import pytest
from nmf import nmf_euclidean

def reconstruct(w,h):
    return [[sum(w[i][a]*h[a][j] for a in range(len(h))) for j in range(len(h[0]))] for i in range(len(w))]

def test_rank_one_nonnegative_matrix_is_reconstructed():
    v=[[1,2,3],[2,4,6],[3,6,9]]
    result=nmf_euclidean(v,1,max_iter=1500,tolerance=1e-10)
    estimate=reconstruct(result["W"],result["H"])
    error=sum((v[i][j]-estimate[i][j])**2 for i in range(3) for j in range(3))**0.5
    assert error < 1e-3
    assert all(value>=0 for row in result["W"]+result["H"] for value in row)
    assert result["errors"][-1] <= result["errors"][0]

def test_deterministic_initialization():
    v=[[1,0,2],[0,3,1]]
    a=nmf_euclidean(v,2,max_iter=10)
    b=nmf_euclidean(v,2,max_iter=10)
    assert a["W"]==b["W"] and a["H"]==b["H"]

@pytest.mark.parametrize("v,rank", [([],1), ([[1,-1],[2,3]],1), ([[1,float("nan")]],1), ([[1,2],[3,4]],0)])
def test_rejects_invalid_matrix_or_rank(v,rank):
    with pytest.raises(ValueError):
        nmf_euclidean(v,rank)

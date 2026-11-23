import pytest
from median_polish import median_polish

def test_exact_additive_two_way_table_is_reconstructed():
    table=[[11,12,13],[21,22,23],[31,32,33]]
    r=median_polish(table)
    for i,row in enumerate(table):
        for j,value in enumerate(row):
            assert r["fitted"][i][j]+r["residuals"][i][j]==pytest.approx(value)
    assert max(abs(v) for row in r["residuals"] for v in row)<1e-10
    assert r["converged"]

def test_row_and_column_effects_are_median_centered():
    r=median_polish([[2,4,6],[8,10,12],[14,16,18]])
    assert sorted(r["row_effects"])[1]==pytest.approx(0)
    assert sorted(r["column_effects"])[1]==pytest.approx(0)

def test_classic_deaths_table_reconstructs_input():
    table=[[14,15,14],[7,4,7],[8,2,10],[15,9,10],[0,2,0]]
    r=median_polish(table)
    for i,row in enumerate(table):
        for j,value in enumerate(row):
            assert r["fitted"][i][j]+r["residuals"][i][j]==pytest.approx(value)

def test_outlier_remains_in_residual_component():
    r=median_polish([[1,2,3],[4,5,6],[7,8,100]])
    assert r["residuals"][2][2]>40

def test_missing_values_are_rejected_by_default():
    with pytest.raises(ValueError): median_polish([[1,2],[3,None]])

def test_missing_values_can_be_ignored_and_preserved():
    r=median_polish([[1,2,None],[3,4,5]],na_rm=True)
    assert r["residuals"][0][2] is None
    assert r["fitted"][0][2] is not None

def test_all_missing_row_and_column_have_zero_effect():
    r=median_polish([[1,None],[None,None],[3,None]],na_rm=True)
    assert r["row_effects"][1]==0
    assert r["column_effects"][1]==0
    assert all(v is None for v in r["residuals"][1])

def test_residual_sum_history_is_nonincreasing():
    r=median_polish([[14,15,14],[7,4,7],[8,2,10],[15,9,10],[0,2,0]])
    assert all(b<=a+1e-10 for a,b in zip(r["residual_sum_history"],r["residual_sum_history"][1:]))

def test_iteration_cap_reports_nonconvergence():
    r=median_polish([[1,2,3],[4,5,6],[7,8,100]],eps=1e-12,max_iterations=1)
    assert r["iterations"]==1
    assert not r["converged"]

@pytest.mark.parametrize("table",[[],[[]],[[1,2],[3]],[[float("inf"),2]],[[None,None]]])
def test_invalid_tables_rejected(table):
    with pytest.raises(ValueError): median_polish(table,na_rm=True)

def test_invalid_convergence_controls_rejected():
    with pytest.raises(ValueError): median_polish([[1]],eps=0)
    with pytest.raises(ValueError): median_polish([[1]],max_iterations=0)
    with pytest.raises(ValueError): median_polish([[1]],na_rm=1)

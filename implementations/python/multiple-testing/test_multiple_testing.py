import math
import pytest
from multiple_testing import adjust_pvalues

def test_bonferroni_known_values():
    r=adjust_pvalues([.01,.04,.2],"bonferroni")
    assert r["adjusted_pvalues"]==pytest.approx([.03,.12,.6])
    assert r["reject"]==[True,False,False]

def test_sidak_known_values():
    r=adjust_pvalues([.01,.04],"sidak")
    assert r["adjusted_pvalues"]==pytest.approx([1-.99**2,1-.96**2])

def test_holm_step_down_known_values():
    assert adjust_pvalues([.01,.04,.03],"holm")["adjusted_pvalues"]==pytest.approx([.03,.06,.06])

def test_bh_known_values_and_order_restoration():
    assert adjust_pvalues([.01,.04,.03],"bh")["adjusted_pvalues"]==pytest.approx([.03,.04,.04])

def test_by_applies_harmonic_dependence_factor():
    c=1+.5+1/3
    assert adjust_pvalues([.01,.04,.03],"by")["adjusted_pvalues"]==pytest.approx([.03*c,.04*c,.04*c])

def test_hochberg_step_up_known_values():
    assert adjust_pvalues([.01,.04,.03],"hochberg")["adjusted_pvalues"]==pytest.approx([.03,.04,.04])

@pytest.mark.parametrize("method",["bonferroni","sidak","holm","hochberg","bh","by"])
def test_permutation_invariance(method):
    p=[.04,.001,.2,.03]; order=[2,0,3,1]
    a=adjust_pvalues(p,method)["adjusted_pvalues"]
    b=adjust_pvalues([p[i] for i in order],method)["adjusted_pvalues"]
    assert b==pytest.approx([a[i] for i in order])

def test_monotone_adjusted_values_in_sorted_order():
    for method in ["holm","hochberg","bh","by"]:
        p=[.2,.01,.05,.03]; r=adjust_pvalues(p,method)["adjusted_pvalues"]
        ordered=[r[i] for i in sorted(range(len(p)),key=lambda i:p[i])]
        assert ordered==sorted(ordered)

def test_ties_and_boundaries():
    for method in ["bonferroni","sidak","holm","hochberg","bh","by"]:
        r=adjust_pvalues([0,.5,.5,1],method)["adjusted_pvalues"]
        assert r[0]==0 and r[-1]==1 and all(0<=v<=1 for v in r)

def test_single_test_family_is_identity():
    for method in ["bonferroni","sidak","holm","hochberg","bh","by"]:
        assert adjust_pvalues([.123],method)["adjusted_pvalues"]==pytest.approx([.123])

def test_alpha_changes_decisions_not_adjusted_values():
    a=adjust_pvalues([.01,.04,.2],"holm",.05)
    b=adjust_pvalues([.01,.04,.2],"holm",.01)
    assert a["adjusted_pvalues"]==pytest.approx(b["adjusted_pvalues"])
    assert a["reject"]!=b["reject"]

@pytest.mark.parametrize("p",[[],[-.1,.2],[.1,1.1],[float("nan")],[float("inf")]])
def test_invalid_pvalues(p):
    with pytest.raises(ValueError): adjust_pvalues(p)

@pytest.mark.parametrize("alpha",[-.1,1.1,float("nan"),"bad",True])
def test_invalid_alpha(alpha):
    with pytest.raises(ValueError): adjust_pvalues([.1,.2],alpha=alpha)

def test_unknown_method():
    with pytest.raises(ValueError): adjust_pvalues([.1,.2],"fdr_magic")

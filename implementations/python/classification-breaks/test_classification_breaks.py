import itertools
import numpy as np
import pytest
from classification_breaks import (box_plot_breaks, ckmeans_breaks, dalenius_hodges_breaks,
    geometric_interval_breaks, head_tail_breaks, standard_deviation_breaks)

def test_geometric_interval_breaks_form_geometric_progression():
    edges=geometric_interval_breaks([1,2,5,10,20,50,100],4)
    assert edges[0]==pytest.approx(1) and edges[-1]==pytest.approx(100)
    ratios=np.diff(np.log(edges)); np.testing.assert_allclose(ratios,np.repeat(ratios[0],len(ratios)))
    with pytest.raises(ValueError,match="positive"): geometric_interval_breaks([-1,1,2],2)

def test_standard_deviation_breaks_are_clipped():
    x=np.array([1,2,3,4,5,6,100]); edges=standard_deviation_breaks(x,2)
    assert edges[0]==x.min() and edges[-1]==x.max()
    assert np.all(np.diff(edges)>0)

def test_box_plot_breaks_include_quartiles_and_fences():
    edges=box_plot_breaks([1,2,3,4,5,6,100])
    assert edges[0]==1 and edges[-1]==100 and 4 in edges

def test_head_tail_breaks_recursively_split_heavy_tail():
    edges=head_tail_breaks([1,2,3,4,100,200])
    assert edges[0]==1 and edges[-1]==200
    assert edges[1]==pytest.approx(310/6)
    assert np.all(np.diff(edges)>0)

def test_dalenius_hodges_breaks_are_ordered_and_bounded():
    x=np.repeat(np.arange(1,21),np.arange(1,21)); edges=dalenius_hodges_breaks(x,4,bins=20)
    assert edges[0]==x.min() and edges[-1]==x.max() and np.all(np.diff(edges)>0)
    with pytest.raises(ValueError,match="bins"): dalenius_hodges_breaks(x,4,bins=2)

def _brute_sse(values,k):
    u=np.unique(values); best=np.inf
    for cuts in itertools.combinations(range(1,len(u)),k-1):
        bounds=(0,*cuts,len(u)); total=0.
        for a,b in zip(bounds[:-1],bounds[1:]):
            group=values[np.isin(values,u[a:b])]
            total+=float(np.sum((group-group.mean())**2))
        best=min(best,total)
    return best

def _sse_from_breaks(values,edges):
    total=0.
    for i,(lo,hi) in enumerate(zip(edges[:-1],edges[1:])):
        mask=(values>=lo)&((values<=hi) if i==len(edges)-2 else (values<hi))
        group=values[mask]
        if group.size: total+=float(np.sum((group-group.mean())**2))
    return total

def test_ckmeans_matches_exhaustive_partition_oracle():
    x=np.array([1,2,2,3,4,5,10,20,30,100,200],dtype=float)
    for k in (1,2,3,4):
        edges=ckmeans_breaks(x,k)
        assert len(edges)==k+1 and edges[0]==x.min() and edges[-1]==x.max()
        assert _sse_from_breaks(x,edges)==pytest.approx(_brute_sse(x,k))

def test_constant_data_and_single_class():
    assert geometric_interval_breaks([2,2,2],1).tolist()==[2.0]
    assert dalenius_hodges_breaks([2,2,2],1).tolist()==[2.0]
    assert ckmeans_breaks([2,2,2],1).tolist()==[2.0]
    assert box_plot_breaks([2,2,2]).tolist()==[2.0]

@pytest.mark.parametrize("bad", [[], [[1,2],[3,4]], [1,np.nan], [1,np.inf]])
def test_invalid_values_rejected(bad):
    with pytest.raises(ValueError): head_tail_breaks(bad)

def test_parameter_validation():
    with pytest.raises(ValueError): ckmeans_breaks([1,2,3],4)
    with pytest.raises(ValueError): geometric_interval_breaks([1,2,3],0)
    with pytest.raises(ValueError): head_tail_breaks([1,2,3],min_head_fraction=1.0)

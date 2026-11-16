import numpy as np
import pytest
from map_algebra import categorical_lookup, local_map_algebra

def test_local_reducers_and_binary_operations():
    a=np.array([[1,2],[3,4]],float); b=np.array([[5,6],[7,8]],float)
    c=np.array([[2,2],[2,2]],float)
    np.testing.assert_allclose(local_map_algebra([a,b,c],"sum"),[[8,10],[12,14]])
    np.testing.assert_allclose(local_map_algebra([a,b],"subtract"),[[-4,-4],[-4,-4]])
    np.testing.assert_allclose(local_map_algebra([a,b],"divide"),[[.2,2/6],[3/7,.5]])

def test_reducer_nodata_policies():
    a=np.array([[1,np.nan],[3,4]],float); b=np.array([[5,6],[np.nan,8]],float)
    strict=local_map_algebra([a,b],"sum")
    ignore=local_map_algebra([a,b],"sum",nodata_policy="ignore")
    assert np.isnan(strict[0,1]) and np.isnan(strict[1,0])
    np.testing.assert_allclose(ignore,[[6,6],[3,12]])

def test_binary_operation_requires_both_inputs():
    out=local_map_algebra([[[1,np.nan]],[[2,3]]],"add",nodata_policy="ignore")
    assert np.isnan(out[0,1])

def test_division_by_zero_is_nodata():
    out=local_map_algebra([[[4,5]],[[2,0]]],"divide")
    np.testing.assert_allclose(out[0,0],2)
    assert np.isnan(out[0,1])

def test_categorical_lookup_policies():
    src=np.array([[1,2,3],[2,np.nan,1]],float)
    np.testing.assert_allclose(categorical_lookup(src,{1:10,2:20}),[[10,20,np.nan],[20,np.nan,10]],equal_nan=True)
    np.testing.assert_allclose(categorical_lookup(src,{1:10,2:20},unknown="keep"),[[10,20,3],[20,np.nan,10]],equal_nan=True)
    with pytest.raises(ValueError,match="unknown categories"):
        categorical_lookup(src,{1:10,2:20},unknown="error")

def test_invalid_inputs_are_rejected():
    with pytest.raises(ValueError,match="identical shapes"):
        local_map_algebra([[[1]],[[1,2]]],"sum")
    with pytest.raises(ValueError,match="exactly two"):
        local_map_algebra([[[1]],[[2]],[[3]]],"divide")
    with pytest.raises(ValueError,match="unsupported"):
        local_map_algebra([[[1]],[[2]]],"median")
    with pytest.raises(ValueError,match="finite"):
        categorical_lookup([[1]],{np.nan:3})

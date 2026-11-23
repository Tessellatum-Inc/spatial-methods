import numpy as np
import pytest
from raster_reclassification import reclassify_ranges


def test_half_open_intervals_and_gaps():
    x=np.array([-1,0,4.999,5,9.999,10,15,np.nan])
    y=reclassify_ranges(x,[(0,5,1),(5,10,2),(10,15,3)],default=-9)
    np.testing.assert_allclose(y,[-9,1,1,2,2,3,-9,np.nan],equal_nan=True)


def test_nodata_is_preserved():
    x=np.array([[1.,2.],[-9999.,np.nan]])
    y=reclassify_ranges(x,[(0,3,7)],default=0,nodata=-9999)
    np.testing.assert_allclose(y,[[7,7],[-9999,np.nan]],equal_nan=True)


def test_rules_are_validated_and_order_independent():
    y=reclassify_ranges([6,1],[(5,10,2),(0,5,1)])
    np.testing.assert_array_equal(y,[2,1])
    with pytest.raises(ValueError): reclassify_ranges([1],[(0,2,1),(1,3,2)])
    with pytest.raises(ValueError): reclassify_ranges([1],[(2,2,1)])
    with pytest.raises(ValueError): reclassify_ranges([1],[(0,2,np.inf)])


def test_invalid_rasters_and_rule_shapes():
    with pytest.raises(ValueError): reclassify_ranges([],[(0,1,1)])
    with pytest.raises(ValueError): reclassify_ranges([np.inf],[(0,1,1)])
    with pytest.raises(ValueError): reclassify_ranges([1],[(0,1)])

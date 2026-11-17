import numpy as np
import pytest
from connected_components import connected_components

def test_separate_regions_receive_distinct_row_major_labels():
    mask=np.array([[1,1,0,0],[1,0,0,1],[0,1,0,1]],dtype=bool)
    labels,sizes=connected_components(mask,connectivity=4)
    assert list(sizes)==[1,2,3]
    assert sizes=={1:3,2:2,3:1}
    assert labels[0,0]==1 and labels[1,3]==2 and labels[2,1]==3

def test_diagonal_contact_depends_on_connectivity():
    mask=np.array([[1,0],[0,1]],dtype=bool)
    _,four=connected_components(mask,connectivity=4)
    _,eight=connected_components(mask,connectivity=8)
    assert len(four)==2
    assert len(eight)==1
    assert list(eight.values())==[2]

def test_invalid_cells_act_as_barriers_and_remain_zero():
    mask=np.ones((1,3),dtype=bool)
    valid=np.array([[1,0,1]],dtype=bool)
    labels,sizes=connected_components(mask,connectivity=4,valid=valid)
    np.testing.assert_array_equal(labels,[[1,0,2]])
    assert sizes=={1:1,2:1}

def test_background_is_zero_and_empty_foreground_has_no_components():
    labels,sizes=connected_components(np.zeros((3,4),dtype=bool))
    assert not labels.any()
    assert sizes=={}

def test_invalid_shapes_and_connectivity_are_rejected():
    with pytest.raises(ValueError,match="2D"):
        connected_components([1,0])
    with pytest.raises(ValueError,match="same 2D shape"):
        connected_components([[1,0]],valid=[[1]])
    with pytest.raises(ValueError,match="connectivity"):
        connected_components([[1]],connectivity=6)
    with pytest.raises(ValueError,match="finite boolean"):
        connected_components([[np.nan]])
    with pytest.raises(ValueError,match="finite boolean"):
        connected_components([[1]],valid=[[np.nan]])


def test_3d_six_connectivity_joins_face_neighbours_only():
    from connected_components import connected_components_3d
    volume = np.zeros((2, 2, 2), dtype=bool)
    volume[0, 0, 0] = True
    volume[1, 0, 0] = True
    volume[1, 1, 1] = True
    labels, sizes = connected_components_3d(volume, connectivity=6)
    assert len(sizes) == 2
    assert sorted(sizes.values()) == [1, 2]
    assert labels[0, 0, 0] == labels[1, 0, 0]


def test_3d_eighteen_and_twenty_six_connectivity_differ_on_corner_touch():
    from connected_components import connected_components_3d
    volume = np.zeros((2, 2, 2), dtype=bool)
    volume[0, 0, 0] = True
    volume[1, 1, 1] = True
    assert len(connected_components_3d(volume, connectivity=18)[1]) == 2
    assert len(connected_components_3d(volume, connectivity=26)[1]) == 1


def test_3d_valid_mask_is_barrier_and_labels_are_row_major():
    from connected_components import connected_components_3d
    volume = np.ones((1, 1, 3), dtype=bool)
    valid = np.array([[[1, 0, 1]]], dtype=bool)
    labels, sizes = connected_components_3d(volume, connectivity=6, valid=valid)
    assert labels.tolist() == [[[1, 0, 2]]]
    assert sizes == {1: 1, 2: 1}


def test_3d_component_input_validation():
    from connected_components import connected_components_3d
    with pytest.raises(ValueError, match="3D"):
        connected_components_3d([[1, 0]])
    with pytest.raises(ValueError, match="connectivity"):
        connected_components_3d(np.ones((2, 2, 2)), connectivity=12)
    with pytest.raises(ValueError, match="same 3D shape"):
        connected_components_3d(np.ones((2, 2, 2)), valid=np.ones((2, 2)))
    with pytest.raises(ValueError, match="only finite"):
        connected_components_3d(np.array([[[1, np.nan]]]))


def test_flood_fill_exact_value_and_connectivity():
    from connected_components import flood_fill
    raster = np.array([[1,0,1],[0,1,0],[1,0,1]])
    assert flood_fill(raster, (0,0), connectivity=4).sum() == 1
    assert flood_fill(raster, (0,0), connectivity=8).sum() == 5


def test_flood_fill_respects_valid_mask_and_invalid_seed():
    from connected_components import flood_fill
    raster = np.ones((1,4), dtype=int)
    valid = np.array([[1,1,0,1]], dtype=bool)
    assert flood_fill(raster, (0,0), valid=valid).tolist() == [[True,True,False,False]]
    assert not flood_fill(raster, (0,2), valid=valid).any()


def test_flood_fill_rejects_invalid_inputs():
    from connected_components import flood_fill
    with pytest.raises(ValueError): flood_fill([[1,2]], (0,2))
    with pytest.raises(ValueError): flood_fill([[1]], (0,0), connectivity=6)
    with pytest.raises(ValueError): flood_fill([[1]], (0.0,0))


def test_rle_round_trip_preserves_shape_dtype_and_values():
    from connected_components import run_length_encode, run_length_decode
    for data in (np.array([[1,1,1],[0,0,2]], dtype=np.int16),
                 np.array([[True,True],[False,False]], dtype=bool),
                 np.array([[1.5,1.5],[2.25,3.0]], dtype=np.float32)):
        encoded = run_length_encode(data)
        decoded = run_length_decode(encoded)
        np.testing.assert_array_equal(decoded, data)
        assert decoded.dtype == data.dtype


def test_rle_single_run_and_invalid_streams():
    from connected_components import run_length_encode, run_length_decode
    assert run_length_encode(np.ones((2,3), dtype=np.uint8))["runs"] == [(1,6)]
    with pytest.raises(ValueError): run_length_encode(np.empty((0,2)))
    with pytest.raises(ValueError): run_length_decode({"shape":(2,2),"dtype":"<i8","runs":[(1,3)]})
    with pytest.raises(ValueError): run_length_decode({"shape":(1,1),"dtype":"<i8","runs":[(1,0)]})

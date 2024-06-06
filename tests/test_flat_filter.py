"""
Author: nagan319
Date: 2024/06/03
"""

import pytest
from src.app.utils.image_processing.utils import Size, Colors
from src.app.utils.image_processing.filters import FlatFilter

"""
Tests for flat filter.

Test coverage:
- type errors raised by invalid values
"""

@pytest.fixture
def valid_input():
    src_path = "valid_src_path.png"
    dst_path = "valid_dst_path.png"
    size = Size(100, 100)  
    corners = [(0, 0), (100, 0), (100, 100), (0, 100)]  #
    return src_path, dst_path, size, corners

@pytest.mark.parametrize("invalid_size", [None, "invalid", True, [(100, 100)]])
def test_invalid_size(valid_input, invalid_size):
    src_path, dst_path, _, corners = valid_input
    with pytest.raises(TypeError):
        FlatFilter(src_path, dst_path, invalid_size, corners)

@pytest.mark.parametrize("invalid_size", [1.5, 3.14, -42.0])
def test_invalid_size_float(valid_input, invalid_size):
    src_path, dst_path, _, corners = valid_input
    with pytest.raises(TypeError):
        FlatFilter(src_path, dst_path, invalid_size, corners)

@pytest.mark.parametrize("invalid_corners", [None, "invalid", True, Size(100, 100)])
def test_invalid_corners(valid_input, invalid_corners):
    src_path, dst_path, size, _ = valid_input
    with pytest.raises(TypeError):
        FlatFilter(src_path, dst_path, size, invalid_corners)

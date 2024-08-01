from typing import Optional, Union

import ensure_test_cases
import pytest

from pss_fleet_data.utils.ensure import positive_float_or_int


@pytest.mark.parametrize(["value", "default", "expected_result"], ensure_test_cases.valid_positive_float_or_int)
def test_positive_float_or_int(
    value: Optional[Union[float, int]],
    default: Optional[Union[float, int]],
    expected_result: Optional[Union[float, int]],
):
    result = positive_float_or_int(value, "", default)
    assert result == expected_result


@pytest.mark.parametrize(["value", "expected_exception"], ensure_test_cases.invalid_float_or_int)
def test_positive_float_or_int_invalid(value: Optional[Union[float, int]], expected_exception: Exception):
    with pytest.raises(expected_exception):
        _ = positive_float_or_int(value, "", None)

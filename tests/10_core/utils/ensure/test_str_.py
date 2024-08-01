from typing import Optional

import ensure_test_cases
import pytest

from pss_fleet_data.utils.ensure import str_


@pytest.mark.parametrize(["value", "default", "expected_result"], ensure_test_cases.valid_str)
def test_str_(value: Optional[str], default: Optional[str], expected_result: Optional[str]):
    result = str_(value, "", default)
    assert result == expected_result


@pytest.mark.parametrize(["value", "expected_exception"], ensure_test_cases.invalid_str)
def test_str__invalid(value: Optional[str], expected_exception: Exception):
    with pytest.raises(expected_exception):
        _ = str_(value, "", None)

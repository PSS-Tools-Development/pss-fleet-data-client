from typing import Optional, Union

import ensure_test_cases
import pytest
from httpx import URL

from pss_fleet_data.utils.ensure import str_or_url


@pytest.mark.parametrize(["value", "default", "expected_result"], ensure_test_cases.valid_str_or_url)
def test_str_or_url(value: Optional[Union[str, URL]], default: Optional[Union[str, URL]], expected_result: Optional[Union[str, URL]]):
    result = str_or_url(value, "", default)
    assert result == expected_result


@pytest.mark.parametrize(["value", "expected_exception"], ensure_test_cases.invalid_str_or_url)
def test_str_or_url_invalid(value: Optional[Union[str, URL]], expected_exception: Exception):
    with pytest.raises(expected_exception):
        _ = str_or_url(value, "", None)

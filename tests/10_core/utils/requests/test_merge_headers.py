from typing import Any, Optional

import pytest

from pss_fleet_data.utils import merge_headers


test_cases_valid = [
    # client_headers, headers, expected_headers
    pytest.param(None, None, {}, id="none_none"),
    pytest.param(None, {}, {}, id="none_empty"),
    pytest.param({}, None, {}, id="empty_none"),
    pytest.param(None, {"A": "1"}, {"A": "1"}, id="none_non-empty"),
    pytest.param({}, {"A": "1"}, {"A": "1"}, id="empty_non-empty"),
    pytest.param({"A": "1"}, None, {"A": "1"}, id="non-empty_none"),
    pytest.param({"A": "1"}, {}, {"A": "1"}, id="non-empty_empty"),
    pytest.param({"A": "a"}, {"A": "1"}, {"A": "1"}, id="overwrite"),
    pytest.param({"A": "1"}, {"B": "2"}, {"A": "1", "B": "2"}, id="non-empty_non-empty"),
    pytest.param({"A": "1", "B": "2"}, {"B": "3"}, {"A": "1", "B": "3"}, id="partial_overwrite"),
]
"""client_headers, headers, expected_headers"""


@pytest.mark.parametrize(["client_headers", "headers", "expected_headers"], test_cases_valid)
def test_merge_headers(client_headers: Optional[dict[str, Any]], headers: Optional[dict[str, Any]], expected_headers: dict[str, str]):
    request_headers = merge_headers(client_headers, headers)
    assert request_headers == expected_headers

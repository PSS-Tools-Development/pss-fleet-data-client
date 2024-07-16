import pytest
from conftest import _DEFAULT_API_KEY


api_keys = [
    # api_key_sent, api_key_expected
    pytest.param(None, _DEFAULT_API_KEY, id="none"),
    pytest.param("", _DEFAULT_API_KEY, id="empty"),
    pytest.param(_DEFAULT_API_KEY, _DEFAULT_API_KEY, id="default"),
    pytest.param("abcdef", "abcdef", id="abcdef"),
]
"""api_key_sent, api_key_expected"""


parameter_dicts = [
    # input, expected_output
    pytest.param(None, {}, id="none"),
    pytest.param({}, {}, id="empty"),
    pytest.param({"from_date": "x"}, {"fromDate": "x"}, id="empty"),
]

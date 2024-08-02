import pytest
from httpx import URL


invalid_str = [
    # value, expected_exception
    pytest.param(123, TypeError, id="int"),
    pytest.param(12.3, TypeError, id="float"),
    pytest.param(complex(12.3, -23.4), TypeError, id="complex"),
    pytest.param(True, TypeError, id="bool"),
    pytest.param(URL("http://example.com"), TypeError, id="url"),
]
"""value, expected_exception"""


invalid_str_or_url = [
    # url, expected_exception
    pytest.param(123, TypeError, id="int"),
    pytest.param(12.3, TypeError, id="float"),
    pytest.param(complex(12.3, -23.4), TypeError, id="complex"),
    pytest.param(True, TypeError, id="bool"),
]
"""url, expected_exception"""


invalid_float_or_int = [
    # url, expected_exception
    pytest.param(-123, ValueError, id="int_negative"),
    pytest.param(-12.3, ValueError, id="float_negative"),
    pytest.param(complex(12.3, -23.4), TypeError, id="complex"),
    pytest.param(True, TypeError, id="bool"),
    pytest.param(URL("http://example.com"), TypeError, id="url"),
    pytest.param("123abc", TypeError, id="str"),
]
"""url, expected_exception"""


valid_str = [
    # value, default, expected_result
    pytest.param(None, None, None, id="none_default_none"),
    pytest.param("", None, "", id="empty_str_default_none"),
    pytest.param("abc", None, "abc", id="str_default_none"),
    pytest.param(None, "", "", id="none_default_empty"),
    pytest.param("", "", "", id="empty_str_default_empty"),
    pytest.param("abc", "", "abc", id="str_default_empty"),
    pytest.param(None, "123", "123", id="none_default_set"),
    pytest.param("", "123", "", id="empty_str_default_set"),
    pytest.param("abc", "123", "abc", id="str_default_set"),
]
"""value, default, expected_result"""


valid_str_or_url = [
    # value, default, expected_result
    pytest.param(None, None, None, id="none"),
    pytest.param(None, "http://example.com", "http://example.com", id="none_with_default"),
    pytest.param("http://example.com", None, "http://example.com", id="http_str"),
    pytest.param("http://example.com", "http://127.0.0.1:8080", "http://example.com", id="http_str_with_default"),
    pytest.param(URL("http://example.com"), None, "http://example.com", id="http_url"),
    pytest.param("https://localhost:1234", None, "https://localhost:1234", id="https_str_with_port"),
    pytest.param(URL("https://localhost:1234"), None, URL("https://localhost:1234"), id="https_url_with_port"),
]
"""value, default, expected_result"""


valid_positive_float_or_int = [
    # value, default, expected_result
    pytest.param(None, None, None, id="none"),
    pytest.param(None, 5.0, 5.0, id="none_with_default_float"),
    pytest.param(None, 5, 5, id="none_with_default_int"),
    pytest.param(10.0, None, 10.0, id="float"),
    pytest.param(10, None, 10, id="int"),
    pytest.param(10.0, 5.0, 10.0, id="float_with_default"),
    pytest.param(10, 5, 10, id="int_with_default"),
]
"""value, default, expected_result"""

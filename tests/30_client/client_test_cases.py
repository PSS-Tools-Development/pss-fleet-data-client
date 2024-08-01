import pytest
from httpx import URL

from pss_fleet_data.core.config import get_config


client_valid = [
    # base_url, api_key, proxy, request_timeout, connect_timeout, expected_base_url, expected_connect_timeout
    pytest.param(None, None, None, None, None, get_config().default_base_url, 5.0, id="all_none"),
    # 5 parameters
    pytest.param(None, None, "https://127.0.0.1:8080", 10.0, None, get_config().default_base_url, 5.0, id="proxy_request_timeout"),
    pytest.param("https://example.com", "123456", "https://127.0.0.1:8080", 10.0, 8.0, "https://example.com", 8.0, id="all"),
]
"""base_url, api_key, proxy, request_timeout, connect_timeout, expected_base_url, expected_connect_timeout"""


api_key_valid = [
    # api_key
    pytest.param(None, id="none"),
    pytest.param("123abc", id="str"),
]
"""api_key"""


base_url_valid = [
    # base_url, expected_base_url
    pytest.param(None, get_config().default_base_url, id="none"),
    pytest.param("http://example.com", "http://example.com", id="http_str"),
    pytest.param(URL("http://example.com"), "http://example.com", id="http_url"),
    pytest.param("https://example.com", "https://example.com", id="https_str"),
    pytest.param(URL("https://example.com"), "https://example.com", id="https_url"),
]
"""base_url, expected_base_url"""


proxy_invalid = [
    # proxy
    pytest.param(None, id="none"),
    pytest.param("http://127.0.0.1:8080", id="http_str"),
    pytest.param(URL("http://127.0.0.1:8080"), id="http_url"),
    pytest.param("https://localhost:1234", id="https_str"),
    pytest.param(URL("https://localhost:1234"), id="https_url"),
]
"""proxy"""


proxy_valid = [
    # proxy
    pytest.param(None, id="none"),
    pytest.param("http://127.0.0.1:8080", id="http_str"),
    pytest.param(URL("http://127.0.0.1:8080"), id="http_url"),
    pytest.param("https://localhost:1234", id="https_str"),
    pytest.param(URL("https://localhost:1234"), id="https_url"),
]
"""proxy"""


timeout_invalid = [
    # request_timeout, connect_timeout, expected_connect_timeout
    pytest.param(None, None, 5.0, id="none_none"),
    pytest.param(10.0, None, 5.0, id="float_none"),
    pytest.param(None, 8.0, 8.0, id="none_float"),
    pytest.param(10.0, 8.0, 8.0, id="float_float"),
    pytest.param(10, None, 5.0, id="int_none"),
    pytest.param(None, 8, 8.0, id="none_int"),
    pytest.param(10, 8, 8.0, id="int_int"),
]
"""request_timeout, connect_timeout, expected_connect_timeout"""


timeout_valid = [
    # request_timeout, connect_timeout, expected_connect_timeout
    pytest.param(None, None, 5.0, id="none_none"),
    pytest.param(10.0, None, 5.0, id="float_none"),
    pytest.param(None, 8.0, 8.0, id="none_float"),
    pytest.param(10.0, 8.0, 8.0, id="float_float"),
    pytest.param(10, None, 5.0, id="int_none"),
    pytest.param(None, 8, 8.0, id="none_int"),
    pytest.param(10, 8, 8.0, id="int_int"),
]
"""request_timeout, connect_timeout, expected_connect_timeout"""


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

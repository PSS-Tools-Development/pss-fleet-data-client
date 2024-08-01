import pytest

from pss_fleet_data.core.config import get_config


client_valid = [
    # base_url, api_key, proxy, request_timeout, connect_timeout, expected_base_url, expected_connect_timeout
    pytest.param(None, None, None, None, None, get_config().default_base_url, 5.0, id="all_none"),
    # 5 parameters
    pytest.param(None, None, "https://127.0.0.1:8080", 10.0, None, get_config().default_base_url, 5.0, id="all"),
    pytest.param("https://example.com", "123456", "https://127.0.0.1:8080", 10.0, 8.0, "https://example.com", 8.0, id="all"),
]
"""base_url, api_key, proxy, request_timeout, connect_timeout, expected_base_url, expected_connect_timeout"""


api_key_valid = [
    # api_key
    pytest.param(None, id="none"),
    pytest.param("123456", id="http"),
    pytest.param("abcdef", id="https"),
]
"""api_key"""


base_url_valid = [
    # base_url, expected_base_url
    pytest.param(None, get_config().default_base_url, id="none"),
    pytest.param("http://example.com", "http://example.com", id="http"),
    pytest.param("https://example.com", "https://example.com", id="https"),
]
"""base_url, expected_base_url"""


proxy_valid = [
    # proxy
    pytest.param(None, id="none"),
    pytest.param("http://127.0.0.1:8080", id="http"),
    pytest.param("https://localhost:1234", id="https"),
]
"""proxy"""


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

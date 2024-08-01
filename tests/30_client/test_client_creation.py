from typing import Optional

import pytest
from httpx import Timeout
from httpx._config import DEFAULT_TIMEOUT_CONFIG

from pss_fleet_data import PssFleetDataClient
from pss_fleet_data.core.config import get_config


test_cases_valid = [
    # base_url, api_key, proxy, timeout, expected_base_url, expected_timeout_config
    pytest.param(None, None, None, None, get_config().default_base_url, DEFAULT_TIMEOUT_CONFIG, id="all_none"),
    # 1 parameter
    pytest.param("https://example.com", None, None, None, "https://example.com", DEFAULT_TIMEOUT_CONFIG, id="base_url"),
    pytest.param(None, "123456", None, None, get_config().default_base_url, DEFAULT_TIMEOUT_CONFIG, id="api_key"),
    pytest.param(None, None, "https://127.0.0.1:8080", None, get_config().default_base_url, DEFAULT_TIMEOUT_CONFIG, id="proxy"),
    pytest.param(None, None, None, 10, get_config().default_base_url, Timeout(10), id="timeout"),
    # 2 parameters
    pytest.param("https://example.com", "123456", None, None, "https://example.com", DEFAULT_TIMEOUT_CONFIG, id="base_url_api_key"),
    pytest.param("https://example.com", None, "https://127.0.0.1:8080", None, "https://example.com", DEFAULT_TIMEOUT_CONFIG, id="base_url_proxy"),
    pytest.param("https://example.com", None, None, 10, "https://example.com", Timeout(10), id="base_url_timeout"),
    pytest.param(None, "123456", "https://127.0.0.1:8080", None, get_config().default_base_url, DEFAULT_TIMEOUT_CONFIG, id="api_key_proxy"),
    pytest.param(None, "123456", None, 10, get_config().default_base_url, Timeout(10), id="api_key_timeout"),
    pytest.param(None, None, "https://127.0.0.1:8080", 10, get_config().default_base_url, Timeout(10), id="proxy_timeout"),
    # 3 parameters
    pytest.param(
        "https://example.com", "123456", "https://127.0.0.1:8080", None, "https://example.com", DEFAULT_TIMEOUT_CONFIG, id="base_url_api_key_proxy"
    ),
    pytest.param("https://example.com", "123456", None, 10, "https://example.com", Timeout(10), id="base_url_api_key_timeout"),
    pytest.param("https://example.com", None, "https://127.0.0.1:8080", 10, "https://example.com", Timeout(10), id="base_url_proxy_timeout"),
    pytest.param(None, "123456", "https://127.0.0.1:8080", 10, get_config().default_base_url, Timeout(10), id="api_key_proxy_timeout"),
    # 4 parameters
    pytest.param("https://example.com", "123456", "https://127.0.0.1:8080", 10, "https://example.com", Timeout(10), id="all"),
]
"""base_url, api_key, proxy, timeout, expected_timeout_config"""


@pytest.mark.parametrize(["base_url", "api_key", "proxy", "timeout", "expected_base_url", "expected_timeout_config"], test_cases_valid)
def test_client_creation(
    base_url: Optional[str],
    api_key: Optional[str],
    proxy: Optional[str],
    timeout: Optional[float],
    expected_base_url: str,
    expected_timeout_config: Timeout,
):
    client = PssFleetDataClient(base_url, api_key, proxy, timeout)
    assert client.base_url == expected_base_url
    assert client.api_key == api_key
    assert client.proxy == proxy
    assert client._PssFleetDataClient__http_client.timeout == expected_timeout_config

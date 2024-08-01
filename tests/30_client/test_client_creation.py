from typing import Optional, Union

import client_test_cases
import pytest

from pss_fleet_data import PssFleetDataClient


@pytest.mark.parametrize(
    [
        "base_url",
        "api_key",
        "proxy",
        "request_timeout",
        "connect_timeout",
        "expected_base_url",
        "expected_connect_timeout",
    ],
    client_test_cases.client_valid,
)
def test_client_creation(
    base_url: Optional[str],
    api_key: Optional[str],
    proxy: Optional[str],
    request_timeout: Optional[float],
    connect_timeout: Optional[float],
    expected_base_url: str,
    expected_connect_timeout: float,
):
    client = PssFleetDataClient(base_url, api_key, proxy, request_timeout, connect_timeout)

    assert client.base_url == expected_base_url
    assert client.api_key == api_key
    assert client.proxy == proxy
    assert client._PssFleetDataClient__http_client.timeout.connect == expected_connect_timeout
    assert client._PssFleetDataClient__http_client.timeout.read == request_timeout
    assert client._PssFleetDataClient__http_client.timeout.write == request_timeout
    assert client._PssFleetDataClient__http_client.timeout.pool == request_timeout


@pytest.mark.parametrize(["api_key"], client_test_cases.api_key_valid)
def test_client_creation_api_key(api_key: Optional[str]):
    client = PssFleetDataClient(api_key=api_key)

    assert client.api_key == api_key


@pytest.mark.parametrize(["base_url", "expected_base_url"], client_test_cases.base_url_valid)
def test_client_creation_base_url(base_url: Optional[str], expected_base_url: str):
    client = PssFleetDataClient(base_url=base_url)

    assert client.base_url == expected_base_url


@pytest.mark.parametrize(["proxy"], client_test_cases.proxy_valid)
def test_client_creation_proxy(proxy: Optional[str]):
    client = PssFleetDataClient(proxy=proxy)

    assert client.proxy == proxy


@pytest.mark.parametrize(["request_timeout", "connect_timeout", "expected_connect_timeout"], client_test_cases.timeout_valid)
def test_client_creation_timeout(
    request_timeout: Optional[Union[float, int]], connect_timeout: Optional[Union[float, int]], expected_connect_timeout: float
):
    client = PssFleetDataClient(request_timeout=request_timeout, connect_timeout=connect_timeout)

    assert client._PssFleetDataClient__http_client.timeout.connect == expected_connect_timeout
    assert client._PssFleetDataClient__http_client.timeout.read == request_timeout
    assert client._PssFleetDataClient__http_client.timeout.write == request_timeout
    assert client._PssFleetDataClient__http_client.timeout.pool == request_timeout

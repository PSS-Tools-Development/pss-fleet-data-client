from typing import Any, Optional, Union

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

    assert not client.api_key or client.api_key == str(api_key)


@pytest.mark.parametrize(["value", "expected_exception"], client_test_cases.invalid_str)
def test_client_creation_api_key_invalid(value: Any, expected_exception: Exception):
    with pytest.raises(expected_exception):
        _ = PssFleetDataClient(api_key=value)


@pytest.mark.parametrize(["base_url", "expected_base_url"], client_test_cases.base_url_valid)
def test_client_creation_base_url(base_url: Optional[str], expected_base_url: str):
    client = PssFleetDataClient(base_url=base_url)

    assert client.base_url == expected_base_url


@pytest.mark.parametrize(["value", "expected_exception"], client_test_cases.invalid_str_or_url)
def test_client_creation_base_url_invalid(value: Any, expected_exception: Exception):
    with pytest.raises(expected_exception):
        _ = PssFleetDataClient(base_url=value)


@pytest.mark.parametrize(["proxy"], client_test_cases.proxy_valid)
def test_client_creation_proxy(proxy: Optional[str]):
    client = PssFleetDataClient(proxy=proxy)

    assert client.proxy == proxy


@pytest.mark.parametrize(["value", "expected_exception"], client_test_cases.invalid_str_or_url)
def test_client_creation_proxy(value: Any, expected_exception: Exception):
    with pytest.raises(expected_exception):
        _ = PssFleetDataClient(proxy=value)


@pytest.mark.parametrize(["request_timeout", "connect_timeout", "expected_connect_timeout"], client_test_cases.timeout_valid)
def test_client_creation_timeout(
    request_timeout: Optional[Union[float, int]], connect_timeout: Optional[Union[float, int]], expected_connect_timeout: float
):
    client = PssFleetDataClient(request_timeout=request_timeout, connect_timeout=connect_timeout)

    assert client._PssFleetDataClient__http_client.timeout.connect == expected_connect_timeout
    assert client._PssFleetDataClient__http_client.timeout.read == request_timeout
    assert client._PssFleetDataClient__http_client.timeout.write == request_timeout
    assert client._PssFleetDataClient__http_client.timeout.pool == request_timeout


@pytest.mark.parametrize(["value", "expected_exception"], client_test_cases.invalid_float_or_int)
def test_client_creation_connect_timeout_invalid(value: Any, expected_exception: Exception):
    with pytest.raises(expected_exception):
        _ = PssFleetDataClient(connect_timeout=value)


@pytest.mark.parametrize(["value", "expected_exception"], client_test_cases.invalid_float_or_int)
def test_client_creation_request_timeout_invalid(value: Any, expected_exception: Exception):
    with pytest.raises(expected_exception):
        _ = PssFleetDataClient(request_timeout=value)

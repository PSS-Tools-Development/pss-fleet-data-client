import re

import pytest
from pytest_httpx import HTTPXMock


@pytest.fixture(scope="function")
def mock_response_empty_collection_get_204(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        text="[]",
    )


@pytest.fixture(scope="function")
def mock_response_empty_get_204(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        text="",
    )


@pytest.fixture(scope="function")
def mock_response_empty_collection_get_204_by_timestamp_daily(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=re.compile(r"^.*?fromDate=2024-04-05.*"),
        text="[]",
    )


@pytest.fixture(scope="function")
def mock_response_empty_collection_get_204_by_timestamp_monthly(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        url=re.compile(r"^.*?fromDate=2024-03-06.*"),
        text="[]",
    )

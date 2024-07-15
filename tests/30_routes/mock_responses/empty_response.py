import pytest
from pytest_httpx import HTTPXMock


@pytest.fixture(scope="function")
def mock_response_empty_collection_get_204(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        text="[]",
    )


@pytest.fixture(scope="function")
def mock_response_empty_get_204(get_collection_1_url: str, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="DELETE",
        url=get_collection_1_url,
        text="",
    )

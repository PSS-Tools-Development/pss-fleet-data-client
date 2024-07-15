import pytest
from pytest_httpx import HTTPXMock


@pytest.fixture(scope="function")
def mock_response_empty_collection_get_204(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        text="[]",
    )

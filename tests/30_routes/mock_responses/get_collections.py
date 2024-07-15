import pytest
from pytest_httpx import HTTPXMock

from client.model.api import ApiCollection


@pytest.fixture(scope="function")
def get_collections_url(base_url: str) -> str:
    return f"{base_url}/collections/"


@pytest.fixture(scope="function")
def mock_response_get_collections_200(api_collection: ApiCollection, get_collections_url: str, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        url=get_collections_url,
        text=f"[{api_collection.model_dump_json()}]",
    )


@pytest.fixture(scope="function")
def mock_response_get_collections_204(get_collections_url: str, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        url=get_collections_url,
        text="[]",
    )

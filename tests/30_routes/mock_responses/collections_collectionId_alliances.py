import pytest
from pytest_httpx import HTTPXMock

from client.model.api import ApiCollection


@pytest.fixture(scope="function")
def mock_response_collections_collectionId_alliances_get_200(api_collection_with_fleets: ApiCollection, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        text=api_collection_with_fleets.model_dump_json(),
    )

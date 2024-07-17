import pytest
from pytest_httpx import HTTPXMock

from client.models.api_models import ApiCollectionMetadata


@pytest.fixture(scope="function")
def mock_response_collections_post_201(api_collection_metadata_9: ApiCollectionMetadata, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        status_code=201,
        text=api_collection_metadata_9.model_dump_json(),
    )

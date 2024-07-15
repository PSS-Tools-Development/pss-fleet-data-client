import pytest
from pytest_httpx import HTTPXMock

from client.model.api import ApiCollection


@pytest.fixture(scope="function")
def get_collection_1_url(base_url) -> str:
    return f"{base_url}/collections/1"


@pytest.fixture(scope="function")
def mock_response_collections_collectionId_delete_204(get_collection_1_url: str, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="DELETE",
        url=get_collection_1_url,
        text="",
    )


@pytest.fixture(scope="function")
def mock_response_collections_collectionId_delete_500(get_collection_1_url: str, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="DELETE",
        url=get_collection_1_url,
        status_code=500,
        json={
            "code": "COLLECTION_NOT_DELETED",
            "message": "The requested Collection could not be deleted.",
            "details": "The Collection with the ID '1' exists, but an error occured while trying to delete it.",
            "timestamp": "2024-07-13T14:04:30.696117+00:00",
            "url": get_collection_1_url,
            "suggestion": "Check, if the Collection with the provided `collectionId` still exists and try again later, if it does.",
            "links": [],
        },
    )


@pytest.fixture(scope="function")
def mock_response_collections_collectionId_get_200(api_collection: ApiCollection, get_collection_1_url: str, httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="GET",
        url=get_collection_1_url,
        text=api_collection.model_dump_json(),
    )

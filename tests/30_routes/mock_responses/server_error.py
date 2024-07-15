import pytest
from pytest_httpx import HTTPXMock

from client.model.api import ApiCollection


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

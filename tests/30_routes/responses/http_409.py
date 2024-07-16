import pytest
from pytest_httpx import HTTPXMock


@pytest.fixture(scope="function")
def mock_response_collections_post_409_non_unique_timestamp(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="POST",
        status_code=409,
        json={
            "code": "NON_UNIQUE_TIMESTAMP",
            "message": "The resource could not be created.",
            "details": "Can't insert collection: A collection with this timestamp ({timestamp}) already exists in the database with the ID '{collection_id}'.",
            "timestamp": "2024-07-16T10:55:30.614758+00:00",
            "url": "https://example.com",
            "suggestion": "If you want to update the Collection in question, delete and re-insert it.",
            "links": [],
        },
    )

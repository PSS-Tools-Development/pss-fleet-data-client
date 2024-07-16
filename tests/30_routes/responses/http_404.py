import pytest
from pytest_httpx import HTTPXMock


@pytest.fixture(scope="function")
def mock_response_alliance_not_found(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        status_code=404,
        json={
            "code": "ALLIANCE_NOT_FOUND",
            "message": "The requested Alliance could not be found.",
            "details": "There is no Alliance with the ID '1'.",
            "timestamp": "2020-01-01T00:00:00+00:00",
            "url": "https://example.com",
            "suggestion": "Check the provided `allianceId` parameter in the path.",
            "links": [],
        },
    )


@pytest.fixture(scope="function")
def mock_response_collection_not_found(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        status_code=404,
        json={
            "code": "COLLECTION_NOT_FOUND",
            "message": "The requested Collection could not be found.",
            "details": "There is no Collection with the ID '1'.",
            "timestamp": "2020-01-01T00:00:00+00:00",
            "url": "https://example.com",
            "suggestion": "Check the provided `collectionId` parameter in the path.",
            "links": [],
        },
    )


@pytest.fixture(scope="function")
def mock_response_user_not_found(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        status_code=404,
        json={
            "code": "USER_NOT_FOUND",
            "message": "The requested User could not be found.",
            "details": "There is no User with the ID '1'.",
            "timestamp": "2020-01-01T00:00:00+00:00",
            "url": "https://example.com",
            "suggestion": "Check the provided `userId` parameter in the path.",
            "links": [],
        },
    )

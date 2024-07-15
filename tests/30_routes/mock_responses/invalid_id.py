import pytest
from pytest_httpx import HTTPXMock


@pytest.fixture(scope="function")
def mock_response_alliance_id_invalid(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        status_code=422,
        json={
            "code": "PARAMETER_ALLIANCE_ID_INVALID",
            "message": "The provided value for the parameter `allianceId` is invalid.",
            "details": "Input should be a valid integer, unable to parse string as an integer",
            "timestamp": "2020-01-01T00:00:00+00:00",
            "url": "https://example.com",
            "suggestion": "",
            "links": [],
        },
    )


@pytest.fixture(scope="function")
def mock_response_collection_id_invalid(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        status_code=422,
        json={
            "code": "PARAMETER_COLLECTION_ID_INVALID",
            "message": "The provided value for the parameter `collectionId` is invalid.",
            "details": "Input should be a valid integer, unable to parse string as an integer",
            "timestamp": "2020-01-01T00:00:00+00:00",
            "url": "https://example.com",
            "suggestion": "",
            "links": [],
        },
    )


@pytest.fixture(scope="function")
def mock_response_user_id_invalid(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        status_code=422,
        json={
            "code": "PARAMETER_USER_ID_INVALID",
            "message": "The provided value for the parameter `userId` is invalid.",
            "details": "Input should be a valid integer, unable to parse string as an integer",
            "timestamp": "2020-01-01T00:00:00+00:00",
            "url": "https://example.com",
            "suggestion": "",
            "links": [],
        },
    )

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
def mock_response_post_422_json_invalid(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        status_code=422,
        json={
            "code": "INVALID_JSON_FORMAT",
            "message": "The uploaded file is not a valid json file.",
            "details": "{error}",
            "timestamp": "2020-01-01T00:00:00+00:00",
            "url": "https://example.com",
            "suggestion": "Fix the JSON.",
            "links": [],
        },
    )


@pytest.fixture(scope="function")
def mock_response_post_422_schema_version_mismatch(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        status_code=422,
        json={
            "code": "SCHEMA_VERSION_MISMATCH",
            "message": "The file contents don't match the declared schema version.",
            "details": "The file contents don't match the declared schema version (expected schema version: {expected_schema_version}):\n{error}",
            "timestamp": "2020-01-01T00:00:00+00:00",
            "url": "https://example.com",
            "suggestion": "",
            "links": [],
        },
    )


@pytest.fixture(scope="function")
def mock_response_post_422_unsupported_schema(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        status_code=422,
        json={
            "code": "UNSUPPORTED_SCHEMA",
            "message": "The provided Collection is of an unsupported schema.",
            "details": "The uploaded file is not a valid Fleet Data Collection file.",
            "timestamp": "2020-01-01T00:00:00+00:00",
            "url": "https://example.com",
            "suggestion": "For the supported schemas, see: https://github.com/Zukunftsmusik/pss-fleet-data?tab=readme-ov-file#schema-descriptions",
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
